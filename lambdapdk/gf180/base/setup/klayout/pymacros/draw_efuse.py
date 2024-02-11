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

import pya
import os

USER = os.environ['USER']
gds_path = f"/home/{USER}/.klayout/pymacros/cells/efuse"


def draw_efuse(layout, device_name):

    layout.read(f"{gds_path}/efuse.gds")
    cell_name = "efuse_cell"

    return layout.cell(cell_name)
