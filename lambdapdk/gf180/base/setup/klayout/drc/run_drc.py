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

"""
Run GlobalFoundries 180nm MCU DRC.

Usage:
    run_drc.py (--help| -h)
    run_drc.py (--path=<file_path>) (--gf180mcu=<combined_options>) [--topcell=<topcell_name>] [--thr=<thr>] [--run_mode=<run_mode>] [--no_feol] [--no_beol] [--connectivity] [--density] [--density_only] [--antenna] [--antenna_only] [--no_offgrid]

Options:
    --help -h                           Print this help message.
    --path=<file_path>                  The input GDS file path.
    --gf180mcu=<combined_options>       Select combined options of metal_top, mim_option, and metal_level. Allowed values (A, B, C).
                                        gf180mcu=A: Select  metal_top=30K  mim_option=A  metal_level=3LM
                                        gf180mcu=B: Select  metal_top=11K  mim_option=B  metal_level=4LM
                                        gf180mcu=C: Select  metal_top=9K   mim_option=B  metal_level=5LM
    --topcell=<topcell_name>            Topcell name to use.
    --thr=<thr>                         The number of threads used in run.
    --run_mode=<run_mode>               Select klayout mode Allowed modes (flat , deep, tiling). [default: flat]
    --no_feol                           Turn off FEOL rules from running.
    --no_beol                           Turn off BEOL rules from running.
    --connectivity                      Turn on connectivity rules.
    --density                           Turn on Density rules.
    --density_only                      Turn on Density rules only.
    --antenna                           Turn on Antenna checks.
    --antenna_only                      Turn on Antenna checks only.
    --no_offgrid                        Turn off OFFGRID checking rules.
"""

from docopt import docopt
import os
import xml.etree.ElementTree as ET
import logging
import subprocess

def get_results(rule_deck,rules,lyrdb, type):

    mytree = ET.parse(f"{lyrdb}_{type}_gf{arguments['--gf180mcu']}.lyrdb")
    myroot = mytree.getroot()

    violated = []

    for lrule in rules:
        # Loop on database to get the violations of required rule
        for z in myroot[7]:
            if f"'{lrule}'" == f"{z[1].text}":
                violated.append(lrule)
                break

    lyrdb_clean = lyrdb.split("/") [-1]

    if len(violated) > 0:
        logging.error(f"\nTotal # of DRC violations in {rule_deck}.drc is {len(violated)}. Please check {lyrdb_clean}_{type}_gf{arguments['--gf180mcu']}.lyrdb file For more details")
        logging.info("Klayout GDS DRC Not Clean")
        logging.info(f"Violated rules are : {violated}\n")
    else:
        logging.info(f"\nCongratulations !!. No DRC Violations found in {lyrdb_clean} for {rule_deck}.drc rule deck with switch gf{arguments['--gf180mcu']}")
        logging.info("Klayout GDS DRC Clean\n")

def get_top_cell_names(gds_path):
    # klayout -b -r script.rb -rd infile=./layouts/caravel.gds.gz

    pdk_root = os.environ['PDK_ROOT']
    pdk      = os.environ['PDK']

    top_cell_names = list()
    proc = subprocess.Popen(['klayout','-b', '-r', f"{pdk_root}/{pdk}/utils/get_top_cell_names.rb", "-rd", "infile={}".format(gds_path)], stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        top_cell_names.append(line.decode().strip())

    return top_cell_names

def clean_gds_from_many_top_cells(gds_path, topcell):
    # klayout -b -r keep_single_top_cell.rb -rd infile=./layouts/caravel.gds.gz -rd topcell=chip_io -rd outfile=test.gds.gz

    pdk_root = os.environ['PDK_ROOT']
    pdk      = os.environ['PDK']

    basename = os.path.basename(gds_path)
    dirname = os.path.dirname(gds_path)
    main_file_name = basename.split(".")[0]
    output_file_path = os.path.join(dirname, "{}_single_top.gds.gz".format(main_file_name))

    proc = subprocess.Popen(['klayout','-b', '-r', f"{pdk_root}/{pdk}/utils/keep_single_top_cell.rb", "-rd", "infile={}".format(gds_path), "-rd", "topcell={}".format(topcell), "-rd", "outfile={}".format(output_file_path)], stdout=subprocess.PIPE)

    while True:
        line = proc.stdout.readline()
        if not line:
            break
        print(line.strip())
    return output_file_path

def main():

    # check gds file existance
    if os.path.exists(arguments["--path"]):
        pass
    else:
        logging.error("The input GDS file path doesn't exist, please recheck.")
        exit()

    # Env. variables
    pdk_root = os.environ['PDK_ROOT']
    pdk      = os.environ['PDK']

    # ======= Checking Klayout version =======
    klayout_v_ = os.popen("klayout -v").read()
    klayout_v_ = klayout_v_.split("\n")[0]
    klayout_v  = int (klayout_v_.split(".") [-1])

    logging.info(f"Your Klayout version is: {klayout_v_}"  )

    if klayout_v < 8:
        logging.info(f"Prerequisites at a minimum: KLayout 0.27.8")
        logging.error("Using this klayout version has not been assesed in this development. Limits are unknown")

    # Switches used in run
    switches = ''

    if arguments["--run_mode"] in ["flat" , "deep", "tiling"]:
        switches = switches + f'-rd run_mode={arguments["--run_mode"]} '
    else:
        logging.error("Allowed klayout modes are (flat , deep , tiling) only")
        exit()

    if   arguments["--gf180mcu"] == "A":   switches = switches + f'-rd metal_top=30K -rd mim_option=A -rd metal_level=3LM '
    elif arguments["--gf180mcu"] == "B":   switches = switches + f'-rd metal_top=11K -rd mim_option=B -rd metal_level=4LM '
    elif arguments["--gf180mcu"] == "C":   switches = switches + f'-rd metal_top=9K  -rd mim_option=B -rd metal_level=5LM '
    else:
        logging.error("gf180mcu switch allowed values are (A , B, C) only")
        exit()

    if arguments["--no_feol"]:      switches = switches + '-rd feol=false '
    else:                           switches = switches + '-rd feol=true  '

    if arguments["--no_beol"]:      switches = switches + '-rd beol=false '
    else:                           switches = switches + '-rd beol=true '

    if arguments["--no_offgrid"]:   switches = switches + '-rd offgrid=false '
    else:                           switches = switches + '-rd offgrid=true '

    if arguments["--connectivity"]: switches = switches + '-rd conn_drc=true '
    else:                           switches = switches + '-rd conn_drc=false '

    if arguments["--density"]:      switches = switches + '-rd density=true '
    else:                           switches = switches + '-rd density=false '

    # Generate databases
    if arguments["--path"]:
        path = arguments["--path"]
        topcell_name = arguments["--topcell"]

        if ".gds" in path:
            name_clean_= path.replace(".gds","")
            name_clean = name_clean_.split("/")[-1]

            tc_list = get_top_cell_names(path)
            if len(tc_list) < 2:
                topcell_name = tc_list[0]
            else:
                print("## File has multiple topcell names")
                # print("## File has multiple topcell names, must provide topcellname.")
                # if topcell_name is None:
                print("## Will have to stop.")
                exit()

            # if not topcell_name is None:
            switches = switches + f'-rd topcell={topcell_name}'

            # Removing old db
            os.system(f"rm -rf {name_clean_}_main_drc_gf{arguments['--gf180mcu']}.lyrdb {name_clean_}_antenna_gf{arguments['--gf180mcu']}.lyrdb {name_clean_}_density_gf{arguments['--gf180mcu']}.lyrdb")

            # Running DRC using klayout
            if (arguments["--antenna_only"]) and not (arguments["--density_only"]):
                logging.info(f"Running Global Foundries 180nm MCU antenna checks on design {name_clean} on cell {topcell_name}:")
                os.system(f"klayout -b -r $PDK_ROOT/$PDK/gf180mcu_antenna.drc -rd input={path} -rd report={name_clean}_antenna_gf{arguments['--gf180mcu']}_gf{arguments['--gf180mcu']}.lyrdb -rd thr={thrCount} {switches}")

            elif (arguments["--density_only"]) and not (arguments["--antenna_only"]):
                logging.info(f"Running Global Foundries 180nm MCU density checks on design {name_clean} on cell {topcell_name}:")
                os.system(f"klayout -b -r $PDK_ROOT/$PDK/gf180mcu_density.drc -rd input={path} -rd report={name_clean}_density_gf{arguments['--gf180mcu']}.lyrdb -rd thr={thrCount} {switches}")

            elif arguments["--antenna_only"] and arguments["--density_only"]:
                logging.info(f"Running Global Foundries 180nm MCU antenna checks on design {name_clean} on cell {topcell_name}:")
                os.system(f"klayout -b -r $PDK_ROOT/$PDK/gf180mcu_antenna.drc -rd input={path} -rd report={name_clean}_antenna_gf{arguments['--gf180mcu']}.lyrdb -rd thr={thrCount} {switches}")

                logging.info(f"Running Global Foundries 180nm MCU density checks on design {name_clean} on cell {topcell_name}:")
                os.system(f"klayout -b -r $PDK_ROOT/$PDK/gf180mcu_density.drc -rd input={path} -rd report={name_clean}_density_gf{arguments['--gf180mcu']}.lyrdb -rd thr={thrCount} {switches}")

            else:
                logging.info(f"Running main Global Foundries 180nm MCU runset on design {name_clean} on cell {topcell_name}:")
                os.system(f"klayout -b -r $PDK_ROOT/$PDK/gf180mcu.drc -rd input={path} -rd report={name_clean}_main_drc_gf{arguments['--gf180mcu']}.lyrdb -rd thr={thrCount} {switches}")
                if arguments["--antenna"]:
                    logging.info(f"Running Global Foundries 180nm MCU antenna checks on design {name_clean} on cell {topcell_name}:")
                    os.system(f"klayout -b -r $PDK_ROOT/$PDK/gf180mcu_antenna.drc -rd input={path} -rd report={name_clean}_antenna_gf{arguments['--gf180mcu']}.lyrdb -rd thr={thrCount} {switches}")
                if arguments["--density"]:
                    logging.info(f"Running Global Foundries 180nm MCU density checks on design {name_clean} on cell {topcell_name}:")
                    os.system(f"klayout -b -r $PDK_ROOT/$PDK/gf180mcu_density.drc -rd input={path} -rd report={name_clean}_density_gf{arguments['--gf180mcu']}.lyrdb -rd thr={thrCount} {switches}")
        else:
            logging.error("Script only support gds files, please select one")
            exit()
    else:
        logging.error("No provided gds file, please add one")
        exit()

    # ======================== Reporting results ========================
    rule_deck_path = [f"{pdk_root}/{pdk}/gf180mcu.drc" , f"{pdk_root}/{pdk}/gf180mcu_antenna.drc" , f"{pdk_root}/{pdk}/gf180mcu_density.drc"]

    # Get rules from rule deck
    rules = []

    # Get rules from rule deck
    for runset in rule_deck_path:
        with open(runset, 'r') as f:
            for line in f:
                if ".output" in line:
                    line_list = line.split('"')
                    if line_list[1] in rules:
                        pass
                    else:
                        rules.append(line_list[1])

    # Get results
    lyrdbs  = [ "main_drc"     , "antenna"          , "density"         ]
    runsets = [ "gf180mcu"     , "gf180mcu_antenna" , "gf180mcu_density"]
    for i,lyrdb in enumerate(lyrdbs):
        if os.path.exists(f"{name_clean_}_{lyrdb}_gf{arguments['--gf180mcu']}.lyrdb"):
            get_results(runsets[i],rules,name_clean_, lyrdb)

# ================================================================
# -------------------------- MAIN --------------------------------
# ================================================================

if __name__ == "__main__":

    # logs format
    logging.basicConfig(level=logging.DEBUG, format=f"%(asctime)s | %(levelname)-7s | %(message)s", datefmt='%d-%b-%Y %H:%M:%S')

    # arguments
    arguments     = docopt(__doc__, version='RUN DRC: 0.1')

    # No. of threads
    thrCount = os.cpu_count()*2 if arguments["--thr"] == None else int(arguments["--thr"])

    # Calling main function
    main()
