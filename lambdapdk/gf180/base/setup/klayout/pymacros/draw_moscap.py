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
## MOS capacitor Pcells Generators for Klayout of GF180MCU
########################################################################################################################

import pya

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

def draw_nmoscap(layout, l, w ,volt, deepnwell, pcmpgr):
    '''
    Usage:-
     used to draw NMOS capacitor (Outside DNWELL) by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of diff length
     w      : Float of diff width
    '''

    # Define layers
    dnwell         = layout.layer(12 , 0 )
    lvpwell        = layout.layer(204, 0 )
    comp           = layout.layer(22 , 0 )
    poly           = layout.layer(30 , 0 )
    nplus          = layout.layer(32 , 0 )
    pplus          = layout.layer(31 , 0 )
    contact        = layout.layer(33 , 0 )
    lvpwell        = layout.layer(204 , 0)
    metal1         = layout.layer(34 , 0 )
    mos_cap_mk     = layout.layer(166, 5 )
    dualgate       = layout.layer(55 , 0 )

    # VARIABLES
    dbu_PERCISION         = 1/layout.dbu
    cmp_w                 = w    * dbu_PERCISION
    cmp_l                 = l    * dbu_PERCISION
    poly_ext              = 0.46 * dbu_PERCISION
    implant_cmp_enc       = 0.16 * dbu_PERCISION
    cmp_poly_enc          = 0.44 * dbu_PERCISION
    cont_size             = 0.22 * dbu_PERCISION
    cont_min_spc          = 0.25 * dbu_PERCISION
    comp_cont_enc         = 0.07 * dbu_PERCISION
    met_cont_enc          = 0.06 * dbu_PERCISION
    metal_cmp_ext_x       = 0.65 * dbu_PERCISION
    metal_cmp_ext_y       = 0.76 * dbu_PERCISION
    met_width             = 1    * dbu_PERCISION
    poly_met_enc_x        = 0.21 * dbu_PERCISION
    poly_met_enc_y        = 0.01 * dbu_PERCISION
    met_con_min           = 0.34 * dbu_PERCISION
    cmp_met_cont_enc_diff = 0.01 * dbu_PERCISION
    cmp_cont_poly_spc     = 0.17 * dbu_PERCISION
    dual_gate_cmp_enc_x   = 0.96 * dbu_PERCISION
    dual_gate_cmp_enc_y   = 1.36 * dbu_PERCISION
    pcmp2ncmp_spc         = 0.36 * dbu_PERCISION
    ply2gr_spc            = 0.3  * dbu_PERCISION
    gr_w                  = 0.36 * dbu_PERCISION
    lvpwell_enc_pcmp      = 0.12 * dbu_PERCISION
    dnwell_enc_lvpwell    = 2.5  * dbu_PERCISION
    dg_enc_dnwell         = 0.5  * dbu_PERCISION
    pcmp_gr2dnw           = 2.5  * dbu_PERCISION

    if volt == "5/6V":
        lvpwell_enc_pcmp      = 0.16 * dbu_PERCISION

    # Inserting nmoscap cell
    cell_index  = layout.add_cell("nmoscap")
    nmoscap_cell = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting diffusion
    nmoscap_cell.shapes(comp).insert(pya.Box(0, 0, cmp_w, cmp_l))
    nmoscap_cell.shapes(nplus).insert(pya.Box(-implant_cmp_enc, -poly_ext, cmp_w+implant_cmp_enc, cmp_l+poly_ext))

    # Inserting poly
    nmoscap_cell.shapes(poly).insert(pya.Box(cmp_poly_enc, -poly_ext, cmp_w-cmp_poly_enc, cmp_l+poly_ext))

    # Inserting left metal
    nmoscap_cell.shapes(metal1).insert(pya.Box(-metal_cmp_ext_x, -metal_cmp_ext_y, -metal_cmp_ext_x+met_width, cmp_l))

    # Inserting right metal
    nmoscap_cell.shapes(metal1).insert(pya.Box(cmp_w+metal_cmp_ext_x-met_width, -metal_cmp_ext_y, cmp_w+metal_cmp_ext_x, cmp_l))

    # Inserting poly metal
    nmoscap_cell.shapes(metal1).insert(pya.Box(cmp_poly_enc+poly_met_enc_x, -poly_ext+poly_met_enc_y, cmp_w-cmp_poly_enc-poly_met_enc_x , cmp_l+poly_ext-poly_met_enc_y))

    # Inserting left contacts
    num_left_con_1, left_con_free_spc_1 = number_spc_contacts(met_con_min, met_cont_enc, cont_min_spc, cont_size)
    num_left_con_2, left_con_free_spc_2 = number_spc_contacts(cmp_l, comp_cont_enc, cont_min_spc, cont_size)
    left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(cmp_met_cont_enc_diff+left_con_free_spc_1 / 2, left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_left_con_1, num_left_con_2)
    nmoscap_cell.insert(left_con_arr)

    # Inserting right contacts
    num_right_con_1, right_con_free_spc_1 = number_spc_contacts(met_con_min, met_cont_enc, cont_min_spc, cont_size)
    num_right_con_2, right_con_free_spc_2 = number_spc_contacts(cmp_l, comp_cont_enc, cont_min_spc, cont_size)
    right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(cmp_w-cmp_met_cont_enc_diff-met_con_min+right_con_free_spc_1 / 2, right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_right_con_1, num_right_con_2)
    nmoscap_cell.insert(right_con_arr)

    # Inserting top contacts
    num_top_con_1, top_con_free_spc_1 = number_spc_contacts(cmp_w-2*cmp_poly_enc-2*poly_met_enc_x, comp_cont_enc, cont_min_spc, cont_size)
    num_top_con_2, top_con_free_spc_2 = number_spc_contacts(poly_ext-poly_met_enc_y, comp_cont_enc, cont_min_spc, cont_size)
    top_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(cmp_poly_enc+poly_met_enc_x+top_con_free_spc_1 / 2, cmp_l+top_con_free_spc_2/2+(cmp_cont_poly_spc-top_con_free_spc_2/2))),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_top_con_1, num_top_con_2)
    nmoscap_cell.insert(top_con_arr)

    # Inserting bottom contacts
    num_bot_con_1, bot_con_free_spc_1 = number_spc_contacts(cmp_w-2*cmp_poly_enc-2*poly_met_enc_x, comp_cont_enc, cont_min_spc, cont_size)
    num_bot_con_2, bot_con_free_spc_2 = number_spc_contacts(poly_ext-poly_met_enc_y, comp_cont_enc, cont_min_spc, cont_size)
    bot_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(cmp_poly_enc+poly_met_enc_x+bot_con_free_spc_1 / 2, -poly_ext+poly_met_enc_y+bot_con_free_spc_2/2-(cmp_cont_poly_spc-bot_con_free_spc_2/2))),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_bot_con_1, num_bot_con_2)
    nmoscap_cell.insert(bot_con_arr)

    # Inserting marker
    nmoscap_cell.shapes(mos_cap_mk).insert(pya.Box(0, 0, cmp_w, cmp_l))

    # Inserting marker
    if deepnwell == True:
        # Inserting PCOMP Guard Ring
        cmp_inner = pya.Box(-pcmp2ncmp_spc, -ply2gr_spc-poly_ext, cmp_w+pcmp2ncmp_spc, cmp_l+poly_ext+ply2gr_spc)
        cmp_outer = pya.Box(-pcmp2ncmp_spc-gr_w, -ply2gr_spc-poly_ext-gr_w, cmp_w+pcmp2ncmp_spc+gr_w, cmp_l+poly_ext+gr_w+ply2gr_spc)
        cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
        nmoscap_cell.shapes(comp).insert(cmp_gr)
        nmoscap_cell.shapes(metal1).insert(cmp_gr)

        pp_inner = pya.Box(-pcmp2ncmp_spc+implant_cmp_enc, -ply2gr_spc-poly_ext+implant_cmp_enc, cmp_w+pcmp2ncmp_spc-implant_cmp_enc, cmp_l+poly_ext+ply2gr_spc-implant_cmp_enc)
        pp_outer = pya.Box(-pcmp2ncmp_spc-gr_w-implant_cmp_enc, -ply2gr_spc-poly_ext-gr_w-implant_cmp_enc, cmp_w+pcmp2ncmp_spc+gr_w+implant_cmp_enc, cmp_l+poly_ext+gr_w+ply2gr_spc+implant_cmp_enc)
        pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
        nmoscap_cell.shapes(pplus).insert(pp_gr)

        # Inserting PCOMP Guard Ring contacts
        num_y_con, y_con_free_spc = number_spc_contacts(2*(gr_w+ply2gr_spc+poly_ext)+cmp_l, comp_cont_enc, cont_min_spc, cont_size)
        num_x_con, x_con_free_spc = number_spc_contacts(cmp_w+2*(comp_cont_enc+pcmp2ncmp_spc-cont_min_spc), comp_cont_enc, cont_min_spc, cont_size)

        left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-pcmp2ncmp_spc-comp_cont_enc-cont_size, -ply2gr_spc-poly_ext-gr_w+y_con_free_spc/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        1, num_y_con)
        nmoscap_cell.insert(left_con_arr)

        bot_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-pcmp2ncmp_spc+cont_min_spc-comp_cont_enc+x_con_free_spc/2, -ply2gr_spc-poly_ext-comp_cont_enc-cont_size)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_x_con, 1)
        nmoscap_cell.insert(bot_con_arr)

        right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(cmp_w+pcmp2ncmp_spc+comp_cont_enc, -ply2gr_spc-poly_ext-gr_w+y_con_free_spc/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        1, num_y_con)
        nmoscap_cell.insert(right_con_arr)

        top_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-pcmp2ncmp_spc+cont_min_spc-comp_cont_enc+x_con_free_spc/2, cmp_l+ply2gr_spc+poly_ext+comp_cont_enc)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_x_con, 1)
        nmoscap_cell.insert(top_con_arr)

        # Inserting Double Guard Ring
        if pcmpgr == True:
            cmp_inner = pya.Box(-pcmp2ncmp_spc-gr_w-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw, -ply2gr_spc-poly_ext-gr_w-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw, cmp_w+pcmp2ncmp_spc+gr_w+lvpwell_enc_pcmp+dnwell_enc_lvpwell+pcmp_gr2dnw, cmp_l+poly_ext+gr_w+lvpwell_enc_pcmp+dnwell_enc_lvpwell+ply2gr_spc+pcmp_gr2dnw)
            cmp_outer = pya.Box(-pcmp2ncmp_spc-2*gr_w-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw, -ply2gr_spc-poly_ext-2*gr_w-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw, cmp_w+pcmp2ncmp_spc+2*gr_w+lvpwell_enc_pcmp+dnwell_enc_lvpwell+pcmp_gr2dnw, cmp_l+poly_ext+2*gr_w+lvpwell_enc_pcmp+dnwell_enc_lvpwell+ply2gr_spc+pcmp_gr2dnw)
            cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
            nmoscap_cell.shapes(comp).insert(cmp_gr)

            pp_inner = pya.Box(-pcmp2ncmp_spc-gr_w-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw+implant_cmp_enc, -ply2gr_spc-poly_ext-gr_w-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw+implant_cmp_enc, cmp_w+pcmp2ncmp_spc+gr_w+lvpwell_enc_pcmp+dnwell_enc_lvpwell+pcmp_gr2dnw-implant_cmp_enc, cmp_l+poly_ext+gr_w+lvpwell_enc_pcmp+dnwell_enc_lvpwell+ply2gr_spc+pcmp_gr2dnw-implant_cmp_enc)
            pp_outer = pya.Box(-pcmp2ncmp_spc-2*gr_w-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw-implant_cmp_enc, -ply2gr_spc-poly_ext-2*gr_w-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw-implant_cmp_enc, cmp_w+pcmp2ncmp_spc+2*gr_w+lvpwell_enc_pcmp+dnwell_enc_lvpwell+pcmp_gr2dnw+implant_cmp_enc, cmp_l+poly_ext+2*gr_w+lvpwell_enc_pcmp+dnwell_enc_lvpwell+ply2gr_spc+pcmp_gr2dnw+implant_cmp_enc)
            pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
            nmoscap_cell.shapes(pplus).insert(pp_gr)

        # Inserting lvpwell
        nmoscap_cell.shapes(lvpwell).insert(pya.Box(-pcmp2ncmp_spc-gr_w-lvpwell_enc_pcmp, -ply2gr_spc-poly_ext-gr_w-lvpwell_enc_pcmp, cmp_w+pcmp2ncmp_spc+gr_w+lvpwell_enc_pcmp, cmp_l+poly_ext+gr_w+lvpwell_enc_pcmp+ply2gr_spc))

        nmoscap_cell.shapes(dnwell).insert(pya.Box(-pcmp2ncmp_spc-gr_w-lvpwell_enc_pcmp-dnwell_enc_lvpwell, -ply2gr_spc-poly_ext-gr_w-lvpwell_enc_pcmp-dnwell_enc_lvpwell, cmp_w+pcmp2ncmp_spc+gr_w+lvpwell_enc_pcmp+dnwell_enc_lvpwell, cmp_l+poly_ext+gr_w+lvpwell_enc_pcmp+dnwell_enc_lvpwell+ply2gr_spc))

    else:
        # Inserting lvpwell
        nmoscap_cell.shapes(lvpwell).insert(pya.Box(0, 0, cmp_w, cmp_l))

        # Inserting bottom metal
        nmoscap_cell.shapes(metal1).insert(pya.Box(-metal_cmp_ext_x, -metal_cmp_ext_y-met_width, cmp_w+metal_cmp_ext_x, -metal_cmp_ext_y))


    if volt == "5/6V":
        # Inserting dualgate
        if deepnwell == True:
            nmoscap_cell.shapes(dualgate).insert(pya.Box(-pcmp2ncmp_spc-gr_w-lvpwell_enc_pcmp-dnwell_enc_lvpwell-dg_enc_dnwell, -ply2gr_spc-poly_ext-gr_w-lvpwell_enc_pcmp-dnwell_enc_lvpwell-dg_enc_dnwell, cmp_w+pcmp2ncmp_spc+gr_w+lvpwell_enc_pcmp+dnwell_enc_lvpwell+dg_enc_dnwell, cmp_l+poly_ext+pcmp2ncmp_spc+gr_w+lvpwell_enc_pcmp+dnwell_enc_lvpwell+dg_enc_dnwell))
        else:
            nmoscap_cell.shapes(dualgate).insert(pya.Box(-dual_gate_cmp_enc_x, -dual_gate_cmp_enc_y, cmp_w+dual_gate_cmp_enc_x, cmp_l+dual_gate_cmp_enc_y))


    nmoscap_cell.flatten(True)
    return nmoscap_cell

def draw_pmoscap(layout, l, w , volt, deepnwell, pcmpgr):
    '''
    Usage:-
     used to draw PMOS capacitor (Outside DNWELL) by specifying parameters
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
    nwell          = layout.layer(21 , 0 )
    metal1         = layout.layer(34 , 0 )
    mos_cap_mk     = layout.layer(166, 5 )
    dualgate       = layout.layer(55 , 0 )

    # VARIABLES
    dbu_PERCISION         = 1/layout.dbu
    cmp_w                 = w    * dbu_PERCISION
    cmp_l                 = l    * dbu_PERCISION
    poly_ext              = 0.46 * dbu_PERCISION
    implant_cmp_enc       = 0.16 * dbu_PERCISION
    cmp_poly_enc          = 0.44 * dbu_PERCISION
    cont_size             = 0.22 * dbu_PERCISION
    cont_min_spc          = 0.25 * dbu_PERCISION
    comp_cont_enc         = 0.07 * dbu_PERCISION
    met_cont_enc          = 0.06 * dbu_PERCISION
    metal_cmp_ext_x       = 0.65 * dbu_PERCISION
    met_width             = 1    * dbu_PERCISION
    poly_met_enc_x        = 0.19 * dbu_PERCISION
    poly_met_enc_y        = 0.01 * dbu_PERCISION
    met_con_min           = 0.34 * dbu_PERCISION
    cmp_met_cont_enc_diff = 0.01 * dbu_PERCISION
    gr_width              = 0.36 * dbu_PERCISION
    ncmp_pcmp_spc         = 0.36 * dbu_PERCISION
    poly_ncmp_spc         = 0.3  * dbu_PERCISION
    nwell_cmp_enc         = 0.16 * dbu_PERCISION
    cmp_met_spc           = 0.11 * dbu_PERCISION
    cont_spc_gr           = 0.11 * dbu_PERCISION
    dual_gate_cmp_enc_x   = 0.96 * dbu_PERCISION
    dual_gate_cmp_enc_y   = 1.36 * dbu_PERCISION
    dnwell_enc_ncmp       = 0.62 * dbu_PERCISION
    dg_enc_dnwell         = 0.5  * dbu_PERCISION
    pcmp_gr2dnw           = 2.5  * dbu_PERCISION

    if volt == "5/6V":
        dnwell_enc_ncmp       = 0.66 * dbu_PERCISION

    # Inserting pmoscap cell
    cell_index  = layout.add_cell("pmoscap")
    pmoscap_cell = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting diffusion
    pmoscap_cell.shapes(comp).insert(pya.Box(0, 0, cmp_w, cmp_l))
    pmoscap_cell.shapes(pplus).insert(pya.Box(-implant_cmp_enc, -poly_ext, cmp_w+implant_cmp_enc, cmp_l+poly_ext))

    # Inserting poly
    pmoscap_cell.shapes(poly).insert(pya.Box(cmp_poly_enc, -poly_ext, cmp_w-cmp_poly_enc, cmp_l+poly_ext))

    # Inserting left cmp metal
    pmoscap_cell.shapes(metal1).insert(pya.Box(-ncmp_pcmp_spc-gr_width, 0 , -metal_cmp_ext_x+met_width, cmp_l))

    # Inserting right cmp metal
    pmoscap_cell.shapes(metal1).insert(pya.Box(cmp_w+metal_cmp_ext_x-met_width, 0, cmp_w+ncmp_pcmp_spc+gr_width, cmp_l))

    # Inserting top cmp metal
    pmoscap_cell.shapes(metal1).insert(pya.Box(cmp_poly_enc+poly_met_enc_x, cmp_l+cmp_met_spc , cmp_w-cmp_poly_enc-poly_met_enc_x , cmp_l+poly_ext-poly_met_enc_y))

    # Inserting bottom cmp metal
    pmoscap_cell.shapes(metal1).insert(pya.Box(cmp_poly_enc+poly_met_enc_x, -poly_ext+poly_met_enc_y, cmp_w-cmp_poly_enc-poly_met_enc_x , -cmp_met_spc))

    # Inserting left cmp contacts
    num_left_con_1, left_con_free_spc_1 = number_spc_contacts(met_con_min, met_cont_enc, cont_min_spc, cont_size)
    num_left_con_2, left_con_free_spc_2 = number_spc_contacts(cmp_l, comp_cont_enc, cont_min_spc, cont_size)
    left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(cmp_met_cont_enc_diff+left_con_free_spc_1 / 2, left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_left_con_1, num_left_con_2)
    pmoscap_cell.insert(left_con_arr)

    # Inserting right cmp contacts
    num_right_con_1, right_con_free_spc_1 = number_spc_contacts(met_con_min, met_cont_enc, cont_min_spc, cont_size)
    num_right_con_2, right_con_free_spc_2 = number_spc_contacts(cmp_l, comp_cont_enc, cont_min_spc, cont_size)
    right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(cmp_w-cmp_met_cont_enc_diff-met_con_min+right_con_free_spc_1 / 2, right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_right_con_1, num_right_con_2)
    pmoscap_cell.insert(right_con_arr)

    # Inserting top cmp contacts
    num_top_con_1, top_con_free_spc_1 = number_spc_contacts(cmp_w-2*cmp_poly_enc-2*poly_met_enc_x, met_cont_enc, cont_min_spc, cont_size)
    num_top_con_2, top_con_free_spc_2 = number_spc_contacts(met_con_min, met_cont_enc, cont_min_spc, cont_size)
    top_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(cmp_poly_enc+poly_met_enc_x+top_con_free_spc_1 / 2, cmp_l+cmp_met_spc+top_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_top_con_1, num_top_con_2)
    pmoscap_cell.insert(top_con_arr)

    # Inserting bottom cmp contacts
    num_bot_con_1, bot_con_free_spc_1 = number_spc_contacts(cmp_w-2*cmp_poly_enc-2*poly_met_enc_x, met_cont_enc, cont_min_spc, cont_size)
    num_bot_con_2, bot_con_free_spc_2 = number_spc_contacts(met_con_min, met_cont_enc, cont_min_spc, cont_size)
    bot_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(cmp_poly_enc+poly_met_enc_x+bot_con_free_spc_1 / 2, -poly_ext+poly_met_enc_y+bot_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_bot_con_1, num_bot_con_2)
    pmoscap_cell.insert(bot_con_arr)

    # Inserting left GR diff
    pmoscap_cell.shapes(comp).insert(pya.Box(-ncmp_pcmp_spc-gr_width, -poly_ext-poly_ncmp_spc , -ncmp_pcmp_spc , cmp_l+poly_ext+poly_ncmp_spc))
    pmoscap_cell.shapes(nplus).insert(pya.Box(-ncmp_pcmp_spc-gr_width-implant_cmp_enc, -poly_ext-poly_ncmp_spc+implant_cmp_enc , -ncmp_pcmp_spc+implant_cmp_enc , cmp_l+poly_ext+poly_ncmp_spc-implant_cmp_enc))
    # Inserting right GR diff
    pmoscap_cell.shapes(comp).insert(pya.Box(cmp_w+ncmp_pcmp_spc, -poly_ext-poly_ncmp_spc , cmp_w+ncmp_pcmp_spc+gr_width , cmp_l+poly_ext+poly_ncmp_spc))
    pmoscap_cell.shapes(nplus).insert(pya.Box(cmp_w+ncmp_pcmp_spc-implant_cmp_enc, -poly_ext-poly_ncmp_spc+implant_cmp_enc , cmp_w+ncmp_pcmp_spc+gr_width+implant_cmp_enc , cmp_l+poly_ext+poly_ncmp_spc-implant_cmp_enc))
    # Inserting top GR diff
    pmoscap_cell.shapes(comp).insert(pya.Box(-ncmp_pcmp_spc-gr_width, cmp_l+poly_ext+poly_ncmp_spc , cmp_w+ncmp_pcmp_spc+gr_width , cmp_l+poly_ext+poly_ncmp_spc+gr_width))
    pmoscap_cell.shapes(nplus).insert(pya.Box(-ncmp_pcmp_spc-gr_width-implant_cmp_enc, cmp_l+poly_ext+poly_ncmp_spc-implant_cmp_enc , cmp_w+ncmp_pcmp_spc+gr_width+implant_cmp_enc , cmp_l+poly_ext+poly_ncmp_spc+gr_width+implant_cmp_enc))
    # Inserting bottom GR diff
    pmoscap_cell.shapes(comp).insert(pya.Box(-ncmp_pcmp_spc-gr_width, -poly_ext-poly_ncmp_spc-gr_width , cmp_w+ncmp_pcmp_spc+gr_width , -poly_ext-poly_ncmp_spc))
    pmoscap_cell.shapes(nplus).insert(pya.Box(-ncmp_pcmp_spc-gr_width-implant_cmp_enc, -poly_ext-poly_ncmp_spc-gr_width-implant_cmp_enc , cmp_w+ncmp_pcmp_spc+gr_width+implant_cmp_enc , -poly_ext-poly_ncmp_spc+implant_cmp_enc))

    # Inserting left GR metal
    pmoscap_cell.shapes(metal1).insert(pya.Box(-ncmp_pcmp_spc-gr_width, -poly_ext-poly_ncmp_spc , -ncmp_pcmp_spc , cmp_l+poly_ext+poly_ncmp_spc))
    # Inserting right GR metal
    pmoscap_cell.shapes(metal1).insert(pya.Box(cmp_w+ncmp_pcmp_spc, -poly_ext-poly_ncmp_spc , cmp_w+ncmp_pcmp_spc+gr_width , cmp_l+poly_ext+poly_ncmp_spc))
    # Inserting top GR metal
    pmoscap_cell.shapes(metal1).insert(pya.Box(-ncmp_pcmp_spc-gr_width, cmp_l+poly_ext+poly_ncmp_spc , cmp_w+ncmp_pcmp_spc+gr_width , cmp_l+poly_ext+poly_ncmp_spc+gr_width))
    # Inserting bottom GR metal
    pmoscap_cell.shapes(metal1).insert(pya.Box(-ncmp_pcmp_spc-gr_width, -poly_ext-poly_ncmp_spc-gr_width , cmp_w+ncmp_pcmp_spc+gr_width , -poly_ext-poly_ncmp_spc))

    # Inserting left GR cont
    num_gr_left_con_1, gr_left_con_free_spc_1 = number_spc_contacts(gr_width, comp_cont_enc, cont_min_spc, cont_size)
    num_gr_left_con_2, gr_left_con_free_spc_2 = number_spc_contacts(cmp_l+2*poly_ext+2*poly_ncmp_spc-2*cont_spc_gr, comp_cont_enc, cont_min_spc, cont_size)
    gr_left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-ncmp_pcmp_spc-gr_width+gr_left_con_free_spc_1 / 2, cont_spc_gr-poly_ext-poly_ncmp_spc+gr_left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_gr_left_con_1, num_gr_left_con_2)
    pmoscap_cell.insert(gr_left_con_arr)

    # Inserting right GR cont
    num_gr_right_con_1, gr_right_con_free_spc_1 = number_spc_contacts(gr_width, comp_cont_enc, cont_min_spc, cont_size)
    num_gr_right_con_2, gr_right_con_free_spc_2 = number_spc_contacts(cmp_l+2*poly_ext+2*poly_ncmp_spc-2*cont_spc_gr, comp_cont_enc, cont_min_spc, cont_size)
    gr_right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(cmp_w+ncmp_pcmp_spc+gr_right_con_free_spc_1 / 2, cont_spc_gr-poly_ext-poly_ncmp_spc+gr_right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_gr_right_con_1, num_gr_right_con_2)
    pmoscap_cell.insert(gr_right_con_arr)

    # Inserting top GR cont
    num_gr_top_con_1, gr_top_con_free_spc_1 = number_spc_contacts(cmp_w+2*ncmp_pcmp_spc+2*gr_width, comp_cont_enc, cont_min_spc, cont_size)
    num_gr_top_con_2, gr_top_con_free_spc_2 = number_spc_contacts(gr_width, comp_cont_enc, cont_min_spc, cont_size)
    gr_top_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-ncmp_pcmp_spc-gr_width+comp_cont_enc, cmp_l+poly_ext+poly_ncmp_spc +gr_top_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_gr_top_con_1, num_gr_top_con_2)
    pmoscap_cell.insert(gr_top_con_arr)

    # Inserting bottom GR cont
    num_gr_top_con_1, gr_top_con_free_spc_1 = number_spc_contacts(cmp_w+2*ncmp_pcmp_spc+2*gr_width, comp_cont_enc, cont_min_spc, cont_size)
    num_gr_top_con_2, gr_top_con_free_spc_2 = number_spc_contacts(gr_width, comp_cont_enc, cont_min_spc, cont_size)
    gr_top_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-ncmp_pcmp_spc-gr_width+comp_cont_enc, -poly_ext-poly_ncmp_spc-gr_width +gr_top_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_gr_top_con_1, num_gr_top_con_2)
    pmoscap_cell.insert(gr_top_con_arr)

    # Inserting marker
    pmoscap_cell.shapes(mos_cap_mk).insert(pya.Box(0, 0, cmp_w, cmp_l))

    # Inserting marker
    if deepnwell == True:
        # Inserting dnwell
        pmoscap_cell.shapes(dnwell).insert(pya.Box(-ncmp_pcmp_spc-gr_width-dnwell_enc_ncmp, -poly_ext-poly_ncmp_spc-gr_width-dnwell_enc_ncmp, cmp_w+ncmp_pcmp_spc+gr_width+dnwell_enc_ncmp , cmp_l+poly_ext+poly_ncmp_spc+gr_width+dnwell_enc_ncmp))

        # Inserting Double Guard Ring
        if pcmpgr == True:
            cmp_inner = pya.Box(-ncmp_pcmp_spc-gr_width-dnwell_enc_ncmp-pcmp_gr2dnw, -poly_ext-poly_ncmp_spc-gr_width-dnwell_enc_ncmp-pcmp_gr2dnw, cmp_w+ncmp_pcmp_spc+gr_width+dnwell_enc_ncmp+pcmp_gr2dnw , cmp_l+poly_ext+poly_ncmp_spc+gr_width+dnwell_enc_ncmp+pcmp_gr2dnw)
            cmp_outer = pya.Box(-ncmp_pcmp_spc-2*gr_width-dnwell_enc_ncmp-pcmp_gr2dnw, -poly_ext-poly_ncmp_spc-2*gr_width-dnwell_enc_ncmp-pcmp_gr2dnw, cmp_w+ncmp_pcmp_spc+2*gr_width+dnwell_enc_ncmp+pcmp_gr2dnw , cmp_l+poly_ext+poly_ncmp_spc+2*gr_width+dnwell_enc_ncmp+pcmp_gr2dnw)
            cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
            pmoscap_cell.shapes(comp).insert(cmp_gr)

            pp_inner = pya.Box(-ncmp_pcmp_spc-gr_width-dnwell_enc_ncmp-pcmp_gr2dnw+implant_cmp_enc, -poly_ext-poly_ncmp_spc-gr_width-dnwell_enc_ncmp-pcmp_gr2dnw+implant_cmp_enc, cmp_w+ncmp_pcmp_spc+gr_width+dnwell_enc_ncmp+pcmp_gr2dnw-implant_cmp_enc , cmp_l+poly_ext+poly_ncmp_spc+gr_width+dnwell_enc_ncmp+pcmp_gr2dnw-implant_cmp_enc)
            pp_outer = pya.Box(-ncmp_pcmp_spc-2*gr_width-dnwell_enc_ncmp-pcmp_gr2dnw-implant_cmp_enc, -poly_ext-poly_ncmp_spc-2*gr_width-dnwell_enc_ncmp-pcmp_gr2dnw-implant_cmp_enc, cmp_w+ncmp_pcmp_spc+2*gr_width+dnwell_enc_ncmp+pcmp_gr2dnw+implant_cmp_enc , cmp_l+poly_ext+poly_ncmp_spc+2*gr_width+dnwell_enc_ncmp+pcmp_gr2dnw+implant_cmp_enc)
            pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
            pmoscap_cell.shapes(pplus).insert(pp_gr)

    else:
        # Inserting nwell
        pmoscap_cell.shapes(nwell).insert(pya.Box(-ncmp_pcmp_spc-gr_width-nwell_cmp_enc, -poly_ext-poly_ncmp_spc-gr_width-nwell_cmp_enc, cmp_w+ncmp_pcmp_spc+gr_width+nwell_cmp_enc , cmp_l+poly_ext+poly_ncmp_spc+gr_width+nwell_cmp_enc))

    if volt == "5/6V":
        # Inserting dualgate
        if deepnwell == True:
            pmoscap_cell.shapes(dualgate).insert(pya.Box(-ncmp_pcmp_spc-gr_width-dnwell_enc_ncmp-dg_enc_dnwell, -poly_ext-poly_ncmp_spc-gr_width-dnwell_enc_ncmp-dg_enc_dnwell, cmp_w+ncmp_pcmp_spc+gr_width+dnwell_enc_ncmp+dg_enc_dnwell, cmp_l+poly_ext+poly_ncmp_spc+gr_width+dnwell_enc_ncmp+dg_enc_dnwell))
        else:
            pmoscap_cell.shapes(dualgate).insert(pya.Box(-dual_gate_cmp_enc_x, -dual_gate_cmp_enc_y, cmp_w+dual_gate_cmp_enc_x, cmp_l+dual_gate_cmp_enc_y))

    pmoscap_cell.flatten(True)
    return pmoscap_cell

def draw_nmoscap_b(layout, l, w , volt):
    '''
    Usage:-
     used to draw 3.3V NMOS capacitor (inside NWell) by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of diff length
     w      : Float of diff width
    '''

    # Define layers
    comp           = layout.layer(22 , 0 )
    poly           = layout.layer(30 , 0 )
    nplus          = layout.layer(32 , 0 )
    contact        = layout.layer(33 , 0 )
    nwell          = layout.layer(21 , 0 )
    metal1         = layout.layer(34 , 0 )
    mos_cap_mk     = layout.layer(166, 5 )
    dualgate       = layout.layer(55 , 0 )

    # VARIABLES
    dbu_PERCISION         = 1/layout.dbu
    cmp_w                 = w    * dbu_PERCISION
    cmp_l                 = l    * dbu_PERCISION
    poly_ext              = 0.3  * dbu_PERCISION
    implant_cmp_enc       = 0.16 * dbu_PERCISION
    cmp_poly_enc          = 0.44 * dbu_PERCISION
    cont_size             = 0.22 * dbu_PERCISION
    cont_min_spc          = 0.25 * dbu_PERCISION
    comp_cont_enc         = 0.07 * dbu_PERCISION
    met_cont_enc          = 0.06 * dbu_PERCISION
    metal_cmp_ext_x       = 0.59 * dbu_PERCISION
    metal_cmp_ext_y       = 2.2  * dbu_PERCISION
    met_width             = 1    * dbu_PERCISION
    poly_met_enc_x        = 0.17 * dbu_PERCISION
    poly_met_enc_y        = 0.01 * dbu_PERCISION
    met_con_min           = 0.34 * dbu_PERCISION
    cmp_met_cont_enc_diff = 0.01 * dbu_PERCISION
    cmp_cont_poly_spc     = 0.17 * dbu_PERCISION
    nwell_cmp_enc_x       = 0.18 * dbu_PERCISION
    nwell_cmp_enc_y       = 1.38 * dbu_PERCISION
    poly_extra_in         = 0.27 * dbu_PERCISION
    poly_extra_out        = 0.9  * dbu_PERCISION
    dualgate_cmp_enc_x    = 0.24 * dbu_PERCISION
    dualgate_cmp_enc_y    = 1.6  * dbu_PERCISION

    # Inserting nmoscap cell
    cell_index  = layout.add_cell("nmoscap_b")
    nmoscap_b_cell = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting diffusion
    nmoscap_b_cell.shapes(comp).insert(pya.Box(0, 0, cmp_w, cmp_l))
    nmoscap_b_cell.shapes(nplus).insert(pya.Box(-nwell_cmp_enc_x, -nwell_cmp_enc_y, cmp_w+nwell_cmp_enc_x, cmp_l+nwell_cmp_enc_y))

    # Inserting nwell
    nmoscap_b_cell.shapes(nwell).insert(pya.Box(-nwell_cmp_enc_x, -nwell_cmp_enc_y, cmp_w+nwell_cmp_enc_x, cmp_l+nwell_cmp_enc_y))

    # Inserting poly
    nmoscap_b_cell.shapes(poly).insert(pya.Box(cmp_poly_enc, -poly_ext, cmp_w-cmp_poly_enc, cmp_l+poly_ext))

    # Inserting extra poly
    nmoscap_b_cell.shapes(poly).insert(pya.Box(cmp_poly_enc+poly_extra_in, cmp_l+poly_ext, cmp_w-cmp_poly_enc-poly_extra_in, cmp_l+poly_ext+poly_extra_out))  #top
    nmoscap_b_cell.shapes(poly).insert(pya.Box(cmp_poly_enc+poly_extra_in, -poly_ext-poly_extra_out, cmp_w-cmp_poly_enc-poly_extra_in, -poly_ext))            #bot

    # Inserting left metal
    nmoscap_b_cell.shapes(metal1).insert(pya.Box(-metal_cmp_ext_x, -metal_cmp_ext_y, -metal_cmp_ext_x+met_width, cmp_l))

    # Inserting right metal
    nmoscap_b_cell.shapes(metal1).insert(pya.Box(cmp_w+metal_cmp_ext_x-met_width, -metal_cmp_ext_y-met_width, cmp_w+metal_cmp_ext_x, cmp_l))

    # Inserting bottom metal
    nmoscap_b_cell.shapes(metal1).insert(pya.Box(-metal_cmp_ext_x, -metal_cmp_ext_y-met_width, cmp_w+metal_cmp_ext_x, -metal_cmp_ext_y))

    # Inserting poly metal
    nmoscap_b_cell.shapes(metal1).insert(pya.Box(cmp_poly_enc+poly_extra_in, -poly_ext-poly_extra_out, cmp_w-cmp_poly_enc-poly_extra_in, cmp_l+poly_ext+poly_extra_out))

    # Inserting left cmp contacts
    num_left_con_1, left_con_free_spc_1 = number_spc_contacts(met_con_min, comp_cont_enc, cont_min_spc, cont_size)
    num_left_con_2, left_con_free_spc_2 = number_spc_contacts(cmp_l, comp_cont_enc, cont_min_spc, cont_size)
    left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(cmp_met_cont_enc_diff+left_con_free_spc_1 / 2, left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_left_con_1, num_left_con_2)
    nmoscap_b_cell.insert(left_con_arr)

    # Inserting right cmp contacts
    num_right_con_1, right_con_free_spc_1 = number_spc_contacts(met_con_min, comp_cont_enc, cont_min_spc, cont_size)
    num_right_con_2, right_con_free_spc_2 = number_spc_contacts(cmp_l, comp_cont_enc, cont_min_spc, cont_size)
    right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(cmp_w-cmp_met_cont_enc_diff-met_con_min+right_con_free_spc_1 / 2, right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_right_con_1, num_right_con_2)
    nmoscap_b_cell.insert(right_con_arr)

    # Inserting top poly contacts
    num_top_con_1, top_con_free_spc_1 = number_spc_contacts(cmp_w-2*cmp_poly_enc-2*poly_extra_in, comp_cont_enc, cont_min_spc, cont_size)
    num_top_con_2, top_con_free_spc_2 = number_spc_contacts(poly_extra_out, comp_cont_enc, cont_min_spc, cont_size)
    top_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(cmp_poly_enc+poly_extra_in+top_con_free_spc_1 / 2, cmp_l+poly_ext+top_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_top_con_1, num_top_con_2)
    nmoscap_b_cell.insert(top_con_arr)

    # Inserting bottom poly contacts
    num_bot_con_1, bot_con_free_spc_1 = number_spc_contacts(cmp_w-2*cmp_poly_enc-2*poly_extra_in, comp_cont_enc, cont_min_spc, cont_size)
    num_bot_con_2, bot_con_free_spc_2 = number_spc_contacts(poly_extra_out, comp_cont_enc, cont_min_spc, cont_size)
    bot_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(cmp_poly_enc+poly_extra_in+bot_con_free_spc_1 / 2, -poly_ext-poly_extra_out+bot_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_bot_con_1, num_bot_con_2)
    nmoscap_b_cell.insert(bot_con_arr)

    # Inserting marker
    nmoscap_b_cell.shapes(mos_cap_mk).insert(pya.Box(0, 0, cmp_w, cmp_l))

    if volt == "5/6V":
        # Inserting dualgate
        nmoscap_b_cell.shapes(dualgate).insert(pya.Box(-dualgate_cmp_enc_x, -dualgate_cmp_enc_y, cmp_w+dualgate_cmp_enc_x, cmp_l+dualgate_cmp_enc_y))



    nmoscap_b_cell.flatten(True)
    return nmoscap_b_cell

def draw_pmoscap_b(layout, l, w , volt):
    '''
    Usage:-
     used to draw PMOS capacitor (inside Psub) by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of diff length
     w      : Float of diff width
    '''

    # Define layers
    comp           = layout.layer(22 , 0 )
    poly           = layout.layer(30 , 0 )
    pplus          = layout.layer(31 , 0 )
    contact        = layout.layer(33 , 0 )
    metal1         = layout.layer(34 , 0 )
    mos_cap_mk     = layout.layer(166, 5 )
    dualgate       = layout.layer(55 , 0 )

    # VARIABLES
    dbu_PERCISION         = 1/layout.dbu
    cmp_w                 = w    * dbu_PERCISION
    cmp_l                 = l    * dbu_PERCISION
    poly_ext              = 0.3  * dbu_PERCISION
    cmp_poly_enc          = 0.44 * dbu_PERCISION
    cont_size             = 0.22 * dbu_PERCISION
    cont_min_spc          = 0.25 * dbu_PERCISION
    comp_cont_enc         = 0.07 * dbu_PERCISION
    met_cont_enc          = 0.06 * dbu_PERCISION
    metal_cmp_ext_x       = 0.59 * dbu_PERCISION
    metal_cmp_ext_y       = 2.2  * dbu_PERCISION
    met_width             = 1    * dbu_PERCISION
    met_con_min           = 0.34 * dbu_PERCISION
    cmp_met_cont_enc_diff = 0.01 * dbu_PERCISION
    nwell_cmp_enc_x       = 0.18 * dbu_PERCISION
    nwell_cmp_enc_y       = 1.38 * dbu_PERCISION
    poly_extra_in         = 0.27 * dbu_PERCISION
    poly_extra_out        = 0.9  * dbu_PERCISION
    dualgate_cmp_enc_x    = 0.24 * dbu_PERCISION
    dualgate_cmp_enc_y    = 1.6  * dbu_PERCISION

    # Inserting pmoscap cell
    cell_index  = layout.add_cell("pmoscap_b")
    pmoscap_b_cell = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting diffusion
    pmoscap_b_cell.shapes(comp).insert(pya.Box(0, 0, cmp_w, cmp_l))
    pmoscap_b_cell.shapes(pplus).insert(pya.Box(-nwell_cmp_enc_x, -nwell_cmp_enc_y, cmp_w+nwell_cmp_enc_x, cmp_l+nwell_cmp_enc_y))

    # Inserting poly
    pmoscap_b_cell.shapes(poly).insert(pya.Box(cmp_poly_enc, -poly_ext, cmp_w-cmp_poly_enc, cmp_l+poly_ext))

    # Inserting extra poly
    pmoscap_b_cell.shapes(poly).insert(pya.Box(cmp_poly_enc+poly_extra_in, cmp_l+poly_ext, cmp_w-cmp_poly_enc-poly_extra_in, cmp_l+poly_ext+poly_extra_out))  #top
    pmoscap_b_cell.shapes(poly).insert(pya.Box(cmp_poly_enc+poly_extra_in, -poly_ext-poly_extra_out, cmp_w-cmp_poly_enc-poly_extra_in, -poly_ext))            #bot

    # Inserting left metal
    pmoscap_b_cell.shapes(metal1).insert(pya.Box(-metal_cmp_ext_x, -metal_cmp_ext_y, -metal_cmp_ext_x+met_width, cmp_l))

    # Inserting right metal
    pmoscap_b_cell.shapes(metal1).insert(pya.Box(cmp_w+metal_cmp_ext_x-met_width, -metal_cmp_ext_y-met_width, cmp_w+metal_cmp_ext_x, cmp_l))

    # Inserting bottom metal
    pmoscap_b_cell.shapes(metal1).insert(pya.Box(-metal_cmp_ext_x, -metal_cmp_ext_y-met_width, cmp_w+metal_cmp_ext_x, -metal_cmp_ext_y))

    # Inserting poly metal
    pmoscap_b_cell.shapes(metal1).insert(pya.Box(cmp_poly_enc+poly_extra_in, -poly_ext-poly_extra_out, cmp_w-cmp_poly_enc-poly_extra_in, cmp_l+poly_ext+poly_extra_out))

    # Inserting left cmp contacts
    num_left_con_1, left_con_free_spc_1 = number_spc_contacts(met_con_min, comp_cont_enc, cont_min_spc, cont_size)
    num_left_con_2, left_con_free_spc_2 = number_spc_contacts(cmp_l, comp_cont_enc, cont_min_spc, cont_size)
    left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(cmp_met_cont_enc_diff+left_con_free_spc_1 / 2, left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_left_con_1, num_left_con_2)
    pmoscap_b_cell.insert(left_con_arr)

    # Inserting right cmp contacts
    num_right_con_1, right_con_free_spc_1 = number_spc_contacts(met_con_min, comp_cont_enc, cont_min_spc, cont_size)
    num_right_con_2, right_con_free_spc_2 = number_spc_contacts(cmp_l, comp_cont_enc, cont_min_spc, cont_size)
    right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(cmp_w-cmp_met_cont_enc_diff-met_con_min+right_con_free_spc_1 / 2, right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_right_con_1, num_right_con_2)
    pmoscap_b_cell.insert(right_con_arr)

    # Inserting top poly contacts
    num_top_con_1, top_con_free_spc_1 = number_spc_contacts(cmp_w-2*cmp_poly_enc-2*poly_extra_in, comp_cont_enc, cont_min_spc, cont_size)
    num_top_con_2, top_con_free_spc_2 = number_spc_contacts(poly_extra_out, comp_cont_enc, cont_min_spc, cont_size)
    top_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(cmp_poly_enc+poly_extra_in+top_con_free_spc_1 / 2, cmp_l+poly_ext+top_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_top_con_1, num_top_con_2)
    pmoscap_b_cell.insert(top_con_arr)

    # Inserting bottom poly contacts
    num_bot_con_1, bot_con_free_spc_1 = number_spc_contacts(cmp_w-2*cmp_poly_enc-2*poly_extra_in, comp_cont_enc, cont_min_spc, cont_size)
    num_bot_con_2, bot_con_free_spc_2 = number_spc_contacts(poly_extra_out, comp_cont_enc, cont_min_spc, cont_size)
    bot_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(cmp_poly_enc+poly_extra_in+bot_con_free_spc_1 / 2, -poly_ext-poly_extra_out+bot_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_bot_con_1, num_bot_con_2)
    pmoscap_b_cell.insert(bot_con_arr)

    # Inserting marker
    pmoscap_b_cell.shapes(mos_cap_mk).insert(pya.Box(0, 0, cmp_w, cmp_l))

    if volt == "5/6V":
        # Inserting dualgate
        pmoscap_b_cell.shapes(dualgate).insert(pya.Box(-dualgate_cmp_enc_x, -dualgate_cmp_enc_y, cmp_w+dualgate_cmp_enc_x, cmp_l+dualgate_cmp_enc_y))


    pmoscap_b_cell.flatten(True)
    return pmoscap_b_cell
