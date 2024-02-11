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
## Resistor Pcells Generators for Klayout of GF180MCU
########################################################################################################################

import pya

tol = 1.05

def number_spc_contacts(box_width, min_enc, cont_spacing, cont_width):
    """ Calculate number of cantacts in a given dimensions and the free space for symmetry.
        By getting the min enclosure,the width of the box,the width ans spacing of the contacts.
        Parameters
        ----------
        box_width    (double) : length you place the via or cont. in
        min_enc      (double) : spacing between the edge of the box and the first contact.
        cont_spacing (double) : spacing between different contacts
        cont_width   (double) : contacts in the same direction
    """
    spc_cont = box_width - 2 * min_enc
    num_cont = int((spc_cont + cont_spacing) / (cont_width + cont_spacing))
    free_spc = box_width - (num_cont * cont_width +
                            (num_cont - 1) * cont_spacing)
    return num_cont, free_spc

def draw_metal_res(layout, l, w , res_type):
    '''
    Usage:-
     used to draw 2-terminal Metal resistor by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of diff length
     w      : Float of diff width
    '''

    # Define layers
    metal1         = layout.layer(34 , 0 )
    metal2         = layout.layer(36 , 0 )
    metal3         = layout.layer(42 , 0 )
    metaltop       = layout.layer(53 , 0 )

    metal1_res     = layout.layer(110, 11 )
    metal2_res     = layout.layer(110, 12 )
    metal3_res     = layout.layer(110, 13 )
    metaltop_res   = layout.layer(110, 16 )

    # VARIABLES
    dbu_PERCISION        = 1/layout.dbu
    metal_res_w          = w    * dbu_PERCISION
    metal_res_l          = l    * dbu_PERCISION

    if res_type == "rm1":
        metal_res     = metal1_res
        metal         = metal1
        metal_res_enc = 0.23 * dbu_PERCISION

    elif res_type == "rm2":
        metal_res     = metal2_res
        metal         = metal2
        metal_res_enc = 0.28 * dbu_PERCISION

    elif res_type == "rm3":
        metal_res     = metal3_res
        metal         = metal3
        metal_res_enc = 0.28 * dbu_PERCISION

    elif res_type == "tm6k":
        metal_res     = metaltop_res
        metal         = metaltop
        metal_res_enc = 0.36 * dbu_PERCISION

    elif res_type == "tm9k" or res_type == "tm11k":
        metal_res     = metaltop_res
        metal         = metaltop
        metal_res_enc = 0.44 * dbu_PERCISION

    elif res_type == "tm30k":
        metal_res     = metaltop_res
        metal         = metaltop
        metal_res_enc = 1.8 * dbu_PERCISION

    else:
        metal_res     = metal1_res
        metal         = metal1
        metal_res_enc = 0.23 * dbu_PERCISION


    # Inserting rm cell
    cell_index  = layout.add_cell("rm")
    rm_cell = layout.cell(cell_index)

    # Inserting metal_res
    rm_cell.shapes(metal_res).insert(pya.Box(0, 0, metal_res_w, metal_res_l))

    # Inserting metal
    rm_cell.shapes(metal).insert(pya.Box(-metal_res_enc, 0 , metal_res_w+metal_res_enc, metal_res_l))

    rm_cell.flatten(True)
    return rm_cell

def draw_nplus_s_res(layout, l, w , sub, deepnwell, pcmpgr):
    '''
    Usage:-
     used to draw 3-terminal salicided n+ diffusion resistor (Outside DNWELL) by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of diff length
     w      : Float of diff width
    '''

    # Define layers
    dnwell         = layout.layer(12 , 0 )
    comp           = layout.layer(22 , 0 )
    lvpwell        = layout.layer(204, 0 )
    pplus          = layout.layer(31 , 0 )
    nplus          = layout.layer(32 , 0 )
    contact        = layout.layer(33 , 0 )
    metal1         = layout.layer(34 , 0 )
    res_mk         = layout.layer(110, 5 )


    # VARIABLES
    dbu_PERCISION         = 1/layout.dbu
    nplus_s_res_w         = w    * dbu_PERCISION
    nplus_s_res_l         = l    * dbu_PERCISION
    cmp_res_enc           = 0.29 * dbu_PERCISION
    implant_cmp_enc       = 0.16 * dbu_PERCISION
    ncmp_pcmp_spc         = 0.72 * dbu_PERCISION
    pcmp_width            = 0.36 * dbu_PERCISION
    metal_width           = 0.34 * dbu_PERCISION
    met_cont_enc          = 0.06 * dbu_PERCISION
    comp_cont_enc         = 0.07 * dbu_PERCISION
    cont_size             = 0.22 * dbu_PERCISION
    cont_min_spc          = 0.25 * dbu_PERCISION
    cmp_met_cont_enc_diff = 0.01 * dbu_PERCISION
    min_cmp_area          = 0.2025 * dbu_PERCISION * dbu_PERCISION
    tie_violat            = 0      * dbu_PERCISION
    gr_w                  = 0.36 * dbu_PERCISION
    dnwell_enc_lvpwell    = 2.5  * dbu_PERCISION
    pcmp_gr2dnw           = 2.5  * dbu_PERCISION
    lvpwell_enc_pcmp      = 0.12 * dbu_PERCISION
    lvpwell_enc_ncmp      = 0.43 * dbu_PERCISION

    # Inserting nplus_s_res cell
    cell_index  = layout.add_cell("nplus_s_resistor")
    nplus_s_res_cell = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting res_mk
    nplus_s_res_cell.shapes(res_mk).insert(pya.Box(0, 0, nplus_s_res_w, nplus_s_res_l))

    # Inserting n diffusion
    nplus_s_res_cell.shapes(comp).insert(pya.Box(-cmp_res_enc, 0, nplus_s_res_w+cmp_res_enc, nplus_s_res_l))
    nplus_s_res_cell.shapes(nplus).insert(pya.Box(-cmp_res_enc-implant_cmp_enc, -implant_cmp_enc , nplus_s_res_w+cmp_res_enc+implant_cmp_enc, nplus_s_res_l+implant_cmp_enc))

    # Inserting ncomp metal
    nplus_s_res_cell.shapes(metal1).insert(pya.Box(-cont_size-met_cont_enc , cmp_met_cont_enc_diff , met_cont_enc , nplus_s_res_l-cmp_met_cont_enc_diff))                       #left
    nplus_s_res_cell.shapes(metal1).insert(pya.Box(nplus_s_res_w-met_cont_enc, cmp_met_cont_enc_diff , nplus_s_res_w+cont_size+met_cont_enc , nplus_s_res_l-cmp_met_cont_enc_diff)) # Right

    # Inserting ncomp contacts
    num_ncmp_left_con_1, ncmp_left_con_free_spc_1 = number_spc_contacts(metal_width, met_cont_enc, cont_min_spc, cont_size)
    num_ncmp_left_con_2, ncmp_left_con_free_spc_2 = number_spc_contacts(nplus_s_res_l-2*cmp_met_cont_enc_diff, met_cont_enc, cont_min_spc, cont_size)
    ncmp_left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-cont_size-met_cont_enc+ncmp_left_con_free_spc_1 / 2, cmp_met_cont_enc_diff+ncmp_left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_left_con_1, num_ncmp_left_con_2)
    nplus_s_res_cell.insert(ncmp_left_con_arr)

    num_ncmp_right_con_1, ncmp_right_con_free_spc_1 = number_spc_contacts(metal_width, met_cont_enc, cont_min_spc, cont_size)
    num_ncmp_right_con_2, ncmp_right_con_free_spc_2 = number_spc_contacts(nplus_s_res_l-2*cmp_met_cont_enc_diff, met_cont_enc, cont_min_spc, cont_size)
    ncmp_right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(nplus_s_res_w-met_cont_enc+ncmp_right_con_free_spc_1 / 2, cmp_met_cont_enc_diff+ncmp_right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_right_con_1, num_ncmp_right_con_2)
    nplus_s_res_cell.insert(ncmp_right_con_arr)

    if deepnwell == True:
        sub = 1
        # Inserting lvpwell
        nplus_s_res_cell.shapes(lvpwell).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width-lvpwell_enc_pcmp, -lvpwell_enc_ncmp , nplus_s_res_w+cmp_res_enc+lvpwell_enc_ncmp, nplus_s_res_l+lvpwell_enc_ncmp))
        # Inserting dnwell
        nplus_s_res_cell.shapes(dnwell).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width-lvpwell_enc_pcmp-dnwell_enc_lvpwell, -lvpwell_enc_ncmp-dnwell_enc_lvpwell , nplus_s_res_w+cmp_res_enc+lvpwell_enc_ncmp+dnwell_enc_lvpwell, nplus_s_res_l+lvpwell_enc_ncmp+dnwell_enc_lvpwell))

        # Inserting Guard Ring
        if pcmpgr == True:
            cmp_inner = pya.Box(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw, -lvpwell_enc_ncmp-dnwell_enc_lvpwell-pcmp_gr2dnw , nplus_s_res_w+cmp_res_enc+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw, nplus_s_res_l+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw)
            cmp_outer = pya.Box(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw-gr_w, -lvpwell_enc_ncmp-dnwell_enc_lvpwell-pcmp_gr2dnw-gr_w , nplus_s_res_w+cmp_res_enc+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw+gr_w, nplus_s_res_l+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw+gr_w)
            cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
            nplus_s_res_cell.shapes(comp).insert(cmp_gr)

            pp_inner = pya.Box(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw+implant_cmp_enc, -lvpwell_enc_ncmp-dnwell_enc_lvpwell-pcmp_gr2dnw+implant_cmp_enc , nplus_s_res_w+cmp_res_enc+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw-implant_cmp_enc, nplus_s_res_l+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw-implant_cmp_enc)
            pp_outer = pya.Box(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw-gr_w-implant_cmp_enc, -lvpwell_enc_ncmp-dnwell_enc_lvpwell-pcmp_gr2dnw-gr_w-implant_cmp_enc , nplus_s_res_w+cmp_res_enc+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw+gr_w+implant_cmp_enc, nplus_s_res_l+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw+gr_w+implant_cmp_enc)
            pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
            nplus_s_res_cell.shapes(pplus).insert(pp_gr)

    else:
        # Inserting lvpwell
        nplus_s_res_cell.shapes(lvpwell).insert(pya.Box(-cmp_res_enc-implant_cmp_enc, -implant_cmp_enc , nplus_s_res_w+cmp_res_enc+implant_cmp_enc, nplus_s_res_l+implant_cmp_enc))


    if sub == 1:
        # Inserting p diffusion
        if (nplus_s_res_l * pcmp_width) < min_cmp_area:
            tie_violat = (min_cmp_area/pcmp_width - nplus_s_res_l)/2 * tol
        nplus_s_res_cell.shapes(comp).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width, -tie_violat, -cmp_res_enc-ncmp_pcmp_spc, nplus_s_res_l+tie_violat))
        nplus_s_res_cell.shapes(pplus).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width-implant_cmp_enc, -implant_cmp_enc-tie_violat , -cmp_res_enc-ncmp_pcmp_spc+implant_cmp_enc, nplus_s_res_l+implant_cmp_enc+tie_violat))

        # Inserting pcomp metal
        nplus_s_res_cell.shapes(metal1).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width, -tie_violat, -cmp_res_enc-ncmp_pcmp_spc, nplus_s_res_l+tie_violat))

        # Inserting pcomp contacts
        num_pcmp_con_1, pcmp_con_free_spc_1 = number_spc_contacts(pcmp_width, comp_cont_enc, cont_min_spc, cont_size)
        num_pcmp_con_2, pcmp_con_free_spc_2 = number_spc_contacts(nplus_s_res_l, comp_cont_enc, cont_min_spc, cont_size)
        pcmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
            pya.Point(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width+pcmp_con_free_spc_1 / 2, pcmp_con_free_spc_2/2)),
            pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
            num_pcmp_con_1, num_pcmp_con_2)
        nplus_s_res_cell.insert(pcmp_con_arr)

    nplus_s_res_cell.flatten(True)
    return nplus_s_res_cell

def draw_pplus_s_res(layout, l, w, deepnwell, pcmpgr):
    '''
    Usage:-
     used to draw3-terminal salicided P+ diffusion resistor (Outside DNWELL) by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of diff length
     w      : Float of diff width
    '''

    # Define layers
    dnwell         = layout.layer(12 , 0 )
    comp           = layout.layer(22 , 0 )
    nwell          = layout.layer(21 , 0 )
    pplus          = layout.layer(31 , 0 )
    nplus          = layout.layer(32 , 0 )
    contact        = layout.layer(33 , 0 )
    metal1         = layout.layer(34 , 0 )
    res_mk         = layout.layer(110, 5 )


    # VARIABLES
    dbu_PERCISION         = 1/layout.dbu
    pplus_s_res_w         = w      * dbu_PERCISION
    pplus_s_res_l         = l      * dbu_PERCISION
    cmp_res_enc           = 0.29   * dbu_PERCISION
    implant_cmp_enc       = 0.16   * dbu_PERCISION
    nwell_pcmp_enc        = 0.8    * dbu_PERCISION
    nwell_ncmp_enc        = 0.12   * dbu_PERCISION
    ncmp_pcmp_spc         = 0.32   * dbu_PERCISION
    ncmp_width            = 0.36   * dbu_PERCISION
    metal_width           = 0.34   * dbu_PERCISION
    met_cont_enc          = 0.06   * dbu_PERCISION
    comp_cont_enc         = 0.07   * dbu_PERCISION
    cont_size             = 0.22   * dbu_PERCISION
    cont_min_spc          = 0.25   * dbu_PERCISION
    cmp_met_cont_enc_diff = 0.01   * dbu_PERCISION
    min_cmp_area          = 0.2025 * dbu_PERCISION * dbu_PERCISION
    tie_violat            = 0      * dbu_PERCISION
    dnwell_ncmp_enc       = 0.62   * dbu_PERCISION
    dnwell_pcmp_enc       = 0.93   * dbu_PERCISION
    pcmp_gr2dnw           = 2.5    * dbu_PERCISION
    gr_w                  = 0.36   * dbu_PERCISION

    # Inserting pplus_s_res cell
    cell_index  = layout.add_cell("pplus_s_resistor")
    pplus_s_res_cell = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting res_mk
    pplus_s_res_cell.shapes(res_mk).insert(pya.Box(0, 0, pplus_s_res_w, pplus_s_res_l))

    # Inserting p diffusion
    pplus_s_res_cell.shapes(comp).insert(pya.Box(-cmp_res_enc, 0, pplus_s_res_w+cmp_res_enc, pplus_s_res_l))
    pplus_s_res_cell.shapes(pplus).insert(pya.Box(-cmp_res_enc-implant_cmp_enc, -implant_cmp_enc , pplus_s_res_w+cmp_res_enc+implant_cmp_enc, pplus_s_res_l+implant_cmp_enc))

    # Inserting pcomp metal
    pplus_s_res_cell.shapes(metal1).insert(pya.Box(-cont_size-met_cont_enc , cmp_met_cont_enc_diff , met_cont_enc , pplus_s_res_l-cmp_met_cont_enc_diff))                       #left
    pplus_s_res_cell.shapes(metal1).insert(pya.Box(pplus_s_res_w-met_cont_enc, cmp_met_cont_enc_diff , pplus_s_res_w+cont_size+met_cont_enc , pplus_s_res_l-cmp_met_cont_enc_diff)) # Right

    # Inserting pcomp contacts
    num_pcmp_left_con_1, pcmp_left_con_free_spc_1 = number_spc_contacts(metal_width, met_cont_enc, cont_min_spc, cont_size)
    num_pcmp_left_con_2, pcmp_left_con_free_spc_2 = number_spc_contacts(pplus_s_res_l-2*cmp_met_cont_enc_diff, met_cont_enc, cont_min_spc, cont_size)
    pcmp_left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-cont_size-met_cont_enc+pcmp_left_con_free_spc_1 / 2, cmp_met_cont_enc_diff+pcmp_left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_pcmp_left_con_1, num_pcmp_left_con_2)
    pplus_s_res_cell.insert(pcmp_left_con_arr)

    num_pcmp_right_con_1, pcmp_right_con_free_spc_1 = number_spc_contacts(metal_width, met_cont_enc, cont_min_spc, cont_size)
    num_pcmp_right_con_2, pcmp_right_con_free_spc_2 = number_spc_contacts(pplus_s_res_l-2*cmp_met_cont_enc_diff, met_cont_enc, cont_min_spc, cont_size)
    pcmp_right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(pplus_s_res_w-met_cont_enc+pcmp_right_con_free_spc_1 / 2, cmp_met_cont_enc_diff+pcmp_right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_pcmp_right_con_1, num_pcmp_right_con_2)
    pplus_s_res_cell.insert(pcmp_right_con_arr)

    # Inserting n diffusion
    if (pplus_s_res_l * ncmp_width) < min_cmp_area:
        tie_violat = (min_cmp_area/ncmp_width - pplus_s_res_l)/2 * tol
    pplus_s_res_cell.shapes(comp).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width, -tie_violat, -cmp_res_enc-ncmp_pcmp_spc, pplus_s_res_l+tie_violat))
    pplus_s_res_cell.shapes(nplus).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width-implant_cmp_enc, -implant_cmp_enc-tie_violat , -cmp_res_enc-ncmp_pcmp_spc+implant_cmp_enc, pplus_s_res_l+implant_cmp_enc+tie_violat))

    # Inserting ncomp metal
    pplus_s_res_cell.shapes(metal1).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width, -tie_violat, -cmp_res_enc-ncmp_pcmp_spc, pplus_s_res_l+tie_violat))

    # Inserting ncomp contacts
    num_ncmp_con_1, ncmp_con_free_spc_1 = number_spc_contacts(ncmp_width, comp_cont_enc, cont_min_spc, cont_size)
    num_ncmp_con_2, ncmp_con_free_spc_2 = number_spc_contacts(pplus_s_res_l, comp_cont_enc, cont_min_spc, cont_size)
    ncmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width+ncmp_con_free_spc_1 / 2, ncmp_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_con_1, num_ncmp_con_2)
    pplus_s_res_cell.insert(ncmp_con_arr)

    if deepnwell == True:
        # Inserting dnwell
        pplus_s_res_cell.shapes(dnwell).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width-dnwell_ncmp_enc, -dnwell_pcmp_enc , pplus_s_res_w+cmp_res_enc+dnwell_pcmp_enc, pplus_s_res_l+dnwell_pcmp_enc))

        # Inserting Guard Ring
        if pcmpgr == True:
            cmp_inner = pya.Box(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width-dnwell_ncmp_enc-pcmp_gr2dnw, -dnwell_pcmp_enc-pcmp_gr2dnw , pplus_s_res_w+cmp_res_enc+dnwell_pcmp_enc+pcmp_gr2dnw, pplus_s_res_l+dnwell_pcmp_enc+pcmp_gr2dnw)
            cmp_outer = pya.Box(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width-dnwell_ncmp_enc-pcmp_gr2dnw-gr_w, -dnwell_pcmp_enc-pcmp_gr2dnw-gr_w , pplus_s_res_w+cmp_res_enc+dnwell_pcmp_enc+pcmp_gr2dnw+gr_w, pplus_s_res_l+dnwell_pcmp_enc+pcmp_gr2dnw+gr_w)
            cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
            pplus_s_res_cell.shapes(comp).insert(cmp_gr)

            pp_inner = pya.Box(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width-dnwell_ncmp_enc-pcmp_gr2dnw+implant_cmp_enc, -dnwell_pcmp_enc-pcmp_gr2dnw+implant_cmp_enc , pplus_s_res_w+cmp_res_enc+dnwell_pcmp_enc+pcmp_gr2dnw-implant_cmp_enc, pplus_s_res_l+dnwell_pcmp_enc+pcmp_gr2dnw-implant_cmp_enc)
            pp_outer = pya.Box(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width-dnwell_ncmp_enc-pcmp_gr2dnw-gr_w-implant_cmp_enc, -dnwell_pcmp_enc-pcmp_gr2dnw-gr_w-implant_cmp_enc , pplus_s_res_w+cmp_res_enc+dnwell_pcmp_enc+pcmp_gr2dnw+gr_w+implant_cmp_enc, pplus_s_res_l+dnwell_pcmp_enc+pcmp_gr2dnw+gr_w+implant_cmp_enc)
            pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
            pplus_s_res_cell.shapes(pplus).insert(pp_gr)

    else:
        # Inserting nwell
        pplus_s_res_cell.shapes(nwell).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width-nwell_ncmp_enc, -nwell_pcmp_enc , pplus_s_res_w+cmp_res_enc+nwell_pcmp_enc, pplus_s_res_l+nwell_pcmp_enc))


    pplus_s_res_cell.flatten(True)
    return pplus_s_res_cell

def draw_nplus_u_res(layout, l, w , sub, deepnwell, pcmpgr):
    '''
    Usage:-
     used to draw 3-terminal unsalicided n+ diffusion resistor (Outside DNWELL) by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of diff length
     w      : Float of diff width
    '''

    # Define layers
    dnwell         = layout.layer(12 , 0 )
    comp           = layout.layer(22 , 0 )
    lvpwell        = layout.layer(204, 0 )
    pplus          = layout.layer(31 , 0 )
    nplus          = layout.layer(32 , 0 )
    contact        = layout.layer(33 , 0 )
    metal1         = layout.layer(34 , 0 )
    sab            = layout.layer(49 , 0 )
    res_mk         = layout.layer(110, 5 )


    # VARIABLES
    dbu_PERCISION         = 1/layout.dbu
    nplus_u_res_w         = w    * dbu_PERCISION
    nplus_u_res_l         = l    * dbu_PERCISION
    cmp_res_enc           = 0.44 * dbu_PERCISION
    sab_res_enc           = 0.23 * dbu_PERCISION
    implant_cmp_enc       = 0.18 * dbu_PERCISION
    ncmp_pcmp_spc         = 0.76 * dbu_PERCISION
    pcmp_width            = 0.36 * dbu_PERCISION
    metal_width           = 0.34 * dbu_PERCISION
    met_cont_enc          = 0.06 * dbu_PERCISION
    comp_cont_enc         = 0.07 * dbu_PERCISION
    cont_size             = 0.22 * dbu_PERCISION
    cont_min_spc          = 0.25 * dbu_PERCISION
    cmp_met_cont_enc_diff = 0.01 * dbu_PERCISION
    min_cmp_area          = 0.2025 * dbu_PERCISION * dbu_PERCISION
    tie_violat            = 0      * dbu_PERCISION
    gr_w                  = 0.36 * dbu_PERCISION
    dnwell_enc_lvpwell    = 2.5  * dbu_PERCISION
    pcmp_gr2dnw           = 2.5  * dbu_PERCISION
    lvpwell_enc_pcmp      = 0.12 * dbu_PERCISION
    lvpwell_enc_ncmp      = 0.43 * dbu_PERCISION

    # Inserting nplus_u_res cell
    cell_index  = layout.add_cell("nplus_u_resistor")
    nplus_u_res_cell = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting res_mk
    nplus_u_res_cell.shapes(res_mk).insert(pya.Box(0, 0, nplus_u_res_w, nplus_u_res_l))

    # Inserting sab
    nplus_u_res_cell.shapes(sab).insert(pya.Box(0, -sab_res_enc, nplus_u_res_w, nplus_u_res_l+sab_res_enc))

    # Inserting n diffusion
    nplus_u_res_cell.shapes(comp).insert(pya.Box(-cmp_res_enc, 0, nplus_u_res_w+cmp_res_enc, nplus_u_res_l))
    nplus_u_res_cell.shapes(nplus).insert(pya.Box(-cmp_res_enc-implant_cmp_enc, -implant_cmp_enc , nplus_u_res_w+cmp_res_enc+implant_cmp_enc, nplus_u_res_l+implant_cmp_enc))

    # Inserting ncomp metal
    nplus_u_res_cell.shapes(metal1).insert(pya.Box(-cmp_res_enc+cmp_met_cont_enc_diff , cmp_met_cont_enc_diff , -cmp_res_enc+cmp_met_cont_enc_diff+metal_width , nplus_u_res_l-cmp_met_cont_enc_diff))    #left
    nplus_u_res_cell.shapes(metal1).insert(pya.Box(nplus_u_res_w+cmp_res_enc-cmp_met_cont_enc_diff-metal_width, cmp_met_cont_enc_diff , nplus_u_res_w+cmp_res_enc-cmp_met_cont_enc_diff , nplus_u_res_l-cmp_met_cont_enc_diff)) # Right

    # Inserting ncomp contacts
    num_ncmp_left_con_1, ncmp_left_con_free_spc_1 = number_spc_contacts(metal_width, met_cont_enc, cont_min_spc, cont_size)
    num_ncmp_left_con_2, ncmp_left_con_free_spc_2 = number_spc_contacts(nplus_u_res_l-2*cmp_met_cont_enc_diff, met_cont_enc, cont_min_spc, cont_size)
    ncmp_left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-cmp_res_enc+cmp_met_cont_enc_diff+ncmp_left_con_free_spc_1 / 2, cmp_met_cont_enc_diff+ncmp_left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_left_con_1, num_ncmp_left_con_2)
    nplus_u_res_cell.insert(ncmp_left_con_arr)

    num_ncmp_right_con_1, ncmp_right_con_free_spc_1 = number_spc_contacts(metal_width, met_cont_enc, cont_min_spc, cont_size)
    num_ncmp_right_con_2, ncmp_right_con_free_spc_2 = number_spc_contacts(nplus_u_res_l-2*cmp_met_cont_enc_diff, met_cont_enc, cont_min_spc, cont_size)
    ncmp_right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(nplus_u_res_w+cmp_res_enc-cmp_met_cont_enc_diff-metal_width+ncmp_right_con_free_spc_1 / 2, cmp_met_cont_enc_diff+ncmp_right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_right_con_1, num_ncmp_right_con_2)
    nplus_u_res_cell.insert(ncmp_right_con_arr)

    if deepnwell == True:
        sub = 1
        # Inserting lvpwell
        nplus_u_res_cell.shapes(lvpwell).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width-lvpwell_enc_pcmp, -lvpwell_enc_ncmp , nplus_u_res_w+cmp_res_enc+lvpwell_enc_ncmp, nplus_u_res_l+lvpwell_enc_ncmp))
        # Inserting dnwell
        nplus_u_res_cell.shapes(dnwell).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width-lvpwell_enc_pcmp-dnwell_enc_lvpwell, -lvpwell_enc_ncmp-dnwell_enc_lvpwell , nplus_u_res_w+cmp_res_enc+lvpwell_enc_ncmp+dnwell_enc_lvpwell, nplus_u_res_l+lvpwell_enc_ncmp+dnwell_enc_lvpwell))

        # Inserting Guard Ring
        if pcmpgr == True:
            cmp_inner = pya.Box(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw, -lvpwell_enc_ncmp-dnwell_enc_lvpwell-pcmp_gr2dnw , nplus_u_res_w+cmp_res_enc+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw, nplus_u_res_l+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw)
            cmp_outer = pya.Box(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw-gr_w, -lvpwell_enc_ncmp-dnwell_enc_lvpwell-pcmp_gr2dnw-gr_w , nplus_u_res_w+cmp_res_enc+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw+gr_w, nplus_u_res_l+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw+gr_w)
            cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
            nplus_u_res_cell.shapes(comp).insert(cmp_gr)

            pp_inner = pya.Box(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw+implant_cmp_enc, -lvpwell_enc_ncmp-dnwell_enc_lvpwell-pcmp_gr2dnw+implant_cmp_enc , nplus_u_res_w+cmp_res_enc+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw-implant_cmp_enc, nplus_u_res_l+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw-implant_cmp_enc)
            pp_outer = pya.Box(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw-gr_w-implant_cmp_enc, -lvpwell_enc_ncmp-dnwell_enc_lvpwell-pcmp_gr2dnw-gr_w-implant_cmp_enc , nplus_u_res_w+cmp_res_enc+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw+gr_w+implant_cmp_enc, nplus_u_res_l+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw+gr_w+implant_cmp_enc)
            pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
            nplus_u_res_cell.shapes(pplus).insert(pp_gr)

    else:
        # Inserting lvpwell
        nplus_u_res_cell.shapes(lvpwell).insert(pya.Box(-cmp_res_enc-implant_cmp_enc, -implant_cmp_enc , nplus_u_res_w+cmp_res_enc+implant_cmp_enc, nplus_u_res_l+implant_cmp_enc))


    if sub == 1:
        # Inserting p diffusion
        if (nplus_u_res_l * pcmp_width) < min_cmp_area:
            tie_violat = (min_cmp_area/pcmp_width - nplus_u_res_l)/2 * tol
        nplus_u_res_cell.shapes(comp).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width, -tie_violat, -cmp_res_enc-ncmp_pcmp_spc, nplus_u_res_l+tie_violat))
        nplus_u_res_cell.shapes(pplus).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width-implant_cmp_enc, -implant_cmp_enc-tie_violat , -cmp_res_enc-ncmp_pcmp_spc+implant_cmp_enc, nplus_u_res_l+tie_violat+implant_cmp_enc))

        # Inserting pcomp metal
        nplus_u_res_cell.shapes(metal1).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width, -tie_violat, -cmp_res_enc-ncmp_pcmp_spc, nplus_u_res_l+tie_violat))

        # Inserting pcomp contacts
        num_pcmp_con_1, pcmp_con_free_spc_1 = number_spc_contacts(pcmp_width, comp_cont_enc, cont_min_spc, cont_size)
        num_pcmp_con_2, pcmp_con_free_spc_2 = number_spc_contacts(nplus_u_res_l, comp_cont_enc, cont_min_spc, cont_size)
        pcmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
            pya.Point(-cmp_res_enc-ncmp_pcmp_spc-pcmp_width+pcmp_con_free_spc_1 / 2, pcmp_con_free_spc_2/2)),
            pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
            num_pcmp_con_1, num_pcmp_con_2)
        nplus_u_res_cell.insert(pcmp_con_arr)

    nplus_u_res_cell.flatten(True)
    return nplus_u_res_cell

def draw_pplus_u_res(layout, l, w, deepnwell, pcmpgr):
    '''
    Usage:-
     used to draw 3-terminal unsalicided P+ diffusion resistor (Outsdie DNWELL) by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of diff length
     w      : Float of diff width
    '''

    # Define layers
    dnwell         = layout.layer(12 , 0 )
    comp           = layout.layer(22 , 0 )
    nwell          = layout.layer(21 , 0 )
    pplus          = layout.layer(31 , 0 )
    nplus          = layout.layer(32 , 0 )
    contact        = layout.layer(33 , 0 )
    metal1         = layout.layer(34 , 0 )
    sab            = layout.layer(49 , 0 )
    res_mk         = layout.layer(110, 5 )


    # VARIABLES
    dbu_PERCISION         = 1/layout.dbu
    pplus_u_res_w         = w    * dbu_PERCISION
    pplus_u_res_l         = l    * dbu_PERCISION
    cmp_res_enc           = 0.44 * dbu_PERCISION
    sab_res_enc           = 0.23 * dbu_PERCISION
    implant_cmp_enc       = 0.18 * dbu_PERCISION
    nwell_ncmp_enc        = 0.12 * dbu_PERCISION
    nwell_pcmp_enc        = 0.93 * dbu_PERCISION
    ncmp_pcmp_spc         = 0.34 * dbu_PERCISION
    ncmp_width            = 0.36 * dbu_PERCISION
    metal_width           = 0.34 * dbu_PERCISION
    met_cont_enc          = 0.06 * dbu_PERCISION
    comp_cont_enc         = 0.07 * dbu_PERCISION
    cont_size             = 0.22 * dbu_PERCISION
    cont_min_spc          = 0.25 * dbu_PERCISION
    cmp_met_cont_enc_diff = 0.01 * dbu_PERCISION
    min_cmp_area          = 0.2025 * dbu_PERCISION * dbu_PERCISION
    tie_violat            = 0      * dbu_PERCISION
    dnwell_ncmp_enc       = 0.62 * dbu_PERCISION
    dnwell_pcmp_enc       = 0.93 * dbu_PERCISION
    pcmp_gr2dnw           = 2.5  * dbu_PERCISION
    gr_w                  = 0.36 * dbu_PERCISION

    # Inserting pplus_u_res cell
    cell_index  = layout.add_cell("pplus_u_resistor")
    pplus_u_res_cell = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting res_mk
    pplus_u_res_cell.shapes(res_mk).insert(pya.Box(0, 0, pplus_u_res_w, pplus_u_res_l))

    # Inserting sab
    pplus_u_res_cell.shapes(sab).insert(pya.Box(0, -sab_res_enc, pplus_u_res_w, pplus_u_res_l+sab_res_enc))

    # Inserting p diffusion
    pplus_u_res_cell.shapes(comp).insert(pya.Box(-cmp_res_enc, 0, pplus_u_res_w+cmp_res_enc, pplus_u_res_l))
    pplus_u_res_cell.shapes(pplus).insert(pya.Box(-cmp_res_enc-implant_cmp_enc, -implant_cmp_enc , pplus_u_res_w+cmp_res_enc+implant_cmp_enc, pplus_u_res_l+implant_cmp_enc))

    # Inserting pcomp metal
    pplus_u_res_cell.shapes(metal1).insert(pya.Box(-cmp_res_enc+cmp_met_cont_enc_diff , cmp_met_cont_enc_diff , -cmp_res_enc+cmp_met_cont_enc_diff+metal_width , pplus_u_res_l-cmp_met_cont_enc_diff))    #left
    pplus_u_res_cell.shapes(metal1).insert(pya.Box(pplus_u_res_w+cmp_res_enc-cmp_met_cont_enc_diff-metal_width, cmp_met_cont_enc_diff , pplus_u_res_w+cmp_res_enc-cmp_met_cont_enc_diff , pplus_u_res_l-cmp_met_cont_enc_diff)) # Right

    # Inserting pcomp contacts
    num_pcmp_left_con_1, pcmp_left_con_free_spc_1 = number_spc_contacts(metal_width, met_cont_enc, cont_min_spc, cont_size)
    num_pcmp_left_con_2, pcmp_left_con_free_spc_2 = number_spc_contacts(pplus_u_res_l-2*cmp_met_cont_enc_diff, met_cont_enc, cont_min_spc, cont_size)
    pcmp_left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-cmp_res_enc+cmp_met_cont_enc_diff+pcmp_left_con_free_spc_1 / 2, cmp_met_cont_enc_diff+pcmp_left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_pcmp_left_con_1, num_pcmp_left_con_2)
    pplus_u_res_cell.insert(pcmp_left_con_arr)

    num_pcmp_right_con_1, pcmp_right_con_free_spc_1 = number_spc_contacts(metal_width, met_cont_enc, cont_min_spc, cont_size)
    num_pcmp_right_con_2, pcmp_right_con_free_spc_2 = number_spc_contacts(pplus_u_res_l-2*cmp_met_cont_enc_diff, met_cont_enc, cont_min_spc, cont_size)
    pcmp_right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(pplus_u_res_w+cmp_res_enc-cmp_met_cont_enc_diff-metal_width+pcmp_right_con_free_spc_1 / 2, cmp_met_cont_enc_diff+pcmp_right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_pcmp_right_con_1, num_pcmp_right_con_2)
    pplus_u_res_cell.insert(pcmp_right_con_arr)

    # Inserting n diffusion
    if (pplus_u_res_l * ncmp_width) < min_cmp_area:
        tie_violat = (min_cmp_area/ncmp_width - pplus_u_res_l)/2 * tol
    pplus_u_res_cell.shapes(comp).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width, -tie_violat, -cmp_res_enc-ncmp_pcmp_spc, pplus_u_res_l+tie_violat))
    pplus_u_res_cell.shapes(nplus).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width-implant_cmp_enc, -implant_cmp_enc-tie_violat , -cmp_res_enc-ncmp_pcmp_spc+implant_cmp_enc, pplus_u_res_l+implant_cmp_enc+tie_violat))

    # Inserting ncomp metal
    pplus_u_res_cell.shapes(metal1).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width, -tie_violat, -cmp_res_enc-ncmp_pcmp_spc, pplus_u_res_l+tie_violat))

    # Inserting ncomp contacts
    num_ncmp_con_1, ncmp_con_free_spc_1 = number_spc_contacts(ncmp_width, comp_cont_enc, cont_min_spc, cont_size)
    num_ncmp_con_2, ncmp_con_free_spc_2 = number_spc_contacts(pplus_u_res_l, comp_cont_enc, cont_min_spc, cont_size)
    ncmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width+ncmp_con_free_spc_1 / 2, ncmp_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_con_1, num_ncmp_con_2)
    pplus_u_res_cell.insert(ncmp_con_arr)

    if deepnwell == True:
        # Inserting dnwell
        pplus_u_res_cell.shapes(dnwell).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width-dnwell_ncmp_enc, -dnwell_pcmp_enc , pplus_u_res_w+cmp_res_enc+dnwell_pcmp_enc, pplus_u_res_l+dnwell_pcmp_enc))

        # Inserting Guard Ring
        if pcmpgr == True:
            cmp_inner = pya.Box(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width-dnwell_ncmp_enc-pcmp_gr2dnw, -dnwell_pcmp_enc-pcmp_gr2dnw , pplus_u_res_w+cmp_res_enc+dnwell_pcmp_enc+pcmp_gr2dnw, pplus_u_res_l+dnwell_pcmp_enc+pcmp_gr2dnw)
            cmp_outer = pya.Box(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width-dnwell_ncmp_enc-pcmp_gr2dnw-gr_w, -dnwell_pcmp_enc-pcmp_gr2dnw-gr_w , pplus_u_res_w+cmp_res_enc+dnwell_pcmp_enc+pcmp_gr2dnw+gr_w, pplus_u_res_l+dnwell_pcmp_enc+pcmp_gr2dnw+gr_w)
            cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
            pplus_u_res_cell.shapes(comp).insert(cmp_gr)

            pp_inner = pya.Box(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width-dnwell_ncmp_enc-pcmp_gr2dnw+implant_cmp_enc, -dnwell_pcmp_enc-pcmp_gr2dnw+implant_cmp_enc , pplus_u_res_w+cmp_res_enc+dnwell_pcmp_enc+pcmp_gr2dnw-implant_cmp_enc, pplus_u_res_l+dnwell_pcmp_enc+pcmp_gr2dnw-implant_cmp_enc)
            pp_outer = pya.Box(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width-dnwell_ncmp_enc-pcmp_gr2dnw-gr_w-implant_cmp_enc, -dnwell_pcmp_enc-pcmp_gr2dnw-gr_w-implant_cmp_enc , pplus_u_res_w+cmp_res_enc+dnwell_pcmp_enc+pcmp_gr2dnw+gr_w+implant_cmp_enc, pplus_u_res_l+dnwell_pcmp_enc+pcmp_gr2dnw+gr_w+implant_cmp_enc)
            pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
            pplus_u_res_cell.shapes(pplus).insert(pp_gr)

    else:
        # Inserting nwell
        pplus_u_res_cell.shapes(nwell).insert(pya.Box(-cmp_res_enc-ncmp_pcmp_spc-ncmp_width-nwell_ncmp_enc, -nwell_pcmp_enc , pplus_u_res_w+cmp_res_enc+nwell_pcmp_enc, pplus_u_res_l+nwell_pcmp_enc))


    pplus_u_res_cell.flatten(True)
    return pplus_u_res_cell

def draw_nwell_res(layout, l, w):
    '''
    Usage:-
     used to draw 3-terminal Nwell resistor under STI (Outside DNWELL) by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of diff length
     w      : Float of diff width
    '''

    # Define layers
    comp           = layout.layer(22 , 0 )
    nwell          = layout.layer(21 , 0 )
    pplus          = layout.layer(31 , 0 )
    nplus          = layout.layer(32 , 0 )
    contact        = layout.layer(33 , 0 )
    metal1         = layout.layer(34 , 0 )
    res_mk         = layout.layer(110, 5 )


    # VARIABLES
    dbu_PERCISION         = 1/layout.dbu
    nwell_res_w           = w    * dbu_PERCISION
    nwell_res_l           = l    * dbu_PERCISION
    nwell_res_enc         = 0.48 * dbu_PERCISION
    res_nwell_ext         = 0.5  * dbu_PERCISION
    implant_cmp_enc       = 0.16 * dbu_PERCISION
    nwell_cmp_enc         = 0.12 * dbu_PERCISION
    ncmp_pcmp_spc         = 0.84 * dbu_PERCISION
    cmp_width             = 0.36 * dbu_PERCISION
    metal_width           = 0.34 * dbu_PERCISION
    met_cont_enc          = 0.06 * dbu_PERCISION
    comp_cont_enc         = 0.07 * dbu_PERCISION
    cont_size             = 0.22 * dbu_PERCISION
    cont_min_spc          = 0.25 * dbu_PERCISION
    cmp_met_cont_enc_diff = 0.01 * dbu_PERCISION

    # Inserting nwell_res cell
    cell_index  = layout.add_cell("nwell_resistor")
    nwell_res_cell = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting res_mk
    nwell_res_cell.shapes(res_mk).insert(pya.Box(0, -res_nwell_ext, nwell_res_w, nwell_res_l+res_nwell_ext))

    # Inserting nwell
    nwell_res_cell.shapes(nwell).insert(pya.Box(-nwell_res_enc, 0, nwell_res_w+nwell_res_enc, nwell_res_l))

    # Inserting n diffusion
    nwell_res_cell.shapes(comp).insert(pya.Box(-cmp_width, nwell_cmp_enc, 0, nwell_res_l-nwell_cmp_enc))           #left
    nwell_res_cell.shapes(comp).insert(pya.Box(nwell_res_w, nwell_cmp_enc, nwell_res_w+cmp_width, nwell_res_l-nwell_cmp_enc))  #right
    nwell_res_cell.shapes(nplus).insert(pya.Box(-cmp_width-implant_cmp_enc, nwell_cmp_enc-implant_cmp_enc , implant_cmp_enc, nwell_res_l-nwell_cmp_enc+implant_cmp_enc))
    nwell_res_cell.shapes(nplus).insert(pya.Box(nwell_res_w-implant_cmp_enc, nwell_cmp_enc-implant_cmp_enc , nwell_res_w+cmp_width+implant_cmp_enc, nwell_res_l-nwell_cmp_enc+implant_cmp_enc))

    # Inserting ncomp metal
    nwell_res_cell.shapes(metal1).insert(pya.Box(-cmp_width, nwell_cmp_enc, 0, nwell_res_l-nwell_cmp_enc))           #left
    nwell_res_cell.shapes(metal1).insert(pya.Box(nwell_res_w, nwell_cmp_enc, nwell_res_w+cmp_width, nwell_res_l-nwell_cmp_enc))  #right

    # Inserting ncomp contacts
    num_ncmp_left_con_1, ncmp_left_con_free_spc_1 = number_spc_contacts(cmp_width, comp_cont_enc, cont_min_spc, cont_size)
    num_ncmp_left_con_2, ncmp_left_con_free_spc_2 = number_spc_contacts(nwell_res_l-2*nwell_cmp_enc, comp_cont_enc, cont_min_spc, cont_size)
    ncmp_left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-cmp_width+ncmp_left_con_free_spc_1 / 2, nwell_cmp_enc+ncmp_left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_left_con_1, num_ncmp_left_con_2)
    nwell_res_cell.insert(ncmp_left_con_arr)

    num_ncmp_right_con_1, ncmp_right_con_free_spc_1 = number_spc_contacts(cmp_width, comp_cont_enc, cont_min_spc, cont_size)
    num_ncmp_right_con_2, ncmp_right_con_free_spc_2 = number_spc_contacts(nwell_res_l-2*nwell_cmp_enc, comp_cont_enc, cont_min_spc, cont_size)
    ncmp_right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(nwell_res_w+ncmp_right_con_free_spc_1 / 2, nwell_cmp_enc+ncmp_right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_right_con_1, num_ncmp_right_con_2)
    nwell_res_cell.insert(ncmp_right_con_arr)

    # Inserting p diffusion
    nwell_res_cell.shapes(comp).insert(pya.Box(-cmp_width-ncmp_pcmp_spc-cmp_width, 0, -cmp_width-ncmp_pcmp_spc , nwell_res_l))
    nwell_res_cell.shapes(pplus).insert(pya.Box(-cmp_width-ncmp_pcmp_spc-cmp_width-implant_cmp_enc, -implant_cmp_enc, -cmp_width-ncmp_pcmp_spc+implant_cmp_enc , nwell_res_l+implant_cmp_enc))

    # Inserting pcomp metal
    nwell_res_cell.shapes(metal1).insert(pya.Box(-cmp_width-ncmp_pcmp_spc-cmp_width, 0, -cmp_width-ncmp_pcmp_spc , nwell_res_l))

    # Inserting pcomp contacts
    num_pcmp_con_1, pcmp_con_free_spc_1 = number_spc_contacts(cmp_width, comp_cont_enc, cont_min_spc, cont_size)
    num_pcmp_con_2, pcmp_con_free_spc_2 = number_spc_contacts(nwell_res_l, comp_cont_enc, cont_min_spc, cont_size)
    pcmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-cmp_width-ncmp_pcmp_spc-cmp_width+pcmp_con_free_spc_1 / 2, pcmp_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_pcmp_con_1, num_pcmp_con_2)
    nwell_res_cell.insert(pcmp_con_arr)

    nwell_res_cell.flatten(True)
    return nwell_res_cell

def draw_pwell_res(layout, l, w, pcmpgr):
    '''
    Usage:-
     used to draw 3-terminal Pwell resistor under STI (Outside DNWELL) by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of diff length
     w      : Float of diff width
    '''

    # Define layers
    comp           = layout.layer(22 , 0 )
    dnwell         = layout.layer(12 , 0 )
    lvpwell        = layout.layer(204, 0 )
    pplus          = layout.layer(31 , 0 )
    nplus          = layout.layer(32 , 0 )
    contact        = layout.layer(33 , 0 )
    metal1         = layout.layer(34 , 0 )
    res_mk         = layout.layer(110, 5 )


    # VARIABLES
    dbu_PERCISION         = 1/layout.dbu
    pwell_res_w           = w    * dbu_PERCISION
    pwell_res_l           = l    * dbu_PERCISION
    pwell_res_enc         = 0.48 * dbu_PERCISION
    dnwell_lvpwell_enc    = 2.5  * dbu_PERCISION
    res_pwell_ext         = 0.5  * dbu_PERCISION
    implant_cmp_enc       = 0.16 * dbu_PERCISION
    pwell_cmp_enc         = 0.12 * dbu_PERCISION
    ncmp_pcmp_spc         = 0.84 * dbu_PERCISION
    cmp_width             = 0.36 * dbu_PERCISION
    comp_cont_enc         = 0.07 * dbu_PERCISION
    cont_size             = 0.22 * dbu_PERCISION
    cont_min_spc          = 0.25 * dbu_PERCISION
    pcmp_gr2dnw           = 2.5  * dbu_PERCISION
    gr_w                  = 0.36 * dbu_PERCISION

    # Inserting pwell_res cell
    cell_index  = layout.add_cell("pwell_resistor")
    pwell_res_cell = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting res_mk
    pwell_res_cell.shapes(res_mk).insert(pya.Box(0, -res_pwell_ext, pwell_res_w, pwell_res_l+res_pwell_ext))

    # Inserting pwell
    pwell_res_cell.shapes(lvpwell).insert(pya.Box(-pwell_res_enc, 0, pwell_res_w+pwell_res_enc, pwell_res_l))

    # Inserting DNWELL
    pwell_res_cell.shapes(dnwell).insert(pya.Box(-pwell_res_enc-dnwell_lvpwell_enc, -dnwell_lvpwell_enc, pwell_res_w+pwell_res_enc+dnwell_lvpwell_enc, pwell_res_l+dnwell_lvpwell_enc))

    # Inserting Guard Ring
    if pcmpgr == True:
        cmp_inner = pya.Box(-pwell_res_enc-dnwell_lvpwell_enc-pcmp_gr2dnw, -dnwell_lvpwell_enc-pcmp_gr2dnw, pwell_res_w+pwell_res_enc+dnwell_lvpwell_enc+pcmp_gr2dnw, pwell_res_l+dnwell_lvpwell_enc+pcmp_gr2dnw)
        cmp_outer = pya.Box(-pwell_res_enc-dnwell_lvpwell_enc-pcmp_gr2dnw-gr_w, -dnwell_lvpwell_enc-pcmp_gr2dnw-gr_w, pwell_res_w+pwell_res_enc+dnwell_lvpwell_enc+pcmp_gr2dnw+gr_w, pwell_res_l+dnwell_lvpwell_enc+pcmp_gr2dnw+gr_w)
        cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
        pwell_res_cell.shapes(comp).insert(cmp_gr)

        pp_inner = pya.Box(-pwell_res_enc-dnwell_lvpwell_enc-pcmp_gr2dnw+implant_cmp_enc, -dnwell_lvpwell_enc-pcmp_gr2dnw+implant_cmp_enc, pwell_res_w+pwell_res_enc+dnwell_lvpwell_enc+pcmp_gr2dnw-implant_cmp_enc, pwell_res_l+dnwell_lvpwell_enc+pcmp_gr2dnw-implant_cmp_enc)
        pp_outer = pya.Box(-pwell_res_enc-dnwell_lvpwell_enc-pcmp_gr2dnw-gr_w-implant_cmp_enc, -dnwell_lvpwell_enc-pcmp_gr2dnw-gr_w-implant_cmp_enc, pwell_res_w+pwell_res_enc+dnwell_lvpwell_enc+pcmp_gr2dnw+gr_w+implant_cmp_enc, pwell_res_l+dnwell_lvpwell_enc+pcmp_gr2dnw+gr_w+implant_cmp_enc)
        pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
        pwell_res_cell.shapes(pplus).insert(pp_gr)

    # Inserting p diffusion
    pwell_res_cell.shapes(comp).insert(pya.Box(-cmp_width, pwell_cmp_enc, 0, pwell_res_l-pwell_cmp_enc))           #left
    pwell_res_cell.shapes(comp).insert(pya.Box(pwell_res_w, pwell_cmp_enc, pwell_res_w+cmp_width, pwell_res_l-pwell_cmp_enc))  #right
    pwell_res_cell.shapes(pplus).insert(pya.Box(-cmp_width-implant_cmp_enc, pwell_cmp_enc-implant_cmp_enc , implant_cmp_enc, pwell_res_l-pwell_cmp_enc+implant_cmp_enc))
    pwell_res_cell.shapes(pplus).insert(pya.Box(pwell_res_w-implant_cmp_enc, pwell_cmp_enc-implant_cmp_enc , pwell_res_w+cmp_width+implant_cmp_enc, pwell_res_l-pwell_cmp_enc+implant_cmp_enc))

    # Inserting ncomp metal
    pwell_res_cell.shapes(metal1).insert(pya.Box(-cmp_width, pwell_cmp_enc, 0, pwell_res_l-pwell_cmp_enc))           #left
    pwell_res_cell.shapes(metal1).insert(pya.Box(pwell_res_w, pwell_cmp_enc, pwell_res_w+cmp_width, pwell_res_l-pwell_cmp_enc))  #right

    # Inserting pcomp contacts
    num_pcmp_left_con_1, pcmp_left_con_free_spc_1 = number_spc_contacts(cmp_width, comp_cont_enc, cont_min_spc, cont_size)
    num_pcmp_left_con_2, pcmp_left_con_free_spc_2 = number_spc_contacts(pwell_res_l-2*pwell_cmp_enc, comp_cont_enc, cont_min_spc, cont_size)
    pcmp_left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-cmp_width+pcmp_left_con_free_spc_1 / 2, pwell_cmp_enc+pcmp_left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_pcmp_left_con_1, num_pcmp_left_con_2)
    pwell_res_cell.insert(pcmp_left_con_arr)

    num_ncmp_right_con_1, ncmp_right_con_free_spc_1 = number_spc_contacts(cmp_width, comp_cont_enc, cont_min_spc, cont_size)
    num_ncmp_right_con_2, ncmp_right_con_free_spc_2 = number_spc_contacts(pwell_res_l-2*pwell_cmp_enc, comp_cont_enc, cont_min_spc, cont_size)
    ncmp_right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(pwell_res_w+ncmp_right_con_free_spc_1 / 2, pwell_cmp_enc+ncmp_right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_right_con_1, num_ncmp_right_con_2)
    pwell_res_cell.insert(ncmp_right_con_arr)

    # Inserting n diffusion
    pwell_res_cell.shapes(comp).insert(pya.Box(-cmp_width-ncmp_pcmp_spc-cmp_width, 0, -cmp_width-ncmp_pcmp_spc , pwell_res_l))
    pwell_res_cell.shapes(nplus).insert(pya.Box(-cmp_width-ncmp_pcmp_spc-cmp_width-implant_cmp_enc, -implant_cmp_enc, -cmp_width-ncmp_pcmp_spc+implant_cmp_enc , pwell_res_l+implant_cmp_enc))

    # Inserting pcomp metal
    pwell_res_cell.shapes(metal1).insert(pya.Box(-cmp_width-ncmp_pcmp_spc-cmp_width, 0, -cmp_width-ncmp_pcmp_spc , pwell_res_l))

    # Inserting pcomp contacts
    num_ncmp_con_1, ncmp_con_free_spc_1 = number_spc_contacts(cmp_width, comp_cont_enc, cont_min_spc, cont_size)
    num_ncmp_con_2, ncmp_con_free_spc_2 = number_spc_contacts(pwell_res_l, comp_cont_enc, cont_min_spc, cont_size)
    ncmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-cmp_width-ncmp_pcmp_spc-cmp_width+ncmp_con_free_spc_1 / 2, ncmp_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_con_1, num_ncmp_con_2)
    pwell_res_cell.insert(ncmp_con_arr)

    pwell_res_cell.flatten(True)
    return pwell_res_cell

def draw_npolyf_s_res(layout, l, w, deepnwell, pcmpgr):
    '''
    Usage:-
     used to draw 3-terminal salicided n+ poly resistor (Outside DNWELL) by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of diff length
     w      : Float of diff width
    '''

    # Define layers
    dnwell         = layout.layer(12 , 0 )
    comp           = layout.layer(22 , 0 )
    poly           = layout.layer(30 , 0 )
    pplus          = layout.layer(31 , 0 )
    nplus          = layout.layer(32 , 0 )
    contact        = layout.layer(33 , 0 )
    metal1         = layout.layer(34 , 0 )
    res_mk         = layout.layer(110, 5 )


    # VARIABLES
    dbu_PERCISION         = 1/layout.dbu
    npolyf_s_res_w        = w    * dbu_PERCISION
    npolyf_s_res_l        = l    * dbu_PERCISION
    poly_res_enc          = 0.29 * dbu_PERCISION
    implant_cmp_enc       = 0.16 * dbu_PERCISION
    implant_poly_enc      = 0.3  * dbu_PERCISION
    npoly_pcmp_spc        = 0.72 * dbu_PERCISION
    pcmp_width            = 0.36 * dbu_PERCISION
    metal_width           = 0.34 * dbu_PERCISION
    met_cont_enc          = 0.06 * dbu_PERCISION
    comp_cont_enc         = 0.07 * dbu_PERCISION
    cont_size             = 0.22 * dbu_PERCISION
    cont_min_spc          = 0.25 * dbu_PERCISION
    cmp_met_cont_enc_diff = 0.01 * dbu_PERCISION
    dnwell_enc_ncmp       = 0.62 * dbu_PERCISION
    dnwell_enc_poly       = 1.34 * dbu_PERCISION
    pcmp_gr2dnw           = 2.5  * dbu_PERCISION
    gr_w                  = 0.36 * dbu_PERCISION

    # Inserting npolyf_s_res cell
    cell_index  = layout.add_cell("npolyf_s_resistor")
    npolyf_s_res_cell = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting res_mk
    npolyf_s_res_cell.shapes(res_mk).insert(pya.Box(0, 0, npolyf_s_res_w, npolyf_s_res_l))

    # Inserting n poly
    npolyf_s_res_cell.shapes(poly).insert(pya.Box(-poly_res_enc, 0, npolyf_s_res_w+poly_res_enc, npolyf_s_res_l))
    npolyf_s_res_cell.shapes(nplus).insert(pya.Box(-poly_res_enc-implant_poly_enc, -implant_poly_enc , npolyf_s_res_w+poly_res_enc+implant_poly_enc, npolyf_s_res_l+implant_poly_enc))

    # Inserting ncomp metal
    npolyf_s_res_cell.shapes(metal1).insert(pya.Box(-cont_size-met_cont_enc , cmp_met_cont_enc_diff , met_cont_enc , npolyf_s_res_l-cmp_met_cont_enc_diff))                       #left
    npolyf_s_res_cell.shapes(metal1).insert(pya.Box(npolyf_s_res_w-met_cont_enc, cmp_met_cont_enc_diff , npolyf_s_res_w+cont_size+met_cont_enc , npolyf_s_res_l-cmp_met_cont_enc_diff)) # Right

    # Inserting ncomp contacts
    num_ncmp_left_con_1, ncmp_left_con_free_spc_1 = number_spc_contacts(metal_width, met_cont_enc, cont_min_spc, cont_size)
    num_ncmp_left_con_2, ncmp_left_con_free_spc_2 = number_spc_contacts(npolyf_s_res_l-2*cmp_met_cont_enc_diff, met_cont_enc, cont_min_spc, cont_size)
    ncmp_left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-cont_size-met_cont_enc+ncmp_left_con_free_spc_1 / 2, cmp_met_cont_enc_diff+ncmp_left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_left_con_1, num_ncmp_left_con_2)
    npolyf_s_res_cell.insert(ncmp_left_con_arr)

    num_ncmp_right_con_1, ncmp_right_con_free_spc_1 = number_spc_contacts(metal_width, met_cont_enc, cont_min_spc, cont_size)
    num_ncmp_right_con_2, ncmp_right_con_free_spc_2 = number_spc_contacts(npolyf_s_res_l-2*cmp_met_cont_enc_diff, met_cont_enc, cont_min_spc, cont_size)
    ncmp_right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(npolyf_s_res_w-met_cont_enc+ncmp_right_con_free_spc_1 / 2, cmp_met_cont_enc_diff+ncmp_right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_right_con_1, num_ncmp_right_con_2)
    npolyf_s_res_cell.insert(ncmp_right_con_arr)

    # Inserting p diffusion
    npolyf_s_res_cell.shapes(comp).insert(pya.Box(-poly_res_enc-npoly_pcmp_spc-pcmp_width, 0, -poly_res_enc-npoly_pcmp_spc, npolyf_s_res_l))

    # Inserting pcomp metal
    npolyf_s_res_cell.shapes(metal1).insert(pya.Box(-poly_res_enc-npoly_pcmp_spc-pcmp_width, 0, -poly_res_enc-npoly_pcmp_spc, npolyf_s_res_l))

    # Inserting pcomp contacts
    num_pcmp_con_1, pcmp_con_free_spc_1 = number_spc_contacts(pcmp_width, comp_cont_enc, cont_min_spc, cont_size)
    num_pcmp_con_2, pcmp_con_free_spc_2 = number_spc_contacts(npolyf_s_res_l, comp_cont_enc, cont_min_spc, cont_size)
    pcmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-poly_res_enc-npoly_pcmp_spc-pcmp_width+pcmp_con_free_spc_1 / 2, pcmp_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_pcmp_con_1, num_pcmp_con_2)
    npolyf_s_res_cell.insert(pcmp_con_arr)

    if deepnwell == True:
        # Inserting Ntap
        npolyf_s_res_cell.shapes(nplus).insert(pya.Box(-poly_res_enc-npoly_pcmp_spc-pcmp_width-implant_cmp_enc, -implant_cmp_enc , -poly_res_enc-npoly_pcmp_spc+implant_cmp_enc, npolyf_s_res_l+implant_cmp_enc))

        # Inserting dnwell
        npolyf_s_res_cell.shapes(dnwell).insert(pya.Box(-poly_res_enc-npoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp, -dnwell_enc_poly , npolyf_s_res_w+poly_res_enc+dnwell_enc_poly, npolyf_s_res_l+dnwell_enc_poly))

        # Inserting Guard Ring
        if pcmpgr == True:
            cmp_inner = pya.Box(-poly_res_enc-npoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw, -dnwell_enc_poly-pcmp_gr2dnw , npolyf_s_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw, npolyf_s_res_l+dnwell_enc_poly+pcmp_gr2dnw)
            cmp_outer = pya.Box(-poly_res_enc-npoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw-gr_w, -dnwell_enc_poly-pcmp_gr2dnw-gr_w , npolyf_s_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw+gr_w, npolyf_s_res_l+dnwell_enc_poly+pcmp_gr2dnw+gr_w)
            cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
            npolyf_s_res_cell.shapes(comp).insert(cmp_gr)

            pp_inner = pya.Box(-poly_res_enc-npoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw+implant_cmp_enc, -dnwell_enc_poly-pcmp_gr2dnw+implant_cmp_enc , npolyf_s_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw-implant_cmp_enc, npolyf_s_res_l+dnwell_enc_poly+pcmp_gr2dnw-implant_cmp_enc)
            pp_outer = pya.Box(-poly_res_enc-npoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw-gr_w-implant_cmp_enc, -dnwell_enc_poly-pcmp_gr2dnw-gr_w-implant_cmp_enc , npolyf_s_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw+gr_w+implant_cmp_enc, npolyf_s_res_l+dnwell_enc_poly+pcmp_gr2dnw+gr_w+implant_cmp_enc)
            pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
            npolyf_s_res_cell.shapes(pplus).insert(pp_gr)

    else:
        npolyf_s_res_cell.shapes(pplus).insert(pya.Box(-poly_res_enc-npoly_pcmp_spc-pcmp_width-implant_cmp_enc, -implant_cmp_enc , -poly_res_enc-npoly_pcmp_spc+implant_cmp_enc, npolyf_s_res_l+implant_cmp_enc))


    npolyf_s_res_cell.flatten(True)
    return npolyf_s_res_cell

def draw_ppolyf_s_res(layout, l, w, deepnwell, pcmpgr):
    '''
    Usage:-
     used to draw 3-terminal salicided p+ poly resistor (Outside DNWELL) by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of diff length
     w      : Float of diff width
    '''

    # Define layers
    dnwell         = layout.layer(12 , 0 )
    comp           = layout.layer(22 , 0 )
    poly           = layout.layer(30 , 0 )
    pplus          = layout.layer(31 , 0 )
    nplus          = layout.layer(32 , 0 )
    contact        = layout.layer(33 , 0 )
    metal1         = layout.layer(34 , 0 )
    res_mk         = layout.layer(110, 5 )


    # VARIABLES
    dbu_PERCISION         = 1/layout.dbu
    ppolyf_s_res_w        = w    * dbu_PERCISION
    ppolyf_s_res_l        = l    * dbu_PERCISION
    poly_res_enc          = 0.29 * dbu_PERCISION
    implant_cmp_enc       = 0.16 * dbu_PERCISION
    implant_poly_enc      = 0.3  * dbu_PERCISION
    ppoly_pcmp_spc        = 0.86 * dbu_PERCISION
    pcmp_width            = 0.36 * dbu_PERCISION
    metal_width           = 0.34 * dbu_PERCISION
    met_cont_enc          = 0.06 * dbu_PERCISION
    comp_cont_enc         = 0.07 * dbu_PERCISION
    cont_size             = 0.22 * dbu_PERCISION
    cont_min_spc          = 0.25 * dbu_PERCISION
    cmp_met_cont_enc_diff = 0.01 * dbu_PERCISION
    dnwell_enc_ncmp       = 0.62 * dbu_PERCISION
    dnwell_enc_poly       = 1.34 * dbu_PERCISION
    pcmp_gr2dnw           = 2.5  * dbu_PERCISION
    gr_w                  = 0.36 * dbu_PERCISION

    # Inserting ppolyf_s_res cell
    cell_index  = layout.add_cell("ppolyf_s_resistor")
    ppolyf_s_res_cell = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting res_mk
    ppolyf_s_res_cell.shapes(res_mk).insert(pya.Box(0, 0, ppolyf_s_res_w, ppolyf_s_res_l))

    # Inserting n poly
    ppolyf_s_res_cell.shapes(poly).insert(pya.Box(-poly_res_enc, 0, ppolyf_s_res_w+poly_res_enc, ppolyf_s_res_l))
    ppolyf_s_res_cell.shapes(pplus).insert(pya.Box(-poly_res_enc-implant_poly_enc, -implant_poly_enc , ppolyf_s_res_w+poly_res_enc+implant_poly_enc, ppolyf_s_res_l+implant_poly_enc))

    # Inserting ncomp metal
    ppolyf_s_res_cell.shapes(metal1).insert(pya.Box(-cont_size-met_cont_enc , cmp_met_cont_enc_diff , met_cont_enc , ppolyf_s_res_l-cmp_met_cont_enc_diff))                       #left
    ppolyf_s_res_cell.shapes(metal1).insert(pya.Box(ppolyf_s_res_w-met_cont_enc, cmp_met_cont_enc_diff , ppolyf_s_res_w+cont_size+met_cont_enc , ppolyf_s_res_l-cmp_met_cont_enc_diff)) # Right

    # Inserting ncomp contacts
    num_ncmp_left_con_1, ncmp_left_con_free_spc_1 = number_spc_contacts(metal_width, met_cont_enc, cont_min_spc, cont_size)
    num_ncmp_left_con_2, ncmp_left_con_free_spc_2 = number_spc_contacts(ppolyf_s_res_l-2*cmp_met_cont_enc_diff, met_cont_enc, cont_min_spc, cont_size)
    ncmp_left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-cont_size-met_cont_enc+ncmp_left_con_free_spc_1 / 2, cmp_met_cont_enc_diff+ncmp_left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_left_con_1, num_ncmp_left_con_2)
    ppolyf_s_res_cell.insert(ncmp_left_con_arr)

    num_ncmp_right_con_1, ncmp_right_con_free_spc_1 = number_spc_contacts(metal_width, met_cont_enc, cont_min_spc, cont_size)
    num_ncmp_right_con_2, ncmp_right_con_free_spc_2 = number_spc_contacts(ppolyf_s_res_l-2*cmp_met_cont_enc_diff, met_cont_enc, cont_min_spc, cont_size)
    ncmp_right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(ppolyf_s_res_w-met_cont_enc+ncmp_right_con_free_spc_1 / 2, cmp_met_cont_enc_diff+ncmp_right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_right_con_1, num_ncmp_right_con_2)
    ppolyf_s_res_cell.insert(ncmp_right_con_arr)

    # Inserting p diffusion
    ppolyf_s_res_cell.shapes(comp).insert(pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width, 0, -poly_res_enc-ppoly_pcmp_spc, ppolyf_s_res_l))

    # Inserting pcomp metal
    ppolyf_s_res_cell.shapes(metal1).insert(pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width, 0, -poly_res_enc-ppoly_pcmp_spc, ppolyf_s_res_l))

    # Inserting pcomp contacts
    num_pcmp_con_1, pcmp_con_free_spc_1 = number_spc_contacts(pcmp_width, comp_cont_enc, cont_min_spc, cont_size)
    num_pcmp_con_2, pcmp_con_free_spc_2 = number_spc_contacts(ppolyf_s_res_l, comp_cont_enc, cont_min_spc, cont_size)
    pcmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-poly_res_enc-ppoly_pcmp_spc-pcmp_width+pcmp_con_free_spc_1 / 2, pcmp_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_pcmp_con_1, num_pcmp_con_2)
    ppolyf_s_res_cell.insert(pcmp_con_arr)

    if deepnwell == True:
        # Inserting Ntap
        ppolyf_s_res_cell.shapes(nplus).insert(pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-implant_cmp_enc, -implant_cmp_enc , -poly_res_enc-ppoly_pcmp_spc+implant_cmp_enc, ppolyf_s_res_l+implant_cmp_enc))

        # Inserting dnwell
        ppolyf_s_res_cell.shapes(dnwell).insert(pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp, -dnwell_enc_poly , ppolyf_s_res_w+poly_res_enc+dnwell_enc_poly, ppolyf_s_res_l+dnwell_enc_poly))

        # Inserting Guard Ring
        if pcmpgr == True:
            cmp_inner = pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw, -dnwell_enc_poly-pcmp_gr2dnw , ppolyf_s_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw, ppolyf_s_res_l+dnwell_enc_poly+pcmp_gr2dnw)
            cmp_outer = pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw-gr_w, -dnwell_enc_poly-pcmp_gr2dnw-gr_w , ppolyf_s_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw+gr_w, ppolyf_s_res_l+dnwell_enc_poly+pcmp_gr2dnw+gr_w)
            cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
            ppolyf_s_res_cell.shapes(comp).insert(cmp_gr)

            pp_inner = pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw+implant_cmp_enc, -dnwell_enc_poly-pcmp_gr2dnw+implant_cmp_enc , ppolyf_s_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw-implant_cmp_enc, ppolyf_s_res_l+dnwell_enc_poly+pcmp_gr2dnw-implant_cmp_enc)
            pp_outer = pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw-gr_w-implant_cmp_enc, -dnwell_enc_poly-pcmp_gr2dnw-gr_w-implant_cmp_enc , ppolyf_s_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw+gr_w+implant_cmp_enc, ppolyf_s_res_l+dnwell_enc_poly+pcmp_gr2dnw+gr_w+implant_cmp_enc)
            pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
            ppolyf_s_res_cell.shapes(pplus).insert(pp_gr)

    else:
        ppolyf_s_res_cell.shapes(pplus).insert(pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-implant_cmp_enc, -implant_cmp_enc , -poly_res_enc-ppoly_pcmp_spc+implant_cmp_enc, ppolyf_s_res_l+implant_cmp_enc))


    ppolyf_s_res_cell.flatten(True)
    return ppolyf_s_res_cell

def draw_npolyf_u_res(layout, l, w, deepnwell, pcmpgr):
    '''
    Usage:-
     used to draw 3-terminal unsalicided n+ poly resistor (Outside DNWELL) by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of diff length
     w      : Float of diff width
    '''

    # Define layers
    dnwell         = layout.layer(12 , 0 )
    comp           = layout.layer(22 , 0 )
    poly           = layout.layer(30 , 0 )
    pplus          = layout.layer(31 , 0 )
    nplus          = layout.layer(32 , 0 )
    contact        = layout.layer(33 , 0 )
    metal1         = layout.layer(34 , 0 )
    sab            = layout.layer(49 , 0 )
    res_mk         = layout.layer(110, 5 )


    # VARIABLES
    dbu_PERCISION         = 1/layout.dbu
    npolyf_u_res_w        = w    * dbu_PERCISION
    npolyf_u_res_l        = l    * dbu_PERCISION
    poly_res_enc          = 0.51 * dbu_PERCISION
    sab_res_enc           = 0.28 * dbu_PERCISION
    implant_cmp_enc       = 0.16 * dbu_PERCISION
    implant_poly_enc      = 0.3  * dbu_PERCISION
    npoly_pcmp_spc        = 0.72 * dbu_PERCISION
    pcmp_width            = 0.36 * dbu_PERCISION
    metal_width           = 0.34 * dbu_PERCISION
    met_cont_enc          = 0.06 * dbu_PERCISION
    comp_cont_enc         = 0.07 * dbu_PERCISION
    cont_size             = 0.22 * dbu_PERCISION
    cont_min_spc          = 0.25 * dbu_PERCISION
    cmp_met_cont_enc_diff = 0.01 * dbu_PERCISION
    dnwell_enc_ncmp       = 0.62 * dbu_PERCISION
    dnwell_enc_poly       = 1.34 * dbu_PERCISION
    pcmp_gr2dnw           = 2.5  * dbu_PERCISION
    gr_w                  = 0.36 * dbu_PERCISION

    # Inserting npolyf_u_res cell
    cell_index  = layout.add_cell("npolyf_u_resistor")
    npolyf_u_res_cell = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting res_mk
    npolyf_u_res_cell.shapes(res_mk).insert(pya.Box(0, 0, npolyf_u_res_w, npolyf_u_res_l))

    # Inserting sab
    npolyf_u_res_cell.shapes(sab).insert(pya.Box(0, -sab_res_enc, npolyf_u_res_w, npolyf_u_res_l+sab_res_enc))

    # Inserting n poly
    npolyf_u_res_cell.shapes(poly).insert(pya.Box(-poly_res_enc, 0, npolyf_u_res_w+poly_res_enc, npolyf_u_res_l))
    npolyf_u_res_cell.shapes(nplus).insert(pya.Box(-poly_res_enc-implant_poly_enc, -implant_poly_enc , npolyf_u_res_w+poly_res_enc+implant_poly_enc, npolyf_u_res_l+implant_poly_enc))

    # Inserting npoly metal
    npolyf_u_res_cell.shapes(metal1).insert(pya.Box(-poly_res_enc+cmp_met_cont_enc_diff , cmp_met_cont_enc_diff , -poly_res_enc+cmp_met_cont_enc_diff+metal_width , npolyf_u_res_l-cmp_met_cont_enc_diff))    #left
    npolyf_u_res_cell.shapes(metal1).insert(pya.Box(npolyf_u_res_w+poly_res_enc-cmp_met_cont_enc_diff-metal_width, cmp_met_cont_enc_diff , npolyf_u_res_w+poly_res_enc-cmp_met_cont_enc_diff , npolyf_u_res_l-cmp_met_cont_enc_diff)) # Right

    # Inserting npoly contacts
    num_ncmp_left_con_1, ncmp_left_con_free_spc_1 = number_spc_contacts(metal_width, met_cont_enc, cont_min_spc, cont_size)
    num_ncmp_left_con_2, ncmp_left_con_free_spc_2 = number_spc_contacts(npolyf_u_res_l-2*cmp_met_cont_enc_diff, met_cont_enc, cont_min_spc, cont_size)
    ncmp_left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-poly_res_enc+cmp_met_cont_enc_diff+ncmp_left_con_free_spc_1 / 2, cmp_met_cont_enc_diff+ncmp_left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_left_con_1, num_ncmp_left_con_2)
    npolyf_u_res_cell.insert(ncmp_left_con_arr)

    num_ncmp_right_con_1, ncmp_right_con_free_spc_1 = number_spc_contacts(metal_width, met_cont_enc, cont_min_spc, cont_size)
    num_ncmp_right_con_2, ncmp_right_con_free_spc_2 = number_spc_contacts(npolyf_u_res_l-2*cmp_met_cont_enc_diff, met_cont_enc, cont_min_spc, cont_size)
    ncmp_right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(npolyf_u_res_w+poly_res_enc-cmp_met_cont_enc_diff-metal_width+ncmp_right_con_free_spc_1 / 2, cmp_met_cont_enc_diff+ncmp_right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_right_con_1, num_ncmp_right_con_2)
    npolyf_u_res_cell.insert(ncmp_right_con_arr)


    # Inserting p diffusion
    npolyf_u_res_cell.shapes(comp).insert(pya.Box(-poly_res_enc-npoly_pcmp_spc-pcmp_width, 0, -poly_res_enc-npoly_pcmp_spc, npolyf_u_res_l))

    # Inserting pcomp metal
    npolyf_u_res_cell.shapes(metal1).insert(pya.Box(-poly_res_enc-npoly_pcmp_spc-pcmp_width, 0, -poly_res_enc-npoly_pcmp_spc, npolyf_u_res_l))

    # Inserting pcomp contacts
    num_pcmp_con_1, pcmp_con_free_spc_1 = number_spc_contacts(pcmp_width, comp_cont_enc, cont_min_spc, cont_size)
    num_pcmp_con_2, pcmp_con_free_spc_2 = number_spc_contacts(npolyf_u_res_l, comp_cont_enc, cont_min_spc, cont_size)
    pcmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-poly_res_enc-npoly_pcmp_spc-pcmp_width+pcmp_con_free_spc_1 / 2, pcmp_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_pcmp_con_1, num_pcmp_con_2)
    npolyf_u_res_cell.insert(pcmp_con_arr)

    if deepnwell == True:
        # Inserting Ntap
        npolyf_u_res_cell.shapes(nplus).insert(pya.Box(-poly_res_enc-npoly_pcmp_spc-pcmp_width-implant_cmp_enc, -implant_cmp_enc , -poly_res_enc-npoly_pcmp_spc+implant_cmp_enc, npolyf_u_res_l+implant_cmp_enc))

        # Inserting dnwell
        npolyf_u_res_cell.shapes(dnwell).insert(pya.Box(-poly_res_enc-npoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp, -dnwell_enc_poly , npolyf_u_res_w+poly_res_enc+dnwell_enc_poly, npolyf_u_res_l+dnwell_enc_poly))

        # Inserting Guard Ring
        if pcmpgr == True:
            cmp_inner = pya.Box(-poly_res_enc-npoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw, -dnwell_enc_poly-pcmp_gr2dnw , npolyf_u_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw, npolyf_u_res_l+dnwell_enc_poly+pcmp_gr2dnw)
            cmp_outer = pya.Box(-poly_res_enc-npoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw-gr_w, -dnwell_enc_poly-pcmp_gr2dnw-gr_w , npolyf_u_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw+gr_w, npolyf_u_res_l+dnwell_enc_poly+pcmp_gr2dnw+gr_w)
            cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
            npolyf_u_res_cell.shapes(comp).insert(cmp_gr)

            pp_inner = pya.Box(-poly_res_enc-npoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw+implant_cmp_enc, -dnwell_enc_poly-pcmp_gr2dnw+implant_cmp_enc , npolyf_u_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw-implant_cmp_enc, npolyf_u_res_l+dnwell_enc_poly+pcmp_gr2dnw-implant_cmp_enc)
            pp_outer = pya.Box(-poly_res_enc-npoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw-gr_w-implant_cmp_enc, -dnwell_enc_poly-pcmp_gr2dnw-gr_w-implant_cmp_enc , npolyf_u_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw+gr_w+implant_cmp_enc, npolyf_u_res_l+dnwell_enc_poly+pcmp_gr2dnw+gr_w+implant_cmp_enc)
            pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
            npolyf_u_res_cell.shapes(pplus).insert(pp_gr)

    else:
        npolyf_u_res_cell.shapes(pplus).insert(pya.Box(-poly_res_enc-npoly_pcmp_spc-pcmp_width-implant_cmp_enc, -implant_cmp_enc , -poly_res_enc-npoly_pcmp_spc+implant_cmp_enc, npolyf_u_res_l+implant_cmp_enc))


    npolyf_u_res_cell.flatten(True)
    return npolyf_u_res_cell

def draw_ppolyf_u_res(layout, l, w, deepnwell, pcmpgr):
    '''
    Usage:-
     used to draw 3-terminal unsalicided p+ poly resistor (Outside DNWELL) by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of diff length
     w      : Float of diff width
    '''

    # Define layers
    dnwell         = layout.layer(12 , 0 )
    comp           = layout.layer(22 , 0 )
    poly           = layout.layer(30 , 0 )
    pplus          = layout.layer(31 , 0 )
    nplus          = layout.layer(32 , 0 )
    contact        = layout.layer(33 , 0 )
    metal1         = layout.layer(34 , 0 )
    sab            = layout.layer(49 , 0 )
    res_mk         = layout.layer(110, 5 )


    # VARIABLES
    dbu_PERCISION         = 1/layout.dbu
    ppolyf_u_res_w        = w    * dbu_PERCISION
    ppolyf_u_res_l        = l    * dbu_PERCISION
    poly_res_enc          = 0.51 * dbu_PERCISION
    sab_res_enc           = 0.28 * dbu_PERCISION
    implant_cmp_enc       = 0.16 * dbu_PERCISION
    implant_poly_enc      = 0.3  * dbu_PERCISION
    ppoly_pcmp_spc        = 0.86 * dbu_PERCISION
    pcmp_width            = 0.36 * dbu_PERCISION
    metal_width           = 0.34 * dbu_PERCISION
    met_cont_enc          = 0.06 * dbu_PERCISION
    comp_cont_enc         = 0.07 * dbu_PERCISION
    cont_size             = 0.22 * dbu_PERCISION
    cont_min_spc          = 0.25 * dbu_PERCISION
    cmp_met_cont_enc_diff = 0.01 * dbu_PERCISION
    dnwell_enc_ncmp       = 0.62 * dbu_PERCISION
    dnwell_enc_poly       = 1.34 * dbu_PERCISION
    pcmp_gr2dnw           = 2.5  * dbu_PERCISION
    gr_w                  = 0.36 * dbu_PERCISION

    # Inserting ppolyf_u_res cell
    cell_index  = layout.add_cell("ppolyf_u_resistor")
    ppolyf_u_res_cell = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting res_mk
    ppolyf_u_res_cell.shapes(res_mk).insert(pya.Box(0, 0, ppolyf_u_res_w, ppolyf_u_res_l))

    # Inserting sab
    ppolyf_u_res_cell.shapes(sab).insert(pya.Box(0, -sab_res_enc, ppolyf_u_res_w, ppolyf_u_res_l+sab_res_enc))

    # Inserting p poly
    ppolyf_u_res_cell.shapes(poly).insert(pya.Box(-poly_res_enc, 0, ppolyf_u_res_w+poly_res_enc, ppolyf_u_res_l))
    ppolyf_u_res_cell.shapes(pplus).insert(pya.Box(-poly_res_enc-implant_poly_enc, -implant_poly_enc , ppolyf_u_res_w+poly_res_enc+implant_poly_enc, ppolyf_u_res_l+implant_poly_enc))

    # Inserting npoly metal
    ppolyf_u_res_cell.shapes(metal1).insert(pya.Box(-poly_res_enc+cmp_met_cont_enc_diff , cmp_met_cont_enc_diff , -poly_res_enc+cmp_met_cont_enc_diff+metal_width , ppolyf_u_res_l-cmp_met_cont_enc_diff))    #left
    ppolyf_u_res_cell.shapes(metal1).insert(pya.Box(ppolyf_u_res_w+poly_res_enc-cmp_met_cont_enc_diff-metal_width, cmp_met_cont_enc_diff , ppolyf_u_res_w+poly_res_enc-cmp_met_cont_enc_diff , ppolyf_u_res_l-cmp_met_cont_enc_diff)) # Right

    # Inserting npoly contacts
    num_ncmp_left_con_1, ncmp_left_con_free_spc_1 = number_spc_contacts(metal_width, met_cont_enc, cont_min_spc, cont_size)
    num_ncmp_left_con_2, ncmp_left_con_free_spc_2 = number_spc_contacts(ppolyf_u_res_l-2*cmp_met_cont_enc_diff, met_cont_enc, cont_min_spc, cont_size)
    ncmp_left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-poly_res_enc+cmp_met_cont_enc_diff+ncmp_left_con_free_spc_1 / 2, cmp_met_cont_enc_diff+ncmp_left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_left_con_1, num_ncmp_left_con_2)
    ppolyf_u_res_cell.insert(ncmp_left_con_arr)

    num_ncmp_right_con_1, ncmp_right_con_free_spc_1 = number_spc_contacts(metal_width, met_cont_enc, cont_min_spc, cont_size)
    num_ncmp_right_con_2, ncmp_right_con_free_spc_2 = number_spc_contacts(ppolyf_u_res_l-2*cmp_met_cont_enc_diff, met_cont_enc, cont_min_spc, cont_size)
    ncmp_right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(ppolyf_u_res_w+poly_res_enc-cmp_met_cont_enc_diff-metal_width+ncmp_right_con_free_spc_1 / 2, cmp_met_cont_enc_diff+ncmp_right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_right_con_1, num_ncmp_right_con_2)
    ppolyf_u_res_cell.insert(ncmp_right_con_arr)


    # Inserting p diffusion
    ppolyf_u_res_cell.shapes(comp).insert(pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width, 0, -poly_res_enc-ppoly_pcmp_spc, ppolyf_u_res_l))

    # Inserting pcomp metal
    ppolyf_u_res_cell.shapes(metal1).insert(pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width, 0, -poly_res_enc-ppoly_pcmp_spc, ppolyf_u_res_l))

    # Inserting pcomp contacts
    num_pcmp_con_1, pcmp_con_free_spc_1 = number_spc_contacts(pcmp_width, comp_cont_enc, cont_min_spc, cont_size)
    num_pcmp_con_2, pcmp_con_free_spc_2 = number_spc_contacts(ppolyf_u_res_l, comp_cont_enc, cont_min_spc, cont_size)
    pcmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-poly_res_enc-ppoly_pcmp_spc-pcmp_width+pcmp_con_free_spc_1 / 2, pcmp_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_pcmp_con_1, num_pcmp_con_2)
    ppolyf_u_res_cell.insert(pcmp_con_arr)

    if deepnwell == True:
        # Inserting Ntap
        ppolyf_u_res_cell.shapes(nplus).insert(pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-implant_cmp_enc, -implant_cmp_enc , -poly_res_enc-ppoly_pcmp_spc+implant_cmp_enc, ppolyf_u_res_l+implant_cmp_enc))

        # Inserting dnwell
        ppolyf_u_res_cell.shapes(dnwell).insert(pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp, -dnwell_enc_poly , ppolyf_u_res_w+poly_res_enc+dnwell_enc_poly, ppolyf_u_res_l+dnwell_enc_poly))

        # Inserting Guard Ring
        if pcmpgr == True:
            cmp_inner = pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw, -dnwell_enc_poly-pcmp_gr2dnw , ppolyf_u_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw, ppolyf_u_res_l+dnwell_enc_poly+pcmp_gr2dnw)
            cmp_outer = pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw-gr_w, -dnwell_enc_poly-pcmp_gr2dnw-gr_w , ppolyf_u_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw+gr_w, ppolyf_u_res_l+dnwell_enc_poly+pcmp_gr2dnw+gr_w)
            cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
            ppolyf_u_res_cell.shapes(comp).insert(cmp_gr)

            pp_inner = pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw+implant_cmp_enc, -dnwell_enc_poly-pcmp_gr2dnw+implant_cmp_enc , ppolyf_u_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw-implant_cmp_enc, ppolyf_u_res_l+dnwell_enc_poly+pcmp_gr2dnw-implant_cmp_enc)
            pp_outer = pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw-gr_w-implant_cmp_enc, -dnwell_enc_poly-pcmp_gr2dnw-gr_w-implant_cmp_enc , ppolyf_u_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw+gr_w+implant_cmp_enc, ppolyf_u_res_l+dnwell_enc_poly+pcmp_gr2dnw+gr_w+implant_cmp_enc)
            pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
            ppolyf_u_res_cell.shapes(pplus).insert(pp_gr)

    else:
        ppolyf_u_res_cell.shapes(pplus).insert(pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-implant_cmp_enc, -implant_cmp_enc , -poly_res_enc-ppoly_pcmp_spc+implant_cmp_enc, ppolyf_u_res_l+implant_cmp_enc))


    ppolyf_u_res_cell.flatten(True)
    return ppolyf_u_res_cell

def draw_ppolyf_u_high_Rs_res(layout, l, w , volt, deepnwell, pcmpgr):
    '''
    Usage:-
     used to draw high-Rs p+ poly resistor (outside DNWELL) by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of diff length
     w      : Float of diff width
    '''

    # Define layers
    dnwell         = layout.layer(12 , 0 )
    comp           = layout.layer(22 , 0 )
    poly           = layout.layer(30 , 0 )
    nplus          = layout.layer(32 , 0 )
    pplus          = layout.layer(31 , 0 )
    contact        = layout.layer(33 , 0 )
    metal1         = layout.layer(34 , 0 )
    sab            = layout.layer(49 , 0 )
    res_mk         = layout.layer(110, 5 )
    resistor       = layout.layer(62 , 0 )
    dualgate       = layout.layer(55 , 0 )

    # VARIABLES
    dbu_PERCISION         = 1/layout.dbu
    ppolyf_u_high_Rs_res_w     = w    * dbu_PERCISION
    ppolyf_u_high_Rs_res_l     = l    * dbu_PERCISION
    poly_res_enc          = 0.64 * dbu_PERCISION
    sab_res_enc           = 0.28 * dbu_PERCISION
    sab_res_ext           = 0.1  * dbu_PERCISION
    implant_cmp_enc       = 0.02 * dbu_PERCISION
    implant_poly_enc      = 0.18 * dbu_PERCISION
    ppoly_pcmp_spc        = 0.7  * dbu_PERCISION
    pcmp_width            = 0.42 * dbu_PERCISION
    metal_width           = 0.34 * dbu_PERCISION
    met_cont_enc          = 0.06 * dbu_PERCISION
    comp_cont_enc         = 0.07 * dbu_PERCISION
    cont_size             = 0.22 * dbu_PERCISION
    cont_min_spc          = 0.25 * dbu_PERCISION
    cmp_met_cont_enc_diff = 0.01 * dbu_PERCISION
    resistor_poly_enc     = 0.4  * dbu_PERCISION
    dnwell_enc_ncmp       = 0.62 * dbu_PERCISION
    dnwell_enc_poly       = 1.34 * dbu_PERCISION
    pcmp_gr2dnw           = 2.5  * dbu_PERCISION
    gr_w                  = 0.36 * dbu_PERCISION
    dg_enc_dnwell         = 0.5  * dbu_PERCISION

    if volt == "5/6V":
        dnwell_enc_ncmp       = 0.66 * dbu_PERCISION


    # Inserting ppolyf_u_high_Rs_res cell
    cell_index  = layout.add_cell("ppolyf_u_high_Rs_resistor")
    ppolyf_u_high_Rs_res_cell = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting res_mk
    ppolyf_u_high_Rs_res_cell.shapes(res_mk).insert(pya.Box(0, 0, ppolyf_u_high_Rs_res_w, ppolyf_u_high_Rs_res_l))

    # Inserting sab
    ppolyf_u_high_Rs_res_cell.shapes(sab).insert(pya.Box(-sab_res_ext, -sab_res_enc, ppolyf_u_high_Rs_res_w+sab_res_ext, ppolyf_u_high_Rs_res_l+sab_res_enc))

    # Inserting p poly
    ppolyf_u_high_Rs_res_cell.shapes(poly).insert(pya.Box(-poly_res_enc, 0, ppolyf_u_high_Rs_res_w+poly_res_enc, ppolyf_u_high_Rs_res_l))
    ppolyf_u_high_Rs_res_cell.shapes(pplus).insert(pya.Box(-poly_res_enc-implant_poly_enc, -implant_poly_enc , 0 , ppolyf_u_high_Rs_res_l+implant_poly_enc))
    ppolyf_u_high_Rs_res_cell.shapes(pplus).insert(pya.Box(ppolyf_u_high_Rs_res_w, -implant_poly_enc , ppolyf_u_high_Rs_res_w+poly_res_enc+implant_poly_enc, ppolyf_u_high_Rs_res_l+implant_poly_enc))

    # Inserting npoly metal
    ppolyf_u_high_Rs_res_cell.shapes(metal1).insert(pya.Box(-poly_res_enc+cmp_met_cont_enc_diff , cmp_met_cont_enc_diff , -poly_res_enc+cmp_met_cont_enc_diff+metal_width , ppolyf_u_high_Rs_res_l-cmp_met_cont_enc_diff))    #left
    ppolyf_u_high_Rs_res_cell.shapes(metal1).insert(pya.Box(ppolyf_u_high_Rs_res_w+poly_res_enc-cmp_met_cont_enc_diff-metal_width, cmp_met_cont_enc_diff , ppolyf_u_high_Rs_res_w+poly_res_enc-cmp_met_cont_enc_diff , ppolyf_u_high_Rs_res_l-cmp_met_cont_enc_diff)) # Right

    # Inserting npoly contacts
    num_ncmp_left_con_1, ncmp_left_con_free_spc_1 = number_spc_contacts(metal_width, met_cont_enc, cont_min_spc, cont_size)
    num_ncmp_left_con_2, ncmp_left_con_free_spc_2 = number_spc_contacts(ppolyf_u_high_Rs_res_l-2*cmp_met_cont_enc_diff, met_cont_enc, cont_min_spc, cont_size)
    ncmp_left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-poly_res_enc+cmp_met_cont_enc_diff+ncmp_left_con_free_spc_1 / 2, cmp_met_cont_enc_diff+ncmp_left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_left_con_1, num_ncmp_left_con_2)
    ppolyf_u_high_Rs_res_cell.insert(ncmp_left_con_arr)

    num_ncmp_right_con_1, ncmp_right_con_free_spc_1 = number_spc_contacts(metal_width, met_cont_enc, cont_min_spc, cont_size)
    num_ncmp_right_con_2, ncmp_right_con_free_spc_2 = number_spc_contacts(ppolyf_u_high_Rs_res_l-2*cmp_met_cont_enc_diff, met_cont_enc, cont_min_spc, cont_size)
    ncmp_right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(ppolyf_u_high_Rs_res_w+poly_res_enc-cmp_met_cont_enc_diff-metal_width+ncmp_right_con_free_spc_1 / 2, cmp_met_cont_enc_diff+ncmp_right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_right_con_1, num_ncmp_right_con_2)
    ppolyf_u_high_Rs_res_cell.insert(ncmp_right_con_arr)


    # Inserting p diffusion
    ppolyf_u_high_Rs_res_cell.shapes(comp).insert(pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width, 0, -poly_res_enc-ppoly_pcmp_spc, ppolyf_u_high_Rs_res_l))

    # Inserting pcomp metal
    ppolyf_u_high_Rs_res_cell.shapes(metal1).insert(pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width, 0, -poly_res_enc-ppoly_pcmp_spc, ppolyf_u_high_Rs_res_l))

    # Inserting pcomp contacts
    num_pcmp_con_1, pcmp_con_free_spc_1 = number_spc_contacts(pcmp_width, comp_cont_enc, cont_min_spc, cont_size)
    num_pcmp_con_2, pcmp_con_free_spc_2 = number_spc_contacts(ppolyf_u_high_Rs_res_l, comp_cont_enc, cont_min_spc, cont_size)
    pcmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-poly_res_enc-ppoly_pcmp_spc-pcmp_width+pcmp_con_free_spc_1 / 2, pcmp_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_pcmp_con_1, num_pcmp_con_2)
    ppolyf_u_high_Rs_res_cell.insert(pcmp_con_arr)

    # Inserting resistor
    ppolyf_u_high_Rs_res_cell.shapes(resistor).insert(pya.Box(-poly_res_enc-resistor_poly_enc, -resistor_poly_enc , ppolyf_u_high_Rs_res_w+poly_res_enc+resistor_poly_enc, ppolyf_u_high_Rs_res_l+resistor_poly_enc))

    if deepnwell == True:
        # Inserting Ntap
        ppolyf_u_high_Rs_res_cell.shapes(nplus).insert(pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-implant_cmp_enc, -implant_cmp_enc , -poly_res_enc-ppoly_pcmp_spc+implant_cmp_enc, ppolyf_u_high_Rs_res_l+implant_cmp_enc))

        # Inserting dnwell
        ppolyf_u_high_Rs_res_cell.shapes(dnwell).insert(pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp, -dnwell_enc_poly , ppolyf_u_high_Rs_res_w+poly_res_enc+dnwell_enc_poly, ppolyf_u_high_Rs_res_l+dnwell_enc_poly))

        # for 5/6V
        # Inserting dualgate
        if volt == "5/6V":
            ppolyf_u_high_Rs_res_cell.shapes(dualgate).insert(pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-dg_enc_dnwell, -dnwell_enc_poly-dg_enc_dnwell , ppolyf_u_high_Rs_res_w+poly_res_enc+dnwell_enc_poly+dg_enc_dnwell, ppolyf_u_high_Rs_res_l+dnwell_enc_poly+dg_enc_dnwell))


        # Inserting Guard Ring
        if pcmpgr == True:
            cmp_inner = pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw, -dnwell_enc_poly-pcmp_gr2dnw , ppolyf_u_high_Rs_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw, ppolyf_u_high_Rs_res_l+dnwell_enc_poly+pcmp_gr2dnw)
            cmp_outer = pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw-gr_w, -dnwell_enc_poly-pcmp_gr2dnw-gr_w , ppolyf_u_high_Rs_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw+gr_w, ppolyf_u_high_Rs_res_l+dnwell_enc_poly+pcmp_gr2dnw+gr_w)
            cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
            ppolyf_u_high_Rs_res_cell.shapes(comp).insert(cmp_gr)

            pp_inner = pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw+implant_cmp_enc, -dnwell_enc_poly-pcmp_gr2dnw+implant_cmp_enc , ppolyf_u_high_Rs_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw-implant_cmp_enc, ppolyf_u_high_Rs_res_l+dnwell_enc_poly+pcmp_gr2dnw-implant_cmp_enc)
            pp_outer = pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-dnwell_enc_ncmp-pcmp_gr2dnw-gr_w-implant_cmp_enc, -dnwell_enc_poly-pcmp_gr2dnw-gr_w-implant_cmp_enc , ppolyf_u_high_Rs_res_w+poly_res_enc+dnwell_enc_poly+pcmp_gr2dnw+gr_w+implant_cmp_enc, ppolyf_u_high_Rs_res_l+dnwell_enc_poly+pcmp_gr2dnw+gr_w+implant_cmp_enc)
            pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
            ppolyf_u_high_Rs_res_cell.shapes(pplus).insert(pp_gr)

    else:
        ppolyf_u_high_Rs_res_cell.shapes(pplus).insert(pya.Box(-poly_res_enc-ppoly_pcmp_spc-pcmp_width-implant_cmp_enc, -implant_cmp_enc , -poly_res_enc-ppoly_pcmp_spc+implant_cmp_enc, ppolyf_u_high_Rs_res_l+implant_cmp_enc))

        # for 5/6V
        # Inserting dualgate
        if volt == "5/6V":
            ppolyf_u_high_Rs_res_cell.shapes(dualgate).insert(pya.Box(-poly_res_enc-resistor_poly_enc, -resistor_poly_enc , ppolyf_u_high_Rs_res_w+poly_res_enc+resistor_poly_enc, ppolyf_u_high_Rs_res_l+resistor_poly_enc))


    ppolyf_u_high_Rs_res_cell.flatten(True)
    return ppolyf_u_high_Rs_res_cell
