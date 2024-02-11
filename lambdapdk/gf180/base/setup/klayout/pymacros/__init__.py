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

#============================================================================
# ---------------- Pcells Generators for Klayout of GF180MCU ----------------
#============================================================================

import pya

from .mos     import *
from .diode   import *
from .bjt     import *
from .moscap  import *
from .mimcap  import *
from .res     import *
from .efuse   import *


# It's a Python class that inherits from the pya.Library class
class gf180mcu(pya.Library):
    """
    The library where we will put the PCell into
    """

    def __init__(self):
        # Set the description
        self.description = "GF180MCU Pcells"

    # Create the PCell declarations
        # MOS DEVICES
        self.layout().register_pcell("nmos", nmos())                    # nmos_3p3 , nmos_5p0 , nmos_6p0
        self.layout().register_pcell("pmos", pmos())                    # pmos_3p3 , pmos_5p0 , pmos_6p0
        self.layout().register_pcell("nmos_6p0_nat", nmos_6p0_nat())
        self.layout().register_pcell("nmos_10p0_asym", nmos_10p0_asym())
        self.layout().register_pcell("pmos_10p0_asym", pmos_10p0_asym())

        # BJT
        self.layout().register_pcell("npn_bjt", npn_bjt())             # vnpn_10x10 , vnpn_5x5 , vnpn_0p54x16 , vnpn_0p54x8 , vnpn_0p54x4 , vnpn_0p54x2
        self.layout().register_pcell("pnp_bjt", pnp_bjt())             # vpnp_10x10 , vpnp_5x5 , vpnp_0p42x10 , vpnp_0p42x5

        # DIODE DEVICES
        self.layout().register_pcell("np_diode"   , np_diode()   )     # np_3p3    , np_6p0
        self.layout().register_pcell("pn_diode"   , pn_diode()   )     # pn_3p3    , pn_6p0
        self.layout().register_pcell("nwp_diode"  , nwp_diode()  )     # nwp_3p3   , nwp_6p0
        self.layout().register_pcell("dnwpw_diode", dnwpw_diode())     # dnwpw_3p3 , dnwpw_6p0
        self.layout().register_pcell("dnwps_diode", dnwps_diode())     # dnwps_3p3 , dnwps_6p0
        self.layout().register_pcell("sc_diode"   , sc_diode()   )

        #MOSCAP
        self.layout().register_pcell("nmoscap"  , nmoscap()  )         # nmoscap_3p3   , nmoscap_6p0
        self.layout().register_pcell("pmoscap"  , pmoscap()  )         # pmoscap_3p3   , pmoscap_6p0
        self.layout().register_pcell("nmoscap_b", nmoscap_b())         # nmoscap_3p3_b , nmoscap_6p0_b
        self.layout().register_pcell("pmoscap_b", pmoscap_b())         # pmoscap_3p3_b , pmoscap_6p0_b

        #MIMCAP
        self.layout().register_pcell("mimcap"  , mimcap())             #mimcap (Option-A) , mimcap_tm (Option-B)

        #RES
        self.layout().register_pcell("metal_resistor"    , metal_resistor()   )

        self.layout().register_pcell("nplus_s_resistor"  , nplus_s_resistor() )
        self.layout().register_pcell("pplus_s_resistor"  , pplus_s_resistor() )

        self.layout().register_pcell("nplus_u_resistor"  , nplus_u_resistor() )
        self.layout().register_pcell("pplus_u_resistor"  , pplus_u_resistor() )

        self.layout().register_pcell("nwell_resistor"    , nwell_resistor()   )
        self.layout().register_pcell("pwell_resistor"    , pwell_resistor()   )

        self.layout().register_pcell("npolyf_s_resistor" , npolyf_s_resistor())
        self.layout().register_pcell("ppolyf_s_resistor" , ppolyf_s_resistor())

        self.layout().register_pcell("npolyf_u_resistor" , npolyf_u_resistor())
        self.layout().register_pcell("ppolyf_u_resistor" , ppolyf_u_resistor())

        self.layout().register_pcell("ppolyf_u_high_Rs_resistor" , ppolyf_u_high_Rs_resistor())

        #eFuse
        # self.layout().register_pcell("efuse"  , efuse())

        # Register us with the name "gf180mcu".
        self.register("gf180mcu")
