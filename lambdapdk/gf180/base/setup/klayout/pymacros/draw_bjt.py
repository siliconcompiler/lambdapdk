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
## BJT Pcells Generators for Klayout of GF180MCU
########################################################################################################################

import pya
import os

USER = os.environ['USER']
gds_path = f"/home/{USER}/.klayout/pymacros/cells/bjt"


def draw_npn(layout, device_name):

    if device_name == "vnpn_10x10":
        layout.read(f"{gds_path}/vnpn_10x10.gds")
        cell_name = "vnpn_10x10"
    elif device_name == "vnpn_5x5":
        layout.read(f"{gds_path}/vnpn_5x5.gds")
        cell_name = "vnpn_5x5"
    elif device_name == "vnpn_0p54x16":
        layout.read(f"{gds_path}/vnpn_0p54x16.gds")
        cell_name = "vnpn_0p54x16"
    elif device_name == "vnpn_0p54x8":
        layout.read(f"{gds_path}/vnpn_0p54x8.gds")
        cell_name = "vnpn_0p54x8"
    elif device_name == "vnpn_0p54x4":
        layout.read(f"{gds_path}/vnpn_0p54x4.gds")
        cell_name = "vnpn_0p54x4"
    elif device_name == "vnpn_0p54x2":
        layout.read(f"{gds_path}/vnpn_0p54x2.gds")
        cell_name = "vnpn_0p54x2"

    return layout.cell(cell_name)


def draw_pnp(layout, device_name):

    if device_name == "vpnp_10x10":
        layout.read(f"{gds_path}/vpnp_10x10.gds")
        cell_name = "vpnp_10x10"
    elif device_name == "vpnp_5x5":
        layout.read(f"{gds_path}/vpnp_5x5.gds")
        cell_name = "vpnp_5x5"
    elif device_name == "vpnp_0p42x10":
        layout.read(f"{gds_path}/vpnp_0p42x10.gds")
        cell_name = "vpnp_0p42x10"
    elif device_name == "vpnp_0p42x5":
        layout.read(f"{gds_path}/vpnp_0p42x5.gds")
        cell_name = "vpnp_0p42x5"

    return layout.cell(cell_name)

