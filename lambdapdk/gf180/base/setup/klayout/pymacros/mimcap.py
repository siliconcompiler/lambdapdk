# Copyright 2022 GlobalFoundries PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

########################################################################################################################
# MIM Capacitor Generator for GF180MCU
########################################################################################################################

import pya
import os
from .draw_mimcap import *

mim_l = 0.28
mim_w = 0.28

class mimcap(pya.PCellDeclarationHelper):
    """
    MIM capacitor Generator for GF180MCU
    """

    def __init__(self):

        # Initializing super class.
        super(mimcap, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.Type_handle  = self.param("mim_option", self.TypeList, "MIM-Option")
        self.Type_handle.add_choice("MIM-A", "MIM-A")
        self.Type_handle.add_choice("MIM-B", "MIM-B")

        self.Type_handle2 = self.param("metal_level", self.TypeList, "Metal level (MIM-B)")
        self.Type_handle2.add_choice("M4", "M4")
        self.Type_handle2.add_choice("M5", "M5")
        self.Type_handle2.add_choice("M6", "M6")

        self.param("l", self.TypeDouble,"Length", default=mim_l, unit="um")
        self.param("w", self.TypeDouble,"Width", default=mim_w, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "mimcap(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the numeric parameter has changed.
        #  We also update the numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.l) < mim_l:
            self.l  = mim_l
        if (self.w) < mim_w:
            self.w  = mim_w
        if (self.mim_option) == "MIM-A":
            self.metal_level = "M3"

    def can_create_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we can use any shape which
        # has a finite bounding box
        return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()

    def parameters_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we set r and l from the shape's
        # bounding box width and layer
        self.r = self.shape.bbox().width() * self.layout.dbu / 2
        self.l = self.layout.get_info(self.layer)

    def transformation_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we use the center of the shape's
        # bounding box to determine the transformation
        return pya.Trans(self.shape.bbox().center())

    def produce_impl(self):
        option = os.environ['GF_PDK_OPTION']
        if option == "A":
            if (self.mim_option) == "MIM-B":
                raise TypeError(f"Current stack ({option}) doesn't allow this option")
        else:
            if (self.mim_option) == "MIM-A":
                raise TypeError(f"Current stack ({option}) doesn't allow this option")
        np_instance = draw_mimcap(self.layout, self.l, self.w, self.mim_option , self.metal_level)
        write_cells = pya.CellInstArray(np_instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(0, 0), pya.Vector(0, 0), 1, 1)

        self.cell.insert(write_cells)
        self.cell.flatten(1)
