/*
 * Copyright 2022 GlobalFoundries PDK Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http:www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

`suppress_faults
`enable_portfaults
`ifdef functional
  `timescale 1ns / 1ps
  `delay_mode_distributed
  `delay_mode_unit
`else
  `timescale 1ns / 1ps
  `delay_mode_path
`endif
module gf180mcu_fd_io__asig_5p0 (ASIG5V, DVDD, DVSS, VDD, VSS);
	inout	ASIG5V;
	inout	DVDD;
	inout	DVSS;
	inout	VDD;
	inout	VSS;
endmodule


//--------EOF---------

/*
 * Copyright 2022 GlobalFoundries PDK Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http:www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

`suppress_faults
`enable_portfaults
`ifdef functional
  `timescale 1ns / 1ps
  `delay_mode_distributed
  `delay_mode_unit
`else
  `timescale 1ns / 1ps
  `delay_mode_path
`endif
module gf180mcu_fd_io__bi_24t (CS, SL, IE, OE, PU, PD, A, PAD, Y, DVDD, DVSS, VDD, VSS);
	input	CS;
	input	SL;
	input	IE;
	input	OE;
	input	PU;
	input	PD;
	input	A;
	inout	PAD;
	output	Y;
	inout	DVDD;
	inout	DVSS;
	inout	VDD;
	inout	VSS;

	supply0 gnd;
	supply1 pwr;

   	and #1 (Y, PAD, IE);
   	bufif1 #1 (PAD, A, OE);

 	rnmos #1 (PAD, gnd, ~OE && ~PU && PD);
 	rnmos #1 (PAD, pwr, ~OE && PU && ~PD);

specify
if (IE==1'b0&&OE==1'b1&&SL==1'b0) (A +=> PAD)=(1.000, 1.000);
if (IE==1'b0&&OE==1'b1&&SL==1'b1) (A +=> PAD)=(1.000, 1.000);
if (A==1'b1&&IE==1'b0&&SL==1'b0) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (A==1'b1&&IE==1'b0&&SL==1'b1) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (A==1'b0&&IE==1'b0&&SL==1'b0) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (A==1'b0&&IE==1'b0&&SL==1'b1) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (CS==1'b0&&OE==1'b0&&PAD==1'b1) (IE +=> Y)=(1.000, 1.000);
if (CS==1'b1&&OE==1'b0&&PAD==1'b1) (IE +=> Y)=(1.000, 1.000);
if (CS==1'b0&&IE==1'b1&&OE==1'b0) (PAD +=> Y)=(1.000, 1.000);
if (CS==1'b1&&IE==1'b1&&OE==1'b0) (PAD +=> Y)=(1.000, 1.000);
endspecify
endmodule


//--------EOF---------

/*
 * Copyright 2022 GlobalFoundries PDK Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http:www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

`suppress_faults
`enable_portfaults
`ifdef functional
  `timescale 1ns / 1ps
  `delay_mode_distributed
  `delay_mode_unit
`else
  `timescale 1ns / 1ps
  `delay_mode_path
`endif
module gf180mcu_fd_io__bi_t (CS, SL, IE, OE, PU, PD, A, PDRV0, PDRV1, PAD, Y, DVDD, DVSS, VDD, VSS);
	input	CS;
	input	SL;
	input	IE;
	input	OE;
	input	PU;
	input	PD;
	input	A;
	input	PDRV0;
	input	PDRV1;
	inout	PAD;
	output	Y;
	inout	DVDD;
	inout	DVSS;
	inout	VDD;
	inout	VSS;

	supply0 gnd;
	supply1 pwr;

   	and #1 (Y, PAD, IE);
   	bufif1 #1 (PAD, A, OE);

 	rnmos #1 (PAD, gnd, ~OE && ~PU && PD);
 	rnmos #1 (PAD, pwr, ~OE && PU && ~PD);

specify
if (IE==1'b0&&OE==1'b1&&PDRV0==1'b0&&PDRV1==1'b0&&SL==1'b0) (A +=> PAD)=(1.000, 1.000);
if (IE==1'b0&&OE==1'b1&&PDRV0==1'b0&&PDRV1==1'b0&&SL==1'b1) (A +=> PAD)=(1.000, 1.000);
if (IE==1'b0&&OE==1'b1&&PDRV0==1'b0&&PDRV1==1'b1&&SL==1'b0) (A +=> PAD)=(1.000, 1.000);
if (IE==1'b0&&OE==1'b1&&PDRV0==1'b0&&PDRV1==1'b1&&SL==1'b1) (A +=> PAD)=(1.000, 1.000);
if (IE==1'b0&&OE==1'b1&&PDRV0==1'b1&&PDRV1==1'b0&&SL==1'b0) (A +=> PAD)=(1.000, 1.000);
if (IE==1'b0&&OE==1'b1&&PDRV0==1'b1&&PDRV1==1'b0&&SL==1'b1) (A +=> PAD)=(1.000, 1.000);
if (IE==1'b0&&OE==1'b1&&PDRV0==1'b1&&PDRV1==1'b1&&SL==1'b0) (A +=> PAD)=(1.000, 1.000);
if (IE==1'b0&&OE==1'b1&&PDRV0==1'b1&&PDRV1==1'b1&&SL==1'b1) (A +=> PAD)=(1.000, 1.000);
if (A==1'b1&&IE==1'b0&&PDRV0==1'b0&&PDRV1==1'b0&&SL==1'b0) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (A==1'b1&&IE==1'b0&&PDRV0==1'b0&&PDRV1==1'b0&&SL==1'b1) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (A==1'b1&&IE==1'b0&&PDRV0==1'b0&&PDRV1==1'b1&&SL==1'b0) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (A==1'b1&&IE==1'b0&&PDRV0==1'b0&&PDRV1==1'b1&&SL==1'b1) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (A==1'b1&&IE==1'b0&&PDRV0==1'b1&&PDRV1==1'b0&&SL==1'b0) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (A==1'b1&&IE==1'b0&&PDRV0==1'b1&&PDRV1==1'b0&&SL==1'b1) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (A==1'b1&&IE==1'b0&&PDRV0==1'b1&&PDRV1==1'b1&&SL==1'b0) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (A==1'b1&&IE==1'b0&&PDRV0==1'b1&&PDRV1==1'b1&&SL==1'b1) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (A==1'b0&&IE==1'b0&&PDRV0==1'b0&&PDRV1==1'b0&&SL==1'b0) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (A==1'b0&&IE==1'b0&&PDRV0==1'b0&&PDRV1==1'b0&&SL==1'b1) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (A==1'b0&&IE==1'b0&&PDRV0==1'b0&&PDRV1==1'b1&&SL==1'b0) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (A==1'b0&&IE==1'b0&&PDRV0==1'b0&&PDRV1==1'b1&&SL==1'b1) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (A==1'b0&&IE==1'b0&&PDRV0==1'b1&&PDRV1==1'b0&&SL==1'b0) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (A==1'b0&&IE==1'b0&&PDRV0==1'b1&&PDRV1==1'b0&&SL==1'b1) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (A==1'b0&&IE==1'b0&&PDRV0==1'b1&&PDRV1==1'b1&&SL==1'b0) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (A==1'b0&&IE==1'b0&&PDRV0==1'b1&&PDRV1==1'b1&&SL==1'b1) (OE => PAD)=(1.000, 1.000, 1.000, 1.000, 1.000, 1.000);
if (CS==1'b0&&OE==1'b0&&PAD==1'b1) (IE +=> Y)=(1.000, 1.000);
if (CS==1'b1&&OE==1'b0&&PAD==1'b1) (IE +=> Y)=(1.000, 1.000);
if (CS==1'b0&&IE==1'b1&&OE==1'b0) (PAD +=> Y)=(1.000, 1.000);
if (CS==1'b1&&IE==1'b1&&OE==1'b0) (PAD +=> Y)=(1.000, 1.000);
endspecify
endmodule


//--------EOF---------

/*
 * Copyright 2022 GlobalFoundries PDK Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http:www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

`suppress_faults
`enable_portfaults
`ifdef functional
  `timescale 1ns / 1ps
  `delay_mode_distributed
  `delay_mode_unit
`else
  `timescale 1ns / 1ps
  `delay_mode_path
`endif
module gf180mcu_fd_io__brk2 (VSS);
	inout	VSS;
endmodule


//--------EOF---------

/*
 * Copyright 2022 GlobalFoundries PDK Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http:www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

`suppress_faults
`enable_portfaults
`ifdef functional
  `timescale 1ns / 1ps
  `delay_mode_distributed
  `delay_mode_unit
`else
  `timescale 1ns / 1ps
  `delay_mode_path
`endif
module gf180mcu_fd_io__brk5 (VSS);
	inout	VSS;
endmodule


//--------EOF---------

/*
 * Copyright 2022 GlobalFoundries PDK Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http:www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

`suppress_faults
`enable_portfaults
`ifdef functional
  `timescale 1ns / 1ps
  `delay_mode_distributed
  `delay_mode_unit
`else
  `timescale 1ns / 1ps
  `delay_mode_path
`endif
module gf180mcu_fd_io__cor (DVDD, DVSS, VDD, VSS);
	inout	DVDD;
	inout	DVSS;
	inout	VDD;
	inout	VSS;
endmodule


//--------EOF---------

/*
 * Copyright 2022 GlobalFoundries PDK Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http:www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

`suppress_faults
`enable_portfaults
`ifdef functional
  `timescale 1ns / 1ps
  `delay_mode_distributed
  `delay_mode_unit
`else
  `timescale 1ns / 1ps
  `delay_mode_path
`endif
module gf180mcu_fd_io__dvdd (DVDD, DVSS, VSS);
	inout	DVDD;
	inout	DVSS;
	inout	VSS;
	supply1	DVDD;
endmodule


//--------EOF---------

/*
 * Copyright 2022 GlobalFoundries PDK Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http:www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

`suppress_faults
`enable_portfaults
`ifdef functional
  `timescale 1ns / 1ps
  `delay_mode_distributed
  `delay_mode_unit
`else
  `timescale 1ns / 1ps
  `delay_mode_path
`endif
module gf180mcu_fd_io__dvss (DVDD, DVSS, VDD);
	inout	DVDD;
	inout	DVSS;
	inout	VDD;
	supply0	DVSS;
endmodule


//--------EOF---------

/*
 * Copyright 2022 GlobalFoundries PDK Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http:www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

`suppress_faults
`enable_portfaults
`ifdef functional
  `timescale 1ns / 1ps
  `delay_mode_distributed
  `delay_mode_unit
`else
  `timescale 1ns / 1ps
  `delay_mode_path
`endif
module gf180mcu_fd_io__fill1 (DVDD, DVSS, VDD, VSS);
	inout	DVDD;
	inout	DVSS;
	inout	VDD;
	inout	VSS;
endmodule


//--------EOF---------

/*
 * Copyright 2022 GlobalFoundries PDK Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http:www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

`suppress_faults
`enable_portfaults
`ifdef functional
  `timescale 1ns / 1ps
  `delay_mode_distributed
  `delay_mode_unit
`else
  `timescale 1ns / 1ps
  `delay_mode_path
`endif
module gf180mcu_fd_io__fill5 (DVDD, DVSS, VDD, VSS);
	inout	DVDD;
	inout	DVSS;
	inout	VDD;
	inout	VSS;
endmodule


//--------EOF---------

/*
 * Copyright 2022 GlobalFoundries PDK Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http:www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

`suppress_faults
`enable_portfaults
`ifdef functional
  `timescale 1ns / 1ps
  `delay_mode_distributed
  `delay_mode_unit
`else
  `timescale 1ns / 1ps
  `delay_mode_path
`endif
module gf180mcu_fd_io__fill10 (DVDD, DVSS, VDD, VSS);
	inout	DVDD;
	inout	DVSS;
	inout	VDD;
	inout	VSS;
endmodule


//--------EOF---------

/*
 * Copyright 2022 GlobalFoundries PDK Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http:www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

`suppress_faults
`enable_portfaults
`ifdef functional
  `timescale 1ns / 1ps
  `delay_mode_distributed
  `delay_mode_unit
`else
  `timescale 1ns / 1ps
  `delay_mode_path
`endif
module gf180mcu_fd_io__fillnc (DVDD, DVSS, VDD, VSS);
	inout	DVDD;
	inout	DVSS;
	inout	VDD;
	inout	VSS;
endmodule


//--------EOF---------

/*
 * Copyright 2022 GlobalFoundries PDK Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http:www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

`suppress_faults
`enable_portfaults
`ifdef functional
  `timescale 1ns / 1ps
  `delay_mode_distributed
  `delay_mode_unit
`else
  `timescale 1ns / 1ps
  `delay_mode_path
`endif
module gf180mcu_fd_io__in_c (PU, PD, PAD, Y, DVDD, DVSS, VDD, VSS);
	input	PU;
	input	PD;
	input	PAD;
	output	Y;
	inout	DVDD;
	inout	DVSS;
	inout	VDD;
	inout	VSS;

	buf #1 (Y, PAD);

specify
(PAD +=> Y)=(1.000, 1.000);
endspecify
endmodule


//--------EOF---------

/*
 * Copyright 2022 GlobalFoundries PDK Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http:www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

`suppress_faults
`enable_portfaults
`ifdef functional
  `timescale 1ns / 1ps
  `delay_mode_distributed
  `delay_mode_unit
`else
  `timescale 1ns / 1ps
  `delay_mode_path
`endif
module gf180mcu_fd_io__in_s (PU, PD, PAD, Y, DVDD, DVSS, VDD, VSS);
	input	PU;
	input	PD;
	input	PAD;
	output	Y;
	inout	DVDD;
	inout	DVSS;
	inout	VDD;
	inout	VSS;

	buf #1 (Y, PAD);

specify
(PAD +=> Y)=(1.000, 1.000);
endspecify
endmodule


//--------EOF---------

