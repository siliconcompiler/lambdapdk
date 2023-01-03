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

layout = RBA::Layout::new
layout.read($infile)

puts "Topcell names"

for t in layout.top_cells
  if t.name != $topcell
    puts "Delete topcell as it's not used for running " + t.name
    layout.prune_cell(t.cell_index, -1)
  else
    puts "Keep topcell " + t.name
  end
end

layout.write($outfile)


