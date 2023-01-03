import siliconcompiler

########################
# SiliconCompiler Setup
########################

def setup(target=None):
    '''Freepdk45 setup'''

    # get root
    root = os.path.dirname(__file__)

    # basic information
    process = 'freepdk45'
    foundry = 'virtual'
    rev = 'r1p0'
    stackup = '10M'
    libtype = '10t'
    node = 45
    wafersize = 300
    hscribe = 0.1
    vscribe = 0.1
    edgemargin = 2
    d0 = 1.25

    # Create chip object
    chip = siliconcompiler.Chip(process)

    # process settings
    chip.set('pdk', process, 'foundry', foundry)
    chip.set('pdk', process, 'node', node)
    chip.set('pdk', process, 'version', rev)
    chip.set('pdk', process, 'stackup', stackup)
    chip.set('pdk', process, 'wafersize', wafersize)
    chip.set('pdk', process, 'edgemargin', edgemargin)
    chip.set('pdk', process, 'hscribe', hscribe)
    chip.set('pdk', process, 'vscribe', vscribe)
    chip.set('pdk', process, 'd0', d0)

    # APR tech file
    for tool in ('openroad', 'klayout', 'magic'):
        chip.set('pdk', process, 'aprtech', tool, stackup, libtype, 'lef',
                 f"{root}/apr/freepdk45.tech.lef")

    # Klayout setup file
    chip.set('pdk', process, 'layermap', 'klayout', 'def', 'gds', stackup,
             f"{root}/klayout/freepdk45.lyt")

    chip.set('pdk', process, 'display', 'klayout', stackup,
             f"{root}/klayout/freepdk45.lyp")
