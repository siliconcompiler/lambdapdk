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
# MOSFET Generator for GF180MCU
########################################################################################################################
import pya
from .draw_mos import *

mos_3p3_l   = 0.28
mos_3p3_w   = 0.22
mos_5_6_w   = 0.3

nmos_5p0_l  = 0.6
nmos_6p0_l  = 0.7

pmos_5p0_l  = 0.5
pmos_6p0_l  = 0.55

nmos_nat_l  = 1.8
nmos_nat_w  = 0.8
mos_grw     = 0.36
mos_ld      = 0.44

ldmos_l_min = 0.6
ldmos_l_max = 20
ldmos_w_min = 4
ldmos_w_max = 50

class nmos(pya.PCellDeclarationHelper):
    """
    NMOS Generator for GF180MCU
    """

    def __init__(self):
        # Initialize super class.
        super(nmos, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.param("deepnwell", self.TypeBoolean, "Deep NWELL", default=0)
        self.param("pcmpgr", self.TypeBoolean, "Deep NWELL Guard Ring", default=0)
        self.Type_handle  = self.param("volt", self.TypeList, "Operating Voltage")
        self.Type_handle.add_choice("3.3V", "3.3V")
        self.Type_handle.add_choice("5V", "5V")
        self.Type_handle.add_choice("6V", "6V")
        self.Type_handle  = self.param("bulk", self.TypeList, "Bulk Type")
        self.Type_handle.add_choice("None", "None")
        self.Type_handle.add_choice("Bulk Tie", "Bulk Tie")
        self.Type_handle.add_choice("Guard Ring", "Guard Ring")

        self.param("w", self.TypeDouble, "Width", default=mos_3p3_w, unit="um")
        self.param("l", self.TypeDouble, "Length", default=mos_3p3_l, unit="um")
        self.param("ld", self.TypeDouble, "Diffusion Length", default=mos_ld, unit="um")
        self.param("nf", self.TypeInt, "Number of Fingers", default=1)
        self.param("grw", self.TypeDouble, "Guard Ring Width", default=mos_grw, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "nmos(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the
        # numeric parameter has changed (by comparing against the effective
        # radius ru) and set ru to the effective radius. We also update the
        # numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if self.volt    == "3.3V":
            if (self.l) < mos_3p3_l:
                self.l  = mos_3p3_l
            if (self.w) < mos_3p3_w:
                self.w  = mos_3p3_w
        elif self.volt  == "5V":
            if (self.l) < nmos_5p0_l:
                self.l  = nmos_5p0_l
            if (self.w) < mos_5_6_w:
                self.w  = mos_5_6_w
        elif self.volt  == "6V":
            if (self.l) < nmos_6p0_l:
                self.l  = nmos_6p0_l
            if (self.w) < mos_5_6_w:
                self.w  = mos_5_6_w
        if (self.grw)   < mos_grw:
            self.grw    = mos_grw

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
        instance = draw_nmos(self.layout, self.l, self.w, self.ld, self.nf, self.grw, self.bulk, self.volt, self.deepnwell, self.pcmpgr)
        write_cells = pya.CellInstArray(instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(0, 0), pya.Vector(0, 0), 1, 1)
        self.cell.insert(write_cells)
        self.cell.flatten(1)

class pmos(pya.PCellDeclarationHelper):
    """
    PMOS Generator for GF180MCU
    """

    def __init__(self):
        # Initialize super class.
        super(pmos, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.param("deepnwell", self.TypeBoolean, "Deep NWELL", default=0)
        self.param("pcmpgr", self.TypeBoolean, "Deep NWELL Guard Ring", default=0)
        self.Type_handle  = self.param("volt", self.TypeList, "Voltage area")
        self.Type_handle.add_choice("3.3V", "3.3V")
        self.Type_handle.add_choice("5V", "5V")
        self.Type_handle.add_choice("6V", "6V")
        self.Type_handle  = self.param("bulk", self.TypeList, "Bulk Type")
        self.Type_handle.add_choice("None", "None")
        self.Type_handle.add_choice("Bulk Tie", "Bulk Tie")
        self.Type_handle.add_choice("Guard Ring", "Guard Ring")

        self.param("w", self.TypeDouble, "Width", default=mos_3p3_w, unit="um")
        self.param("l", self.TypeDouble, "Length", default=mos_3p3_l, unit="um")
        self.param("ld", self.TypeDouble, "Diffusion Length", default=mos_ld, unit="um")
        self.param("nf", self.TypeInt, "Number of Fingers", default=1)
        self.param("grw", self.TypeDouble, "Guard Ring Width", default=mos_grw, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "pmos(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the
        # numeric parameter has changed (by comparing against the effective
        # radius ru) and set ru to the effective radius. We also update the
        # numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if self.volt    == "3.3V":
            if (self.l) < mos_3p3_l:
                self.l  = mos_3p3_l
            if (self.w) < mos_3p3_w:
                self.w  = mos_3p3_w
        elif self.volt  == "5V":
            if (self.l) < pmos_5p0_l:
                self.l  = pmos_5p0_l
            if (self.w) < mos_5_6_w:
                self.w  = mos_5_6_w
        elif self.volt  == "6V":
            if (self.l) < pmos_6p0_l:
                self.l  = pmos_6p0_l
            if (self.w) < mos_5_6_w:
                self.w  = mos_5_6_w
        if (self.grw)   < mos_grw:
            self.grw    = mos_grw

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
        instance = draw_pmos(self.layout, self.l, self.w, self.ld, self.nf, self.grw, self.bulk, self.volt, self.deepnwell, self.pcmpgr)
        write_cells = pya.CellInstArray(instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(0, 0), pya.Vector(0, 0), 1, 1)
        self.cell.insert(write_cells)
        self.cell.flatten(1)

class nmos_6p0_nat(pya.PCellDeclarationHelper):
    """
    6V Native NMOS Generator for GF180MCU
    """

    def __init__(self):
        # Initialize super class.
        super(nmos_6p0_nat, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.Type_handle  = self.param("bulk", self.TypeList, "Bulk Type")
        self.Type_handle.add_choice("None", "None")
        self.Type_handle.add_choice("Bulk Tie", "Bulk Tie")
        self.Type_handle.add_choice("Guard Ring", "Guard Ring")

        self.param("w", self.TypeDouble, "Width", default=nmos_nat_w, unit="um")
        self.param("l", self.TypeDouble, "Length", default=nmos_nat_l, unit="um")
        self.param("ld", self.TypeDouble, "Diffusion Length", default=mos_ld, unit="um")
        self.param("nf", self.TypeInt, "Number of Fingers", default=1)
        self.param("grw", self.TypeDouble, "Guard Ring Width", default=mos_grw, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "nmos_6p0_nat(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the
        # numeric parameter has changed (by comparing against the effective
        # radius ru) and set ru to the effective radius. We also update the
        # numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.l) < nmos_nat_l:
            self.l = nmos_nat_l
        if (self.w) < nmos_nat_w:
            self.w = nmos_nat_w
        if (self.grw) < mos_grw:
            self.grw = mos_grw

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
        instance = draw_nmos_6p0_nat(self.layout, self.l, self.w, self.ld, self.nf, self.grw, self.bulk)
        write_cells = pya.CellInstArray(instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(0, 0), pya.Vector(0, 0), 1, 1)
        self.cell.insert(write_cells)
        self.cell.flatten(1)

class nmos_10p0_asym(pya.PCellDeclarationHelper):
    """
    10V LDNMOS Generator for GF180MCU
    """

    def __init__(self):
        # Initialize super class.
        super(nmos_10p0_asym, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================

        self.param("w", self.TypeDouble, "Width", default=ldmos_w_min, unit="um")
        self.param("l", self.TypeDouble, "Length", default=ldmos_l_min, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "nmos_10p0_asym(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the
        # numeric parameter has changed (by comparing against the effective
        # radius ru) and set ru to the effective radius. We also update the
        # numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.l) < ldmos_l_min:
            self.l = ldmos_l_min
        if (self.l) > ldmos_l_max:
            self.l = ldmos_l_max
        if (self.w) < ldmos_w_min:
            self.w = ldmos_w_min
        if (self.w) > ldmos_w_max:
            self.w = ldmos_w_max

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
        instance = draw_nmos_10p0_asym(self.layout, self.l, self.w)
        write_cells = pya.CellInstArray(instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(0, 0), pya.Vector(0, 0), 1, 1)
        self.cell.insert(write_cells)
        self.cell.flatten(1)

class pmos_10p0_asym(pya.PCellDeclarationHelper):
    """
    10V LDPMOS Generator for GF180MCU
    """

    def __init__(self):
        # Initialize super class.
        super(pmos_10p0_asym, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================

        self.param("w", self.TypeDouble, "Width", default=ldmos_w_min, unit="um")
        self.param("l", self.TypeDouble, "Length", default=ldmos_l_min, unit="um")
        self.param("double_gr", self.TypeBoolean, "Double Guard Ring", default=1)
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "pmos_10p0_asym(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the
        # numeric parameter has changed (by comparing against the effective
        # radius ru) and set ru to the effective radius. We also update the
        # numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.l) < ldmos_l_min:
            self.l = ldmos_l_min
        if (self.l) > ldmos_l_max:
            self.l = ldmos_l_max
        if (self.w) < ldmos_w_min:
            self.w = ldmos_w_min
        if (self.w) > ldmos_w_max:
            self.w = ldmos_w_max

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
        instance = draw_pmos_10p0_asym(self.layout, self.l, self.w, self.double_gr)
        write_cells = pya.CellInstArray(instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(0, 0), pya.Vector(0, 0), 1, 1)
        self.cell.insert(write_cells)
        self.cell.flatten(1)
