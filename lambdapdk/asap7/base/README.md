This is a one time copy of the ASAP library. The golden version which might be updated fron time to time can be found at:

https://github.com/The-OpenROAD-Project/asap7


* BSD 3-Clause License
* 
* Copyright 2020 Lawrence T. Clark, Vinay Vashishtha, or Arizona State
* University
* 
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions are met:
* 
* 1. Redistributions of source code must retain the above copyright notice,
* this list of conditions and the following disclaimer.
* 
* 2. Redistributions in binary form must reproduce the above copyright
* notice, this list of conditions and the following disclaimer in the
* documentation and/or other materials provided with the distribution.
* 
* 3. Neither the name of the copyright holder nor the names of its
* contributors may be used to endorse or promote products derived from this
* software without specific prior written permission.
* 
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
* AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
* IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
* ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
* LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
* CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
* SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
* INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
* CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
* ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
* POSSIBILITY OF SUCH DAMAGE.

*--------------------------------------------------------------------------
* ASAP7 PDK 
*--------------------------------------------------------------------------

* PDK Version	     : 1p7

* Readme File Author : Vinay Vashishtha
* Created On 	     : August 23, 2015
* Last Modified On   : December 10, 2020
* Description	     : This file describes the PDK directory structure and
* 		       the steps required to install the ASAP7 PDK. 
*--------------------------------------------------------------------------

*** PDK Directory Structure

▾ calibre/		
  ▾  ruledirs/						: Contains Mentor Graphics Calibre SVRF rules used
							  for design rule check (DRC), layout-vs-schematic
							  (LVS), and parasitic extraction.
    ▾ drc/
	drcRules_calibre_asap7.rul 			: File containing the ASAP7 design rules for use
							  with Mentor Graphics Calibre DRC.
    ▾ lvs/
	lvsRules_calibre_asap7.rul 			: File containing the ASAP7 LVS rules for use with
							  Mentor Graphics Calibre LVS.
    ▾ rcx/
        pexMap_calibre_asap7.rul 			: File containing SVRF commands used for mapping
							  between calibrate layers and physical layers.

        rcxRules_calibre_asap7.C 			: A capacitance rule file created with xCalibrate.

        rcxRules_calibre_asap7.R 			: A resistance rule file created with xCalibrate.

        rcxRules_calibre_asap7.xact 			: A Calibre xACT rule file created with xCalibrate.

        rcxControl_calibre_asap7.rul 			: Top-level SVRF file for extraction control. Includes
							  the files 'rcxRules_calibre_asap7.C',
							  'rcxRules_calibre_asap7.R', 'rcxRules_calibre_asap7.xact',
							  'lvsRules_calibre_asap7.rul', and 'pexMap_calibre_asap7.rul'

  ▸ rundirs/						: If required, files generated by Calibre may be
							  re-directed to the drc, lvs, and pex
							  sub-directories included within. The
							  runsets for Calibre DRC, LVS, and PEX have also
							  been provided.
    ▾ drc/
      ▾ runset_dir_drc/
          drcRunset_asap7 				: File created by Calibre Interactive to store the settings
							  specified in the DRC interface. This particular runset
							  points to the supplied DRC rule file.
    ▾ lvs/
      ▾ runset_dir_lvs/
          lvsRunset_asap7 				: File created by Calibre Interactive to store the settings
							  specified in the LVS interface. This particular runset
							  points to the supplied LVS rule file.
    
    ▾ pex/                                                
      ▾ runset_dir_pex/
          pexRunset_asap7 				: File created by Calibre Interactive to store the settings
                                                          specified in the PEX interface. This particular runset
							  points to the supplied parasitic extraction rule files.
    
▾ cdslib/						: Directory containing the ASAP7 technology file and technology
							  library, script to set up the PDK, sample cds.lib for
							  specifying both technology and design libraries, a display
							  resource file, and other files required for specifying tool
							  related paths and settings related to the Cadence Design
							  Framework II (DFII). 


  ▸ asap7_TechLib_10/					: ASAP7 technology library.
							  Any user-created design library must be attached to this technology library for 
							  designing with the ASAP7 PDK. It also contains ASAP7 transistors supplied for use
							  during transistor-level design. Both N-type and P-type MOSFETs come in four
							  Vt flavors, viz. regular Vt (RVT), low Vt (LVT), super-low Vt (SLVT), and
							  SRAM Vt. The latter is a special Vt layer provided for use in SRAMs. The
							  view 'symbol' must be used for the purpose of device instantiation. Defined
							  as 'asap7_TechLib' in the cds.lib.

  ▾ setup/						: Contains the setup files for Cadence Virtuoso.


      cds.lib						: Any libraries defined in this file appear in the Cadence
							  'Library Manager' window. Libraries are defined using the
							  keyword 'DEFINE', the library name, and path to that library. 
							  This particular file is copied to the user's local run
							  directory upon sourcing the setup script. It defines the
							  ASAP7 technology as well as standard cell library, and a
							  library 'sample'—bundled with the Cadence design
							  suite—containing logic gate symbols. It also includes another
							  cds.lib bundled with Cadence design suite, which defines the
							  following libraries from Cadence: 'cdsDefTechLib',
							  'analogLib', 'functional', 'rfLib', 'rfExamples', 'ahdlLib',
							  'basic', and 'US_8ths'.

      cdsenv						: Cadence environment variable file that allows for the
							  configuring of various Cadence environment related
							  settings. This particular cdsenv file also sets the x and y
							  snap spacing values, that specify the smallest incremental
							  amount by which the cursor moves in Cadence Virtuoso Layout
							  Editor, to 1 nm.

      cdsinit 						: Cadence initialization file containing SKILL code for
						          additional customization. Among other things, this particular
							  cdsinit file contains SKILL code that adds Calibre Interactive
							  to the Virtuoso Layout Editor tool menu.



      display.drf					: ASAP7 PDK display resource file that specifies the manner,
							  such as color and pattern, in which the PDK layers are
							  displayed in Virtuoso.

      rve_vis_asap7_*.cto				: CTO file intended for use with Calibre RVE. This file has been
							  created for the ease of viewing of layers associated with a
							  particular DRC when highlighting the DRC through Calibre RVE.

      setup_asap7.csh					: C Shell script to copy all the necessary files and
							  directories, such the Calibre directories and SVRF rule files,
							  HSpice models, cds.lib, .cdsinit, .cdsenv, and set_pdk_path.csh file,
							  required to use the PDK, into the user's local run directory.

▸ docs/							: Contains documents pertaining to the ASAP7 PDK.

▸ models/						: Contains HSpice transistor models that will be
							  used in ASAP7 PDK.
  ▾ hspice/
      7nm_FF.pm 					: HSpice model for the ASAP7 transistors for simulation at the
							  FF corner.

      7nm_SS.pm 					: HSpice model for the ASAP7 transistors for simulation at the
							  SS corner.

      7nm_TT.pm 					: HSpice model for the ASAP7 transistors for simulation at 
							  TT condition.

▸ asap7ssc7p5t_*					: A design library containing sample standard cells. Defined as 
							  'asap7ssc7p5t' in the cds.lib.


*--------------------------
* PDK Usage Instructions
*--------------------------

* Instructions to the administrator/course instructor for setting up the
* PDK 
*--------------------------------------------------------------------------

1. Copy the PDK 'asap7PDK_r1p7' (where 1p7 is the PDK version number) to an
   install area.

2. Change the environment variable value $PDK_DIR in the following files by
   replacing the string 'PDKDirectory' with the absolute path to the PDK
   directory (including the PDK directory name):

	./cdslib/setup/set_pdk_path.csh


* Instructions to the end-user for setting up a local PDK run directory
*--------------------------------------------------------------------------

   NOTE: Ask your course instructor/administrator for the path where the
   ASAP7 PDK is located. This path must replace any occurrence
   of the string 'PDKDirectory' so as to become the value for the
   environmental variable 'PDK_DIR' that you will need to use below for setting
   up the local PDK run directory.

   NOTE: Once the local PDK run directory has been setup, a user will only
   need to repeat steps 4. and 5. to start Virtuoso.

1. Create a local directory, whence you intend to run the PDK, under
   your home directory. This can be accomplished by using the following
   command for instance: 

   cd ; mkdir asap7_rundir


2. Set the environmental variable PDK_DIR using the following command, so
   that it points to the ASAP7 PDK directory:

   setenv PDK_DIR PDKDirectory


3. Go to the run directory created in the above step. Then use the
   following command : 

   source $PDK_DIR/cdslib/setup/setup_asap7.csh 


   NOTE: Source the aforementioned script just once when first setting up
   the local directory. You will not need to source this again when
   starting Virtuoso. If you do, then your old 'cds.lib' file will be
   replaced with a new one and all the user-defined libraries will be
   removed--which you will then need to define again. 

   Sourcing this script will copy all the necessary files and directories,
   such the Calibre directories and SVRF rule files, HSpice models, cds.lib,
   .cdsinit, .cdsenv, and set_pdk_path.csh file, required to use the PDK, into your
   run directory.

   For the ease of viewing of layers associated with a particular DRC when
   highlighting the DRC through Calibre RVE, add the following line to your
   startup script:

   setenv MGC_RVE_CTO_FILE $PWD/rve_vis_asap7.cto

4. Ensure that you are in the PDK run directory created in step 1.
   Also, ensure that you have sourced any startup scripts required for the
   various Cadence, Mentor Graphics, and Synopsys tools.
   Then type the following command.

   source set_pdk_path.csh

   Note that the above file also contains the environmental variables to
   specify the metal grids offsets from either X or Y axis, depending on the
   metal routing direction. The default offset value is 0 nm. To offset a
   particular grid by 'p' nm, specify the variable value as p*10. Thus, for an
   offset of 24 nm, the corresponding variable value is 240.

5. Start Virtuoso by typing:

   virtuoso &

*--------------------------------------------------------------------------
   NOTES 
*--------------------------------------------------------------------------

1. Well and substrate (p_sub) pins may be used as well/substrate tap
   substitutes for convenience when executing layout versus schematic (LVS)
   check at standard cell level. This requires connecting the pins 'VDD' and
   'VSS' by name through the use of LVS options. However, instead of
   employing these pins, physical substrate and well taps must be used at
   stipulated distances for latchup prevention when executing LVS at upper
   levels of a design hierarchy.
2. The Calibre parasitic extraction deck and runset provided with the PDK
   are meant for use with Calibre xACT 3D. 