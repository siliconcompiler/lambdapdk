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
# Resistor Generator for GF180MCU
########################################################################################################################

import pya
import os
from .draw_res import *

rm1_l           = 0.23
rm1_w           = 0.23

rm2_3_l         = 0.28
rm2_3_w         = 0.28

tm6k_l          = 0.36
tm6k_w          = 0.36

tm9_11k_l       = 0.44
tm9_11k_w       = 0.44

tm30k_l         = 1.8
tm30k_w         = 1.8

nplus_s_l       = 0.42
nplus_s_w       = 0.42

pplus_s_l       = 0.42
pplus_s_w       = 0.42

nplus_u_l       = 0.42
nplus_u_w       = 0.42

pplus_u_l       = 0.42
pplus_u_w       = 0.42

nwell_l         = 0.42
nwell_w         = 0.42

pwell_l         = 0.42
pwell_w         = 0.42

npolyf_s_l      = 0.42
npolyf_s_w      = 0.42

ppolyf_s_l      = 0.42
ppolyf_s_w      = 0.42

npolyf_u_l      = 0.42
npolyf_u_w      = 0.42

ppolyf_u_l      = 0.42
ppolyf_u_w      = 0.42

ppolyf_u_h_res_l    = 0.42
ppolyf_u_h_res_w    = 0.42

class metal_resistor(pya.PCellDeclarationHelper):
    """
    2-terminal Metal resistor Generator for GF180MCU
    """

    def __init__(self):

        # Initializing super class.
        super(metal_resistor, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.Type_handle  = self.param("res_type", self.TypeList, "Metal resistor type")
        self.Type_handle.add_choice("rm1", "rm1")
        self.Type_handle.add_choice("rm2", "rm2")
        self.Type_handle.add_choice("rm3", "rm3")
        self.Type_handle.add_choice("tm6k" , "tm6k" )
        self.Type_handle.add_choice("tm9k" , "tm9k" )
        self.Type_handle.add_choice("tm11k" , "tm11k" )
        self.Type_handle.add_choice("tm30k" , "tm30k" )

        self.param("l", self.TypeDouble,"Width", default=rm1_l, unit="um")
        self.param("w", self.TypeDouble,"Length", default=rm1_w, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")
        self.param("array_x", self.TypeInt,"Repeat X", default=1)
        self.param("array_y", self.TypeInt,"Repeat Y", default=1)
        self.param("x_spacing", self.TypeDouble,"spacing in x_direction", default=3, unit="um")
        self.param("y_spacing", self.TypeDouble,"spacing in y_direction", default=3, unit="um")


    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "metal_resistor(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the numeric parameter has changed.
        #  We also update the numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.res_type) == "rm1":
            if (self.l) < rm1_l:
                self.l  = rm1_l
            if (self.w) < rm1_w:
                self.w  = rm1_w

        if (self.res_type) == "rm2" or (self.res_type) == "rm3":
            if (self.l) < rm2_3_l:
                self.l  = rm2_3_l
            if (self.w) < rm2_3_w:
                self.w  = rm2_3_w

        if (self.res_type) == "tm6k" :
            if (self.l) < tm6k_l:
                self.l  = tm6k_l
            if (self.w) < tm6k_w:
                self.w  = tm6k_w

        if (self.res_type) == "tm9k" or (self.res_type) == "tm11k":
            if (self.l) < tm9_11k_l:
                self.l  = tm9_11k_l
            if (self.w) < tm9_11k_w:
                self.w  = tm9_11k_w

        if (self.res_type) == "tm30k" :
            if (self.l) < tm30k_l:
                self.l  = tm30k_l
            if (self.w) < tm30k_w:
                self.w  = tm30k_w

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
        dbu_PERCISION = 1/self.layout.dbu
        option = os.environ['GF_PDK_OPTION']
        if option == "A":
            if ((self.res_type) == "rm3") or ((self.res_type) == "tm6k") or ((self.res_type) == "tm9k") or ((self.res_type) == "tm11k"):
                raise TypeError(f"Current stack ({option}) doesn't allow this option")
        elif option == "B":
            if ((self.res_type) == "tm6k") or ((self.res_type) == "tm9k") or ((self.res_type) == "tm30k"):
                raise TypeError(f"Current stack ({option}) doesn't allow this option")
        else:
            if ((self.res_type) == "tm6k") or ((self.res_type) == "tm11k") or ((self.res_type) == "tm30k"):
                raise TypeError(f"Current stack ({option}) doesn't allow this option")
        np_instance = draw_metal_res(self.layout, self.l, self.w , self.res_type)
        write_cells = pya.CellInstArray(np_instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(self.x_spacing*dbu_PERCISION, 0), pya.Vector(0, self.y_spacing*dbu_PERCISION), self.array_x, self.array_y)

        self.cell.insert(write_cells)
        self.cell.flatten(1)

class nplus_s_resistor(pya.PCellDeclarationHelper):
    """
    3-terminal salicided n+ diffusion resistor (Outside DNWELL) Generator for GF180MCU
    """

    def __init__(self):

        # Initializing super class.
        super(nplus_s_resistor, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.param("deepnwell", self.TypeBoolean, "Deep NWELL", default=0)
        self.param("pcmpgr", self.TypeBoolean, "Guard Ring", default=0)
        self.param("l", self.TypeDouble,"Width", default=nplus_s_l, unit="um")
        self.param("w", self.TypeDouble,"Length", default=nplus_s_w, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")
        self.param("array_x", self.TypeInt,"Repeat X", default=1)
        self.param("array_y", self.TypeInt,"Repeat Y", default=1)
        self.param("x_spacing", self.TypeDouble,"spacing in x_direction", default=3, unit="um")
        self.param("y_spacing", self.TypeDouble,"spacing in y_direction", default=3, unit="um")
        self.param("sub", self.TypeBoolean, "Substrate terminal", default=1)


    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "nplus_s_resistor(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the numeric parameter has changed.
        #  We also update the numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.l) < nplus_s_l:
            self.l  = nplus_s_l
        if (self.w) < nplus_s_w:
            self.w  = nplus_s_w

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
        dbu_PERCISION = 1/self.layout.dbu
        np_instance = draw_nplus_s_res(self.layout, self.l, self.w , self.sub, self.deepnwell, self.pcmpgr)
        write_cells = pya.CellInstArray(np_instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(self.x_spacing*dbu_PERCISION, 0), pya.Vector(0, self.y_spacing*dbu_PERCISION), self.array_x, self.array_y)

        self.cell.insert(write_cells)
        self.cell.flatten(1)

class pplus_s_resistor(pya.PCellDeclarationHelper):
    """
    3-terminal salicided P+ diffusion resistor (Outside DNWELL) Generator for GF180MCU
    """

    def __init__(self):

        # Initializing super class.
        super(pplus_s_resistor, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.param("deepnwell", self.TypeBoolean, "Deep NWELL", default=0)
        self.param("pcmpgr", self.TypeBoolean, "Guard Ring", default=0)
        self.param("l", self.TypeDouble,"Width", default=pplus_s_l, unit="um")
        self.param("w", self.TypeDouble,"Length", default=pplus_s_w, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")
        self.param("array_x", self.TypeInt,"Repeat X", default=1)
        self.param("array_y", self.TypeInt,"Repeat Y", default=1)
        self.param("x_spacing", self.TypeDouble,"spacing in x_direction", default=3, unit="um")
        self.param("y_spacing", self.TypeDouble,"spacing in y_direction", default=3, unit="um")


    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "pplus_s_resistor(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the numeric parameter has changed.
        #  We also update the numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.l) < pplus_s_l:
            self.l  = pplus_s_l
        if (self.w) < pplus_s_w:
            self.w  = pplus_s_w

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
        dbu_PERCISION = 1/self.layout.dbu
        np_instance = draw_pplus_s_res(self.layout, self.l, self.w, self.deepnwell, self.pcmpgr)
        write_cells = pya.CellInstArray(np_instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(self.x_spacing*dbu_PERCISION, 0), pya.Vector(0, self.y_spacing*dbu_PERCISION), self.array_x, self.array_y)

        self.cell.insert(write_cells)
        self.cell.flatten(1)

class nplus_u_resistor(pya.PCellDeclarationHelper):
    """
    3-terminal unsalicided n+ diffusion resistor (Outside DNWELL) Generator for GF180MCU
    """

    def __init__(self):

        # Initializing super class.
        super(nplus_u_resistor, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.param("deepnwell", self.TypeBoolean, "Deep NWELL", default=0)
        self.param("pcmpgr", self.TypeBoolean, "Guard Ring", default=0)
        self.param("l", self.TypeDouble,"Width", default=nplus_u_l, unit="um")
        self.param("w", self.TypeDouble,"Length", default=nplus_u_w, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")
        self.param("array_x", self.TypeInt,"Repeat X", default=1)
        self.param("array_y", self.TypeInt,"Repeat Y", default=1)
        self.param("x_spacing", self.TypeDouble,"spacing in x_direction", default=3, unit="um")
        self.param("y_spacing", self.TypeDouble,"spacing in y_direction", default=3, unit="um")
        self.param("sub", self.TypeBoolean, "Substrate terminal", default=1)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "nplus_u_resistor(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the numeric parameter has changed.
        #  We also update the numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.l) < nplus_u_l:
            self.l  = nplus_u_l
        if (self.w) < nplus_u_w:
            self.w  = nplus_u_w

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
        dbu_PERCISION = 1/self.layout.dbu
        np_instance = draw_nplus_u_res(self.layout, self.l, self.w , self.sub, self.deepnwell, self.pcmpgr)
        write_cells = pya.CellInstArray(np_instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(self.x_spacing*dbu_PERCISION, 0), pya.Vector(0, self.y_spacing*dbu_PERCISION), self.array_x, self.array_y)

        self.cell.insert(write_cells)
        self.cell.flatten(1)

class pplus_u_resistor(pya.PCellDeclarationHelper):
    """
    3-terminal salicided P+ diffusion resistor (Outside DNWELL) Generator for GF180MCU
    """

    def __init__(self):

        # Initializing super class.
        super(pplus_u_resistor, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.param("deepnwell", self.TypeBoolean, "Deep NWELL", default=0)
        self.param("pcmpgr", self.TypeBoolean, "Guard Ring", default=0)
        self.param("l", self.TypeDouble,"Width", default=pplus_u_l, unit="um")
        self.param("w", self.TypeDouble,"Length", default=pplus_u_w, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")
        self.param("array_x", self.TypeInt,"Repeat X", default=1)
        self.param("array_y", self.TypeInt,"Repeat Y", default=1)
        self.param("x_spacing", self.TypeDouble,"spacing in x_direction", default=3, unit="um")
        self.param("y_spacing", self.TypeDouble,"spacing in y_direction", default=3, unit="um")


    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "pplus_u_resistor(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the numeric parameter has changed.
        #  We also update the numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.l) < pplus_u_l:
            self.l  = pplus_u_l
        if (self.w) < pplus_u_w:
            self.w  = pplus_u_w

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
        dbu_PERCISION = 1/self.layout.dbu
        np_instance = draw_pplus_u_res(self.layout, self.l, self.w, self.deepnwell, self.pcmpgr)
        write_cells = pya.CellInstArray(np_instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(self.x_spacing*dbu_PERCISION, 0), pya.Vector(0, self.y_spacing*dbu_PERCISION), self.array_x, self.array_y)

        self.cell.insert(write_cells)
        self.cell.flatten(1)

class nwell_resistor(pya.PCellDeclarationHelper):
    """
    3-terminal Nwell resistor under STI (Outside DNWELL) Generator for GF180MCU
    """

    def __init__(self):

        # Initializing super class.
        super(nwell_resistor, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.param("l", self.TypeDouble,"Width", default=nwell_l, unit="um")
        self.param("w", self.TypeDouble,"Length", default=nwell_w, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")
        self.param("array_x", self.TypeInt,"Repeat X", default=1)
        self.param("array_y", self.TypeInt,"Repeat Y", default=1)
        self.param("x_spacing", self.TypeDouble,"spacing in x_direction", default=3, unit="um")
        self.param("y_spacing", self.TypeDouble,"spacing in y_direction", default=3, unit="um")


    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "nwell_resistor(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the numeric parameter has changed.
        #  We also update the numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.l) < nwell_l:
            self.l  = nwell_l
        if (self.w) < nwell_w:
            self.w  = nwell_w

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
        dbu_PERCISION = 1/self.layout.dbu
        np_instance = draw_nwell_res(self.layout, self.l, self.w)
        write_cells = pya.CellInstArray(np_instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(self.x_spacing*dbu_PERCISION, 0), pya.Vector(0, self.y_spacing*dbu_PERCISION), self.array_x, self.array_y)

        self.cell.insert(write_cells)
        self.cell.flatten(1)

class pwell_resistor(pya.PCellDeclarationHelper):
    """
    3-terminal Pwell resistor under STI (Outside DNWELL) Generator for GF180MCU
    """

    def __init__(self):

        # Initializing super class.
        super(pwell_resistor, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.param("pcmpgr", self.TypeBoolean, "Guard Ring", default=0)
        self.param("l", self.TypeDouble,"Width", default=pwell_l, unit="um")
        self.param("w", self.TypeDouble,"Length", default=pwell_w, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")
        self.param("array_x", self.TypeInt,"Repeat X", default=1)
        self.param("array_y", self.TypeInt,"Repeat Y", default=1)
        self.param("x_spacing", self.TypeDouble,"spacing in x_direction", default=3, unit="um")
        self.param("y_spacing", self.TypeDouble,"spacing in y_direction", default=3, unit="um")


    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "pwell_resistor(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the numeric parameter has changed.
        #  We also update the numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.l) < pwell_l:
            self.l  = pwell_l
        if (self.w) < pwell_w:
            self.w  = pwell_w

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
        dbu_PERCISION = 1/self.layout.dbu
        np_instance = draw_pwell_res(self.layout, self.l, self.w, self.pcmpgr)
        write_cells = pya.CellInstArray(np_instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(self.x_spacing*dbu_PERCISION, 0), pya.Vector(0, self.y_spacing*dbu_PERCISION), self.array_x, self.array_y)

        self.cell.insert(write_cells)
        self.cell.flatten(1)

class npolyf_s_resistor(pya.PCellDeclarationHelper):
    """
    3-terminal salicided n+ poly resistor (Outside DNWELL) Generator for GF180MCU
    """

    def __init__(self):

        # Initializing super class.
        super(npolyf_s_resistor, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.param("deepnwell", self.TypeBoolean, "Deep NWELL", default=0)
        self.param("pcmpgr", self.TypeBoolean, "Guard Ring", default=0)
        self.param("l", self.TypeDouble,"Width", default=npolyf_s_l, unit="um")
        self.param("w", self.TypeDouble,"Length", default=npolyf_s_w, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")
        self.param("array_x", self.TypeInt,"Repeat X", default=1)
        self.param("array_y", self.TypeInt,"Repeat Y", default=1)
        self.param("x_spacing", self.TypeDouble,"spacing in x_direction", default=3, unit="um")
        self.param("y_spacing", self.TypeDouble,"spacing in y_direction", default=3, unit="um")


    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "npolyf_s_resistor(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the numeric parameter has changed.
        #  We also update the numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.l) < npolyf_s_l:
            self.l  = npolyf_s_l
        if (self.w) < npolyf_s_w:
            self.w  = npolyf_s_w

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
        dbu_PERCISION = 1/self.layout.dbu
        np_instance = draw_npolyf_s_res(self.layout, self.l, self.w, self.deepnwell, self.pcmpgr)
        write_cells = pya.CellInstArray(np_instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(self.x_spacing*dbu_PERCISION, 0), pya.Vector(0, self.y_spacing*dbu_PERCISION), self.array_x, self.array_y)

        self.cell.insert(write_cells)
        self.cell.flatten(1)

class ppolyf_s_resistor(pya.PCellDeclarationHelper):
    """
    3-terminal salicided p+ poly resistor (Outside DNWELL) Generator for GF180MCU
    """

    def __init__(self):

        # Initializing super class.
        super(ppolyf_s_resistor, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.param("deepnwell", self.TypeBoolean, "Deep NWELL", default=0)
        self.param("pcmpgr", self.TypeBoolean, "Guard Ring", default=0)
        self.param("l", self.TypeDouble,"Width", default=ppolyf_s_l, unit="um")
        self.param("w", self.TypeDouble,"Length", default=ppolyf_s_w, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")
        self.param("array_x", self.TypeInt,"Repeat X", default=1)
        self.param("array_y", self.TypeInt,"Repeat Y", default=1)
        self.param("x_spacing", self.TypeDouble,"spacing in x_direction", default=3, unit="um")
        self.param("y_spacing", self.TypeDouble,"spacing in y_direction", default=3, unit="um")


    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "ppolyf_s_resistor(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the numeric parameter has changed.
        #  We also update the numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.l) < ppolyf_s_l:
            self.l  = ppolyf_s_l
        if (self.w) < ppolyf_s_w:
            self.w  = ppolyf_s_w

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
        dbu_PERCISION = 1/self.layout.dbu
        np_instance = draw_ppolyf_s_res(self.layout, self.l, self.w, self.deepnwell, self.pcmpgr)
        write_cells = pya.CellInstArray(np_instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(self.x_spacing*dbu_PERCISION, 0), pya.Vector(0, self.y_spacing*dbu_PERCISION), self.array_x, self.array_y)

        self.cell.insert(write_cells)
        self.cell.flatten(1)

class npolyf_u_resistor(pya.PCellDeclarationHelper):
    """
    3-terminal unsalicided n+ poly resistor (Outside DNWELL) Generator for GF180MCU
    """

    def __init__(self):

        # Initializing super class.
        super(npolyf_u_resistor, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.param("deepnwell", self.TypeBoolean, "Deep NWELL", default=0)
        self.param("pcmpgr", self.TypeBoolean, "Guard Ring", default=0)
        self.param("l", self.TypeDouble,"Width", default=npolyf_u_l, unit="um")
        self.param("w", self.TypeDouble,"Length", default=npolyf_u_w, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")
        self.param("array_x", self.TypeInt,"Repeat X", default=1)
        self.param("array_y", self.TypeInt,"Repeat Y", default=1)
        self.param("x_spacing", self.TypeDouble,"spacing in x_direction", default=3, unit="um")
        self.param("y_spacing", self.TypeDouble,"spacing in y_direction", default=3, unit="um")


    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "npolyf_u_resistor(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the numeric parameter has changed.
        #  We also update the numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.l) < npolyf_u_l:
            self.l  = npolyf_u_l
        if (self.w) < npolyf_u_w:
            self.w  = npolyf_u_w

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
        dbu_PERCISION = 1/self.layout.dbu
        np_instance = draw_npolyf_u_res(self.layout, self.l, self.w, self.deepnwell, self.pcmpgr)
        write_cells = pya.CellInstArray(np_instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(self.x_spacing*dbu_PERCISION, 0), pya.Vector(0, self.y_spacing*dbu_PERCISION), self.array_x, self.array_y)

        self.cell.insert(write_cells)
        self.cell.flatten(1)

class ppolyf_u_resistor(pya.PCellDeclarationHelper):
    """
    3-terminal unsalicided p+ poly resistor (Outside DNWELL) Generator for GF180MCU
    """

    def __init__(self):

        # Initializing super class.
        super(ppolyf_u_resistor, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.param("deepnwell", self.TypeBoolean, "Deep NWELL", default=0)
        self.param("pcmpgr", self.TypeBoolean, "Guard Ring", default=0)
        self.param("l", self.TypeDouble,"Width", default=ppolyf_u_l, unit="um")
        self.param("w", self.TypeDouble,"Length", default=ppolyf_u_w, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")
        self.param("array_x", self.TypeInt,"Repeat X", default=1)
        self.param("array_y", self.TypeInt,"Repeat Y", default=1)
        self.param("x_spacing", self.TypeDouble,"spacing in x_direction", default=3, unit="um")
        self.param("y_spacing", self.TypeDouble,"spacing in y_direction", default=3, unit="um")


    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "ppolyf_u_resistor(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the numeric parameter has changed.
        #  We also update the numerical value or the shape, depending on which on has not changed.
        self.area = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.l) < ppolyf_u_l:
            self.l  = ppolyf_u_l
        if (self.w) < ppolyf_u_w:
            self.w  = ppolyf_u_w

    def can_create_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we can use any shape which
        # has a finite bounding box
        return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()

    def parameters_from_shape_impl(self):
        #     # Implement the "Create PCell from shape" protocol: we set r and l from the shape's
        #     # bounding box width and layer
        self.r = self.shape.bbox().width() * self.layout.dbu / 2
        self.l = self.layout.get_info(self.layer)

    def transformation_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we use the center of the shape's
        # bounding box to determine the transformation
        return pya.Trans(self.shape.bbox().center())

    def produce_impl(self):
        dbu_PERCISION = 1/self.layout.dbu
        np_instance = draw_ppolyf_u_res(self.layout, self.l, self.w, self.deepnwell, self.pcmpgr)
        write_cells = pya.CellInstArray(np_instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(self.x_spacing*dbu_PERCISION, 0), pya.Vector(0, self.y_spacing*dbu_PERCISION), self.array_x, self.array_y)

        self.cell.insert(write_cells)
        self.cell.flatten(1)

class ppolyf_u_high_Rs_resistor(pya.PCellDeclarationHelper):
    """
    high-Rs p+ poly resistor (outside DNWELL) Generator for GF180MCU
    """

    def __init__(self):

        # Initializing super class.
        super(ppolyf_u_high_Rs_resistor, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================
        self.param("deepnwell", self.TypeBoolean, "Deep NWELL", default=0)
        self.param("pcmpgr", self.TypeBoolean, "Guard Ring", default=0)
        self.Type_handle  = self.param("volt", self.TypeList, "Voltage area")
        self.Type_handle.add_choice("3.3V", "3.3V")
        self.Type_handle.add_choice("5/6V", "5/6V")

        self.param("l", self.TypeDouble,"Width", default=ppolyf_u_h_res_l, unit="um")
        self.param("w", self.TypeDouble,"Length", default=ppolyf_u_h_res_w, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")
        self.param("array_x", self.TypeInt,"Repeat X", default=1)
        self.param("array_y", self.TypeInt,"Repeat Y", default=1)
        self.param("x_spacing", self.TypeDouble,"spacing in x_direction", default=3, unit="um")
        self.param("y_spacing", self.TypeDouble,"spacing in y_direction", default=3, unit="um")

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "ppolyf_u_high_Rs_resistor(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the numeric parameter has changed.
        #  We also update the numerical value or the shape, depending on which on has not changed.
        self.area = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if (self.l) < ppolyf_u_h_res_l:
            self.l  = ppolyf_u_h_res_l
        if (self.w) < ppolyf_u_h_res_w:
            self.w  = ppolyf_u_h_res_w

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
        dbu_PERCISION = 1/self.layout.dbu
        np_instance = draw_ppolyf_u_high_Rs_res(self.layout, self.l, self.w , self.volt, self.deepnwell, self.pcmpgr)
        write_cells = pya.CellInstArray(np_instance.cell_index(), pya.Trans(pya.Point(0, 0)),
                      pya.Vector(self.x_spacing*dbu_PERCISION, 0), pya.Vector(0, self.y_spacing*dbu_PERCISION), self.array_x, self.array_y)

        self.cell.insert(write_cells)
        self.cell.flatten(1)
