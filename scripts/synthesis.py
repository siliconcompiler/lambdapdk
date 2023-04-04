################################################################################
# Script for auto-generatinv lambda views using Yosys
###############################################################################

import glob
import re
import os
import siliconcompiler

# Get List of stdlib cells in lambdalib
cells = glob.glob('submodules/lambdalib/stdlib/rtl/la_*.v')

exclude = ['la_decap',
           'la_keeper',
           'la_footer',
           'la_header',
           'la_antenna',
           ]

# TODO: make script less janky

pdks ={};

pdks['sky130'] = {}
pdks['sky130']['target'] = 'skywater130_demo'
pdks['sky130']['libs'] = ['sky130hd']


pdks['freepdk45'] = {}
pdks['freepdk45']['target'] = 'freepdk45_demo'
pdks['freepdk45']['libs'] = ['nangate45']

#TODO: ASAP7 misbehaving...
#ERROR: FF la_dffsqn.qn_$_DFF_PN0__Q (type $_DFF_PN0_) cannot be legalized: dffs with async set or reset are not supported

#pdks['asap7'] = {}
#pdks['asap7']['target'] = 'asap7_demo'
#pdks['asap7']['libs'] = ['asap7sc7p5t_rvt',
#                         'asap7sc7p5t_lvt',
#                         'asap7sc7p5t_slvt']

for pdk in pdks.keys():
    target = pdks[pdk]['target']
    builddir = f'build_{pdk}'
    for lib in pdks[pdk]['libs']:
        os.system(f'mkdir -p lambdapdk/{pdk}/libs/{lib}/lambda')
        for verilog in cells:
            design = re.match(r'.*?(\w+)\.v', verilog).group(1)
            if (design not in exclude):
                # don't rerun
                if not os.path.isdir(f"{builddir}/{design}"):
                    chip = siliconcompiler.Chip(design)
                    chip.input(verilog)
                    chip.load_target(target)
                    chip.set('asic', 'logiclib', lib)
                    chip.set('option', 'builddir', builddir)
                    chip.set('option', 'steplist', ['import', 'syn'])
                    chip.set('option', 'quiet', True)
                    chip.run()
                # copy cells into tree
                os.system(f"cp {builddir}/{design}/job0/syn/0/outputs/{design}.vg lambdapdk/{pdk}/libs/{lib}/lambda")
