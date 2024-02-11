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
## Diode Pcells Generators for Klayout of GF180MCU
########################################################################################################################

import pya

def number_spc_contacts(box_width, min_enc, cont_spacing, cont_width):
    """ Calculate number of cantacts in a given dimensions and the free space for symmetry.
        By getting the min enclosure,the width of the box,the width ans spacing of the contacts.
        Parameters
        -----
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

def draw_np_diode(layout, l, w , volt, deepnwell, pcmpgr):
    '''
    Usage:-
     used to draw N+/LVPWELL diode (Outside DNWELL) by specifying parameters
    Arguments:-
     layout     : Object of layout
     l          : Float of diff length
     w          : Float of diff width
     volt       : String of operating voltage of the diode [3.3V, 5V/6V]
     deepnwell  : Boolean of using Deep NWELL device
     pcmpgr     : Boolean of using P+ Guard Ring for Deep NWELL devices only
    '''

    # Define layers
    dnwell              = layout.layer(12 , 0 )
    lvpwell             = layout.layer(204, 0 )
    comp                = layout.layer(22 , 0 )
    nplus               = layout.layer(32 , 0 )
    pplus               = layout.layer(31 , 0 )
    contact             = layout.layer(33 , 0 )
    metal1              = layout.layer(34 , 0 )
    dualgate            = layout.layer(55 , 0 )
    diode_mk            = layout.layer(115, 5 )

    # Define variables
    dbu_PERCISION       = 1/layout.dbu
    pcmp2ncmp_spc       = 0.48 * dbu_PERCISION
    ncmp_w              = 0.36 * dbu_PERCISION
    pcmp_w              = w * dbu_PERCISION
    cmp_l               = l * dbu_PERCISION
    implant_comp_enc    = 0.16 * dbu_PERCISION
    comp_cont_enc       = 0.07 * dbu_PERCISION
    cont_size           = 0.22 * dbu_PERCISION
    cont_min_spc        = 0.28 * dbu_PERCISION
    dualgate_cmp_enc    = 0.24 * dbu_PERCISION
    dg_enc_dnwell       = 0.5  * dbu_PERCISION
    dnwell_enc_lvpwell  = 2.5  * dbu_PERCISION
    lvpwell_enc_ncmp    = 0.6  * dbu_PERCISION
    lvpwell_enc_pcmp    = 0.16 * dbu_PERCISION
    min_cmp_area        = 0.2025 * dbu_PERCISION * dbu_PERCISION
    tie_violat          = 0      * dbu_PERCISION
    pcmp_gr2dnw         = 2.5    * dbu_PERCISION

    # Inserting np cell
    cell_index      = layout.add_cell("np_diode")
    np_diode_cell   = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell       = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting diffusion
    if (cmp_l * ncmp_w) < min_cmp_area:
        tie_violat = (min_cmp_area/ncmp_w - cmp_l)/2
    np_diode_cell.shapes(comp).insert(pya.Box(0, -tie_violat, ncmp_w, cmp_l+tie_violat))
    np_diode_cell.shapes(pplus).insert(pya.Box(-implant_comp_enc, -implant_comp_enc-tie_violat, ncmp_w+implant_comp_enc, cmp_l+implant_comp_enc+tie_violat))

    np_diode_cell.shapes(comp).insert(pya.Box(ncmp_w+pcmp2ncmp_spc, 0, ncmp_w+pcmp2ncmp_spc+pcmp_w, cmp_l))
    np_diode_cell.shapes(nplus).insert(pya.Box(ncmp_w+pcmp2ncmp_spc-implant_comp_enc, -implant_comp_enc, ncmp_w+pcmp2ncmp_spc+pcmp_w+implant_comp_enc, cmp_l+implant_comp_enc))

    # Inserting metal
    np_diode_cell.shapes(metal1).insert(pya.Box(0, -tie_violat, ncmp_w, cmp_l+tie_violat))
    np_diode_cell.shapes(metal1).insert(pya.Box(ncmp_w+pcmp2ncmp_spc, 0, ncmp_w+pcmp2ncmp_spc+pcmp_w, cmp_l))


    # Inserting pcomp contacts
    num_ncmp_con_1, ncmp_con_free_spc_1 = number_spc_contacts(ncmp_w, comp_cont_enc, cont_min_spc, cont_size)
    num_ncmp_con_2, ncmp_con_free_spc_2 = number_spc_contacts(cmp_l, comp_cont_enc, cont_min_spc, cont_size)
    ncmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(ncmp_con_free_spc_1 / 2, ncmp_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_con_1, num_ncmp_con_2)
    np_diode_cell.insert(ncmp_con_arr)

    # Inserting ncomp contacts
    num_pcmp_con_1, pcmp_con_free_spc_1 = number_spc_contacts(pcmp_w, comp_cont_enc, cont_min_spc, cont_size)
    num_pcmp_con_2, pcmp_con_free_spc_2 = number_spc_contacts(cmp_l, comp_cont_enc, cont_min_spc, cont_size)
    pcmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(ncmp_w+pcmp2ncmp_spc+pcmp_con_free_spc_1 / 2, pcmp_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_pcmp_con_1, num_pcmp_con_2)
    np_diode_cell.insert(pcmp_con_arr)

    # Inserting Deep NWELL layers
    if deepnwell == True:
        np_diode_cell.shapes(lvpwell).insert(pya.Box(-lvpwell_enc_pcmp, -lvpwell_enc_ncmp, ncmp_w+pcmp2ncmp_spc+pcmp_w+lvpwell_enc_ncmp, cmp_l+lvpwell_enc_ncmp))
        np_diode_cell.shapes(dnwell).insert(pya.Box(-lvpwell_enc_pcmp-dnwell_enc_lvpwell, -lvpwell_enc_ncmp-dnwell_enc_lvpwell, ncmp_w+pcmp2ncmp_spc+pcmp_w+lvpwell_enc_ncmp+dnwell_enc_lvpwell, cmp_l+lvpwell_enc_ncmp+dnwell_enc_lvpwell))

        # Inserting Deep NWELL P+ Guard Ring
        if pcmpgr == True:
            cmp_inner   = pya.Box(-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw, -lvpwell_enc_ncmp-dnwell_enc_lvpwell-pcmp_gr2dnw, ncmp_w+pcmp2ncmp_spc+pcmp_w+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw, cmp_l+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw)
            cmp_outer   = pya.Box(-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw-ncmp_w, -lvpwell_enc_ncmp-dnwell_enc_lvpwell-pcmp_gr2dnw-ncmp_w, ncmp_w+pcmp2ncmp_spc+pcmp_w+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw+ncmp_w, cmp_l+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw+ncmp_w)
            cmp_gr      = pya.Region(cmp_outer) - pya.Region(cmp_inner)
            np_diode_cell.shapes(comp).insert(cmp_gr)

            pp_inner = pya.Box(-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw+implant_comp_enc, -lvpwell_enc_ncmp-dnwell_enc_lvpwell-pcmp_gr2dnw+implant_comp_enc, ncmp_w+pcmp2ncmp_spc+pcmp_w+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw-implant_comp_enc, cmp_l+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw-implant_comp_enc)
            pp_outer = pya.Box(-lvpwell_enc_pcmp-dnwell_enc_lvpwell-pcmp_gr2dnw-ncmp_w-implant_comp_enc, -lvpwell_enc_ncmp-dnwell_enc_lvpwell-pcmp_gr2dnw-ncmp_w-implant_comp_enc, ncmp_w+pcmp2ncmp_spc+pcmp_w+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw+ncmp_w+implant_comp_enc, cmp_l+lvpwell_enc_ncmp+dnwell_enc_lvpwell+pcmp_gr2dnw+ncmp_w+implant_comp_enc)
            pp_gr    = pya.Region(pp_outer) - pya.Region(pp_inner)
            np_diode_cell.shapes(pplus).insert(pp_gr)

    if volt == "5/6V":
        # Inserting marker
        np_diode_cell.shapes(diode_mk).insert(pya.Box(-dualgate_cmp_enc, -dualgate_cmp_enc, ncmp_w+pcmp2ncmp_spc+pcmp_w+dualgate_cmp_enc, cmp_l+dualgate_cmp_enc))
        # Inserting dualgate
        if deepnwell == True:
            np_diode_cell.shapes(dualgate).insert(pya.Box(-lvpwell_enc_pcmp-dnwell_enc_lvpwell-dg_enc_dnwell, -lvpwell_enc_ncmp-dnwell_enc_lvpwell-dg_enc_dnwell, ncmp_w+pcmp2ncmp_spc+pcmp_w+lvpwell_enc_ncmp+dnwell_enc_lvpwell+dg_enc_dnwell, cmp_l+lvpwell_enc_ncmp+dnwell_enc_lvpwell+dg_enc_dnwell))
        else:
            np_diode_cell.shapes(dualgate).insert(pya.Box(-dualgate_cmp_enc, -dualgate_cmp_enc, ncmp_w+pcmp2ncmp_spc+pcmp_w+dualgate_cmp_enc, cmp_l+dualgate_cmp_enc))
    else:
        np_diode_cell.shapes(diode_mk).insert(pya.Box(-implant_comp_enc, -implant_comp_enc, ncmp_w+pcmp2ncmp_spc+pcmp_w+implant_comp_enc, cmp_l+implant_comp_enc))

    np_diode_cell.flatten(True)
    return np_diode_cell

def draw_pn_diode(layout, l, w , volt, deepnwell, pcmpgr):
    '''
    Usage:-
     used to draw 3.3V P+/Nwell diode (Outside DNWELL) by specifying parameters
    Arguments:-
     layout     : Object of layout
     l          : Float of diffusion length
     w          : Float of diffusion width
     volt       : String of operating voltage of the diode [3.3V, 5V/6V]
     deepnwell  : Boolean of using Deep NWELL device
     pcmpgr     : Boolean of using P+ Guard Ring for Deep NWELL devices only
    '''

    # Define layers
    dnwell              = layout.layer(12 , 0 )
    comp                = layout.layer(22 , 0 )
    nplus               = layout.layer(32 , 0 )
    pplus               = layout.layer(31 , 0 )
    nwell               = layout.layer(21 , 0 )
    contact             = layout.layer(33 , 0 )
    metal1              = layout.layer(34 , 0 )
    dualgate            = layout.layer(55 , 0 )
    diode_mk            = layout.layer(115, 5 )

    # Define variables
    dbu_PERCISION       = 1/layout.dbu
    pcmp2ncmp_spc       = 0.48      * dbu_PERCISION
    ncmp_w              = 0.36      * dbu_PERCISION
    pcmp_w              = w         * dbu_PERCISION
    cmp_l               = l         * dbu_PERCISION
    implant_comp_enc    = 0.16      * dbu_PERCISION
    comp_cont_enc       = 0.07      * dbu_PERCISION
    cont_size           = 0.22      * dbu_PERCISION
    cont_min_spc        = 0.28      * dbu_PERCISION

    nwell_ncmp_enc      = 0.12      * dbu_PERCISION
    nwell_pcmp_enc      = 0.43      * dbu_PERCISION
    dg_enc_dnwell       = 0.5       * dbu_PERCISION
    dnwell_enc_nwell    = 0.5       * dbu_PERCISION
    min_cmp_area        = 0.2025    * dbu_PERCISION * dbu_PERCISION
    tie_violat          = 0         * dbu_PERCISION
    pcmp_gr2dnw         = 2.5       * dbu_PERCISION
    dnwell_violat       = 0         * dbu_PERCISION

    if volt == "5/6V" or deepnwell == True:
        nwell_ncmp_enc  = 0.16      * dbu_PERCISION
        nwell_pcmp_enc  = 0.6       * dbu_PERCISION
        dnwell_violat   = 0.12      * dbu_PERCISION

    # Inserting pn cell
    cell_index      = layout.add_cell("pn_diode")
    pn_diode_cell   = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell       = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting diffusion
    if (cmp_l * ncmp_w) < min_cmp_area:
        tie_violat = (min_cmp_area/ncmp_w - cmp_l)/2
    pn_diode_cell.shapes(comp).insert(pya.Box(0, -tie_violat, ncmp_w, cmp_l+tie_violat))
    pn_diode_cell.shapes(nplus).insert(pya.Box(-implant_comp_enc, -implant_comp_enc-tie_violat, ncmp_w+implant_comp_enc, cmp_l+implant_comp_enc+tie_violat))

    pn_diode_cell.shapes(comp).insert(pya.Box(ncmp_w+pcmp2ncmp_spc, 0, ncmp_w+pcmp2ncmp_spc+pcmp_w, cmp_l))
    pn_diode_cell.shapes(pplus).insert(pya.Box(ncmp_w+pcmp2ncmp_spc-implant_comp_enc, -implant_comp_enc, ncmp_w+pcmp2ncmp_spc+pcmp_w+implant_comp_enc, cmp_l+implant_comp_enc))

    # Inserting metal
    pn_diode_cell.shapes(metal1).insert(pya.Box(0, -tie_violat, ncmp_w, cmp_l+tie_violat))
    pn_diode_cell.shapes(metal1).insert(pya.Box(ncmp_w+pcmp2ncmp_spc, 0, ncmp_w+pcmp2ncmp_spc+pcmp_w, cmp_l))

    # Inserting nwell
    pn_diode_cell.shapes(nwell).insert(pya.Box(-nwell_ncmp_enc-dnwell_violat, -nwell_pcmp_enc, ncmp_w+pcmp2ncmp_spc+pcmp_w+nwell_pcmp_enc, cmp_l+nwell_pcmp_enc))


    # Inserting pcomp contacts
    num_ncmp_con_1, ncmp_con_free_spc_1 = number_spc_contacts(ncmp_w, comp_cont_enc, cont_min_spc, cont_size)
    num_ncmp_con_2, ncmp_con_free_spc_2 = number_spc_contacts(cmp_l, comp_cont_enc, cont_min_spc, cont_size)
    ncmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(ncmp_con_free_spc_1 / 2, ncmp_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_con_1, num_ncmp_con_2)
    pn_diode_cell.insert(ncmp_con_arr)

    # Inserting ncomp contacts
    num_pcmp_con_1, pcmp_con_free_spc_1 = number_spc_contacts(pcmp_w, comp_cont_enc, cont_min_spc, cont_size)
    num_pcmp_con_2, pcmp_con_free_spc_2 = number_spc_contacts(cmp_l, comp_cont_enc, cont_min_spc, cont_size)
    pcmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(ncmp_w+pcmp2ncmp_spc+pcmp_con_free_spc_1 / 2, pcmp_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_pcmp_con_1, num_pcmp_con_2)
    pn_diode_cell.insert(pcmp_con_arr)

    # Inserting Deep NWELL layers
    if deepnwell == True:
        pn_diode_cell.shapes(dnwell).insert(pya.Box(-nwell_ncmp_enc-dnwell_enc_nwell-dnwell_violat, -nwell_pcmp_enc-dnwell_enc_nwell, ncmp_w+pcmp2ncmp_spc+pcmp_w+nwell_pcmp_enc+dnwell_enc_nwell, cmp_l+nwell_pcmp_enc+dnwell_enc_nwell))

        # Inserting Deep NWELL P+ Guard Ring
        if pcmpgr == True:
            cmp_inner = pya.Box(-nwell_ncmp_enc-dnwell_enc_nwell-pcmp_gr2dnw-dnwell_violat, -nwell_pcmp_enc-dnwell_enc_nwell-pcmp_gr2dnw, ncmp_w+pcmp2ncmp_spc+pcmp_w+nwell_pcmp_enc+dnwell_enc_nwell+pcmp_gr2dnw, cmp_l+nwell_pcmp_enc+dnwell_enc_nwell+pcmp_gr2dnw)
            cmp_outer = pya.Box(-nwell_ncmp_enc-dnwell_enc_nwell-pcmp_gr2dnw-ncmp_w-dnwell_violat, -nwell_pcmp_enc-dnwell_enc_nwell-pcmp_gr2dnw-ncmp_w, ncmp_w+pcmp2ncmp_spc+pcmp_w+nwell_pcmp_enc+dnwell_enc_nwell+pcmp_gr2dnw+ncmp_w, cmp_l+nwell_pcmp_enc+dnwell_enc_nwell+pcmp_gr2dnw+ncmp_w)
            cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
            pn_diode_cell.shapes(comp).insert(cmp_gr)

            pp_inner = pya.Box(-nwell_ncmp_enc-dnwell_enc_nwell-pcmp_gr2dnw+implant_comp_enc-dnwell_violat, -nwell_pcmp_enc-dnwell_enc_nwell-pcmp_gr2dnw+implant_comp_enc, ncmp_w+pcmp2ncmp_spc+pcmp_w+nwell_pcmp_enc+dnwell_enc_nwell+pcmp_gr2dnw-implant_comp_enc, cmp_l+nwell_pcmp_enc+dnwell_enc_nwell+pcmp_gr2dnw-implant_comp_enc)
            pp_outer = pya.Box(-nwell_ncmp_enc-dnwell_enc_nwell-pcmp_gr2dnw-ncmp_w-implant_comp_enc-dnwell_violat, -nwell_pcmp_enc-dnwell_enc_nwell-pcmp_gr2dnw-ncmp_w-implant_comp_enc, ncmp_w+pcmp2ncmp_spc+pcmp_w+nwell_pcmp_enc+dnwell_enc_nwell+pcmp_gr2dnw+ncmp_w+implant_comp_enc, cmp_l+nwell_pcmp_enc+dnwell_enc_nwell+pcmp_gr2dnw+ncmp_w+implant_comp_enc)
            pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
            pn_diode_cell.shapes(pplus).insert(pp_gr)

    if volt == "5/6V":
        # Inserting dualgate
        if deepnwell == True:
            pn_diode_cell.shapes(dualgate).insert(pya.Box(-nwell_ncmp_enc-dnwell_enc_nwell-dg_enc_dnwell-dnwell_violat, -nwell_pcmp_enc-dnwell_enc_nwell-dg_enc_dnwell, ncmp_w+pcmp2ncmp_spc+pcmp_w+nwell_pcmp_enc+dnwell_enc_nwell+dg_enc_dnwell, cmp_l+nwell_pcmp_enc+dnwell_enc_nwell+dg_enc_dnwell))
        else:
            pn_diode_cell.shapes(dualgate).insert(pya.Box(-nwell_ncmp_enc-dnwell_violat-dnwell_violat, -nwell_pcmp_enc, ncmp_w+pcmp2ncmp_spc+pcmp_w+nwell_pcmp_enc, cmp_l+nwell_pcmp_enc))

    # Inserting marker
    pn_diode_cell.shapes(diode_mk).insert(pya.Box(ncmp_w+pcmp2ncmp_spc, 0, ncmp_w+pcmp2ncmp_spc+pcmp_w, cmp_l))

    pn_diode_cell.flatten(True)
    return pn_diode_cell

def draw_nwp_diode(layout, l, w , volt):
    '''
    Usage:-
     used to draw 3.3V Nwell/Psub diode by specifying parameters
    Arguments:-
     layout     : Object of layout
     l          : Float of diff length
     w          : Float of diff width
     volt       : String of operating voltage of the diode [3.3V, 5V/6V]
    '''

    # Define layers
    comp                = layout.layer(22 , 0 )
    nplus               = layout.layer(32 , 0 )
    pplus               = layout.layer(31 , 0 )
    nwell               = layout.layer (21 , 0)
    contact             = layout.layer(33 , 0 )
    metal1              = layout.layer(34 , 0 )
    dualgate            = layout.layer(55 , 0 )
    well_diode_mk       = layout.layer(153, 51)

    # Define variables
    dbu_PERCISION       = 1/layout.dbu
    pcmp2ncmp_spc       = 0.44  * dbu_PERCISION
    ncmp_w              = 0.36  * dbu_PERCISION
    pcmp_w              = w     * dbu_PERCISION
    cmp_l               = l     * dbu_PERCISION
    implant_comp_enc    = 0.16  * dbu_PERCISION
    comp_cont_enc       = 0.07  * dbu_PERCISION
    cont_size           = 0.22  * dbu_PERCISION
    cont_min_spc        = 0.28  * dbu_PERCISION
    dualgate_cmp_enc    = 0.24  * dbu_PERCISION

    # Inserting nwp cell
    cell_index      = layout.add_cell("nwp_diode")
    nwp_diode_cell  = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell       = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting diffusion
    nwp_diode_cell.shapes(comp).insert(pya.Box(0, 0, ncmp_w, cmp_l))
    nwp_diode_cell.shapes(pplus).insert(pya.Box(-implant_comp_enc, -implant_comp_enc, ncmp_w+implant_comp_enc, cmp_l+implant_comp_enc))

    nwp_diode_cell.shapes(comp).insert(pya.Box(ncmp_w+pcmp2ncmp_spc, 0, ncmp_w+pcmp2ncmp_spc+pcmp_w, cmp_l))
    nwp_diode_cell.shapes(nplus).insert(pya.Box(ncmp_w+pcmp2ncmp_spc-implant_comp_enc, -implant_comp_enc, ncmp_w+pcmp2ncmp_spc+pcmp_w+implant_comp_enc, cmp_l+implant_comp_enc))

    # Inserting nwell
    nwp_diode_cell.shapes(nwell).insert(pya.Box(ncmp_w+pcmp2ncmp_spc-implant_comp_enc, -implant_comp_enc, ncmp_w+pcmp2ncmp_spc+pcmp_w+implant_comp_enc, cmp_l+implant_comp_enc))

    # Inserting metal
    nwp_diode_cell.shapes(metal1).insert(pya.Box(0, 0, ncmp_w, cmp_l))
    nwp_diode_cell.shapes(metal1).insert(pya.Box(ncmp_w+pcmp2ncmp_spc, 0, ncmp_w+pcmp2ncmp_spc+pcmp_w, cmp_l))

    # Inserting pcomp contacts
    num_ncmp_con_1, ncmp_con_free_spc_1 = number_spc_contacts(ncmp_w, comp_cont_enc, cont_min_spc, cont_size)
    num_ncmp_con_2, ncmp_con_free_spc_2 = number_spc_contacts(cmp_l, comp_cont_enc, cont_min_spc, cont_size)
    ncmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(ncmp_con_free_spc_1 / 2, ncmp_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_con_1, num_ncmp_con_2)
    nwp_diode_cell.insert(ncmp_con_arr)

    # Inserting ncomp contacts
    num_pcmp_con_1, pcmp_con_free_spc_1 = number_spc_contacts(pcmp_w, comp_cont_enc, cont_min_spc, cont_size)
    num_pcmp_con_2, pcmp_con_free_spc_2 = number_spc_contacts(cmp_l, comp_cont_enc, cont_min_spc, cont_size)
    pcmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(ncmp_w+pcmp2ncmp_spc+pcmp_con_free_spc_1 / 2, pcmp_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_pcmp_con_1, num_pcmp_con_2)
    nwp_diode_cell.insert(pcmp_con_arr)

    if volt == "5/6V":
        # Inserting marker
        nwp_diode_cell.shapes(well_diode_mk).insert(pya.Box(-dualgate_cmp_enc, -dualgate_cmp_enc, ncmp_w+pcmp2ncmp_spc+pcmp_w+dualgate_cmp_enc, cmp_l+dualgate_cmp_enc))
        # Inserting dualgate
        nwp_diode_cell.shapes(dualgate).insert(pya.Box(-dualgate_cmp_enc, -dualgate_cmp_enc, ncmp_w+pcmp2ncmp_spc+pcmp_w+dualgate_cmp_enc, cmp_l+dualgate_cmp_enc))
    else:
        # Inserting marker
        nwp_diode_cell.shapes(well_diode_mk).insert(pya.Box(-implant_comp_enc, -implant_comp_enc, ncmp_w+pcmp2ncmp_spc+pcmp_w+implant_comp_enc, cmp_l+implant_comp_enc))

    nwp_diode_cell.flatten(True)
    return nwp_diode_cell

def draw_dnwpw_diode(layout, l, w , volt):
    '''
    Usage:-
     used to draw LVPWELL/DNWELL diode by specifying parameters
    Arguments:-
     layout     : Object of layout
     l          : Float of diff length
     w          : Float of diff width
     volt       : String of operating voltage of the diode [3.3V, 5V/6V]
    '''

    # Define layers
    lvpwell                 = layout.layer(204, 0 )
    dnwell                  = layout.layer(12 , 0 )
    comp                    = layout.layer(22 , 0 )
    nplus                   = layout.layer(32 , 0 )
    pplus                   = layout.layer(31 , 0 )
    nwell                   = layout.layer(21 , 0 )
    contact                 = layout.layer(33 , 0 )
    metal1                  = layout.layer(34 , 0 )
    dualgate                = layout.layer(55 , 0 )
    well_diode_mk           = layout.layer(153, 51)

    # Define variables
    dbu_PERCISION           = 1/layout.dbu
    lvpwell_w               = w    * dbu_PERCISION
    lvpwell_l               = l    * dbu_PERCISION
    dnwell_lvpwell_enc      = 2.5  * dbu_PERCISION
    lvpwell_pcmp_enc        = 0.12 * dbu_PERCISION
    cmp_w                   = 0.36 * dbu_PERCISION
    pcmp2ncmp_spc           = 0.32 * dbu_PERCISION
    implant_comp_enc        = 0.16 * dbu_PERCISION
    ncmp_ext                = 0.56 * dbu_PERCISION
    lvpwell_gr_spc          = 5    * dbu_PERCISION
    cont_spc_tol            = 0.11 * dbu_PERCISION
    comp_cont_enc           = 0.07 * dbu_PERCISION
    cont_size               = 0.22 * dbu_PERCISION
    cont_min_spc            = 0.25 * dbu_PERCISION
    dualgate_lvpwell_enc    = 3    * dbu_PERCISION
    pcmp2ncmp_spc           = 0.32 * dbu_PERCISION
    lvpwell_pcmp_enc        = 0.12 * dbu_PERCISION

    if volt == "5/6V":
        pcmp2ncmp_spc       = 0.36 * dbu_PERCISION
        lvpwell_pcmp_enc    = 0.16 * dbu_PERCISION

    # Inserting dnwpw cell
    cell_index       = layout.add_cell("dnwpw_diode")
    dnwpw_diode_cell = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell       = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting lvpwell
    dnwpw_diode_cell.shapes(lvpwell).insert(pya.Box(0, 0, lvpwell_w, lvpwell_l))

    # Inserting dnwell
    dnwpw_diode_cell.shapes(dnwell).insert(pya.Box(-dnwell_lvpwell_enc, -dnwell_lvpwell_enc, lvpwell_w+dnwell_lvpwell_enc, lvpwell_l+dnwell_lvpwell_enc))

    # Inserting p diffusion
    dnwpw_diode_cell.shapes(comp).insert(pya.Box(lvpwell_pcmp_enc, lvpwell_pcmp_enc , lvpwell_pcmp_enc+cmp_w, lvpwell_l-lvpwell_pcmp_enc))                                    # left
    dnwpw_diode_cell.shapes(pplus).insert(pya.Box(lvpwell_pcmp_enc-implant_comp_enc, lvpwell_pcmp_enc-implant_comp_enc , lvpwell_pcmp_enc+cmp_w+implant_comp_enc, lvpwell_l-lvpwell_pcmp_enc+implant_comp_enc))

    dnwpw_diode_cell.shapes(comp).insert(pya.Box(lvpwell_w-lvpwell_pcmp_enc-cmp_w, lvpwell_pcmp_enc , lvpwell_w-lvpwell_pcmp_enc , lvpwell_l-lvpwell_pcmp_enc))               # right
    dnwpw_diode_cell.shapes(pplus).insert(pya.Box(lvpwell_w-lvpwell_pcmp_enc-cmp_w-implant_comp_enc, lvpwell_pcmp_enc-implant_comp_enc , lvpwell_w-lvpwell_pcmp_enc+implant_comp_enc , lvpwell_l-lvpwell_pcmp_enc+implant_comp_enc))

    dnwpw_diode_cell.shapes(comp).insert(pya.Box(lvpwell_pcmp_enc+cmp_w, lvpwell_l-lvpwell_pcmp_enc-cmp_w , lvpwell_w-lvpwell_pcmp_enc-cmp_w , lvpwell_l-lvpwell_pcmp_enc))   # top
    dnwpw_diode_cell.shapes(pplus).insert(pya.Box(lvpwell_pcmp_enc+cmp_w+implant_comp_enc, lvpwell_l-lvpwell_pcmp_enc-cmp_w-implant_comp_enc , lvpwell_w-lvpwell_pcmp_enc-cmp_w-implant_comp_enc , lvpwell_l-lvpwell_pcmp_enc+implant_comp_enc)) # top

    dnwpw_diode_cell.shapes(comp).insert(pya.Box(lvpwell_pcmp_enc+cmp_w, lvpwell_pcmp_enc , lvpwell_w-lvpwell_pcmp_enc-cmp_w , lvpwell_pcmp_enc+cmp_w))                       # bottom
    dnwpw_diode_cell.shapes(pplus).insert(pya.Box(lvpwell_pcmp_enc+cmp_w+implant_comp_enc, lvpwell_pcmp_enc-implant_comp_enc , lvpwell_w-lvpwell_pcmp_enc-cmp_w-implant_comp_enc, lvpwell_pcmp_enc+cmp_w+implant_comp_enc)) # bottom

    # Inserting pcomp metal
    dnwpw_diode_cell.shapes(metal1).insert(pya.Box(lvpwell_pcmp_enc, lvpwell_pcmp_enc , lvpwell_pcmp_enc+cmp_w, lvpwell_l-lvpwell_pcmp_enc))                                  # left
    dnwpw_diode_cell.shapes(metal1).insert(pya.Box(lvpwell_w-lvpwell_pcmp_enc-cmp_w, lvpwell_pcmp_enc , lvpwell_w-lvpwell_pcmp_enc , lvpwell_l-lvpwell_pcmp_enc))             # right
    dnwpw_diode_cell.shapes(metal1).insert(pya.Box(lvpwell_pcmp_enc+cmp_w, lvpwell_l-lvpwell_pcmp_enc-cmp_w , lvpwell_w-lvpwell_pcmp_enc-cmp_w , lvpwell_l-lvpwell_pcmp_enc)) # top
    dnwpw_diode_cell.shapes(metal1).insert(pya.Box(lvpwell_pcmp_enc+cmp_w, lvpwell_pcmp_enc , lvpwell_w-lvpwell_pcmp_enc-cmp_w , lvpwell_pcmp_enc+cmp_w))                     # bottom

    # Inserting pcomp contacts
    num_pcmp_left_con_1, pcmp_left_con_free_spc_1 = number_spc_contacts(cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    num_pcmp_left_con_2, pcmp_left_con_free_spc_2 = number_spc_contacts(lvpwell_l-2*lvpwell_pcmp_enc, comp_cont_enc, cont_min_spc, cont_size)
    pcmp_left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(lvpwell_pcmp_enc+pcmp_left_con_free_spc_1 / 2, lvpwell_pcmp_enc+pcmp_left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_pcmp_left_con_1, num_pcmp_left_con_2)
    dnwpw_diode_cell.insert(pcmp_left_con_arr)

    num_cmp_right_con_1, cmp_right_con_free_spc_1 = number_spc_contacts(cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    num_cmp_right_con_2, cmp_right_con_free_spc_2 = number_spc_contacts(lvpwell_l-2*lvpwell_pcmp_enc, comp_cont_enc, cont_min_spc, cont_size)
    cmp_right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(lvpwell_w-lvpwell_pcmp_enc-cmp_w+cmp_right_con_free_spc_1 / 2, lvpwell_pcmp_enc+cmp_right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_cmp_right_con_1, num_cmp_right_con_2)
    dnwpw_diode_cell.insert(cmp_right_con_arr)

    num_cmp_top_con_1, cmp_top_con_free_spc_1 = number_spc_contacts(lvpwell_w-2*lvpwell_pcmp_enc-2*cmp_w-2*cont_spc_tol, comp_cont_enc, cont_min_spc, cont_size)
    num_cmp_top_con_2, cmp_top_con_free_spc_2 = number_spc_contacts(cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    cmp_top_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(lvpwell_pcmp_enc+cmp_w+cont_spc_tol+cmp_top_con_free_spc_1 / 2, lvpwell_l-lvpwell_pcmp_enc-cmp_w+cmp_top_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_cmp_top_con_1, num_cmp_top_con_2)
    dnwpw_diode_cell.insert(cmp_top_con_arr)

    num_cmp_bot_con_1, cmp_bot_con_free_spc_1 = number_spc_contacts(lvpwell_w-2*lvpwell_pcmp_enc-2*cmp_w-2*cont_spc_tol, comp_cont_enc, cont_min_spc, cont_size)
    num_cmp_bot_con_2, cmp_bot_con_free_spc_2 = number_spc_contacts(cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    cmp_bot_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(lvpwell_pcmp_enc+cmp_w+cont_spc_tol+cmp_bot_con_free_spc_1 / 2, lvpwell_pcmp_enc+cmp_bot_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_cmp_bot_con_1, num_cmp_bot_con_2)
    dnwpw_diode_cell.insert(cmp_bot_con_arr)

    # Inserting n diffusion
    dnwpw_diode_cell.shapes(comp).insert(pya.Box(lvpwell_pcmp_enc-pcmp2ncmp_spc-cmp_w, -ncmp_ext , lvpwell_pcmp_enc-pcmp2ncmp_spc, lvpwell_l+ncmp_ext))
    dnwpw_diode_cell.shapes(nplus).insert(pya.Box(lvpwell_pcmp_enc-pcmp2ncmp_spc-cmp_w-implant_comp_enc, -ncmp_ext-implant_comp_enc , lvpwell_pcmp_enc-pcmp2ncmp_spc+implant_comp_enc, lvpwell_l+ncmp_ext+implant_comp_enc))

    # Inserting ncomp metal
    dnwpw_diode_cell.shapes(metal1).insert(pya.Box(lvpwell_pcmp_enc-pcmp2ncmp_spc-cmp_w, -ncmp_ext , lvpwell_pcmp_enc-pcmp2ncmp_spc, lvpwell_l+ncmp_ext))

    # Inserting ncomp contacts
    num_pcmp_con_1, pcmp_con_free_spc_1 = number_spc_contacts(cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    num_pcmp_con_2, pcmp_con_free_spc_2 = number_spc_contacts(lvpwell_l+2*ncmp_ext, comp_cont_enc, cont_min_spc, cont_size)
    pcmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(lvpwell_pcmp_enc-pcmp2ncmp_spc-cmp_w+pcmp_con_free_spc_1 / 2, -ncmp_ext+pcmp_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_pcmp_con_1, num_pcmp_con_2)
    dnwpw_diode_cell.insert(pcmp_con_arr)

    # Inserting GR
    dnwpw_diode_cell.shapes(comp).insert(pya.Box(-lvpwell_gr_spc-cmp_w, -lvpwell_gr_spc-cmp_w, -lvpwell_gr_spc , lvpwell_l+lvpwell_gr_spc+cmp_w))                     #left
    dnwpw_diode_cell.shapes(pplus).insert(pya.Box(-lvpwell_gr_spc-cmp_w-implant_comp_enc, -lvpwell_gr_spc-cmp_w-implant_comp_enc, -lvpwell_gr_spc+implant_comp_enc , lvpwell_l+lvpwell_gr_spc+cmp_w+implant_comp_enc))

    dnwpw_diode_cell.shapes(comp).insert(pya.Box(lvpwell_w+lvpwell_gr_spc, -lvpwell_gr_spc-cmp_w, lvpwell_w+lvpwell_gr_spc+cmp_w , lvpwell_l+lvpwell_gr_spc+cmp_w))   #right
    dnwpw_diode_cell.shapes(pplus).insert(pya.Box(lvpwell_w+lvpwell_gr_spc-implant_comp_enc, -lvpwell_gr_spc-cmp_w-implant_comp_enc, lvpwell_w+lvpwell_gr_spc+cmp_w+implant_comp_enc , lvpwell_l+lvpwell_gr_spc+cmp_w+implant_comp_enc))

    dnwpw_diode_cell.shapes(comp).insert(pya.Box(-lvpwell_gr_spc , lvpwell_l+lvpwell_gr_spc , lvpwell_w+lvpwell_gr_spc , lvpwell_l+lvpwell_gr_spc+cmp_w))              #top
    dnwpw_diode_cell.shapes(pplus).insert(pya.Box(-lvpwell_gr_spc+implant_comp_enc , lvpwell_l+lvpwell_gr_spc-implant_comp_enc , lvpwell_w+lvpwell_gr_spc-implant_comp_enc , lvpwell_l+lvpwell_gr_spc+cmp_w+implant_comp_enc))

    dnwpw_diode_cell.shapes(comp).insert(pya.Box(-lvpwell_gr_spc , -lvpwell_gr_spc-cmp_w , lvpwell_w+lvpwell_gr_spc , -lvpwell_gr_spc))                                #bot
    dnwpw_diode_cell.shapes(pplus).insert(pya.Box(-lvpwell_gr_spc+implant_comp_enc , -lvpwell_gr_spc-cmp_w-implant_comp_enc , lvpwell_w+lvpwell_gr_spc-implant_comp_enc , -lvpwell_gr_spc+implant_comp_enc))

    # Inserting GR metal
    dnwpw_diode_cell.shapes(metal1).insert(pya.Box(-lvpwell_gr_spc-cmp_w, -lvpwell_gr_spc-cmp_w, -lvpwell_gr_spc , lvpwell_l+lvpwell_gr_spc+cmp_w))                    #left
    dnwpw_diode_cell.shapes(metal1).insert(pya.Box(lvpwell_w+lvpwell_gr_spc, -lvpwell_gr_spc-cmp_w, lvpwell_w+lvpwell_gr_spc+cmp_w , lvpwell_l+lvpwell_gr_spc+cmp_w))  #right
    dnwpw_diode_cell.shapes(metal1).insert(pya.Box(-lvpwell_gr_spc , lvpwell_l+lvpwell_gr_spc , lvpwell_w+lvpwell_gr_spc , lvpwell_l+lvpwell_gr_spc+cmp_w))            #top
    dnwpw_diode_cell.shapes(metal1).insert(pya.Box(-lvpwell_gr_spc , -lvpwell_gr_spc-cmp_w , lvpwell_w+lvpwell_gr_spc , -lvpwell_gr_spc))                              #bot

    # Inserting GR contacts
    num_gr_left_con_1, gr_left_con_free_spc_1 = number_spc_contacts(cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    num_gr_left_con_2, gr_left_con_free_spc_2 = number_spc_contacts(lvpwell_l+2*lvpwell_gr_spc+2*cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    gr_left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-lvpwell_gr_spc-cmp_w+gr_left_con_free_spc_1 / 2, -lvpwell_gr_spc-cmp_w+gr_left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_gr_left_con_1, num_gr_left_con_2)
    dnwpw_diode_cell.insert(gr_left_con_arr)

    num_gr_right_con_1, gr_right_con_free_spc_1 = number_spc_contacts(cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    num_gr_right_con_2, gr_right_con_free_spc_2 = number_spc_contacts(lvpwell_l+2*lvpwell_gr_spc+2*cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    gr_right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(lvpwell_w+lvpwell_gr_spc+gr_right_con_free_spc_1 / 2, -lvpwell_gr_spc-cmp_w+gr_right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_gr_right_con_1, num_gr_right_con_2)
    dnwpw_diode_cell.insert(gr_right_con_arr)

    num_gr_top_con_1, gr_top_con_free_spc_1 = number_spc_contacts(lvpwell_w+2*lvpwell_gr_spc-2*cont_spc_tol, comp_cont_enc, cont_min_spc, cont_size)
    num_gr_top_con_2, gr_top_con_free_spc_2 = number_spc_contacts(cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    gr_top_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-lvpwell_gr_spc+cont_spc_tol+gr_top_con_free_spc_1 / 2, lvpwell_l+lvpwell_gr_spc+gr_top_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_gr_top_con_1, num_gr_top_con_2)
    dnwpw_diode_cell.insert(gr_top_con_arr)

    num_gr_bot_con_1, gr_bot_con_free_spc_1 = number_spc_contacts(lvpwell_w+2*lvpwell_gr_spc-2*cont_spc_tol, comp_cont_enc, cont_min_spc, cont_size)
    num_gr_bot_con_2, gr_bot_con_free_spc_2 = number_spc_contacts(cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    gr_bot_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-lvpwell_gr_spc+cont_spc_tol+gr_bot_con_free_spc_1 / 2, -lvpwell_gr_spc-cmp_w+gr_bot_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_gr_bot_con_1, num_gr_bot_con_2)
    dnwpw_diode_cell.insert(gr_bot_con_arr)

    # Inserting marker
    dnwpw_diode_cell.shapes(well_diode_mk).insert(pya.Box(0, 0, lvpwell_w, lvpwell_l))

    if volt == "5/6V":
        # Inserting dualgate
        dnwpw_diode_cell.shapes(dualgate).insert(pya.Box(-dualgate_lvpwell_enc, -dualgate_lvpwell_enc, lvpwell_w+dualgate_lvpwell_enc, lvpwell_l+dualgate_lvpwell_enc))

    dnwpw_diode_cell.flatten(True)
    return dnwpw_diode_cell

def draw_dnwps_diode(layout, l, w , volt):
    '''
    Usage:-
     used to draw LVPWELL/DNWELL diode by specifying parameters
    Arguments:-
     layout     : Object of layout
     l          : Float of diff length
     w          : Float of diff width
     volt       : String of operating voltage of the diode [3.3V, 5V/6V]
    '''

    # Define layers
    lvpwell                 = layout.layer(204, 0 )
    dnwell                  = layout.layer(12 , 0 )
    comp                    = layout.layer(22 , 0 )
    nplus                   = layout.layer(32 , 0 )
    pplus                   = layout.layer(31 , 0 )
    nwell                   = layout.layer (21 , 0)
    contact                 = layout.layer(33 , 0 )
    metal1                  = layout.layer(34 , 0 )
    dualgate                = layout.layer(55 , 0 )
    well_diode_mk           = layout.layer(153, 51)

    # Define variables
    dbu_PERCISION           = 1/layout.dbu
    dnwell_w                = w    * dbu_PERCISION
    dnwell_l                = l    * dbu_PERCISION
    dnwell_pcmp_enc         = 0.62 * dbu_PERCISION
    cmp_w                   = 0.36 * dbu_PERCISION
    pcmp2ncmp_spc           = 0.32 * dbu_PERCISION
    implant_comp_enc        = 0.03 * dbu_PERCISION
    ncmp_ext                = 0.56 * dbu_PERCISION
    lvpwell_gr_spc          = 2.5  * dbu_PERCISION
    cont_spc_tol            = 0.11 * dbu_PERCISION
    comp_cont_enc           = 0.07 * dbu_PERCISION
    cont_size               = 0.22 * dbu_PERCISION
    cont_min_spc            = 0.25 * dbu_PERCISION
    dualgate_lvpwell_enc    = 0.5  * dbu_PERCISION

    if volt == "5/6V":
        dnwell_pcmp_enc     = 0.66 * dbu_PERCISION


    # Inserting dnwps cell
    cell_index       = layout.add_cell("dnwps_diode")
    dnwps_diode_cell = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell       = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting dnwell
    dnwps_diode_cell.shapes(dnwell).insert(pya.Box(0, 0, dnwell_w, dnwell_l))

    # Inserting n diffusion
    dnwps_diode_cell.shapes(comp).insert(pya.Box(dnwell_pcmp_enc, dnwell_pcmp_enc , dnwell_pcmp_enc+cmp_w, dnwell_l-dnwell_pcmp_enc))                                    # left
    dnwps_diode_cell.shapes(nplus).insert(pya.Box(dnwell_pcmp_enc-implant_comp_enc, dnwell_pcmp_enc-implant_comp_enc , dnwell_pcmp_enc+cmp_w+implant_comp_enc, dnwell_l-dnwell_pcmp_enc+implant_comp_enc))

    dnwps_diode_cell.shapes(comp).insert(pya.Box(dnwell_w-dnwell_pcmp_enc-cmp_w, dnwell_pcmp_enc , dnwell_w-dnwell_pcmp_enc , dnwell_l-dnwell_pcmp_enc))               # right
    dnwps_diode_cell.shapes(nplus).insert(pya.Box(dnwell_w-dnwell_pcmp_enc-cmp_w-implant_comp_enc, dnwell_pcmp_enc-implant_comp_enc , dnwell_w-dnwell_pcmp_enc+implant_comp_enc , dnwell_l-dnwell_pcmp_enc+implant_comp_enc))

    dnwps_diode_cell.shapes(comp).insert(pya.Box(dnwell_pcmp_enc+cmp_w, dnwell_l-dnwell_pcmp_enc-cmp_w , dnwell_w-dnwell_pcmp_enc-cmp_w , dnwell_l-dnwell_pcmp_enc))   # top
    dnwps_diode_cell.shapes(nplus).insert(pya.Box(dnwell_pcmp_enc+cmp_w+implant_comp_enc, dnwell_l-dnwell_pcmp_enc-cmp_w-implant_comp_enc , dnwell_w-dnwell_pcmp_enc-cmp_w-implant_comp_enc , dnwell_l-dnwell_pcmp_enc+implant_comp_enc)) # top

    dnwps_diode_cell.shapes(comp).insert(pya.Box(dnwell_pcmp_enc+cmp_w, dnwell_pcmp_enc , dnwell_w-dnwell_pcmp_enc-cmp_w , dnwell_pcmp_enc+cmp_w))                       # bottom
    dnwps_diode_cell.shapes(nplus).insert(pya.Box(dnwell_pcmp_enc+cmp_w+implant_comp_enc, dnwell_pcmp_enc-implant_comp_enc , dnwell_w-dnwell_pcmp_enc-cmp_w-implant_comp_enc, dnwell_pcmp_enc+cmp_w+implant_comp_enc)) # bottom

    # Inserting ncomp metal
    dnwps_diode_cell.shapes(metal1).insert(pya.Box(dnwell_pcmp_enc, dnwell_pcmp_enc , dnwell_pcmp_enc+cmp_w, dnwell_l-dnwell_pcmp_enc))                                  # left
    dnwps_diode_cell.shapes(metal1).insert(pya.Box(dnwell_w-dnwell_pcmp_enc-cmp_w, dnwell_pcmp_enc , dnwell_w-dnwell_pcmp_enc , dnwell_l-dnwell_pcmp_enc))             # right
    dnwps_diode_cell.shapes(metal1).insert(pya.Box(dnwell_pcmp_enc+cmp_w, dnwell_l-dnwell_pcmp_enc-cmp_w , dnwell_w-dnwell_pcmp_enc-cmp_w , dnwell_l-dnwell_pcmp_enc)) # top
    dnwps_diode_cell.shapes(metal1).insert(pya.Box(dnwell_pcmp_enc+cmp_w, dnwell_pcmp_enc , dnwell_w-dnwell_pcmp_enc-cmp_w , dnwell_pcmp_enc+cmp_w))                     # bottom

    # Inserting ncomp contacts
    num_pcmp_left_con_1, pcmp_left_con_free_spc_1 = number_spc_contacts(cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    num_pcmp_left_con_2, pcmp_left_con_free_spc_2 = number_spc_contacts(dnwell_l-2*dnwell_pcmp_enc, comp_cont_enc, cont_min_spc, cont_size)
    pcmp_left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(dnwell_pcmp_enc+pcmp_left_con_free_spc_1 / 2, dnwell_pcmp_enc+pcmp_left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_pcmp_left_con_1, num_pcmp_left_con_2)
    dnwps_diode_cell.insert(pcmp_left_con_arr)

    num_cmp_right_con_1, cmp_right_con_free_spc_1 = number_spc_contacts(cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    num_cmp_right_con_2, cmp_right_con_free_spc_2 = number_spc_contacts(dnwell_l-2*dnwell_pcmp_enc, comp_cont_enc, cont_min_spc, cont_size)
    cmp_right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(dnwell_w-dnwell_pcmp_enc-cmp_w+cmp_right_con_free_spc_1 / 2, dnwell_pcmp_enc+cmp_right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_cmp_right_con_1, num_cmp_right_con_2)
    dnwps_diode_cell.insert(cmp_right_con_arr)

    num_cmp_top_con_1, cmp_top_con_free_spc_1 = number_spc_contacts(dnwell_w-2*dnwell_pcmp_enc-2*cmp_w-2*cont_spc_tol, comp_cont_enc, cont_min_spc, cont_size)
    num_cmp_top_con_2, cmp_top_con_free_spc_2 = number_spc_contacts(cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    cmp_top_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(dnwell_pcmp_enc+cmp_w+cont_spc_tol+cmp_top_con_free_spc_1 / 2, dnwell_l-dnwell_pcmp_enc-cmp_w+cmp_top_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_cmp_top_con_1, num_cmp_top_con_2)
    dnwps_diode_cell.insert(cmp_top_con_arr)

    num_cmp_bot_con_1, cmp_bot_con_free_spc_1 = number_spc_contacts(dnwell_w-2*dnwell_pcmp_enc-2*cmp_w-2*cont_spc_tol, comp_cont_enc, cont_min_spc, cont_size)
    num_cmp_bot_con_2, cmp_bot_con_free_spc_2 = number_spc_contacts(cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    cmp_bot_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(dnwell_pcmp_enc+cmp_w+cont_spc_tol+cmp_bot_con_free_spc_1 / 2, dnwell_pcmp_enc+cmp_bot_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_cmp_bot_con_1, num_cmp_bot_con_2)
    dnwps_diode_cell.insert(cmp_bot_con_arr)

    # Inserting GR
    dnwps_diode_cell.shapes(comp).insert(pya.Box(-lvpwell_gr_spc-cmp_w, -lvpwell_gr_spc-cmp_w, -lvpwell_gr_spc , dnwell_l+lvpwell_gr_spc+cmp_w))                     #left
    dnwps_diode_cell.shapes(pplus).insert(pya.Box(-lvpwell_gr_spc-cmp_w-implant_comp_enc, -lvpwell_gr_spc-cmp_w-implant_comp_enc, -lvpwell_gr_spc+implant_comp_enc , dnwell_l+lvpwell_gr_spc+cmp_w+implant_comp_enc))

    dnwps_diode_cell.shapes(comp).insert(pya.Box(dnwell_w+lvpwell_gr_spc, -lvpwell_gr_spc-cmp_w, dnwell_w+lvpwell_gr_spc+cmp_w , dnwell_l+lvpwell_gr_spc+cmp_w))   #right
    dnwps_diode_cell.shapes(pplus).insert(pya.Box(dnwell_w+lvpwell_gr_spc-implant_comp_enc, -lvpwell_gr_spc-cmp_w-implant_comp_enc, dnwell_w+lvpwell_gr_spc+cmp_w+implant_comp_enc , dnwell_l+lvpwell_gr_spc+cmp_w+implant_comp_enc))

    dnwps_diode_cell.shapes(comp).insert(pya.Box(-lvpwell_gr_spc , dnwell_l+lvpwell_gr_spc , dnwell_w+lvpwell_gr_spc , dnwell_l+lvpwell_gr_spc+cmp_w))              #top
    dnwps_diode_cell.shapes(pplus).insert(pya.Box(-lvpwell_gr_spc+implant_comp_enc , dnwell_l+lvpwell_gr_spc-implant_comp_enc , dnwell_w+lvpwell_gr_spc-implant_comp_enc , dnwell_l+lvpwell_gr_spc+cmp_w+implant_comp_enc))

    dnwps_diode_cell.shapes(comp).insert(pya.Box(-lvpwell_gr_spc , -lvpwell_gr_spc-cmp_w , dnwell_w+lvpwell_gr_spc , -lvpwell_gr_spc))                                #bot
    dnwps_diode_cell.shapes(pplus).insert(pya.Box(-lvpwell_gr_spc+implant_comp_enc , -lvpwell_gr_spc-cmp_w-implant_comp_enc , dnwell_w+lvpwell_gr_spc-implant_comp_enc , -lvpwell_gr_spc+implant_comp_enc))

    # Inserting GR metal
    dnwps_diode_cell.shapes(metal1).insert(pya.Box(-lvpwell_gr_spc-cmp_w, -lvpwell_gr_spc-cmp_w, -lvpwell_gr_spc , dnwell_l+lvpwell_gr_spc+cmp_w))                    #left
    dnwps_diode_cell.shapes(metal1).insert(pya.Box(dnwell_w+lvpwell_gr_spc, -lvpwell_gr_spc-cmp_w, dnwell_w+lvpwell_gr_spc+cmp_w , dnwell_l+lvpwell_gr_spc+cmp_w))  #right
    dnwps_diode_cell.shapes(metal1).insert(pya.Box(-lvpwell_gr_spc , dnwell_l+lvpwell_gr_spc , dnwell_w+lvpwell_gr_spc , dnwell_l+lvpwell_gr_spc+cmp_w))            #top
    dnwps_diode_cell.shapes(metal1).insert(pya.Box(-lvpwell_gr_spc , -lvpwell_gr_spc-cmp_w , dnwell_w+lvpwell_gr_spc , -lvpwell_gr_spc))                              #bot

    # Inserting GR contacts
    num_gr_left_con_1, gr_left_con_free_spc_1 = number_spc_contacts(cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    num_gr_left_con_2, gr_left_con_free_spc_2 = number_spc_contacts(dnwell_l+2*lvpwell_gr_spc+2*cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    gr_left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-lvpwell_gr_spc-cmp_w+gr_left_con_free_spc_1 / 2, -lvpwell_gr_spc-cmp_w+gr_left_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_gr_left_con_1, num_gr_left_con_2)
    dnwps_diode_cell.insert(gr_left_con_arr)

    num_gr_right_con_1, gr_right_con_free_spc_1 = number_spc_contacts(cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    num_gr_right_con_2, gr_right_con_free_spc_2 = number_spc_contacts(dnwell_l+2*lvpwell_gr_spc+2*cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    gr_right_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(dnwell_w+lvpwell_gr_spc+gr_right_con_free_spc_1 / 2, -lvpwell_gr_spc-cmp_w+gr_right_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_gr_right_con_1, num_gr_right_con_2)
    dnwps_diode_cell.insert(gr_right_con_arr)

    num_gr_top_con_1, gr_top_con_free_spc_1 = number_spc_contacts(dnwell_w+2*lvpwell_gr_spc-2*cont_spc_tol, comp_cont_enc, cont_min_spc, cont_size)
    num_gr_top_con_2, gr_top_con_free_spc_2 = number_spc_contacts(cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    gr_top_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-lvpwell_gr_spc+cont_spc_tol+gr_top_con_free_spc_1 / 2, dnwell_l+lvpwell_gr_spc+gr_top_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_gr_top_con_1, num_gr_top_con_2)
    dnwps_diode_cell.insert(gr_top_con_arr)

    num_gr_bot_con_1, gr_bot_con_free_spc_1 = number_spc_contacts(dnwell_w+2*lvpwell_gr_spc-2*cont_spc_tol, comp_cont_enc, cont_min_spc, cont_size)
    num_gr_bot_con_2, gr_bot_con_free_spc_2 = number_spc_contacts(cmp_w, comp_cont_enc, cont_min_spc, cont_size)
    gr_bot_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(-lvpwell_gr_spc+cont_spc_tol+gr_bot_con_free_spc_1 / 2, -lvpwell_gr_spc-cmp_w+gr_bot_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_gr_bot_con_1, num_gr_bot_con_2)
    dnwps_diode_cell.insert(gr_bot_con_arr)

    # Inserting marker
    dnwps_diode_cell.shapes(well_diode_mk).insert(pya.Box(0, 0, dnwell_w, dnwell_l))

    if volt == "5/6V":
        # Inserting dualgate
        dnwps_diode_cell.shapes(dualgate).insert(pya.Box(-dualgate_lvpwell_enc, -dualgate_lvpwell_enc, dnwell_w+dualgate_lvpwell_enc, dnwell_l+dualgate_lvpwell_enc))

    dnwps_diode_cell.flatten(True)
    return dnwps_diode_cell

def draw_sc_diode(layout, l, w , m, pcmpgr):
    '''
    Usage:-
     used to draw N+/LVPWELL diode (Outside DNWELL) by specifying parameters
    Arguments:-
     layout     : Object of layout
     l          : Float of diff length
     w          : Float of diff width
     m          : Integer of number of fingers
     pcmpgr     : Boolean of using P+ Guard Ring for Deep NWELL devices only
    '''

    # Define layers
    comp                = layout.layer(22 , 0 )
    nplus               = layout.layer(32 , 0 )
    dnwell              = layout.layer(12 , 0 )
    pplus               = layout.layer(31 , 0 )
    contact             = layout.layer(33 , 0 )
    metal1              = layout.layer(34 , 0 )
    sc_diode_mk         = layout.layer(241, 0 )

    # Define variables
    dbu_PERCISION       = 1/layout.dbu
    ncmp_metcmp_spc     = 0.28 * dbu_PERCISION
    ncmp_w              = 0.36 * dbu_PERCISION
    sc_w                = w    * dbu_PERCISION
    sc_l                = l    * dbu_PERCISION
    implant_comp_enc    = 0.03 * dbu_PERCISION
    comp_cont_enc       = 0.07 * dbu_PERCISION
    cont_size           = 0.22 * dbu_PERCISION
    cont_min_spc        = 0.25 * dbu_PERCISION

    metcmp_min_spc      = 0.92 * dbu_PERCISION
    met_cmp_enc_in      = 0.23 * dbu_PERCISION
    met_ncmp_enc        = 0.46 * dbu_PERCISION
    dnwell_cmp_enc_x    = 0.76 * dbu_PERCISION
    dnwell_cmp_enc_y    = 1.4  * dbu_PERCISION
    sc_mk_cmp_enc       = 0.16 * dbu_PERCISION
    met_conn_w          = 0.23 * dbu_PERCISION
    pcmp_gr2dnw         = 2.5  * dbu_PERCISION

    ncmp_min_spc        = 2*ncmp_metcmp_spc + sc_w
    cmp_total_w         = (m+1)*ncmp_w + m*ncmp_min_spc

    # Inserting np cell
    cell_index      = layout.add_cell("sc_diode")
    sc_diode_cell   = layout.cell(cell_index)

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell       = layout.cell(cont_cell_index)
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Inserting ncomp sc finger cell
    ncmp_cell_index = layout.add_cell("ncomp")
    ncmp_cell       = layout.cell(ncmp_cell_index)
    ncmp_cell.shapes(comp).insert(pya.Box.new(0, 0, ncmp_w, sc_l))
    ncmp_cell.shapes(nplus).insert(pya.Box.new(-implant_comp_enc, -implant_comp_enc, ncmp_w+implant_comp_enc, sc_l+implant_comp_enc))
    ncmp_cell.shapes(metal1).insert(pya.Box.new(0 , -met_cmp_enc_in, ncmp_w, sc_l))
    ## Inserting pcomp contacts
    num_ncmp_con_1, ncmp_con_free_spc_1 = number_spc_contacts(ncmp_w, comp_cont_enc, cont_min_spc, cont_size)
    num_ncmp_con_2, ncmp_con_free_spc_2 = number_spc_contacts(sc_l, comp_cont_enc, cont_min_spc, cont_size)
    ncmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(ncmp_con_free_spc_1 / 2, ncmp_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_ncmp_con_1, num_ncmp_con_2)
    ncmp_cell.insert(ncmp_con_arr)

    # Inserting comp_metal sc finger cell
    met_cmp_cell_index  = layout.add_cell("comp_metal")
    met_cmp_cell        = layout.cell(met_cmp_cell_index)
    met_cmp_cell.shapes(comp).insert(pya.Box.new(0, 0, sc_w, sc_l))

    if m > 1:
        met_cmp_cell.shapes(metal1).insert(pya.Box.new(0, 0, sc_w, sc_l+met_cmp_enc_in))
    else:
        met_cmp_cell.shapes(metal1).insert(pya.Box.new(0, 0, sc_w, sc_l))

    ## Inserting comp_metal contacts
    num_met_cmp_con_1, met_cmp_con_free_spc_1 = number_spc_contacts(sc_w, comp_cont_enc, cont_min_spc, cont_size)
    num_met_cmp_con_2, met_cmp_con_free_spc_2 = number_spc_contacts(sc_l, comp_cont_enc, cont_min_spc, cont_size)
    met_cmp_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(met_cmp_con_free_spc_1 / 2, met_cmp_con_free_spc_2/2)),
        pya.Vector(cont_min_spc + cont_size, 0), pya.Vector(0,cont_min_spc + cont_size),
        num_met_cmp_con_1, num_met_cmp_con_2)
    met_cmp_cell.insert(met_cmp_con_arr)

    # Inserting ncomp fingers
    ncmp_arr = pya.CellInstArray(ncmp_cell.cell_index(), pya.Trans(
        pya.Point(0, 0)),
        pya.Vector(ncmp_min_spc + ncmp_w, 0), pya.Vector(0,ncmp_min_spc + ncmp_w),
        m+1, 1)
    sc_diode_cell.insert(ncmp_arr)

    # Inserting metal comp fingers
    metcmp_arr = pya.CellInstArray(met_cmp_cell.cell_index(), pya.Trans(
        pya.Point(ncmp_w+ncmp_metcmp_spc, 0)),
        pya.Vector(metcmp_min_spc + sc_w, 0), pya.Vector(0,metcmp_min_spc + sc_w),
        m, 1)
    sc_diode_cell.insert(metcmp_arr)

    # Inserting Deep NWELL
    sc_diode_cell.shapes(dnwell).insert(pya.Box(-dnwell_cmp_enc_x, -dnwell_cmp_enc_y, cmp_total_w+dnwell_cmp_enc_x, sc_l+dnwell_cmp_enc_y))

    # Inserting Deep NWELL P+ Guard Ring
    if pcmpgr == True:
        cmp_inner   = pya.Box(-dnwell_cmp_enc_x-pcmp_gr2dnw, -dnwell_cmp_enc_y-pcmp_gr2dnw, cmp_total_w+dnwell_cmp_enc_x+pcmp_gr2dnw, sc_l+dnwell_cmp_enc_y+pcmp_gr2dnw)
        cmp_outer   = pya.Box(-dnwell_cmp_enc_x-ncmp_w-pcmp_gr2dnw, -dnwell_cmp_enc_y-ncmp_w-pcmp_gr2dnw, cmp_total_w+dnwell_cmp_enc_x+ncmp_w+pcmp_gr2dnw, sc_l+dnwell_cmp_enc_y+ncmp_w+pcmp_gr2dnw)
        cmp_gr      = pya.Region(cmp_outer) - pya.Region(cmp_inner)
        sc_diode_cell.shapes(comp).insert(cmp_gr)

        pp_inner    = pya.Box(-dnwell_cmp_enc_x+implant_comp_enc-pcmp_gr2dnw, -dnwell_cmp_enc_y+implant_comp_enc-pcmp_gr2dnw, cmp_total_w+dnwell_cmp_enc_x-implant_comp_enc+pcmp_gr2dnw, sc_l+dnwell_cmp_enc_y-implant_comp_enc+pcmp_gr2dnw)
        pp_outer    = pya.Box(-dnwell_cmp_enc_x-ncmp_w-implant_comp_enc-pcmp_gr2dnw, -dnwell_cmp_enc_y-ncmp_w-implant_comp_enc-pcmp_gr2dnw, cmp_total_w+dnwell_cmp_enc_x+ncmp_w+implant_comp_enc+pcmp_gr2dnw, sc_l+dnwell_cmp_enc_y+ncmp_w+implant_comp_enc+pcmp_gr2dnw)
        pp_gr       = pya.Region(pp_outer) - pya.Region(pp_inner)
        sc_diode_cell.shapes(pplus).insert(pp_gr)

    # Inserting sc_marker
    sc_diode_cell.shapes(sc_diode_mk).insert(pya.Box(-sc_mk_cmp_enc, -sc_mk_cmp_enc, cmp_total_w+sc_mk_cmp_enc, sc_l+sc_mk_cmp_enc))

    # Inserting connection metal  [bottom]
    sc_diode_cell.shapes(metal1).insert(pya.Box(0, -met_ncmp_enc, cmp_total_w, -met_ncmp_enc+met_conn_w))

    # Inserting connection metal  [Top]
    if m > 1:
        sc_diode_cell.shapes(metal1).insert(pya.Box(ncmp_w+ncmp_metcmp_spc, sc_l+met_ncmp_enc-met_conn_w, cmp_total_w-ncmp_w-ncmp_metcmp_spc, sc_l+met_ncmp_enc))

    sc_diode_cell.flatten(True)
    return sc_diode_cell
