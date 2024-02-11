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
## MIM Capacitor Pcells Generators for Klayout of GF180MCU
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

def draw_mimcap(layout, l, w , mim_option , metal_level):
    '''
    Usage:-
     used to draw 1.0fF/um2 MIM capacitor by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of diff length
     w      : Float of diff width
    '''

    # Define layers
    metal2         = layout.layer(36 , 0 )
    metal3         = layout.layer(42 , 0 )
    metal4         = layout.layer(46 , 0 )
    metal5         = layout.layer(81 , 0 )
    metaltop       = layout.layer(53 , 0 )
    via2           = layout.layer(38 , 0 )
    via3           = layout.layer(40 , 0 )
    via4           = layout.layer(41 , 0 )
    via5           = layout.layer(82 , 0 )
    fusetop        = layout.layer(75 , 0 )
    cap_mk         = layout.layer(117, 5 )
    mim_l_mk       = layout.layer(117, 10)

    # MIM Option selection
    if mim_option == "MIM-A":
        topmet = metal3
        botmet = metal2
        topvia = via2

    elif mim_option == "MIM-B":
        if metal_level == "M4":
            topmet = metal4
            botmet = metal3
            topvia = via3
        elif metal_level == "M5":
            topmet = metal5
            botmet = metal4
            topvia = via4
        elif metal_level == "M6":
            topmet = metaltop
            botmet = metal5
            topvia = via5
    else:
        topmet = metal3
        botmet = metal2
        topvia = via2

    # VARIABLES
    dbu_PERCISION         = 1/layout.dbu
    topmet_w              = w    * dbu_PERCISION
    topmet_l              = l    * dbu_PERCISION
    top_bot_enc           = 0.6  * dbu_PERCISION
    mim_l_mk_width        = 0.1  * dbu_PERCISION
    via_size              = 0.26 * dbu_PERCISION
    via_min_spc           = 0.5  * dbu_PERCISION
    met_via_enc           = 0.4  * dbu_PERCISION

    # Inserting nmoscap cell
    cell_index  = layout.add_cell("mimcap")
    mimcap_cell = layout.cell(cell_index)

    # Inserting a via cell
    cont_cell_index = layout.add_cell("topvia")
    cont_cell = layout.cell(cont_cell_index)
    cont_cell.shapes(topvia).insert(pya.Box.new(0, 0, via_size, via_size))

    # Inserting top_metal
    mimcap_cell.shapes(topmet).insert(pya.Box(0, 0, topmet_w, topmet_l))

    # Inserting fusetop
    mimcap_cell.shapes(fusetop).insert(pya.Box(0, 0, topmet_w, topmet_l))

    # Inserting bot_metal
    mimcap_cell.shapes(botmet).insert(pya.Box(-top_bot_enc, -top_bot_enc,  topmet_w+top_bot_enc, topmet_l+top_bot_enc))

    # Inserting bottom metal vias
    num_left_con_1, left_con_free_spc_1 = number_spc_contacts(topmet_w, met_via_enc, via_min_spc, via_size)
    num_left_con_2, left_con_free_spc_2 = number_spc_contacts(topmet_l, met_via_enc, via_min_spc, via_size)
    left_con_arr = pya.CellInstArray(cont_cell.cell_index(), pya.Trans(
        pya.Point(left_con_free_spc_1 / 2, left_con_free_spc_2/2)),
        pya.Vector(via_min_spc + via_size, 0), pya.Vector(0,via_min_spc + via_size),
        num_left_con_1, num_left_con_2)
    mimcap_cell.insert(left_con_arr)

    # Inserting mim_l_mk
    mimcap_cell.shapes(mim_l_mk).insert(pya.Box(0, 0,topmet_w, mim_l_mk_width))

    # Inserting marker
    mimcap_cell.shapes(cap_mk).insert(pya.Box(-top_bot_enc, -top_bot_enc,  topmet_w+top_bot_enc, topmet_l+top_bot_enc))

    mimcap_cell.flatten(True)
    return mimcap_cell
