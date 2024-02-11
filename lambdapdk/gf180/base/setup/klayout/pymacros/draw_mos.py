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
## MOSFET Pcells Generators for Klayout of GF180MCU
########################################################################################################################

import pya

tol = 1.05

def draw_nmos(layout, l, w, ld, nf, grw, bulk, volt, deepnwell, pcmpgr):
    '''
    Usage:-
     used to draw NMOS transistor by specifying parameters
    Arguments:-
     layout     : Object of layout
     l          : Float of gate length
     w          : Float of gate width
     ld         : Float of diffusion length
     nf         : Integer of number of fingers
     grw        : Float of guard ring width [If enabled]
     bulk       : String of bulk connection type [None, Bulk Tie, Guard Ring]
     volt       : String of operating voltage of the MOSFET [3.3V, 5V, 6V]
     deepnwell  : Boolean of using Deep NWELL device
     pcmpgr     : Boolean of using P+ Guard Ring for Deep NWELL devices only
    '''

    # Define layers
    dnwell                  = layout.layer(12 , 0 )
    lvpwell                 = layout.layer(204, 0 )
    dualgate                = layout.layer(55 , 0 )
    v5_xtor                 = layout.layer(112, 1 )
    comp                    = layout.layer(22 , 0 )
    poly2                   = layout.layer(30 , 0 )
    nplus                   = layout.layer(32 , 0 )
    pplus                   = layout.layer(31 , 0 )
    contact                 = layout.layer(33 , 0 )
    metal1                  = layout.layer(34 , 0 )

    # Define variables
    dbu_PERCISION           = 1/layout.dbu
    nf                      = int(nf)
    grw                     = grw       * dbu_PERCISION
    ld                      = ld        * dbu_PERCISION
    l                       = l         * dbu_PERCISION
    w                       = w         * dbu_PERCISION
    cmp2cont                = 0.07      * dbu_PERCISION
    cont_size               = 0.22      * dbu_PERCISION
    np_enc_cmp              = 0.16      * dbu_PERCISION
    pp_enc_cmp              = 0.16      * dbu_PERCISION
    cont2ply                = 0.15      * dbu_PERCISION
    ply_ext_cmp             = 0.22      * dbu_PERCISION
    np_enc_gate             = 0.23      * dbu_PERCISION
    cont2cont               = 0.28      * dbu_PERCISION
    dg_enc_ply              = 0.4       * dbu_PERCISION
    dg_enc_cmp              = 0.24      * dbu_PERCISION
    cmp2cmp                 = 0.28      * dbu_PERCISION
    ply2gr                  = 0.1       * dbu_PERCISION
    ld_violat               = 0         * dbu_PERCISION
    tie_violat              = 0         * dbu_PERCISION
    metal_violat            = 0.01      * dbu_PERCISION
    min_cmp_area            = 0.2025    * dbu_PERCISION * dbu_PERCISION
    dg_enc_dnwell           = 0.5       * dbu_PERCISION
    lvpwell_enc_ncmp        = 0.43      * dbu_PERCISION
    lvpwell_enc_pcmp        = 0.12      * dbu_PERCISION
    dnwell_enc_lvpwell      = 2.5       * dbu_PERCISION
    pcmp_gr2dnw             = 2.5       * dbu_PERCISION
    gr_w                    = 0.36      * dbu_PERCISION

    if deepnwell == True:
        cmp2cmp             = 0.36      * dbu_PERCISION
        ply2gr              = 0.3       * dbu_PERCISION

    if volt == "5V" or volt == "6V":
        lvpwell_enc_ncmp    = 0.6       * dbu_PERCISION
        lvpwell_enc_pcmp    = 0.16      * dbu_PERCISION
        cmp2cmp             = 0.36      * dbu_PERCISION
        ply2gr              = 0.3       * dbu_PERCISION
        cmp2cmp             = 0.36      * dbu_PERCISION

    if w < cont_size+2*cmp2cont:
        if nf == 1:
            if volt == "5V" or volt == "6V":
                ld_violat   = 0.22      * dbu_PERCISION
            else:
                ld_violat   = 0.02      * dbu_PERCISION

    # Inserting NMOS cell
    cell_index  = layout.add_cell("nmos")
    cell        = layout.cell(cell_index)

    w_changed = False

    # Inserting diffusion
    if w < cont_size+2*cmp2cont:
        cell.shapes(comp).insert(pya.Box(0, (cont_size+2*cmp2cont - w)/2, (2 * (ld + ld_violat) + l + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)), w + (cont_size+2*cmp2cont - w)/2))
        w = cont_size+2*cmp2cont
        w_changed = True
    else:
        cell.shapes(comp).insert(pya.Box(0, 0, (2 * ld + l + (nf - 1) * (ld + l + cont2ply - cmp2cont)), w))

    cell.shapes(nplus).insert(pya.Box(-np_enc_cmp, -np_enc_gate, (2 * (ld + ld_violat) + l + np_enc_cmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)), w + np_enc_gate))

    # Inserting gate/s
    # Inserting a gate cell
    gate_cell_index = layout.add_cell("gate")
    gate_cell = layout.cell(gate_cell_index)
    gate_cell.shapes(poly2).insert(pya.Box(ld + ld_violat, -ply_ext_cmp, (ld + ld_violat + l), (w + ply_ext_cmp)))

    # adding gate array
    cell.insert(pya.CellInstArray.new(gate_cell_index, pya.Trans.new(pya.Point.new(0, 0)),
            pya.Point.new(ld + ld_violat + l + cont2ply - cmp2cont, 0), pya.Point.new(0, 0), int(nf), 1))


    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell       = layout.cell(cont_cell_index)

    # Inserting shapes now into the *contact* cell
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Contact array count and postions
    nx = int((ld - (cont_size+cmp2cont+cont2ply))/(cont2cont+cont_size)) + 1
    ny = int((w - (cont_size+2*cmp2cont))/(cont2cont+cont_size)) + 1
    dx = (ld - nx * cont_size - (nx - 1) * cont2cont)*cmp2cont/cont_size
    dy = (w - ny * cont_size - (ny - 1) * cont2cont)/2

    # adding contact array and metals
    # Left contacts
    if not (w_changed == True and nf > 1) and (ld >= 440):
        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(dx, dy)),
                pya.Point.new((cont2cont+cont_size), 0), pya.Point.new(0, (cont2cont+cont_size)), nx, ny))
        # Left metal
        cell.shapes(metal1).insert(pya.Box(-metal_violat, -metal_violat, ld + metal_violat - (cont_size-2*cmp2cont), w + metal_violat))

    # Adding diffusion to avoid contact violation
    if nf == 1 and w_changed == True:
        cell.shapes(comp).insert(pya.Box(0, 0, ld - (cont_size-2*cmp2cont), w))

    # Right contacts and metals for each finger
    for i in range(nf):
        # Contacts
        if not (w_changed == True and nf > 1) and (ld >= 440):
            cell.insert(pya.CellInstArray.new(cont_cell_index,
                pya.Trans.new(pya.Point.new(((l + ld + ld_violat + cont2ply - cmp2cont) * i + 2 * (ld + ld_violat) + l - cont_size - dx), dy)),
                pya.Point.new(-(cont2cont+cont_size), 0), pya.Point.new(0, (cont2cont+cont_size)), nx, ny))
            # Metals
            cell.shapes(metal1).insert(pya.Box((ld + 2 * ld_violat + l + cont2ply - cmp2cont)*(i + 1), - metal_violat,
             ld + metal_violat + ld_violat + (ld + ld_violat + l + cont2ply - cmp2cont)*(i + 1) - (cont_size-2*cmp2cont), w + metal_violat))

    # Adding diffusion to avoid contact violation
    if nf == 1 and w_changed == True:
            cell.shapes(comp).insert(pya.Box((ld + 2 * ld_violat + l + cont2ply - cmp2cont)*(i + 1), 0, ld + ld_violat + (ld + ld_violat + l + cont2ply - cmp2cont)*(i + 1) - (cont_size-2*cmp2cont), w))
            region = pya.Region.new(cell.begin_shapes_rec(comp))
            region.merge()
            cell.clear(comp)
            cell.shapes(comp).insert(region)

    if bulk == "Bulk Tie":
        if deepnwell == True:
            if volt == "5V":
                # Inserting 5V layers
                cell.shapes(v5_xtor).insert(pya.Box(-dg_enc_dnwell-dnwell_enc_lvpwell-lvpwell_enc_pcmp-cmp2cmp-ld,
                 -dg_enc_dnwell-dnwell_enc_lvpwell-lvpwell_enc_ncmp,
                (2 * (ld + ld_violat) + l + dg_enc_dnwell + dnwell_enc_lvpwell + lvpwell_enc_ncmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                 w + lvpwell_enc_ncmp + dnwell_enc_lvpwell + dg_enc_dnwell))

                cell.shapes(dualgate).insert(pya.Box(-dg_enc_dnwell-dnwell_enc_lvpwell-lvpwell_enc_pcmp-cmp2cmp-ld,
                 -dg_enc_dnwell-dnwell_enc_lvpwell-lvpwell_enc_ncmp,
                (2 * (ld + ld_violat) + l + dg_enc_dnwell + dnwell_enc_lvpwell + lvpwell_enc_ncmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                 w + lvpwell_enc_ncmp + dnwell_enc_lvpwell + dg_enc_dnwell))

            elif volt == "6V":
                # Inserting 6V layers
                cell.shapes(dualgate).insert(pya.Box(-dg_enc_dnwell-dnwell_enc_lvpwell-lvpwell_enc_pcmp-cmp2cmp-ld,
                 -dg_enc_dnwell-dnwell_enc_lvpwell-lvpwell_enc_ncmp,
                (2 * (ld + ld_violat) + l + dg_enc_dnwell + dnwell_enc_lvpwell + lvpwell_enc_ncmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                 w + lvpwell_enc_ncmp + dnwell_enc_lvpwell + dg_enc_dnwell))

            # Inserting LVPWELL
            cell.shapes(lvpwell).insert(pya.Box(-lvpwell_enc_pcmp-cmp2cmp-ld, -lvpwell_enc_ncmp,
            (2 * (ld + ld_violat) + l + lvpwell_enc_ncmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
             w + lvpwell_enc_ncmp))

            # Inserting DNWELL
            cell.shapes(dnwell).insert(pya.Box(-dnwell_enc_lvpwell-lvpwell_enc_pcmp-cmp2cmp-ld, -dnwell_enc_lvpwell-lvpwell_enc_ncmp,
            (2 * (ld + ld_violat) + l + dnwell_enc_lvpwell + lvpwell_enc_ncmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
             w + lvpwell_enc_ncmp + dnwell_enc_lvpwell))

            # Inserting Double Guard Ring
            if pcmpgr == True:
                cmp_inner = pya.Box(-dnwell_enc_lvpwell-lvpwell_enc_pcmp-cmp2cmp-ld-pcmp_gr2dnw, -dnwell_enc_lvpwell-lvpwell_enc_ncmp-pcmp_gr2dnw,
                    (2 * (ld + ld_violat) + l + dnwell_enc_lvpwell + lvpwell_enc_ncmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont))+pcmp_gr2dnw,
                     w + lvpwell_enc_ncmp + dnwell_enc_lvpwell+pcmp_gr2dnw)
                cmp_outer = pya.Box(-dnwell_enc_lvpwell-lvpwell_enc_pcmp-cmp2cmp-ld-pcmp_gr2dnw-gr_w, -dnwell_enc_lvpwell-lvpwell_enc_ncmp-pcmp_gr2dnw-gr_w,
                    (2 * (ld + ld_violat) + l + dnwell_enc_lvpwell + lvpwell_enc_ncmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont))+pcmp_gr2dnw+gr_w,
                     w + lvpwell_enc_ncmp + dnwell_enc_lvpwell+pcmp_gr2dnw+gr_w)
                cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
                cell.shapes(comp).insert(cmp_gr)

                pp_inner = pya.Box(-dnwell_enc_lvpwell-lvpwell_enc_pcmp-cmp2cmp-ld-pcmp_gr2dnw+pp_enc_cmp, -dnwell_enc_lvpwell-lvpwell_enc_ncmp-pcmp_gr2dnw+pp_enc_cmp,
                    (2 * (ld + ld_violat) + l + dnwell_enc_lvpwell + lvpwell_enc_ncmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont))+pcmp_gr2dnw-pp_enc_cmp,
                     w + lvpwell_enc_ncmp + dnwell_enc_lvpwell+pcmp_gr2dnw-pp_enc_cmp)
                pp_outer = pya.Box(-dnwell_enc_lvpwell-lvpwell_enc_pcmp-cmp2cmp-ld-pcmp_gr2dnw-gr_w-pp_enc_cmp, -dnwell_enc_lvpwell-lvpwell_enc_ncmp-pcmp_gr2dnw-gr_w-pp_enc_cmp,
                    (2 * (ld + ld_violat) + l + dnwell_enc_lvpwell + lvpwell_enc_ncmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont))+pcmp_gr2dnw+gr_w+pp_enc_cmp,
                     w + lvpwell_enc_ncmp + dnwell_enc_lvpwell+pcmp_gr2dnw+gr_w+pp_enc_cmp)
                pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
                cell.shapes(pplus).insert(pp_gr)

        else:
            if volt == "5V":
                # Inserting 5V layers
                cell.shapes(v5_xtor).insert(pya.Box(- (cmp2cmp+dg_enc_cmp) - ld,  -(dg_enc_ply+ply_ext_cmp),  (2 * (ld + ld_violat) + l + dg_enc_cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), w + (dg_enc_ply+ply_ext_cmp)))
                cell.shapes(dualgate).insert(pya.Box(- (cmp2cmp+dg_enc_cmp) - ld,  -(dg_enc_ply+ply_ext_cmp),  (2 * (ld + ld_violat) + l + dg_enc_cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), w + (dg_enc_ply+ply_ext_cmp)))
            elif volt == "6V":
                # Inserting 6V layers
                cell.shapes(dualgate).insert(pya.Box(- (cmp2cmp+dg_enc_cmp) - ld,  -(dg_enc_ply+ply_ext_cmp),  (2 * (ld + ld_violat) + l + dg_enc_cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), w + (dg_enc_ply+ply_ext_cmp)))

        # Inserting Tie
        if (w * ld) < min_cmp_area:
            tie_violat = (min_cmp_area/ld - w)/2 * tol
        cell.shapes(comp).insert(pya.Box(- cmp2cmp - ld, -tie_violat, -cmp2cmp, w + tie_violat))
        cell.shapes(pplus).insert(pya.Box(- cmp2cmp - pp_enc_cmp - ld, -pp_enc_cmp-tie_violat, -cmp2cmp+pp_enc_cmp, w + tie_violat + pp_enc_cmp))

        # Tie contacts
        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new((- (cmp2cmp+cont_size) - dx * cont_size/(2 *cmp2cont)), dy)),
                pya.Point.new(-(cont2cont+cont_size), 0), pya.Point.new(0, (cont2cont+cont_size)), nx, ny))

        # Tie metal
        cell.shapes(metal1).insert(pya.Box(- cmp2cmp - ld, -tie_violat, -cmp2cmp, w + tie_violat))

    elif bulk == "Guard Ring":
        if deepnwell == True:
            if volt == "5V":
                # Inserting 5V layers
                cell.shapes(v5_xtor).insert(pya.Box(-dg_enc_dnwell-dnwell_enc_lvpwell-lvpwell_enc_pcmp-cmp2cmp - grw,
                 -dg_enc_dnwell-dnwell_enc_lvpwell-lvpwell_enc_pcmp-(ply_ext_cmp + ply2gr) - grw,
                 (2 * (ld + ld_violat) + l + grw + cmp2cmp + lvpwell_enc_pcmp + dnwell_enc_lvpwell + dg_enc_dnwell + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)),
                 (w + (ply_ext_cmp + ply2gr) + grw + lvpwell_enc_pcmp + dnwell_enc_lvpwell + dg_enc_dnwell)))

                cell.shapes(dualgate).insert(pya.Box(-dg_enc_dnwell-dnwell_enc_lvpwell-lvpwell_enc_pcmp-cmp2cmp - grw,
                 -dg_enc_dnwell-dnwell_enc_lvpwell-lvpwell_enc_pcmp-(ply_ext_cmp + ply2gr) - grw,
                 (2 * (ld + ld_violat) + l + grw + cmp2cmp + lvpwell_enc_pcmp + dnwell_enc_lvpwell + dg_enc_dnwell + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)),
                 (w + (ply_ext_cmp + ply2gr) + grw + lvpwell_enc_pcmp + dnwell_enc_lvpwell + dg_enc_dnwell)))

            elif volt == "6V":
                # Inserting 6V layers
                cell.shapes(dualgate).insert(pya.Box(-dg_enc_dnwell-dnwell_enc_lvpwell-lvpwell_enc_pcmp-cmp2cmp - grw,
                 -dg_enc_dnwell-dnwell_enc_lvpwell-lvpwell_enc_pcmp-(ply_ext_cmp + ply2gr) - grw,
                 (2 * (ld + ld_violat) + l + grw + cmp2cmp + lvpwell_enc_pcmp + dnwell_enc_lvpwell + dg_enc_dnwell + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)),
                 (w + (ply_ext_cmp + ply2gr) + grw + lvpwell_enc_pcmp + dnwell_enc_lvpwell + dg_enc_dnwell)))

            # Inserting LVPWELL
            cell.shapes(lvpwell).insert(pya.Box(-lvpwell_enc_pcmp-cmp2cmp - grw, -lvpwell_enc_pcmp-(ply_ext_cmp + ply2gr) - grw,
             (2 * (ld + ld_violat) + l + grw + cmp2cmp + lvpwell_enc_pcmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)),
             (w + (ply_ext_cmp + ply2gr) + grw + lvpwell_enc_pcmp)))

            # Inserting DNWELL
            cell.shapes(dnwell).insert(pya.Box(-dnwell_enc_lvpwell-lvpwell_enc_pcmp-cmp2cmp - grw,
             -dnwell_enc_lvpwell-lvpwell_enc_pcmp-(ply_ext_cmp + ply2gr) - grw,
             (2 * (ld + ld_violat) + l + grw + cmp2cmp + lvpwell_enc_pcmp + dnwell_enc_lvpwell + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)),
             (w + (ply_ext_cmp + ply2gr) + grw + lvpwell_enc_pcmp + dnwell_enc_lvpwell)))

            # Inserting Double Guard Ring
            if pcmpgr == True:
                cmp_inner = pya.Box(-dnwell_enc_lvpwell-lvpwell_enc_pcmp-cmp2cmp - grw - pcmp_gr2dnw,
                    -dnwell_enc_lvpwell-lvpwell_enc_pcmp-(ply_ext_cmp + ply2gr) - grw - pcmp_gr2dnw,
                    (2 * (ld + ld_violat) + l + grw + cmp2cmp + lvpwell_enc_pcmp + dnwell_enc_lvpwell + pcmp_gr2dnw + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)),
                    (w + (ply_ext_cmp + ply2gr) + grw + pcmp_gr2dnw + lvpwell_enc_pcmp + dnwell_enc_lvpwell))
                cmp_outer = pya.Box(-dnwell_enc_lvpwell-lvpwell_enc_pcmp-cmp2cmp - grw - pcmp_gr2dnw - gr_w,
                    -dnwell_enc_lvpwell-lvpwell_enc_pcmp-(ply_ext_cmp + ply2gr) - grw - pcmp_gr2dnw - gr_w,
                    (2 * (ld + ld_violat) + l + grw + cmp2cmp + lvpwell_enc_pcmp + dnwell_enc_lvpwell + pcmp_gr2dnw + gr_w + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)),
                    (w + (ply_ext_cmp + ply2gr) + grw + pcmp_gr2dnw + gr_w + lvpwell_enc_pcmp + dnwell_enc_lvpwell))
                cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
                cell.shapes(comp).insert(cmp_gr)

                pp_inner = pya.Box(-dnwell_enc_lvpwell-lvpwell_enc_pcmp-cmp2cmp - grw - pcmp_gr2dnw + pp_enc_cmp,
                    -dnwell_enc_lvpwell-lvpwell_enc_pcmp-(ply_ext_cmp + ply2gr) - grw - pcmp_gr2dnw + pp_enc_cmp,
                    (2 * (ld + ld_violat) + l + grw + cmp2cmp + lvpwell_enc_pcmp + dnwell_enc_lvpwell + pcmp_gr2dnw - pp_enc_cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)),
                    (w + (ply_ext_cmp + ply2gr) + grw + pcmp_gr2dnw + lvpwell_enc_pcmp + dnwell_enc_lvpwell - pp_enc_cmp))
                pp_outer = pya.Box(-dnwell_enc_lvpwell-lvpwell_enc_pcmp-cmp2cmp - grw - pcmp_gr2dnw - gr_w - pp_enc_cmp,
                    -dnwell_enc_lvpwell-lvpwell_enc_pcmp-(ply_ext_cmp + ply2gr) - grw - pcmp_gr2dnw - gr_w - pp_enc_cmp,
                    (2 * (ld + ld_violat) + l + grw + cmp2cmp + lvpwell_enc_pcmp + dnwell_enc_lvpwell + pcmp_gr2dnw + gr_w + pp_enc_cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)),
                    (w + (ply_ext_cmp + ply2gr) + grw + pcmp_gr2dnw + gr_w + pp_enc_cmp + lvpwell_enc_pcmp + dnwell_enc_lvpwell))
                pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
                cell.shapes(pplus).insert(pp_gr)

        else:
            if volt == "5V":
                # Inserting 5V layers
                cell.shapes(v5_xtor).insert(pya.Box(-(cmp2cmp+dg_enc_cmp) - grw, -(ply_ext_cmp+ply2gr+dg_enc_cmp) - grw,  (2 * (ld + ld_violat) + l + grw + (cmp2cmp+dg_enc_cmp) + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), (w + ply_ext_cmp+ply2gr+dg_enc_cmp + grw)))
                cell.shapes(dualgate).insert(pya.Box(-(cmp2cmp+dg_enc_cmp) - grw, -(ply_ext_cmp+ply2gr+dg_enc_cmp) - grw,  (2 * (ld + ld_violat) + l + grw + (cmp2cmp+dg_enc_cmp) + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), (w + ply_ext_cmp+ply2gr+dg_enc_cmp + grw)))
            elif volt == "6V":
                # Inserting 6V layers
                cell.shapes(dualgate).insert(pya.Box(-(cmp2cmp+dg_enc_cmp) - grw, -(ply_ext_cmp+ply2gr+dg_enc_cmp) - grw,  (2 * (ld + ld_violat) + l + grw + (cmp2cmp+dg_enc_cmp) + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), (w + ply_ext_cmp+ply2gr+dg_enc_cmp + grw)))

        # Inserting guard ring diffusion
        cell.shapes(comp).insert(
        pya.Polygon(
            [
                pya.Point(-cmp2cmp - grw, -(ply_ext_cmp + ply2gr) - grw),
                pya.Point(-cmp2cmp - grw, (w + (ply_ext_cmp + ply2gr))),
                pya.Point(-cmp2cmp, (w + (ply_ext_cmp + ply2gr))),
                pya.Point(-cmp2cmp, -(ply_ext_cmp + ply2gr)),
                pya.Point((2 * (ld + ld_violat) + l + cmp2cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), -(ply_ext_cmp + ply2gr)),
                pya.Point((2 * (ld + ld_violat) + l + cmp2cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), (w + (ply_ext_cmp + ply2gr))),
                pya.Point(-cmp2cmp - grw, (w + (ply_ext_cmp + ply2gr))),
                pya.Point(-cmp2cmp - grw, (w + (ply_ext_cmp + ply2gr) + grw)),
                pya.Point((2 * (ld + ld_violat) + l + grw + cmp2cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), (w + (ply_ext_cmp + ply2gr) + grw)),
                pya.Point((2 * (ld + ld_violat) + l + grw + cmp2cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), -(ply_ext_cmp + ply2gr) - grw),
            ],
            True,
            )
        )
        cell.shapes(pplus).insert(
        pya.Polygon(
            [
                pya.Point(-(cmp2cmp+pp_enc_cmp) - grw, -(ply_ext_cmp + ply2gr + pp_enc_cmp) - grw),
                pya.Point(-(cmp2cmp+pp_enc_cmp) - grw, (w + (ply_ext_cmp + ply2gr - pp_enc_cmp))),
                pya.Point(-(cmp2cmp-pp_enc_cmp), (w + (ply_ext_cmp + ply2gr - pp_enc_cmp))),
                pya.Point(-(cmp2cmp-pp_enc_cmp), -(ply_ext_cmp + ply2gr - pp_enc_cmp)),
                pya.Point((2 * (ld + ld_violat) + l + (cmp2cmp-pp_enc_cmp) + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), -(ply_ext_cmp + ply2gr - pp_enc_cmp)),
                pya.Point((2 * (ld + ld_violat) + l + (cmp2cmp-pp_enc_cmp) + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), (w + (ply_ext_cmp + ply2gr - pp_enc_cmp))),
                pya.Point(-(cmp2cmp+pp_enc_cmp) - grw, (w + (ply_ext_cmp + ply2gr - pp_enc_cmp))),
                pya.Point(-(cmp2cmp+pp_enc_cmp) - grw, (w + (ply_ext_cmp + ply2gr + pp_enc_cmp) + grw)),
                pya.Point((2 * (ld + ld_violat) + l + grw + (cmp2cmp+pp_enc_cmp) + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), (w + (ply_ext_cmp + ply2gr + pp_enc_cmp) + grw)),
                pya.Point((2 * (ld + ld_violat) + l + grw + (cmp2cmp+pp_enc_cmp) + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), -(ply_ext_cmp + ply2gr + pp_enc_cmp) - grw),
            ],
            True,
            )
        )

        # Inserting Guard Ring metal
        cell.shapes(metal1).insert(
        pya.Polygon(
            [
                pya.Point(-cmp2cmp - grw, -(ply_ext_cmp + ply2gr) - grw),
                pya.Point(-cmp2cmp - grw, (w + (ply_ext_cmp + ply2gr))),
                pya.Point(-cmp2cmp, (w + (ply_ext_cmp + ply2gr))),
                pya.Point(-cmp2cmp, -(ply_ext_cmp + ply2gr)),
                pya.Point((2 * (ld + ld_violat) + l + cmp2cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), -(ply_ext_cmp + ply2gr)),
                pya.Point((2 * (ld + ld_violat) + l + cmp2cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), (w + (ply_ext_cmp + ply2gr))),
                pya.Point(-cmp2cmp - grw, (w + (ply_ext_cmp + ply2gr))),
                pya.Point(-cmp2cmp - grw, (w + (ply_ext_cmp + ply2gr) + grw)),
                pya.Point((2 * (ld + ld_violat) + l + grw + cmp2cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), (w + (ply_ext_cmp + ply2gr) + grw)),
                pya.Point((2 * (ld + ld_violat) + l + grw + cmp2cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), -(ply_ext_cmp + ply2gr) - grw),
            ],
            True,
            )
        )

        nxgr    = int((grw - (cont_size+2*cmp2cont))/(cont2cont+cont_size)) + 1
        nygr    = int(((2 * grw + w + 2*(ply_ext_cmp + ply2gr)) - (cont_size+2*cmp2cont))/(cont2cont+cont_size)) + 1
        dxgr    = (grw - nxgr * cont_size - (nxgr - 1) * cont2cont)/2
        dygr    = ((2 * grw + w + 2*(ply_ext_cmp + ply2gr)) - nygr * cont_size - (nygr - 1) * cont2cont)/2
        nxgr_h  = int(((2 * (ld + ld_violat) + l + 2*cmp2cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)) - 2*cont2cont)/(cont2cont+cont_size)) + 1
        dxgr_h  = ((2 * (ld + ld_violat) + l + cont2cont + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)) - nxgr_h * cont_size - (nxgr_h - 1) * cont2cont)/2

        # Inserting Guard Ring contacts
        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new((-cmp2cmp - grw + dxgr), (-(ply_ext_cmp+ply2gr) - grw + dygr))),
                    pya.Point.new((cont2cont+cont_size), 0), pya.Point.new(0, (cont2cont+cont_size)), nxgr, nygr))
        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(-(2*cmp2cont) + dxgr_h, -(2*cont_size) - ply2gr - dxgr)),
                    pya.Point.new((cont2cont+cont_size), 0), pya.Point.new(0, -(cont2cont+cont_size)), nxgr_h, nxgr))
        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(2 * (ld + ld_violat) + l + grw - dxgr + (cmp2cmp-cont_size) + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont), (-(ply_ext_cmp+ply2gr) - grw + dygr))),
                    pya.Point.new(-(cont2cont+cont_size), 0), pya.Point.new(0, (cont2cont+cont_size)), nxgr, nygr))
        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new((-(2*cmp2cont) + dxgr_h), (w + (ply_ext_cmp+ply2gr) + dxgr))),
                    pya.Point.new((cont2cont+cont_size), 0), pya.Point.new(0, (cont2cont+cont_size)), nxgr_h, nxgr))

    else:
        if deepnwell == True:
            if volt == "5V":
                # Inserting 5V layers
                cell.shapes(v5_xtor).insert(pya.Box(-dg_enc_dnwell-dnwell_enc_lvpwell-lvpwell_enc_ncmp,-dg_enc_dnwell-dnwell_enc_lvpwell-lvpwell_enc_ncmp,
                (2 * (ld + ld_violat) + l + dg_enc_dnwell + dnwell_enc_lvpwell + lvpwell_enc_ncmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                 w + lvpwell_enc_ncmp + dnwell_enc_lvpwell + dg_enc_dnwell))

                cell.shapes(dualgate).insert(pya.Box(-dg_enc_dnwell-dnwell_enc_lvpwell-lvpwell_enc_ncmp,-dg_enc_dnwell-dnwell_enc_lvpwell-lvpwell_enc_ncmp,
                (2 * (ld + ld_violat) + l + dg_enc_dnwell + dnwell_enc_lvpwell + lvpwell_enc_ncmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                 w + lvpwell_enc_ncmp + dnwell_enc_lvpwell + dg_enc_dnwell))

            elif volt == "6V":
                # Inserting 6V layers
                cell.shapes(dualgate).insert(pya.Box(-dg_enc_dnwell-dnwell_enc_lvpwell-lvpwell_enc_ncmp,-dg_enc_dnwell-dnwell_enc_lvpwell-lvpwell_enc_ncmp,
                (2 * (ld + ld_violat) + l + dg_enc_dnwell + dnwell_enc_lvpwell + lvpwell_enc_ncmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                 w + lvpwell_enc_ncmp + dnwell_enc_lvpwell + dg_enc_dnwell))

            # Inserting LVPWELL
            cell.shapes(lvpwell).insert(pya.Box(-lvpwell_enc_ncmp,-lvpwell_enc_ncmp,
            (2 * (ld + ld_violat) + l + lvpwell_enc_ncmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
             w + lvpwell_enc_ncmp))

            # Inserting DNWELL
            cell.shapes(dnwell).insert(pya.Box(-dnwell_enc_lvpwell-lvpwell_enc_ncmp,-dnwell_enc_lvpwell-lvpwell_enc_ncmp,
            (2 * (ld + ld_violat) + l + dnwell_enc_lvpwell + lvpwell_enc_ncmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
             w + lvpwell_enc_ncmp + dnwell_enc_lvpwell))

             # Inserting Double Guard Ring
            if pcmpgr == True:
                cmp_inner = pya.Box(-dnwell_enc_lvpwell-lvpwell_enc_ncmp - pcmp_gr2dnw, -dnwell_enc_lvpwell-lvpwell_enc_ncmp - pcmp_gr2dnw ,
                    (2 * (ld + ld_violat) + l + dnwell_enc_lvpwell + lvpwell_enc_ncmp + pcmp_gr2dnw + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                    w + lvpwell_enc_ncmp + dnwell_enc_lvpwell + pcmp_gr2dnw)
                cmp_outer = pya.Box(-dnwell_enc_lvpwell-lvpwell_enc_ncmp - pcmp_gr2dnw - gr_w, -dnwell_enc_lvpwell-lvpwell_enc_ncmp - pcmp_gr2dnw - gr_w,
                    (2 * (ld + ld_violat) + l + dnwell_enc_lvpwell + lvpwell_enc_ncmp + pcmp_gr2dnw + gr_w + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                    w + lvpwell_enc_ncmp + dnwell_enc_lvpwell + pcmp_gr2dnw + gr_w)
                cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
                cell.shapes(comp).insert(cmp_gr)

                pp_inner = pya.Box(-dnwell_enc_lvpwell-lvpwell_enc_ncmp - pcmp_gr2dnw + pp_enc_cmp, -dnwell_enc_lvpwell-lvpwell_enc_ncmp - pcmp_gr2dnw + pp_enc_cmp ,
                    (2 * (ld + ld_violat) + l + dnwell_enc_lvpwell + lvpwell_enc_ncmp + pcmp_gr2dnw - pp_enc_cmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                    w + lvpwell_enc_ncmp + dnwell_enc_lvpwell + pcmp_gr2dnw - pp_enc_cmp)
                pp_outer = pya.Box(-dnwell_enc_lvpwell-lvpwell_enc_ncmp - pcmp_gr2dnw - gr_w - pp_enc_cmp, -dnwell_enc_lvpwell-lvpwell_enc_ncmp - pcmp_gr2dnw - gr_w - pp_enc_cmp,
                    (2 * (ld + ld_violat) + l + dnwell_enc_lvpwell + lvpwell_enc_ncmp + pcmp_gr2dnw + gr_w + pp_enc_cmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                    w + lvpwell_enc_ncmp + dnwell_enc_lvpwell + pcmp_gr2dnw + gr_w + pp_enc_cmp)
                pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
                cell.shapes(pplus).insert(pp_gr)

        else:
            if volt == "5V":
                # Inserting 5V layers
                cell.shapes(v5_xtor).insert(pya.Box(- dg_enc_cmp,  -(dg_enc_ply+ply_ext_cmp),  (2 * (ld + ld_violat) + l + dg_enc_cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), w + (dg_enc_ply+ply_ext_cmp)))
                cell.shapes(dualgate).insert(pya.Box(- dg_enc_cmp,  -(dg_enc_ply+ply_ext_cmp),  (2 * (ld + ld_violat) + l + dg_enc_cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), w + (dg_enc_ply+ply_ext_cmp)))
            elif volt == "6V":
                # Inserting 6V layers
                cell.shapes(dualgate).insert(pya.Box(- dg_enc_cmp,  -(dg_enc_ply+ply_ext_cmp),  (2 * (ld + ld_violat) + l + dg_enc_cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), w + (dg_enc_ply+ply_ext_cmp)))

    cell.flatten(True)
    return cell

def draw_pmos(layout, l, w, ld, nf, grw, bulk, volt, deepnwell, pcmpgr):
    '''
    Usage:-
     used to draw PMOS transistor by specifying parameters
    Arguments:-
     layout     : Object of layout
     l          : Float of gate length
     w          : Float of gate width
     ld         : Float of diffusion length
     nf         : Integer of number of fingers
     grw        : Float of guard ring width [If enabled]
     bulk       : String of bulk connection type [None, Bulk Tie, Guard Ring]
     volt       : String of operating voltage of the MOSFET [3.3V, 5V, 6V]
     deepnwell  : Boolean of using Deep NWELL device
     pcmpgr     : Boolean of using P+ Guard Ring for Deep NWELL devices only
    '''

    # Define layers
    dnwell                  = layout.layer(12 , 0 )
    dualgate                = layout.layer(55 , 0 )
    v5_xtor                 = layout.layer(112, 1 )
    nwell                   = layout.layer(21 , 0 )
    comp                    = layout.layer(22 , 0 )
    poly2                   = layout.layer(30 , 0 )
    nplus                   = layout.layer(32 , 0 )
    pplus                   = layout.layer(31 , 0 )
    contact                 = layout.layer(33 , 0 )
    metal1                  = layout.layer(34 , 0 )

    # Define variables
    dbu_PERCISION           = 1/layout.dbu
    nf                      = int(nf)
    grw                     = grw       * dbu_PERCISION
    ld                      = ld        * dbu_PERCISION
    l                       = l         * dbu_PERCISION
    w                       = w         * dbu_PERCISION
    cmp2cont                = 0.07      * dbu_PERCISION
    cont_size               = 0.22      * dbu_PERCISION
    np_enc_cmp              = 0.16      * dbu_PERCISION
    pp_enc_cmp              = 0.16      * dbu_PERCISION
    cont2ply                = 0.15      * dbu_PERCISION
    ply_ext_cmp             = 0.22      * dbu_PERCISION
    np_enc_gate             = 0.23      * dbu_PERCISION
    cont2cont               = 0.28      * dbu_PERCISION
    dg_enc_ply              = 0.4       * dbu_PERCISION
    dg_enc_cmp              = 0.24      * dbu_PERCISION
    cmp2cmp                 = 0.28      * dbu_PERCISION
    ply2gr                  = 0.1       * dbu_PERCISION
    nwell_enc_pcomp         = 0.43      * dbu_PERCISION
    nwell_enc_ncomp         = 0.12      * dbu_PERCISION
    ld_violat               = 0         * dbu_PERCISION
    tie_violat              = 0         * dbu_PERCISION
    metal_violat            = 0.01      * dbu_PERCISION
    min_cmp_area            = 0.2025    * dbu_PERCISION * dbu_PERCISION
    dg_enc_dnwell           = 0.5       * dbu_PERCISION
    dnwell_enc_ncmp         = 0.62      * dbu_PERCISION
    dnwell_enc_pcmp         = 0.93      * dbu_PERCISION
    pcmp_gr2dnw             = 2.5       * dbu_PERCISION
    gr_w                    = 0.36      * dbu_PERCISION

    if deepnwell == True:
        cmp2cmp             = 0.36      * dbu_PERCISION
        ply2gr              = 0.3       * dbu_PERCISION

    if volt == "5V" or volt == "6V":
        cmp2cmp             = 0.36      * dbu_PERCISION
        ply2gr              = 0.3       * dbu_PERCISION
        cmp2cmp             = 0.36      * dbu_PERCISION
        dnwell_enc_ncmp     = 0.66      * dbu_PERCISION
        dnwell_enc_pcmp     = 1.1       * dbu_PERCISION
        nwell_enc_pcomp     = 0.6       * dbu_PERCISION
        nwell_enc_ncomp     = 0.16      * dbu_PERCISION

    if w < cont_size+2*cmp2cont:
        if nf == 1:
            if volt == "5V" or volt == "6V":
                ld_violat   = 0.22      * dbu_PERCISION
            else:
                ld_violat   = 0.02      * dbu_PERCISION

    # Inserting PMOS cell
    cell_index  = layout.add_cell("pmos")
    cell        = layout.cell(cell_index)

    w_changed = False

    # Inserting diffusion
    if w < cont_size+2*cmp2cont:
        cell.shapes(comp).insert(pya.Box(0, (cont_size+2*cmp2cont - w)/2, (2 * (ld + ld_violat) + l + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)), w + (cont_size+2*cmp2cont - w)/2))
        w = cont_size+2*cmp2cont
        w_changed = True
    else:
        cell.shapes(comp).insert(pya.Box(0, 0, (2 * ld + l + (nf - 1) * (ld + l + cont2ply - cmp2cont)), w))

    cell.shapes(pplus).insert(pya.Box(-np_enc_cmp, -np_enc_gate, (2 * (ld + ld_violat) + l + np_enc_cmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)), w + np_enc_gate))

    # Inserting gate/s
    # Inserting a gate cell
    gate_cell_index = layout.add_cell("gate")
    gate_cell = layout.cell(gate_cell_index)
    gate_cell.shapes(poly2).insert(pya.Box(ld + ld_violat, -ply_ext_cmp, (ld + ld_violat + l), (w + ply_ext_cmp)))

    # adding gate array
    cell.insert(pya.CellInstArray.new(gate_cell_index, pya.Trans.new(pya.Point.new(0, 0)),
            pya.Point.new(ld + ld_violat + l + cont2ply - cmp2cont, 0), pya.Point.new(0, 0), int(nf), 1))


    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell       = layout.cell(cont_cell_index)

    # Inserting shapes now into the *contact* cell
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Contact array count and postions
    nx = int((ld - (cont_size+cmp2cont+cont2ply))/(cont2cont+cont_size)) + 1
    ny = int((w - (cont_size+2*cmp2cont))/(cont2cont+cont_size)) + 1
    dx = (ld - nx * cont_size - (nx - 1) * cont2cont)*cmp2cont/cont_size
    dy = (w - ny * cont_size - (ny - 1) * cont2cont)/2

    # adding contact array and metals
    # Left contacts
    if not (w_changed == True and nf > 1) and (ld >= 440):
        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(dx, dy)),
                pya.Point.new((cont2cont+cont_size), 0), pya.Point.new(0, (cont2cont+cont_size)), nx, ny))
        # Left metal
        cell.shapes(metal1).insert(pya.Box(-metal_violat, -metal_violat, ld + metal_violat - (cont_size-2*cmp2cont), w + metal_violat))

    # Adding diffusion to avoid contact violation
    if nf == 1 and w_changed == True:
        cell.shapes(comp).insert(pya.Box(0, 0, ld - (cont_size-2*cmp2cont), w))

    # Right contacts and metals for each finger
    for i in range(nf):
        # Contacts
        if not (w_changed == True and nf > 1) and (ld >= 440):
            cell.insert(pya.CellInstArray.new(cont_cell_index,
                pya.Trans.new(pya.Point.new(((l + ld + ld_violat + cont2ply - cmp2cont) * i + 2 * (ld + ld_violat) + l - cont_size - dx), dy)),
                pya.Point.new(-(cont2cont+cont_size), 0), pya.Point.new(0, (cont2cont+cont_size)), nx, ny))
            # Metals
            cell.shapes(metal1).insert(pya.Box((ld + 2 * ld_violat + l + cont2ply - cmp2cont)*(i + 1), - metal_violat,
             ld + metal_violat + ld_violat + (ld + ld_violat + l + cont2ply - cmp2cont)*(i + 1) - (cont_size-2*cmp2cont), w + metal_violat))

    # Adding diffusion to avoid contact violation
    if nf == 1 and w_changed == True:
            cell.shapes(comp).insert(pya.Box((ld + 2 * ld_violat + l + cont2ply - cmp2cont)*(i + 1), 0, ld + ld_violat + (ld + ld_violat + l + cont2ply - cmp2cont)*(i + 1) - (cont_size-2*cmp2cont), w))
            region = pya.Region.new(cell.begin_shapes_rec(comp))
            region.merge()
            cell.clear(comp)
            cell.shapes(comp).insert(region)

    if bulk == "Bulk Tie":
        if deepnwell == True:
            if volt == "5V":
                # Inserting 5V layers
                cell.shapes(v5_xtor).insert(pya.Box(-dg_enc_dnwell-dnwell_enc_ncmp-cmp2cmp-ld,-dg_enc_dnwell-dnwell_enc_pcmp,
                (2 * (ld + ld_violat) + l + dg_enc_dnwell + dnwell_enc_pcmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                 w + dnwell_enc_pcmp + dg_enc_dnwell))

                cell.shapes(dualgate).insert(pya.Box(-dg_enc_dnwell-dnwell_enc_ncmp-cmp2cmp-ld,-dg_enc_dnwell-dnwell_enc_pcmp,
                (2 * (ld + ld_violat) + l + dg_enc_dnwell + dnwell_enc_pcmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                 w + dnwell_enc_pcmp + dg_enc_dnwell))

            elif volt == "6V":
                # Inserting 6V layers
                cell.shapes(dualgate).insert(pya.Box(-dg_enc_dnwell-dnwell_enc_ncmp-cmp2cmp-ld,-dg_enc_dnwell-dnwell_enc_pcmp,
                (2 * (ld + ld_violat) + l + dg_enc_dnwell + dnwell_enc_pcmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                 w + dnwell_enc_pcmp + dg_enc_dnwell))

            # Inserting DNWELL
            cell.shapes(dnwell).insert(pya.Box(-dnwell_enc_ncmp-cmp2cmp-ld,-dnwell_enc_pcmp,
            (2 * (ld + ld_violat) + l + dnwell_enc_pcmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
             w + dnwell_enc_pcmp))

            # Inserting Double Guard Ring
            if pcmpgr == True:
                cmp_inner = pya.Box(-dnwell_enc_ncmp-cmp2cmp-ld-pcmp_gr2dnw, -dnwell_enc_pcmp-pcmp_gr2dnw,
                    (2 * (ld + ld_violat) + l + dnwell_enc_pcmp + pcmp_gr2dnw + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                    w + dnwell_enc_pcmp + pcmp_gr2dnw)
                cmp_outer = pya.Box(-dnwell_enc_ncmp-cmp2cmp-ld-pcmp_gr2dnw-gr_w, -dnwell_enc_pcmp-pcmp_gr2dnw-gr_w,
                    (2 * (ld + ld_violat) + l + dnwell_enc_pcmp + pcmp_gr2dnw + gr_w + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                    w + dnwell_enc_pcmp + pcmp_gr2dnw + gr_w)
                cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
                cell.shapes(comp).insert(cmp_gr)

                pp_inner = pya.Box(-dnwell_enc_ncmp-cmp2cmp-ld-pcmp_gr2dnw+pp_enc_cmp, -dnwell_enc_pcmp-pcmp_gr2dnw+pp_enc_cmp,
                    (2 * (ld + ld_violat) + l + dnwell_enc_pcmp + pcmp_gr2dnw - pp_enc_cmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                    w + dnwell_enc_pcmp + pcmp_gr2dnw - pp_enc_cmp)
                pp_outer = pya.Box(-dnwell_enc_ncmp-cmp2cmp-ld-pcmp_gr2dnw-gr_w- pp_enc_cmp, -dnwell_enc_pcmp-pcmp_gr2dnw-gr_w- pp_enc_cmp,
                    (2 * (ld + ld_violat) + l + dnwell_enc_pcmp + pcmp_gr2dnw + gr_w + pp_enc_cmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                    w + dnwell_enc_pcmp + pcmp_gr2dnw + gr_w + pp_enc_cmp)
                pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
                cell.shapes(pplus).insert(pp_gr)

        else:
            if volt == "5V":
                # Inserting 5V layers
                cell.shapes(v5_xtor).insert(pya.Box(- (cmp2cmp+dg_enc_cmp) - ld,  -(dg_enc_ply+ply_ext_cmp),  (2 * (ld + ld_violat) + l + dg_enc_cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), w + (dg_enc_ply+ply_ext_cmp)))
                cell.shapes(dualgate).insert(pya.Box(- (cmp2cmp+dg_enc_cmp) - ld,  -(dg_enc_ply+ply_ext_cmp),  (2 * (ld + ld_violat) + l + dg_enc_cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), w + (dg_enc_ply+ply_ext_cmp)))
            elif volt == "6V":
                # Inserting 6V layers
                cell.shapes(dualgate).insert(pya.Box(- (cmp2cmp+dg_enc_cmp) - ld,  -(dg_enc_ply+ply_ext_cmp),  (2 * (ld + ld_violat) + l + dg_enc_cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), w + (dg_enc_ply+ply_ext_cmp)))

            # Inserting nwell
            cell.shapes(nwell).insert(pya.Box(- nwell_enc_ncomp - cmp2cmp - ld,  -nwell_enc_pcomp,  (2 * (ld + ld_violat) + l + nwell_enc_pcomp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), w + nwell_enc_pcomp))

        # Inserting Tie
        if (w * ld) < min_cmp_area:
            tie_violat = (min_cmp_area/ld - w)/2 * tol
        cell.shapes(comp).insert(pya.Box(- cmp2cmp - ld, -tie_violat, -cmp2cmp, w + tie_violat))
        cell.shapes(nplus).insert(pya.Box(- cmp2cmp - np_enc_cmp - ld, -np_enc_cmp-tie_violat, -cmp2cmp+np_enc_cmp, w + tie_violat + np_enc_cmp))

        # Tie contacts
        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new((- (cmp2cmp+cont_size) - dx * cont_size/(2 *cmp2cont)), dy)),
                pya.Point.new(-(cont2cont+cont_size), 0), pya.Point.new(0, (cont2cont+cont_size)), nx, ny))

        # Tie metal
        cell.shapes(metal1).insert(pya.Box(- cmp2cmp - ld, -tie_violat, -cmp2cmp, w + tie_violat))

    elif bulk == "Guard Ring":
        if deepnwell == True:
            if volt == "5V":
                # Inserting 5V layers
                cell.shapes(v5_xtor).insert(pya.Box(-dg_enc_dnwell-dnwell_enc_ncmp-cmp2cmp - grw,
                 -dg_enc_dnwell-dnwell_enc_ncmp-(ply_ext_cmp + ply2gr) - grw,
                 (2 * (ld + ld_violat) + l + grw + cmp2cmp + dnwell_enc_ncmp + dg_enc_dnwell + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)),
                 (w + (ply_ext_cmp + ply2gr) + grw + dnwell_enc_ncmp + dg_enc_dnwell)))

                cell.shapes(dualgate).insert(pya.Box(-dg_enc_dnwell-dnwell_enc_ncmp-cmp2cmp - grw,
                 -dg_enc_dnwell-dnwell_enc_ncmp-(ply_ext_cmp + ply2gr) - grw,
                 (2 * (ld + ld_violat) + l + grw + cmp2cmp + dnwell_enc_ncmp + dg_enc_dnwell + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)),
                 (w + (ply_ext_cmp + ply2gr) + grw + dnwell_enc_ncmp + dg_enc_dnwell)))

            elif volt == "6V":
                # Inserting 6V layers
                cell.shapes(dualgate).insert(pya.Box(-dg_enc_dnwell-dnwell_enc_ncmp-cmp2cmp - grw,
                 -dg_enc_dnwell-dnwell_enc_ncmp-(ply_ext_cmp + ply2gr) - grw,
                 (2 * (ld + ld_violat) + l + grw + cmp2cmp + dnwell_enc_ncmp + dg_enc_dnwell + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)),
                 (w + (ply_ext_cmp + ply2gr) + grw + dnwell_enc_ncmp + dg_enc_dnwell)))

            # Inserting DNWELL
            cell.shapes(dnwell).insert(pya.Box(-dnwell_enc_ncmp-cmp2cmp - grw,
             -dnwell_enc_ncmp-(ply_ext_cmp + ply2gr) - grw,
             (2 * (ld + ld_violat) + l + grw + cmp2cmp + dnwell_enc_ncmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)),
             (w + (ply_ext_cmp + ply2gr) + grw + dnwell_enc_ncmp)))

            # Inserting Double Guard Ring
            if pcmpgr == True:
                cmp_inner = pya.Box(-dnwell_enc_ncmp-cmp2cmp - grw - pcmp_gr2dnw,
                    -dnwell_enc_ncmp-(ply_ext_cmp + ply2gr) - grw - pcmp_gr2dnw,
                    (2 * (ld + ld_violat) + l + grw + cmp2cmp + dnwell_enc_ncmp + pcmp_gr2dnw + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)),
                    (w + (ply_ext_cmp + ply2gr) + grw + dnwell_enc_ncmp + pcmp_gr2dnw))
                cmp_outer = pya.Box(-dnwell_enc_ncmp-cmp2cmp - grw - pcmp_gr2dnw - gr_w,
                    -dnwell_enc_ncmp-(ply_ext_cmp + ply2gr) - grw - pcmp_gr2dnw - gr_w,
                    (2 * (ld + ld_violat) + l + grw + cmp2cmp + dnwell_enc_ncmp + pcmp_gr2dnw + gr_w + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)),
                    (w + (ply_ext_cmp + ply2gr) + grw + dnwell_enc_ncmp + pcmp_gr2dnw + gr_w))
                cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
                cell.shapes(comp).insert(cmp_gr)

                pp_inner = pya.Box(-dnwell_enc_ncmp-cmp2cmp - grw - pcmp_gr2dnw + pp_enc_cmp,
                    -dnwell_enc_ncmp-(ply_ext_cmp + ply2gr) - grw - pcmp_gr2dnw + pp_enc_cmp,
                    (2 * (ld + ld_violat) + l + grw + cmp2cmp + dnwell_enc_ncmp + pcmp_gr2dnw - pp_enc_cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)),
                    (w + (ply_ext_cmp + ply2gr) + grw + dnwell_enc_ncmp + pcmp_gr2dnw - pp_enc_cmp))
                pp_outer = pya.Box(-dnwell_enc_ncmp-cmp2cmp - grw - pcmp_gr2dnw - gr_w - pp_enc_cmp,
                    -dnwell_enc_ncmp-(ply_ext_cmp + ply2gr) - grw - pcmp_gr2dnw - gr_w - pp_enc_cmp,
                    (2 * (ld + ld_violat) + l + grw + cmp2cmp + dnwell_enc_ncmp + pcmp_gr2dnw + gr_w + pp_enc_cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)),
                    (w + (ply_ext_cmp + ply2gr) + grw + dnwell_enc_ncmp + pcmp_gr2dnw + gr_w + pp_enc_cmp))
                pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
                cell.shapes(pplus).insert(pp_gr)

        else:
            if volt == "5V":
                # Inserting 5V layers
                cell.shapes(v5_xtor).insert(pya.Box(-(cmp2cmp+dg_enc_cmp) - grw, -(ply_ext_cmp+ply2gr+dg_enc_cmp) - grw,  (2 * (ld + ld_violat) + l + grw + (cmp2cmp+dg_enc_cmp) + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), (w + ply_ext_cmp+ply2gr+dg_enc_cmp + grw)))
                cell.shapes(dualgate).insert(pya.Box(-(cmp2cmp+dg_enc_cmp) - grw, -(ply_ext_cmp+ply2gr+dg_enc_cmp) - grw,  (2 * (ld + ld_violat) + l + grw + (cmp2cmp+dg_enc_cmp) + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), (w + ply_ext_cmp+ply2gr+dg_enc_cmp + grw)))
            elif volt == "6V":
                # Inserting 6V layers
                cell.shapes(dualgate).insert(pya.Box(-(cmp2cmp+dg_enc_cmp) - grw, -(ply_ext_cmp+ply2gr+dg_enc_cmp) - grw,  (2 * (ld + ld_violat) + l + grw + (cmp2cmp+dg_enc_cmp) + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), (w + ply_ext_cmp+ply2gr+dg_enc_cmp + grw)))

            # Inserting nwell
            cell.shapes(nwell).insert(pya.Box(- nwell_enc_ncomp - cmp2cmp - grw, - ply_ext_cmp - ply2gr - nwell_enc_ncomp - grw,  (2 * (ld + ld_violat) + l + grw + nwell_enc_ncomp + cmp2cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), (w + ply_ext_cmp + ply2gr + nwell_enc_ncomp + grw)))

        # Inserting Guard Ring diffusion
        cell.shapes(comp).insert(
        pya.Polygon(
            [
                pya.Point(-cmp2cmp - grw, -(ply_ext_cmp + ply2gr) - grw),
                pya.Point(-cmp2cmp - grw, (w + (ply_ext_cmp + ply2gr))),
                pya.Point(-cmp2cmp, (w + (ply_ext_cmp + ply2gr))),
                pya.Point(-cmp2cmp, -(ply_ext_cmp + ply2gr)),
                pya.Point((2 * (ld + ld_violat) + l + cmp2cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), -(ply_ext_cmp + ply2gr)),
                pya.Point((2 * (ld + ld_violat) + l + cmp2cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), (w + (ply_ext_cmp + ply2gr))),
                pya.Point(-cmp2cmp - grw, (w + (ply_ext_cmp + ply2gr))),
                pya.Point(-cmp2cmp - grw, (w + (ply_ext_cmp + ply2gr) + grw)),
                pya.Point((2 * (ld + ld_violat) + l + grw + cmp2cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), (w + (ply_ext_cmp + ply2gr) + grw)),
                pya.Point((2 * (ld + ld_violat) + l + grw + cmp2cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), -(ply_ext_cmp + ply2gr) - grw),
            ],
            True,
            )
        )
        cell.shapes(nplus).insert(
        pya.Polygon(
            [
                pya.Point(-(cmp2cmp+pp_enc_cmp) - grw, -(ply_ext_cmp + ply2gr + pp_enc_cmp) - grw),
                pya.Point(-(cmp2cmp+pp_enc_cmp) - grw, (w + (ply_ext_cmp + ply2gr - pp_enc_cmp))),
                pya.Point(-(cmp2cmp-pp_enc_cmp), (w + (ply_ext_cmp + ply2gr - pp_enc_cmp))),
                pya.Point(-(cmp2cmp-pp_enc_cmp), -(ply_ext_cmp + ply2gr - pp_enc_cmp)),
                pya.Point((2 * (ld + ld_violat) + l + (cmp2cmp-pp_enc_cmp) + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), -(ply_ext_cmp + ply2gr - pp_enc_cmp)),
                pya.Point((2 * (ld + ld_violat) + l + (cmp2cmp-pp_enc_cmp) + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), (w + (ply_ext_cmp + ply2gr - pp_enc_cmp))),
                pya.Point(-(cmp2cmp+pp_enc_cmp) - grw, (w + (ply_ext_cmp + ply2gr - pp_enc_cmp))),
                pya.Point(-(cmp2cmp+pp_enc_cmp) - grw, (w + (ply_ext_cmp + ply2gr + pp_enc_cmp) + grw)),
                pya.Point((2 * (ld + ld_violat) + l + grw + (cmp2cmp+pp_enc_cmp) + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), (w + (ply_ext_cmp + ply2gr + pp_enc_cmp) + grw)),
                pya.Point((2 * (ld + ld_violat) + l + grw + (cmp2cmp+pp_enc_cmp) + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), -(ply_ext_cmp + ply2gr + pp_enc_cmp) - grw),
            ],
            True,
            )
        )

        # Inserting Guard Ring metal
        cell.shapes(metal1).insert(
        pya.Polygon(
            [
                pya.Point(-cmp2cmp - grw, -(ply_ext_cmp + ply2gr) - grw),
                pya.Point(-cmp2cmp - grw, (w + (ply_ext_cmp + ply2gr))),
                pya.Point(-cmp2cmp, (w + (ply_ext_cmp + ply2gr))),
                pya.Point(-cmp2cmp, -(ply_ext_cmp + ply2gr)),
                pya.Point((2 * (ld + ld_violat) + l + cmp2cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), -(ply_ext_cmp + ply2gr)),
                pya.Point((2 * (ld + ld_violat) + l + cmp2cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), (w + (ply_ext_cmp + ply2gr))),
                pya.Point(-cmp2cmp - grw, (w + (ply_ext_cmp + ply2gr))),
                pya.Point(-cmp2cmp - grw, (w + (ply_ext_cmp + ply2gr) + grw)),
                pya.Point((2 * (ld + ld_violat) + l + grw + cmp2cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), (w + (ply_ext_cmp + ply2gr) + grw)),
                pya.Point((2 * (ld + ld_violat) + l + grw + cmp2cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), -(ply_ext_cmp + ply2gr) - grw),
            ],
            True,
            )
        )

        nxgr    = int((grw - (cont_size+2*cmp2cont))/(cont2cont+cont_size)) + 1
        nygr    = int(((2 * grw + w + 2*(ply_ext_cmp + ply2gr)) - (cont_size+2*cmp2cont))/(cont2cont+cont_size)) + 1
        dxgr    = (grw - nxgr * cont_size - (nxgr - 1) * cont2cont)/2
        dygr    = ((2 * grw + w + 2*(ply_ext_cmp + ply2gr)) - nygr * cont_size - (nygr - 1) * cont2cont)/2
        nxgr_h  = int(((2 * (ld + ld_violat) + l + 2*cmp2cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)) - 2*cont2cont)/(cont2cont+cont_size)) + 1
        dxgr_h  = ((2 * (ld + ld_violat) + l + cont2cont + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)) - nxgr_h * cont_size - (nxgr_h - 1) * cont2cont)/2

        # Inserting Guard Ring contacts
        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new((-cmp2cmp - grw + dxgr), (-(ply_ext_cmp+ply2gr) - grw + dygr))),
                    pya.Point.new((cont2cont+cont_size), 0), pya.Point.new(0, (cont2cont+cont_size)), nxgr, nygr))
        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(-(2*cmp2cont) + dxgr_h, -(2*cont_size) - ply2gr - dxgr)),
                    pya.Point.new((cont2cont+cont_size), 0), pya.Point.new(0, -(cont2cont+cont_size)), nxgr_h, nxgr))
        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(2 * (ld + ld_violat) + l + grw - dxgr + (cmp2cmp-cont_size) + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont), (-(ply_ext_cmp+ply2gr) - grw + dygr))),
                    pya.Point.new(-(cont2cont+cont_size), 0), pya.Point.new(0, (cont2cont+cont_size)), nxgr, nygr))
        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new((-(2*cmp2cont) + dxgr_h), (w + (ply_ext_cmp+ply2gr) + dxgr))),
                    pya.Point.new((cont2cont+cont_size), 0), pya.Point.new(0, (cont2cont+cont_size)), nxgr_h, nxgr))

    else:
        if deepnwell == True:
            if volt == "5V":
                # Inserting 5V layers
                cell.shapes(v5_xtor).insert(pya.Box(-dg_enc_dnwell-dnwell_enc_pcmp,-dg_enc_dnwell-dnwell_enc_pcmp,
                (2 * (ld + ld_violat) + l + dg_enc_dnwell + dnwell_enc_pcmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                 w + dnwell_enc_pcmp + dg_enc_dnwell))

                cell.shapes(dualgate).insert(pya.Box(-dg_enc_dnwell-dnwell_enc_pcmp,-dg_enc_dnwell-dnwell_enc_pcmp,
                (2 * (ld + ld_violat) + l + dg_enc_dnwell + dnwell_enc_pcmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                 w + dnwell_enc_pcmp + dg_enc_dnwell))

            elif volt == "6V":
                # Inserting 6V layers
                cell.shapes(dualgate).insert(pya.Box(-dg_enc_dnwell-dnwell_enc_pcmp,-dg_enc_dnwell-dnwell_enc_pcmp,
                (2 * (ld + ld_violat) + l + dg_enc_dnwell + dnwell_enc_pcmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                 w + dnwell_enc_pcmp + dg_enc_dnwell))

            # Inserting DNWELL
            cell.shapes(dnwell).insert(pya.Box(-dnwell_enc_pcmp,-dnwell_enc_pcmp,
            (2 * (ld + ld_violat) + l + dnwell_enc_pcmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
             w + dnwell_enc_pcmp))

            # Inserting Double Guard Ring
            if pcmpgr == True:
                cmp_inner = pya.Box(-dnwell_enc_pcmp - pcmp_gr2dnw, -dnwell_enc_pcmp - pcmp_gr2dnw,
                    (2 * (ld + ld_violat) + l + dnwell_enc_pcmp + pcmp_gr2dnw + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                    w + dnwell_enc_pcmp + pcmp_gr2dnw)
                cmp_outer = pya.Box(-dnwell_enc_pcmp - pcmp_gr2dnw - gr_w, -dnwell_enc_pcmp - pcmp_gr2dnw - gr_w,
                    (2 * (ld + ld_violat) + l + dnwell_enc_pcmp + pcmp_gr2dnw + gr_w + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                    w + dnwell_enc_pcmp + pcmp_gr2dnw + gr_w)
                cmp_gr = pya.Region(cmp_outer) - pya.Region(cmp_inner)
                cell.shapes(comp).insert(cmp_gr)

                pp_inner = pya.Box(-dnwell_enc_pcmp - pcmp_gr2dnw + pp_enc_cmp, -dnwell_enc_pcmp - pcmp_gr2dnw + pp_enc_cmp,
                    (2 * (ld + ld_violat) + l + dnwell_enc_pcmp + pcmp_gr2dnw - pp_enc_cmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                    w + dnwell_enc_pcmp + pcmp_gr2dnw - pp_enc_cmp)
                pp_outer = pya.Box(-dnwell_enc_pcmp - pcmp_gr2dnw - gr_w - pp_enc_cmp, -dnwell_enc_pcmp - pcmp_gr2dnw - gr_w - pp_enc_cmp,
                    (2 * (ld + ld_violat) + l + dnwell_enc_pcmp + pcmp_gr2dnw + gr_w + pp_enc_cmp + (nf - 1) * (ld + ld_violat + l + cont2ply - cmp2cont)),
                    w + dnwell_enc_pcmp + pcmp_gr2dnw + gr_w + pp_enc_cmp)
                pp_gr = pya.Region(pp_outer) - pya.Region(pp_inner)
                cell.shapes(pplus).insert(pp_gr)

        else:
            if volt == "5V":
                # Inserting 5V layers
                cell.shapes(v5_xtor).insert(pya.Box(- dg_enc_cmp,  -(dg_enc_ply+ply_ext_cmp),  (2 * (ld + ld_violat) + l + dg_enc_cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), w + (dg_enc_ply+ply_ext_cmp)))
                cell.shapes(dualgate).insert(pya.Box(- dg_enc_cmp,  -(dg_enc_ply+ply_ext_cmp),  (2 * (ld + ld_violat) + l + dg_enc_cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), w + (dg_enc_ply+ply_ext_cmp)))
            elif volt == "6V":
                # Inserting 6V layers
                cell.shapes(dualgate).insert(pya.Box(- dg_enc_cmp,  -(dg_enc_ply+ply_ext_cmp),  (2 * (ld + ld_violat) + l + dg_enc_cmp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), w + (dg_enc_ply+ply_ext_cmp)))

            # Inserting NWELL
            cell.shapes(nwell).insert(pya.Box(- nwell_enc_pcomp,  -nwell_enc_pcomp,  (2 * (ld + ld_violat) + l + nwell_enc_pcomp + (nf - 1) * ((ld + ld_violat) + l + cont2ply - cmp2cont)), w + nwell_enc_pcomp))


    cell.flatten(True)
    return cell

def draw_nmos_6p0_nat(layout, l, w, ld, nf, grw, bulk):
    '''
    Usage:-
     used to draw Native NMOS 6V transistor by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of gate length
     w      : Float of gate width
     ld     : Float of diffusion length
     nf     : Integer of number of fingers
     grw    : Float of guard ring width [If enabled]
     bulk   : String of bulk connection type [None, Bulk Tie, Guard Ring]
    '''

    # Define layers
    dualgate                = layout.layer(55 , 0 )
    nat                     = layout.layer(5  , 0 )
    comp                    = layout.layer(22 , 0 )
    poly2                   = layout.layer(30 , 0 )
    nplus                   = layout.layer(32 , 0 )
    pplus                   = layout.layer(31 , 0 )
    contact                 = layout.layer(33 , 0 )
    metal1                  = layout.layer(34 , 0 )

    # Define variables
    dbu_PERCISION           = 1/layout.dbu
    nf                      = int(nf)
    grw                     = grw       * dbu_PERCISION
    ld                      = ld        * dbu_PERCISION
    l                       = l         * dbu_PERCISION
    w                       = w         * dbu_PERCISION
    cmp2cont                = 0.07      * dbu_PERCISION
    cont_size               = 0.22      * dbu_PERCISION
    np_enc_cmp              = 0.16      * dbu_PERCISION
    pp_enc_cmp              = 0.16      * dbu_PERCISION
    cont2ply                = 0.15      * dbu_PERCISION
    ply_ext_cmp             = 0.22      * dbu_PERCISION
    np_enc_gate             = 0.23      * dbu_PERCISION
    cont2cont               = 0.28      * dbu_PERCISION
    cmp2cmp                 = 0.36      * dbu_PERCISION
    nat_enc_cmp             = 2         * dbu_PERCISION

    # Inserting NMOS cell
    cell_index  = layout.add_cell("nmos_6p0_nat")
    cell        = layout.cell(cell_index)

    # Inserting diffusion
    cell.shapes(comp).insert(pya.Box(0, 0, (2 * ld + l + (nf - 1) * (ld + l + cont2ply - cmp2cont)), w))
    cell.shapes(nplus).insert(pya.Box(-np_enc_cmp, -np_enc_gate, (2 * ld + l + np_enc_cmp + (nf - 1) * (ld + l + cont2ply - cmp2cont)), w + np_enc_gate))
    cell.shapes(nat).insert(pya.Box(-nat_enc_cmp, -nat_enc_cmp, (2 * ld + l + nat_enc_cmp + (nf - 1) * (ld + l + cont2ply - cmp2cont)), w + nat_enc_cmp))
    cell.shapes(dualgate).insert(pya.Box(-nat_enc_cmp, -nat_enc_cmp, (2 * ld + l + nat_enc_cmp + (nf - 1) * (ld + l + cont2ply - cmp2cont)), w + nat_enc_cmp))

    # Inserting gate/s
    # Inserting a gate cell
    gate_cell_index = layout.add_cell("gate")
    gate_cell = layout.cell(gate_cell_index)
    gate_cell.shapes(poly2).insert(pya.Box(ld, -ply_ext_cmp, (ld + l), (w + ply_ext_cmp)))

    # adding gate array
    cell.insert(pya.CellInstArray.new(gate_cell_index, pya.Trans.new(pya.Point.new(0, 0)),
            pya.Point.new(ld + l + cont2ply - cmp2cont, 0), pya.Point.new(0, 0), int(nf), 1))


    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell       = layout.cell(cont_cell_index)

    # Inserting shapes now into the *contact* cell
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Contact array count and postions
    nx = int((ld - (cont_size+cmp2cont+cont2ply))/(cont2cont+cont_size)) + 1
    ny = int((w - (cont_size+2*cmp2cont))/(cont2cont+cont_size)) + 1
    dx = (ld - nx * cont_size - (nx - 1) * cont2cont)*cmp2cont/cont_size
    dy = (w - ny * cont_size - (ny - 1) * cont2cont)/2

    # adding contact array and metals
    # Left contacts
    cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(dx, dy)),
            pya.Point.new((cont2cont+cont_size), 0), pya.Point.new(0, (cont2cont+cont_size)), nx, ny))
    # Left metal
    cell.shapes(metal1).insert(pya.Box(0, 0, ld - (cont_size-2*cmp2cont), w))

     # Right contacts and metals for each finger
    for i in range(nf):
        # Contacts
        cell.insert(pya.CellInstArray.new(cont_cell_index,
            pya.Trans.new(pya.Point.new(((l + ld + cont2ply - cmp2cont) * i + 2 * ld + l - cont_size - dx), dy)),
            pya.Point.new(-(cont2cont+cont_size), 0), pya.Point.new(0, (cont2cont+cont_size)), nx, ny))
        # Metals
        cell.shapes(metal1).insert(pya.Box((ld + l + cont2ply - cmp2cont)*(i + 1), 0, ld + (ld + l + cont2ply - cmp2cont)*(i + 1) - (cont_size-2*cmp2cont), w))

    if bulk == "Bulk Tie":
        # Inserting tie
        cell.shapes(comp).insert(pya.Box(- (nat_enc_cmp + cmp2cmp) - ld, 0, -(nat_enc_cmp + cmp2cmp), w))
        cell.shapes(pplus).insert(pya.Box(- (nat_enc_cmp + cmp2cmp + pp_enc_cmp) - ld, -pp_enc_cmp, -(nat_enc_cmp + cmp2cmp - pp_enc_cmp), w + pp_enc_cmp))

        # Tie contacts
        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new((- (nat_enc_cmp + cmp2cmp + cont_size) - dx * cont_size/(2 *cmp2cont)), dy)),
                pya.Point.new(-(cont2cont+cont_size), 0), pya.Point.new(0, (cont2cont+cont_size)), nx, ny))

        # Tie metal
        cell.shapes(metal1).insert(pya.Box(- (nat_enc_cmp + cmp2cmp) - ld, 0, -(nat_enc_cmp + cmp2cmp), w))

    elif bulk == "Guard Ring":
        # Inserting Guard Ring diffusion
        cell.shapes(comp).insert(
        pya.Polygon(
            [
                pya.Point(-(nat_enc_cmp + cmp2cmp) - grw, -(nat_enc_cmp + cmp2cmp) - grw),
                pya.Point(-(nat_enc_cmp + cmp2cmp) - grw, (w + (nat_enc_cmp + cmp2cmp))),
                pya.Point(-(nat_enc_cmp + cmp2cmp), (w + (nat_enc_cmp + cmp2cmp))),
                pya.Point(-(nat_enc_cmp + cmp2cmp), -(nat_enc_cmp + cmp2cmp)),
                pya.Point((2 * ld + l + (nat_enc_cmp + cmp2cmp) + (nf - 1) * (ld + l)), -(nat_enc_cmp + cmp2cmp)),
                pya.Point((2 * ld + l + (nat_enc_cmp + cmp2cmp) + (nf - 1) * (ld + l)), (w + (nat_enc_cmp + cmp2cmp))),
                pya.Point(-(nat_enc_cmp + cmp2cmp) - grw, (w + (nat_enc_cmp + cmp2cmp))),
                pya.Point(-(nat_enc_cmp + cmp2cmp) - grw, (w + (nat_enc_cmp + cmp2cmp) + grw)),
                pya.Point((2 * ld + l + grw + (nat_enc_cmp + cmp2cmp) + (nf - 1) * (ld + l)), (w + (nat_enc_cmp + cmp2cmp) + grw)),
                pya.Point((2 * ld + l + grw + (nat_enc_cmp + cmp2cmp) + (nf - 1) * (ld + l)), -(nat_enc_cmp + cmp2cmp) - grw),
            ],
            True,
            )
        )
        cell.shapes(pplus).insert(
        pya.Polygon(
            [
                pya.Point(-(nat_enc_cmp + cmp2cmp + pp_enc_cmp) - grw, -(nat_enc_cmp + cmp2cmp + pp_enc_cmp) - grw),
                pya.Point(-(nat_enc_cmp + cmp2cmp + pp_enc_cmp) - grw, (w + (nat_enc_cmp + cmp2cmp - pp_enc_cmp))),
                pya.Point(-(nat_enc_cmp + cmp2cmp - pp_enc_cmp), (w + (nat_enc_cmp + cmp2cmp - pp_enc_cmp))),
                pya.Point(-(nat_enc_cmp + cmp2cmp - pp_enc_cmp), -(nat_enc_cmp + cmp2cmp - pp_enc_cmp)),
                pya.Point((2 * ld + l + (nat_enc_cmp + cmp2cmp - pp_enc_cmp) + (nf - 1) * (ld + l)), -(nat_enc_cmp + cmp2cmp - pp_enc_cmp)),
                pya.Point((2 * ld + l + (nat_enc_cmp + cmp2cmp - pp_enc_cmp) + (nf - 1) * (ld + l)), (w + (nat_enc_cmp + cmp2cmp - pp_enc_cmp))),
                pya.Point(-(nat_enc_cmp + cmp2cmp + pp_enc_cmp) - grw, (w + (nat_enc_cmp + cmp2cmp - pp_enc_cmp))),
                pya.Point(-(nat_enc_cmp + cmp2cmp + pp_enc_cmp) - grw, (w + (nat_enc_cmp + cmp2cmp + pp_enc_cmp) + grw)),
                pya.Point((2 * ld + l + grw + (nat_enc_cmp + cmp2cmp + pp_enc_cmp) + (nf - 1) * (ld + l)), (w + (nat_enc_cmp + cmp2cmp + pp_enc_cmp) + grw)),
                pya.Point((2 * ld + l + grw + (nat_enc_cmp + cmp2cmp + pp_enc_cmp) + (nf - 1) * (ld + l)), -(nat_enc_cmp + cmp2cmp + pp_enc_cmp) - grw),
            ],
            True,
            )
        )

        # Inserting Guard Ring metal
        cell.shapes(metal1).insert(
        pya.Polygon(
            [
                pya.Point(-(nat_enc_cmp + cmp2cmp) - grw, -(nat_enc_cmp + cmp2cmp) - grw),
                pya.Point(-(nat_enc_cmp + cmp2cmp) - grw, (w + (nat_enc_cmp + cmp2cmp))),
                pya.Point(-(nat_enc_cmp + cmp2cmp), (w + (nat_enc_cmp + cmp2cmp))),
                pya.Point(-(nat_enc_cmp + cmp2cmp), -(nat_enc_cmp + cmp2cmp)),
                pya.Point((2 * ld + l + (nat_enc_cmp + cmp2cmp) + (nf - 1) * (ld + l)), -(nat_enc_cmp + cmp2cmp)),
                pya.Point((2 * ld + l + (nat_enc_cmp + cmp2cmp) + (nf - 1) * (ld + l)), (w + (nat_enc_cmp + cmp2cmp))),
                pya.Point(-(nat_enc_cmp + cmp2cmp) - grw, (w + (nat_enc_cmp + cmp2cmp))),
                pya.Point(-(nat_enc_cmp + cmp2cmp) - grw, (w + (nat_enc_cmp + cmp2cmp) + grw)),
                pya.Point((2 * ld + l + grw + (nat_enc_cmp + cmp2cmp) + (nf - 1) * (ld + l)), (w + (nat_enc_cmp + cmp2cmp) + grw)),
                pya.Point((2 * ld + l + grw + (nat_enc_cmp + cmp2cmp) + (nf - 1) * (ld + l)), -(nat_enc_cmp + cmp2cmp) - grw),
            ],
            True,
            )
        )

        nxgr    = int((grw - (cont_size+2*cmp2cont))/(cont2cont+cont_size)) + 1
        nygr    = int(((2 * grw + w + 2*(nat_enc_cmp + cmp2cmp)) - (cont_size+2*cmp2cont))/(cont2cont+cont_size)) + 1
        dxgr    = (grw - nxgr * cont_size - (nxgr - 1) * cont2cont)/2
        dygr    = ((2 * grw + w + 2*(nat_enc_cmp + cmp2cmp)) - nygr * cont_size - (nygr - 1) * cont2cont)/2
        nxgr_h  = int(((2 * ld + l + 2*(nat_enc_cmp + cmp2cmp) + (nf - 1) * (ld + l))- 2*cont2cont)/(cont2cont+cont_size)) + 1
        dxgr_h  = ((2 * ld + l + (nat_enc_cmp + cmp2cmp) + (nf - 1) * (ld + l)) - nxgr_h * cont_size - (nxgr_h - 1) * cont2cont)/2

        # Inserting Guard Ring contacts
        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new((-(nat_enc_cmp + cmp2cmp) - grw + dxgr), (-(nat_enc_cmp + cmp2cmp) - grw + dygr))),
                    pya.Point.new((cont2cont+cont_size), 0), pya.Point.new(0, (cont2cont+cont_size)), nxgr, nygr))
        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(-(nat_enc_cmp + cmp2cmp)/2 + dxgr_h, -(nat_enc_cmp + cmp2cmp + cont_size) - dxgr)),
                    pya.Point.new((cont2cont+cont_size), 0), pya.Point.new(0, -(cont2cont+cont_size)), nxgr_h, nxgr))
        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(2 * ld + l + grw - dxgr + nat_enc_cmp + cmp2cmp - cont_size + (nf - 1) * (ld + l), (-(nat_enc_cmp + cmp2cmp) - grw + dygr))),
                    pya.Point.new(-(cont2cont+cont_size), 0), pya.Point.new(0, (cont2cont+cont_size)), nxgr, nygr))
        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(-(nat_enc_cmp + cmp2cmp)/2 + dxgr_h, w + (nat_enc_cmp + cmp2cmp) + dxgr)),
                    pya.Point.new((cont2cont+cont_size), 0), pya.Point.new(0, (cont2cont+cont_size)), nxgr_h, nxgr))

    cell.flatten(True)
    return cell

def draw_nmos_10p0_asym(layout, l, w):
    '''
    Usage:-
     used to draw LDNMOS 10V transistor by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of gate length
     w      : Float of gate width
    '''

    # Define layers
    dualgate                = layout.layer(55 , 0 )
    ldmos_xtor              = layout.layer(226, 0 )
    mvsd                    = layout.layer(210, 0 )
    comp                    = layout.layer(22 , 0 )
    poly2                   = layout.layer(30 , 0 )
    nplus                   = layout.layer(32 , 0 )
    pplus                   = layout.layer(31 , 0 )
    contact                 = layout.layer(33 , 0 )
    metal1                  = layout.layer(34 , 0 )

    # Define variables
    dbu_PERCISION           = 1/layout.dbu
    l                       = l         * dbu_PERCISION
    w                       = w         * dbu_PERCISION
    cmp2cont                = 0.07      * dbu_PERCISION
    cont_size               = 0.22      * dbu_PERCISION
    np_enc_cmp              = 0.16      * dbu_PERCISION
    pp_enc_cmp              = 0.16      * dbu_PERCISION
    cont2ply                = 0.15      * dbu_PERCISION
    metal_w                 = 0.38      * dbu_PERCISION
    ply_ext_cmp             = 0.4       * dbu_PERCISION
    ply_fld                 = 0.2       * dbu_PERCISION
    np_enc_gate             = 0.23      * dbu_PERCISION
    cont2cont               = 0.25      * dbu_PERCISION
    cmp2cmp                 = 0.36      * dbu_PERCISION
    cmp2gr                  = 0.4       * dbu_PERCISION
    mvsd_ext_cmp            = 0.5       * dbu_PERCISION
    mvsd_ov_cmp             = 0.4       * dbu_PERCISION
    mvsd2gr                 = 1         * dbu_PERCISION
    ply2gr                  = 0.4       * dbu_PERCISION
    drain2ply               = 0.16      * dbu_PERCISION
    dg_enc_cmp              = 0.5       * dbu_PERCISION


    # Inserting NMOS cell
    cell_index  = layout.add_cell("nmos_10p0_asym")
    cell        = layout.cell(cell_index)

    # Inserting layers for LDMOS
    cell.shapes(dualgate).insert(pya.Box(
     -(dg_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont2ply+cont_size+cmp2cont+mvsd_ov_cmp+cmp2cmp) - l, -(mvsd_ext_cmp+mvsd2gr+2*cmp2cont+cont_size+dg_enc_cmp) - w/2,
      (dg_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont2ply+cont_size+cmp2cont+mvsd_ov_cmp+cmp2cmp) + l,  (mvsd_ext_cmp+mvsd2gr+2*cmp2cont+cont_size+dg_enc_cmp) + w/2))
    cell.shapes(ldmos_xtor).insert(pya.Box(
     -(dg_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont2ply+cont_size+cmp2cont+mvsd_ov_cmp+cmp2cmp) - l, -(mvsd_ext_cmp+mvsd2gr+2*cmp2cont+cont_size+dg_enc_cmp) - w/2,
      (dg_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont2ply+cont_size+cmp2cont+mvsd_ov_cmp+cmp2cmp) + l,  (mvsd_ext_cmp+mvsd2gr+2*cmp2cont+cont_size+dg_enc_cmp) + w/2))

    # Inserting drain diffusion
    cell.shapes(comp).insert(pya.Box(-cont_size/2, -w/2, cont_size/2, w/2))
    cell.shapes(mvsd).insert(pya.Box(-(cont_size/2+cmp2cmp+mvsd_ov_cmp), -w/2 - mvsd_ext_cmp, (cont_size/2+cmp2cmp+mvsd_ov_cmp), w/2 + mvsd_ext_cmp))

    # Inserting source diffusion
    cell.shapes(comp).insert(pya.Box((cont_size/2+cmp2cmp), -w/2, (cont_size/2+cmp2cmp+mvsd_ov_cmp+cont2ply+cont_size+cmp2cont) + l, w/2))
    cell.shapes(comp).insert(pya.Box(-(cont_size/2+cmp2cmp), -w/2, -(cont_size/2+cmp2cmp+mvsd_ov_cmp+cont2ply+cont_size+cmp2cont) - l, w/2))

    cell.shapes(nplus).insert(pya.Box(-(cont_size/2+cmp2cmp+mvsd_ov_cmp+cont2ply+cont_size+cmp2cont+np_enc_cmp) - l, -w/2 - np_enc_gate,
     (cont_size/2+cmp2cmp+mvsd_ov_cmp+cont2ply+cont_size+cmp2cont+np_enc_cmp) + l, w/2 + np_enc_gate))

    # Inserting gates
    cell.shapes(poly2).insert(pya.Box((cont_size/2+drain2ply), -w/2 - ply_ext_cmp, (cont_size/2+cmp2cmp+mvsd_ov_cmp) + l, w/2 + mvsd_ext_cmp+mvsd2gr-ply2gr))
    cell.shapes(poly2).insert(pya.Box(-(cont_size/2+drain2ply), -w/2 - ply_ext_cmp, -(cont_size/2+cmp2cmp+mvsd_ov_cmp) - l, w/2 + mvsd_ext_cmp+mvsd2gr-ply2gr))

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell       = layout.cell(cont_cell_index)

    # Inserting shapes now into the *contact* cell
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Contact array count and postions
    ny = int((w - (cont_size+2*cmp2cont))/(cont_size+cont2cont)) + 1
    dy = (w - ny * cont_size - (ny - 1) * cont2cont)/2
    ng = int(((l + mvsd_ov_cmp + ply_fld) - (cont_size+2*cmp2cont))/(cont_size+cont2cont)) + 1
    dg = (l + mvsd_ov_cmp + ply_fld - ng * cont_size - (ng - 1) * cont2cont)/2

    # Inserting contact array and metals
    # gate contacts and metal
    cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new((cont_size/2+drain2ply) + dg, w/2 + mvsd_ext_cmp+mvsd2gr-ply2gr-(metal_w+cont_size)/2)),
            pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), ng, 1))
    cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(-(1.5*cont_size+drain2ply) - dg, w/2 + mvsd_ext_cmp+mvsd2gr-ply2gr-(metal_w+cont_size)/2)),
            pya.Point.new(-(cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), ng, 1))
    cell.shapes(metal1).insert(pya.Box((cont_size/2+drain2ply), w/2 + mvsd_ext_cmp+mvsd2gr-ply2gr-metal_w,
     (cont_size/2+cmp2cmp+mvsd_ov_cmp) + l, w/2 + mvsd_ext_cmp+mvsd2gr-ply2gr))
    cell.shapes(metal1).insert(pya.Box(-(cont_size/2+drain2ply), w/2 + mvsd_ext_cmp+mvsd2gr-ply2gr-metal_w,
     -(cont_size/2+cmp2cmp+mvsd_ov_cmp) - l, w/2 + mvsd_ext_cmp+mvsd2gr-ply2gr))

    # Drain contacts and metal
    cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(-cont_size/2, -w/2 + dy)),
            pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), 1, ny))
    cell.shapes(metal1).insert(pya.Box(-metal_w/2, -w/2, metal_w/2, w/2))

    # Source contacts and metals
    cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new((cont_size/2+cmp2cmp+mvsd_ov_cmp+cont2ply) + l, -w/2 + dy)),
            pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), 1, ny))
    cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(-(1.5*cont_size+cmp2cmp+mvsd_ov_cmp+cont2ply) - l, -w/2 + dy)),
            pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), 1, ny))
    cell.shapes(metal1).insert(pya.Box((1.5*cont_size+cmp2cmp+mvsd_ov_cmp+cont2ply+cmp2cont-metal_w) + l, -w/2, (1.5*cont_size+cmp2cmp+mvsd_ov_cmp+cont2ply+cmp2cont) + l, w/2))
    cell.shapes(metal1).insert(pya.Box(-(1.5*cont_size+cmp2cmp+mvsd_ov_cmp+cont2ply+cmp2cont-metal_w) - l, -w/2, -(1.5*cont_size+cmp2cmp+mvsd_ov_cmp+cont2ply+cmp2cont) - l, w/2))

    # Inserting Guard Ring diffusion
    cell.shapes(comp).insert(
    pya.Polygon(
        [
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) - l, -(mvsd_ext_cmp+mvsd2gr+2*cmp2cont+cont_size) - w/2),
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) - l, (mvsd_ext_cmp+mvsd2gr) + w/2),
            pya.Point(-(0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) - l, (mvsd_ext_cmp+mvsd2gr) + w/2),
            pya.Point(-(0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) - l, -(mvsd_ext_cmp+mvsd2gr) - w/2),
            pya.Point((0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) + l, -(mvsd_ext_cmp+mvsd2gr) - w/2),
            pya.Point((0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) + l, (mvsd_ext_cmp+mvsd2gr) + w/2),
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) - l, (mvsd_ext_cmp+mvsd2gr) + w/2),
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) - l, (mvsd_ext_cmp+mvsd2gr+2*cmp2cont+cont_size) + w/2),
            pya.Point((2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) + l, (mvsd_ext_cmp+mvsd2gr+2*cmp2cont+cont_size) + w/2),
            pya.Point((2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) + l, -(mvsd_ext_cmp+mvsd2gr+2*cmp2cont+cont_size) - w/2),
        ],
        True,
        )
    )

    cell.shapes(pplus).insert(
    pya.Polygon(
        [
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp+pp_enc_cmp) - l, -(mvsd_ext_cmp+mvsd2gr+2*cmp2cont+cont_size+pp_enc_cmp) - w/2),
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp+pp_enc_cmp) - l, (mvsd_ext_cmp+mvsd2gr-pp_enc_cmp) + w/2),
            pya.Point(-(0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp-pp_enc_cmp) - l, (mvsd_ext_cmp+mvsd2gr-pp_enc_cmp) + w/2),
            pya.Point(-(0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp-pp_enc_cmp) - l, -(mvsd_ext_cmp+mvsd2gr-pp_enc_cmp) - w/2),
            pya.Point((0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp-pp_enc_cmp) + l, -(mvsd_ext_cmp+mvsd2gr-pp_enc_cmp) - w/2),
            pya.Point((0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp-pp_enc_cmp) + l, (mvsd_ext_cmp+mvsd2gr-pp_enc_cmp) + w/2),
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp+pp_enc_cmp) - l, (mvsd_ext_cmp+mvsd2gr-pp_enc_cmp) + w/2),
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp+pp_enc_cmp) - l, (mvsd_ext_cmp+mvsd2gr+2*cmp2cont+cont_size+pp_enc_cmp) + w/2),
            pya.Point((2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp+pp_enc_cmp) + l, (mvsd_ext_cmp+mvsd2gr+2*cmp2cont+cont_size+pp_enc_cmp) + w/2),
            pya.Point((2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp+pp_enc_cmp) + l, -(mvsd_ext_cmp+mvsd2gr+2*cmp2cont+cont_size+pp_enc_cmp) - w/2),
        ],
        True,
        )
    )

    cell.shapes(metal1).insert(
    pya.Polygon(
        [
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) - l, -(mvsd_ext_cmp+mvsd2gr+2*cmp2cont+cont_size) - w/2),
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) - l, (mvsd_ext_cmp+mvsd2gr) + w/2),
            pya.Point(-(0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) - l, (mvsd_ext_cmp+mvsd2gr) + w/2),
            pya.Point(-(0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) - l, -(mvsd_ext_cmp+mvsd2gr) - w/2),
            pya.Point((0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) + l, -(mvsd_ext_cmp+mvsd2gr) - w/2),
            pya.Point((0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) + l, (mvsd_ext_cmp+mvsd2gr) + w/2),
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) - l, (mvsd_ext_cmp+mvsd2gr) + w/2),
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) - l, (mvsd_ext_cmp+mvsd2gr+2*cmp2cont+cont_size) + w/2),
            pya.Point((2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) + l, (mvsd_ext_cmp+mvsd2gr+2*cmp2cont+cont_size) + w/2),
            pya.Point((2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) + l, -(mvsd_ext_cmp+mvsd2gr+2*cmp2cont+cont_size) - w/2),
        ],
        True,
        )
    )

    nygr    = int((w + 2*(mvsd_ext_cmp+mvsd2gr+cmp2cont+cont_size)+cont2cont)/(cont_size+cont2cont))
    dygr    = (w + 2*(mvsd_ext_cmp+mvsd2gr+cmp2cont+cont_size) - nygr * (cont_size+cont2cont)+ cont2cont)/2
    nxgr_h  = int((2 * l + 2*(0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp+cmp2cont)- cont2cont)/(cont_size+cont2cont))
    dxgr_h  = (2 * l + 2*(0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp+cmp2cont) - nxgr_h * (cont_size+cont2cont) + cont2cont)/2

    # Inserting Guard Ring contacts
    cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(-(cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) - l,
     dygr - (mvsd_ext_cmp+mvsd2gr+cmp2cont+cont_size) - w/2)), pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), 1, nygr))

    cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(dxgr_h - (0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp+cmp2cont) - l,
     -(mvsd_ext_cmp+mvsd2gr+cmp2cont+cont_size) - w/2)), pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), nxgr_h, 1))

    cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new((cmp2cont+0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp) + l,
     dygr - (mvsd_ext_cmp+mvsd2gr+cmp2cont+cont_size) - w/2)), pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), 1, nygr))

    cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(dxgr_h - (0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvsd_ov_cmp+cmp2cmp+cmp2cont) - l,
     (mvsd_ext_cmp+mvsd2gr+cmp2cont) + w/2)), pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), nxgr_h, 1))

    cell.flatten(True)
    return cell

def draw_pmos_10p0_asym(layout, l, w, dgr_en):
    '''
    Usage:-
     used to draw LDPMOS 10V transistor by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of gate length
     w      : Float of gate width
     dgr_en : Boolean to enable double guard ring
    '''

    # Define layers
    dnwell                  = layout.layer(12 , 0 )
    dualgate                = layout.layer(55 , 0 )
    ldmos_xtor              = layout.layer(226, 0 )
    mvpsd                   = layout.layer(11 , 39)
    comp                    = layout.layer(22 , 0 )
    poly2                   = layout.layer(30 , 0 )
    nplus                   = layout.layer(32 , 0 )
    pplus                   = layout.layer(31 , 0 )
    contact                 = layout.layer(33 , 0 )
    metal1                  = layout.layer(34 , 0 )

    # Define variables
    dbu_PERCISION           = 1/layout.dbu
    l                       = l         * dbu_PERCISION
    w                       = w         * dbu_PERCISION
    cmp2cont                = 0.07      * dbu_PERCISION
    cont_size               = 0.22      * dbu_PERCISION
    np_enc_cmp              = 0.16      * dbu_PERCISION
    pp_enc_cmp              = 0.16      * dbu_PERCISION
    cont2ply                = 0.15      * dbu_PERCISION
    metal_w                 = 0.38      * dbu_PERCISION
    ply_ext_cmp             = 0.4       * dbu_PERCISION
    ply_fld                 = 0.2       * dbu_PERCISION
    np_enc_gate             = 0.23      * dbu_PERCISION
    cont2cont               = 0.25      * dbu_PERCISION
    cmp2cmp                 = 0.36      * dbu_PERCISION
    cmp2gr                  = 0.4       * dbu_PERCISION
    mvpsd_ext_cmp           = 0.8       * dbu_PERCISION
    mvpsd_ov_cmp            = 0.4       * dbu_PERCISION
    mvpsd2gr                = 1         * dbu_PERCISION
    ply2gr                  = 0.4       * dbu_PERCISION
    drain2ply               = 0.16      * dbu_PERCISION
    dnw_enc_cmp             = 0.66      * dbu_PERCISION
    dg_enc_pcmp             = 0.5       * dbu_PERCISION
    pcmp_gr2dnw             = 2.5       * dbu_PERCISION


    # Inserting PMOS cell
    cell_index  = layout.add_cell("pmos_10p0_asym")
    cell        = layout.cell(cell_index)

    # Inserting layers for LDMOS
    cell.shapes(dnwell).insert(pya.Box(
     -(dnw_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, -(mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+dnw_enc_cmp) - w/2,
      (dnw_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l,  (mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+dnw_enc_cmp) + w/2))
    cell.shapes(dualgate).insert(pya.Box(
     -(dg_enc_pcmp+pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, -(mvpsd_ext_cmp+mvpsd2gr+4*cmp2cont+2*cont_size+dg_enc_pcmp+pcmp_gr2dnw+dnw_enc_cmp) - w/2,
      (dg_enc_pcmp+pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l,  (mvpsd_ext_cmp+mvpsd2gr+4*cmp2cont+2*cont_size+dg_enc_pcmp+pcmp_gr2dnw+dnw_enc_cmp) + w/2))
    cell.shapes(ldmos_xtor).insert(pya.Box(
     -(dg_enc_pcmp+pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, -(mvpsd_ext_cmp+mvpsd2gr+4*cmp2cont+2*cont_size+dg_enc_pcmp+pcmp_gr2dnw+dnw_enc_cmp) - w/2,
      (dg_enc_pcmp+pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l,  (mvpsd_ext_cmp+mvpsd2gr+4*cmp2cont+2*cont_size+dg_enc_pcmp+pcmp_gr2dnw+dnw_enc_cmp) + w/2))

    # Inserting drain diffusion
    cell.shapes(comp).insert(pya.Box(-cont_size/2, -w/2, cont_size/2, w/2))
    cell.shapes(mvpsd).insert(pya.Box(-(cont_size/2+cmp2cmp+mvpsd_ov_cmp), -w/2 - mvpsd_ext_cmp, (cont_size/2+cmp2cmp+mvpsd_ov_cmp), w/2 + mvpsd_ext_cmp))

    # Inserting source diffusion
    cell.shapes(comp).insert(pya.Box((cont_size/2+cmp2cmp), -w/2, (cont_size/2+cmp2cmp+mvpsd_ov_cmp+cont2ply+cont_size+cmp2cont) + l, w/2))
    cell.shapes(comp).insert(pya.Box(-(cont_size/2+cmp2cmp), -w/2, -(cont_size/2+cmp2cmp+mvpsd_ov_cmp+cont2ply+cont_size+cmp2cont) - l, w/2))

    cell.shapes(pplus).insert(pya.Box(-(cont_size/2+cmp2cmp+mvpsd_ov_cmp+cont2ply+cont_size+cmp2cont+np_enc_cmp) - l, -w/2 - np_enc_gate,
     (cont_size/2+cmp2cmp+mvpsd_ov_cmp+cont2ply+cont_size+cmp2cont+np_enc_cmp) + l, w/2 + np_enc_gate))

    # Inserting gates
    cell.shapes(poly2).insert(pya.Box((cont_size/2+drain2ply), -w/2 - ply_ext_cmp, (cont_size/2+cmp2cmp+mvpsd_ov_cmp) + l, w/2 + mvpsd_ext_cmp+mvpsd2gr-ply2gr))
    cell.shapes(poly2).insert(pya.Box(-(cont_size/2+drain2ply), -w/2 - ply_ext_cmp, -(cont_size/2+cmp2cmp+mvpsd_ov_cmp) - l, w/2 + mvpsd_ext_cmp+mvpsd2gr-ply2gr))

    # Inserting a contact cell
    cont_cell_index = layout.add_cell("contact")
    cont_cell       = layout.cell(cont_cell_index)

    # Inserting shapes now into the *contact* cell
    cont_cell.shapes(contact).insert(pya.Box.new(0, 0, cont_size, cont_size))

    # Contact array count and postions
    ny = int((w - (cont_size+2*cmp2cont))/(cont_size+cont2cont)) + 1
    dy = (w - ny * cont_size - (ny - 1) * cont2cont)/2
    ng = int(((l + mvpsd_ov_cmp + ply_fld) - (cont_size+2*cmp2cont))/(cont_size+cont2cont)) + 1
    dg = (l + mvpsd_ov_cmp + ply_fld - ng * cont_size - (ng - 1) * cont2cont)/2

    # Inserting contact array and metals
    # Gate contacts and metal
    cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new((cont_size/2+drain2ply) + dg, w/2 + mvpsd_ext_cmp+mvpsd2gr-ply2gr-(metal_w+cont_size)/2)),
            pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), ng, 1))
    cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(-(1.5*cont_size+drain2ply) - dg, w/2 + mvpsd_ext_cmp+mvpsd2gr-ply2gr-(metal_w+cont_size)/2)),
            pya.Point.new(-(cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), ng, 1))
    cell.shapes(metal1).insert(pya.Box((cont_size/2+drain2ply), w/2 + mvpsd_ext_cmp+mvpsd2gr-ply2gr-metal_w,
     (cont_size/2+cmp2cmp+mvpsd_ov_cmp) + l, w/2 + mvpsd_ext_cmp+mvpsd2gr-ply2gr))
    cell.shapes(metal1).insert(pya.Box(-(cont_size/2+drain2ply), w/2 + mvpsd_ext_cmp+mvpsd2gr-ply2gr-metal_w,
     -(cont_size/2+cmp2cmp+mvpsd_ov_cmp) - l, w/2 + mvpsd_ext_cmp+mvpsd2gr-ply2gr))

    # Drain contacts and metal
    cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(-cont_size/2, -w/2 + dy)),
            pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), 1, ny))
    cell.shapes(metal1).insert(pya.Box(-metal_w/2, -w/2, metal_w/2, w/2))

    # Source contacts and metals
    cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new((cont_size/2+cmp2cmp+mvpsd_ov_cmp+cont2ply) + l, -w/2 + dy)),
            pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), 1, ny))
    cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(-(1.5*cont_size+cmp2cmp+mvpsd_ov_cmp+cont2ply) - l, -w/2 + dy)),
            pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), 1, ny))
    cell.shapes(metal1).insert(pya.Box((1.5*cont_size+cmp2cmp+mvpsd_ov_cmp+cont2ply+cmp2cont-metal_w) + l, -w/2, (1.5*cont_size+cmp2cmp+mvpsd_ov_cmp+cont2ply+cmp2cont) + l, w/2))
    cell.shapes(metal1).insert(pya.Box(-(1.5*cont_size+cmp2cmp+mvpsd_ov_cmp+cont2ply+cmp2cont-metal_w) - l, -w/2, -(1.5*cont_size+cmp2cmp+mvpsd_ov_cmp+cont2ply+cmp2cont) - l, w/2))

    # Inserting Guard Ring diffusion
    cell.shapes(comp).insert(
    pya.Polygon(
        [
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, -(mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size) - w/2),
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, (mvpsd_ext_cmp+mvpsd2gr) + w/2),
            pya.Point(-(0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, (mvpsd_ext_cmp+mvpsd2gr) + w/2),
            pya.Point(-(0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, -(mvpsd_ext_cmp+mvpsd2gr) - w/2),
            pya.Point((0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l, -(mvpsd_ext_cmp+mvpsd2gr) - w/2),
            pya.Point((0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l, (mvpsd_ext_cmp+mvpsd2gr) + w/2),
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, (mvpsd_ext_cmp+mvpsd2gr) + w/2),
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, (mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size) + w/2),
            pya.Point((2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l, (mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size) + w/2),
            pya.Point((2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l, -(mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size) - w/2),
        ],
        True,
        )
    )

    cell.shapes(nplus).insert(
    pya.Polygon(
        [
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp+pp_enc_cmp) - l, -(mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pp_enc_cmp) - w/2),
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp+pp_enc_cmp) - l, (mvpsd_ext_cmp+mvpsd2gr-pp_enc_cmp) + w/2),
            pya.Point(-(0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp-pp_enc_cmp) - l, (mvpsd_ext_cmp+mvpsd2gr-pp_enc_cmp) + w/2),
            pya.Point(-(0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp-pp_enc_cmp) - l, -(mvpsd_ext_cmp+mvpsd2gr-pp_enc_cmp) - w/2),
            pya.Point((0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp-pp_enc_cmp) + l, -(mvpsd_ext_cmp+mvpsd2gr-pp_enc_cmp) - w/2),
            pya.Point((0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp-pp_enc_cmp) + l, (mvpsd_ext_cmp+mvpsd2gr-pp_enc_cmp) + w/2),
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp+pp_enc_cmp) - l, (mvpsd_ext_cmp+mvpsd2gr-pp_enc_cmp) + w/2),
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp+pp_enc_cmp) - l, (mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pp_enc_cmp) + w/2),
            pya.Point((2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp+pp_enc_cmp) + l, (mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pp_enc_cmp) + w/2),
            pya.Point((2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp+pp_enc_cmp) + l, -(mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pp_enc_cmp) - w/2),
        ],
        True,
        )
    )

    cell.shapes(metal1).insert(
    pya.Polygon(
        [
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, -(mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size) - w/2),
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, (mvpsd_ext_cmp+mvpsd2gr) + w/2),
            pya.Point(-(0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, (mvpsd_ext_cmp+mvpsd2gr) + w/2),
            pya.Point(-(0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, -(mvpsd_ext_cmp+mvpsd2gr) - w/2),
            pya.Point((0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l, -(mvpsd_ext_cmp+mvpsd2gr) - w/2),
            pya.Point((0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l, (mvpsd_ext_cmp+mvpsd2gr) + w/2),
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, (mvpsd_ext_cmp+mvpsd2gr) + w/2),
            pya.Point(-(2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, (mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size) + w/2),
            pya.Point((2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l, (mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size) + w/2),
            pya.Point((2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l, -(mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size) - w/2),
        ],
        True,
        )
    )

    nygr    = int((w + 2*(mvpsd_ext_cmp+mvpsd2gr+cmp2cont+cont_size)+cont2cont)/(cont_size+cont2cont))
    dygr    = (w + 2*(mvpsd_ext_cmp+mvpsd2gr+cmp2cont+cont_size) - nygr * (cont_size+cont2cont)+ cont2cont)/2
    nxgr_h  = int((2 * l + 2*(0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp+cmp2cont)- cont2cont)/(cont_size+cont2cont))
    dxgr_h  = (2 * l + 2*(0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp+cmp2cont) - nxgr_h * (cont_size+cont2cont) + cont2cont)/2

    # Inserting Guard Ring contacts
    cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(-(cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l,
     dygr - (mvpsd_ext_cmp+mvpsd2gr+cmp2cont+cont_size) - w/2)), pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), 1, nygr))

    cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(dxgr_h - (0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp+cmp2cont) - l,
     -(mvpsd_ext_cmp+mvpsd2gr+cmp2cont+cont_size) - w/2)), pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), nxgr_h, 1))

    cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new((cmp2cont+0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l,
     dygr - (mvpsd_ext_cmp+mvpsd2gr+cmp2cont+cont_size) - w/2)), pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), 1, nygr))

    cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(dxgr_h - (0.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp+cmp2cont) - l,
     (mvpsd_ext_cmp+mvpsd2gr+cmp2cont) + w/2)), pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), nxgr_h, 1))

    # Inserting DNWELL Guard Ring
    if dgr_en:
        # Inserting DNWELL Guard Ring diffusion
        cell.shapes(comp).insert(
        pya.Polygon(
            [
                pya.Point(-(pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, -(mvpsd_ext_cmp+mvpsd2gr+4*cmp2cont+2*cont_size+pcmp_gr2dnw+dnw_enc_cmp) - w/2),
                pya.Point(-(pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, (mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pcmp_gr2dnw+dnw_enc_cmp) + w/2),
                pya.Point(-(pcmp_gr2dnw+dnw_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, (mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pcmp_gr2dnw+dnw_enc_cmp) + w/2),
                pya.Point(-(pcmp_gr2dnw+dnw_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, -(mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pcmp_gr2dnw+dnw_enc_cmp) - w/2),
                pya.Point((pcmp_gr2dnw+dnw_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l, -(mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pcmp_gr2dnw+dnw_enc_cmp) - w/2),
                pya.Point((pcmp_gr2dnw+dnw_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l, (mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pcmp_gr2dnw+dnw_enc_cmp) + w/2),
                pya.Point(-(pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, (mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pcmp_gr2dnw+dnw_enc_cmp) + w/2),
                pya.Point(-(pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, (mvpsd_ext_cmp+mvpsd2gr+4*cmp2cont+2*cont_size+pcmp_gr2dnw+dnw_enc_cmp) + w/2),
                pya.Point((pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l, (mvpsd_ext_cmp+mvpsd2gr+4*cmp2cont+2*cont_size+pcmp_gr2dnw+dnw_enc_cmp) + w/2),
                pya.Point((pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l, -(mvpsd_ext_cmp+mvpsd2gr+4*cmp2cont+2*cont_size+pcmp_gr2dnw+dnw_enc_cmp) - w/2),
            ],
            True,
            )
        )

        cell.shapes(pplus).insert(
        pya.Polygon(
            [
                pya.Point(-(pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp+np_enc_cmp) - l, -(mvpsd_ext_cmp+mvpsd2gr+4*cmp2cont+2*cont_size+pcmp_gr2dnw+dnw_enc_cmp+np_enc_cmp) - w/2),
                pya.Point(-(pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp+np_enc_cmp) - l, (mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pcmp_gr2dnw+dnw_enc_cmp-np_enc_cmp) + w/2),
                pya.Point(-(pcmp_gr2dnw+dnw_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp-np_enc_cmp) - l, (mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pcmp_gr2dnw+dnw_enc_cmp-np_enc_cmp) + w/2),
                pya.Point(-(pcmp_gr2dnw+dnw_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp-np_enc_cmp) - l, -(mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pcmp_gr2dnw+dnw_enc_cmp-np_enc_cmp) - w/2),
                pya.Point((pcmp_gr2dnw+dnw_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp-np_enc_cmp) + l, -(mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pcmp_gr2dnw+dnw_enc_cmp-np_enc_cmp) - w/2),
                pya.Point((pcmp_gr2dnw+dnw_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp-np_enc_cmp) + l, (mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pcmp_gr2dnw+dnw_enc_cmp-np_enc_cmp) + w/2),
                pya.Point(-(pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp+np_enc_cmp) - l, (mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pcmp_gr2dnw+dnw_enc_cmp-np_enc_cmp) + w/2),
                pya.Point(-(pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp+np_enc_cmp) - l, (mvpsd_ext_cmp+mvpsd2gr+4*cmp2cont+2*cont_size+pcmp_gr2dnw+dnw_enc_cmp+np_enc_cmp) + w/2),
                pya.Point((pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp+np_enc_cmp) + l, (mvpsd_ext_cmp+mvpsd2gr+4*cmp2cont+2*cont_size+pcmp_gr2dnw+dnw_enc_cmp+np_enc_cmp) + w/2),
                pya.Point((pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp+np_enc_cmp) + l, -(mvpsd_ext_cmp+mvpsd2gr+4*cmp2cont+2*cont_size+pcmp_gr2dnw+dnw_enc_cmp+np_enc_cmp) - w/2),
            ],
            True,
            )
        )

        # Inserting DNWELL Guard Ring metal
        cell.shapes(metal1).insert(
        pya.Polygon(
            [
                pya.Point(-(pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, -(mvpsd_ext_cmp+mvpsd2gr+4*cmp2cont+2*cont_size+pcmp_gr2dnw+dnw_enc_cmp) - w/2),
                pya.Point(-(pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, (mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pcmp_gr2dnw+dnw_enc_cmp) + w/2),
                pya.Point(-(pcmp_gr2dnw+dnw_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, (mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pcmp_gr2dnw+dnw_enc_cmp) + w/2),
                pya.Point(-(pcmp_gr2dnw+dnw_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, -(mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pcmp_gr2dnw+dnw_enc_cmp) - w/2),
                pya.Point((pcmp_gr2dnw+dnw_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l, -(mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pcmp_gr2dnw+dnw_enc_cmp) - w/2),
                pya.Point((pcmp_gr2dnw+dnw_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l, (mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pcmp_gr2dnw+dnw_enc_cmp) + w/2),
                pya.Point(-(pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, (mvpsd_ext_cmp+mvpsd2gr+2*cmp2cont+cont_size+pcmp_gr2dnw+dnw_enc_cmp) + w/2),
                pya.Point(-(pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l, (mvpsd_ext_cmp+mvpsd2gr+4*cmp2cont+2*cont_size+pcmp_gr2dnw+dnw_enc_cmp) + w/2),
                pya.Point((pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l, (mvpsd_ext_cmp+mvpsd2gr+4*cmp2cont+2*cont_size+pcmp_gr2dnw+dnw_enc_cmp) + w/2),
                pya.Point((pcmp_gr2dnw+dnw_enc_cmp+4*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l, -(mvpsd_ext_cmp+mvpsd2gr+4*cmp2cont+2*cont_size+pcmp_gr2dnw+dnw_enc_cmp) - w/2),
            ],
            True,
            )
        )

        # Inserting DNWELL guard ring contacts
        nygr = int((w + 2*(mvpsd_ext_cmp+mvpsd2gr+3*cmp2cont+2*cont_size+pcmp_gr2dnw+dnw_enc_cmp)+cont2cont)/(cont_size+cont2cont))
        dygr = (w + 2*(mvpsd_ext_cmp+mvpsd2gr+3*cmp2cont+2*cont_size+pcmp_gr2dnw+dnw_enc_cmp) - nygr * (cont_size+cont2cont) + cont2cont)/2
        nxgr_h = int((2 * l + 2*(pcmp_gr2dnw+dnw_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+2*cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp)- cont2cont)/(cont_size+cont2cont))
        dxgr_h = (2 * l + 2*(pcmp_gr2dnw+dnw_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+2*cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - nxgr_h * (cont_size+cont2cont) + cont2cont)/2

        # Inserting DNWELL Guard Ring contacts
        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(-(pcmp_gr2dnw+dnw_enc_cmp+3*cmp2cont+2.5*cont_size+cmp2gr+cont_size+cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l,
         dygr - (mvpsd_ext_cmp+mvpsd2gr+3*cmp2cont+2*cont_size+pcmp_gr2dnw+dnw_enc_cmp) - w/2)), pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), 1, nygr))

        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(dxgr_h - (pcmp_gr2dnw+dnw_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+2*cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l,
         -(mvpsd_ext_cmp+mvpsd2gr+3*cmp2cont+2*cont_size+pcmp_gr2dnw+dnw_enc_cmp) - w/2)), pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, -(cont_size+cont2cont)), nxgr_h, 1))

        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new((pcmp_gr2dnw+dnw_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+2*cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) + l,
         dygr - (mvpsd_ext_cmp+mvpsd2gr+3*cmp2cont+2*cont_size+pcmp_gr2dnw+dnw_enc_cmp) - w/2)), pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), 1, nygr))

        cell.insert(pya.CellInstArray.new(cont_cell_index, pya.Trans.new(pya.Point.new(dxgr_h - (pcmp_gr2dnw+dnw_enc_cmp+2*cmp2cont+1.5*cont_size+cmp2gr+cont_size+2*cmp2cont+cont2ply+mvpsd_ov_cmp+cmp2cmp) - l,
         mvpsd_ext_cmp+mvpsd2gr+3*cmp2cont+cont_size+pcmp_gr2dnw+dnw_enc_cmp + w/2)), pya.Point.new((cont_size+cont2cont), 0), pya.Point.new(0, (cont_size+cont2cont)), nxgr_h, 1))

    cell.flatten(True)
    return cell
