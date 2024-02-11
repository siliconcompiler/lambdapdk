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
# MOS Capacitor Generator for GF180MCU
########################################################################################################################

import pya
from .draw_moscap import *

nmoscap_l   = 0.36
nmoscap_w   = 0.22

pmoscap_l   = 0.36
pmoscap_w   = 0.22

nmoscap_b_l = 0.36
nmoscap_b_w = 0.22

pmoscap_b_l = 0.36
pmoscap_b_w = 0.22

class nmoscap(pya.PCellDeclarationHelper):
    """
    NMOS capacitor (Outside DNWELL) Generator for GF180MCU
    """

    def __init__(self):

        # Initializing super class.
        super(nmoscap, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.param("deepnwell", self.TypeBoolean, "Deep NWELL", default=0)
        self.param("pcmpgr", self.TypeBoolean, "Guard Ring", default=0)
        self.Type_handle  = self.param("volt", self.TypeList, "Voltage area")
        self.Type_handle.add_choice("3.3V", "3.3V")
        self.Type_handle.add_choice("5/6V", "5/6V")

        self.param("l", self.TypeDouble,"Length", default=nmoscap_l, unit="um")
        self.param("w", self.TypeDouble,"Width", default=nmoscap_w, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "nmoscap(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the numeric parameter has changed.
        #  We also update the numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.l) < nmoscap_l:
            self.l  = nmoscap_l
        if (self.w) < nmoscap_w:
            self.w  = nmoscap_w

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
        np_instance = draw_nmoscap(self.layout, self.l, self.w , self.volt, self.deepnwell, self.pcmpgr)
        write_cells = pya.CellInstArray(np_instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(0, 0), pya.Vector(0, 0), 1, 1)

        self.cell.insert(write_cells)
        self.cell.flatten(1)

class pmoscap(pya.PCellDeclarationHelper):
    """
    3.3V PMOS capacitor (Outside DNWELL) Generator for GF180MCU
    """

    def __init__(self):

        # Initializing super class.
        super(pmoscap, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.param("deepnwell", self.TypeBoolean, "Deep NWELL", default=0)
        self.param("pcmpgr", self.TypeBoolean, "Guard Ring", default=0)
        self.Type_handle  = self.param("volt", self.TypeList, "Voltage area")
        self.Type_handle.add_choice("3.3V", "3.3V")
        self.Type_handle.add_choice("5/6V", "5/6V")

        self.param("l", self.TypeDouble,"Length", default=pmoscap_l, unit="um")
        self.param("w", self.TypeDouble,"Width", default=pmoscap_w, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "pmoscap(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the numeric parameter has changed.
        #  We also update the numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.l) < pmoscap_l:
            self.l  = pmoscap_l
        if (self.w) < pmoscap_w:
            self.w  = pmoscap_w

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
        np_instance = draw_pmoscap(self.layout, self.l, self.w , self.volt, self.deepnwell, self.pcmpgr)
        write_cells = pya.CellInstArray(np_instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(0, 0), pya.Vector(0, 0), 1, 1)

        self.cell.insert(write_cells)
        self.cell.flatten(1)

class nmoscap_b(pya.PCellDeclarationHelper):
    """
    3.3V NMOS capacitor (inside NWell) Generator for GF180MCU
    """

    def __init__(self):

        # Initializing super class.
        super(nmoscap_b, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.Type_handle  = self.param("volt", self.TypeList, "Voltage area")
        self.Type_handle.add_choice("3.3V", "3.3V")
        self.Type_handle.add_choice("5/6V", "5/6V")

        self.param("l", self.TypeDouble,"Length", default=nmoscap_b_l, unit="um")
        self.param("w", self.TypeDouble,"Width", default=nmoscap_b_w, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "nmoscap_b(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the numeric parameter has changed.
        #  We also update the numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.l) < nmoscap_b_l:
            self.l  = nmoscap_b_l
        if (self.w) < nmoscap_b_w:
            self.w  = nmoscap_b_w

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
        np_instance = draw_nmoscap_b(self.layout, self.l, self.w , self.volt)
        write_cells = pya.CellInstArray(np_instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(0, 0), pya.Vector(0, 0), 1, 1)

        self.cell.insert(write_cells)
        self.cell.flatten(1)

class pmoscap_b(pya.PCellDeclarationHelper):
    """
    3.3V PMOS capacitor (inside Psub) Generator for GF180MCU
    """

    def __init__(self):

        # Initializing super class.
        super(pmoscap_b, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.Type_handle  = self.param("volt", self.TypeList, "Voltage area")
        self.Type_handle.add_choice("3.3V", "3.3V")
        self.Type_handle.add_choice("5/6V", "5/6V")

        self.param("l", self.TypeDouble,"Length", default=pmoscap_b_l, unit="um")
        self.param("w", self.TypeDouble,"Width", default=pmoscap_b_w, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "pmoscap_b(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the numeric parameter has changed.
        #  We also update the numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.l) < pmoscap_b_l:
            self.l  = pmoscap_b_l
        if (self.w) < pmoscap_b_w:
            self.w  = pmoscap_b_w

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
        np_instance = draw_pmoscap_b(self.layout, self.l, self.w , self.volt)
        write_cells = pya.CellInstArray(np_instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(0, 0), pya.Vector(0, 0), 1, 1)

        self.cell.insert(write_cells)
        self.cell.flatten(1)
