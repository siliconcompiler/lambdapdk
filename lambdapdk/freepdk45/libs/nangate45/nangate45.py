import os
import siliconcompiler

########################
# SiliconCompiler Setup
########################

def setup(target=None):
    '''Nangate45 setup'''

    # get root
    root = os.path.dirname(__file__)

    # basic information
    libname = 'nangate45'
    process = 'freepdk45'
    stackup = '10M'
    libtype = '10t'
    version = 'r1p0'
    corner = 'typical'
    objectives = ['setup']

    # Create chip object
    chip = siliconcompiler.Chip(libname)

    # version
    chip.set('package', 'version', version)

    # hardened process/stackup
    chip.set('asic', 'pdk', process)
    chip.set('asic', 'stackup', stackup)

    # timing
    chip.add('model', 'timing', 'nldm', corner,
            f"{root}/nldm/NangateOpenCellLibrary_typical.lib")

    # lef
    chip.add('layout', 'database', libname, 'lef', stackup,
            f"{root}/lef/NangateOpenCellLibrary.macro.mod.lef")

    # gds
    chip.add('layout', 'database', libname, 'gds', stackup,
            f"{root}/gds/NangateOpenCellLibrary.gds")

    # driver
    chip.add('asic', 'cells','driver', "BUF_X4")

    # clock buffers
    chip.add('asic', 'cells','clkbuf', "BUF_X4")

    # tie cells
    chip.add('asic', 'cells','tie', ["LOGIC1_X1/Z",
                                     "LOGIC0_X1/Z"])

    # buffer cell
    chip.add('asic', 'cells', 'buf', ['BUF_X1/A/Z'])

    # hold cells
    chip.add('asic', 'cells', 'hold', "BUF_X1")

    # filler
    chip.add('asic', 'cells', 'filler', ["FILLCELL_X1",
                                         "FILLCELL_X2",
                                         "FILLCELL_X4",
                                         "FILLCELL_X8",
                                         "FILLCELL_X16",
                                         "FILLCELL_X32"])

    # Stupid small cells
    chip.add('asic', 'cells', 'ignore', ["AOI211_X1",
                                         "OAI211_X1"])

    # Tapcell
    chip.add('asic', 'cells','tap', "FILLCELL_X1")

    # Endcap
    chip.add('asic', 'cells','endcap', "FILLCELL_X1")

    return chip
#########################
if __name__ == "__main__":

    chip = setup()
    chip.write_manifest('nangate45.csv')
