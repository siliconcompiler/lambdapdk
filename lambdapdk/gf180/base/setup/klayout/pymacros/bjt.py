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
# BJT Generator for GF180MCU
########################################################################################################################

import pya
from .draw_bjt import *


class npn_bjt(pya.PCellDeclarationHelper):
    """
    NPN BJT Generator for GF180MCU
    """

    def __init__(self):

        # Important: initialize the super class
        super(npn_bjt, self).__init__()
        self.Type_handle = self.param("Type", self.TypeList, "Type")
        self.Type_handle.add_choice("vnpn_10x10", "vnpn_10x10")
        self.Type_handle.add_choice("vnpn_5x5", "vnpn_5x5")
        self.Type_handle.add_choice("vnpn_0p54x16", "vnpn_0p54x16")
        self.Type_handle.add_choice("vnpn_0p54x8", "vnpn_0p54x8")
        self.Type_handle.add_choice("vnpn_0p54x4", "vnpn_0p54x4")
        self.Type_handle.add_choice("vnpn_0p54x2", "vnpn_0p54x2")
        self.param("Model", self.TypeString, "Model", default="gf180mcu_fd_pr__npn",readonly=True)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return str(self.Type)

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the
        # numeric parameter has changed (by comparing against the effective
        # radius ru) and set ru to the effective radius. We also update the
        # numerical value or the shape, depending on which on has not changed.
        pass


    def can_create_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we can use any shape which
        # has a finite bounding box
        # return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()
        pass

    def parameters_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we set r and l from the shape's
        # bounding box width and layer
        # self.r = self.shape.bbox().width() * self.layout.dbu / 2
        # self.l = self.layout.get_info(self.layer)
        pass

    def transformation_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we use the center of the shape's
        # bounding box to determine the transformation
        # return pya.Trans(self.shape.bbox().center())
        pass

    def produce_impl(self):

        # This is the main part of the implementation: create the layout

        self.percision = 1/self.layout.dbu
        npn_instance = draw_npn(layout=self.layout,device_name=self.Type)
        write_cells = pya.CellInstArray(npn_instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                              pya.Vector(0, 0), pya.Vector(0, 0),1 , 1)

        self.cell.flatten(1)
        self.cell.insert(write_cells)
        self.layout.cleanup()

class pnp_bjt(pya.PCellDeclarationHelper):
    """
    PNP BJT Generator for GF180MCU
    """

    def __init__(self):

        # Important: initialize the super class
        super(pnp_bjt, self).__init__()
        self.Type_handle = self.param("Type", self.TypeList, "Type")
        self.Type_handle.add_choice("vpnp_10x10", "vpnp_10x10")
        self.Type_handle.add_choice("vpnp_5x5", "vpnp_5x5")
        self.Type_handle.add_choice("vpnp_0p42x10", "vpnp_0p42x10")
        self.Type_handle.add_choice("vpnp_0p42x5", "vpnp_0p42x5")
        self.param("Model", self.TypeString, "Model", default="gf180mcu_fd_pr__pnp",readonly=True)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return str(self.Type)

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the
        # numeric parameter has changed (by comparing against the effective
        # radius ru) and set ru to the effective radius. We also update the
        # numerical value or the shape, depending on which on has not changed.
        pass


    def can_create_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we can use any shape which
        # has a finite bounding box
        # return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()
        pass

    def parameters_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we set r and l from the shape's
        # bounding box width and layer
        # self.r = self.shape.bbox().width() * self.layout.dbu / 2
        # self.l = self.layout.get_info(self.layer)
        pass

    def transformation_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we use the center of the shape's
        # bounding box to determine the transformation
        # return pya.Trans(self.shape.bbox().center())
        pass

    def produce_impl(self):

        # This is the main part of the implementation: create the layout

        self.percision = 1/self.layout.dbu
        pnp_instance = draw_pnp(layout=self.layout,device_name=self.Type)
        write_cells = pya.CellInstArray(pnp_instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                              pya.Vector(0, 0), pya.Vector(0, 0),1 , 1)

        self.cell.flatten(1)
        self.cell.insert(write_cells)
        self.layout.cleanup()




