# Copyright 2024 ZeroASIC Corp
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Metals
set_layer_rc {{ corner }} \
    -layer metal1 \
    -capacitance 0.06999999999999999 \
    -resistance 0.00105
set_layer_rc {{ corner }} \
    -layer metal2 \
    -capacitance 0.06999999999999999 \
    -resistance 0.00105
set_layer_rc {{ corner }} \
    -layer metal3 \
    -capacitance 0.06999999999999999 \
    -resistance 0.00105
set_layer_rc {{ corner }} \
    -layer metal4 \
    -capacitance 0.06999999999999999 \
    -resistance 0.00105
set_layer_rc {{ corner }} \
    -layer topmetal \
    -capacitance 0.06999999999999999 \
    -resistance 0.00105

# Vias
set_layer_rc {{ corner }} \
    -via via1 \
    -resistance 0.006999999999999999
set_layer_rc {{ corner }} \
    -via via2 \
    -resistance 0.006999999999999999
set_layer_rc {{ corner }} \
    -via via3 \
    -resistance 0.006999999999999999
set_layer_rc {{ corner }} \
    -via via4 \
    -resistance 0.006999999999999999
