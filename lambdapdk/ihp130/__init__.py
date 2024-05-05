
import os
import siliconcompiler
from lambdapdk import register_data_source


pdk_rev = '87764498e0f2118c69396b16a46ce91b46305341'


def register_ihp130_data_source(chip):
    chip.register_package_source(
        'ihp130',
        path='git+https://github.com/IHP-GmbH/IHP-Open-PDK',
        ref=pdk_rev)


####################################################
# PDK Setup
####################################################
def setup(chip):
    '''
    The 'skywater130' Open Source PDK is a collaboration between Google and
    SkyWater Technology Foundry to provide a fully open source Process
    Design Kit and related resources, which can be used to create
    manufacturable designs at SkyWater's facility.

    Skywater130 Process Highlights:

    * 130nm process
    * support for internal 1.8V with 5.0V I/Os (operable at 2.5V)
    * 1 level of local interconnect
    * 5 levels of metal

    PDK content:

    * An open source design rule manual
    * multiple standard digital cell libraries
    * primitive cell libraries and models for creating analog designs
    * EDA support files for multiple open source and proprietary flows

    More information:

    * https://skywater-pdk.readthedocs.io/

    Sources:

    * https://github.com/google/skywater-pdk
    '''

    foundry = 'ihp'
    process = 'ihp130'
    stackup = '5M2TL'

    node = 130
    # TODO: dummy numbers, only matter for cost estimation
    wafersize = 300
    hscribe = 0.1
    vscribe = 0.1
    edgemargin = 2

    lpdkdir = os.path.join('lambdapdk', 'ihp130', 'base')

    pdk = siliconcompiler.PDK(chip, process, package='ihp130')
    register_ihp130_data_source(pdk)
    register_data_source(pdk)

    # process name
    pdk.set('pdk', process, 'foundry', foundry)
    pdk.set('pdk', process, 'node', node)
    pdk.set('pdk', process, 'version', pdk_rev)
    pdk.set('pdk', process, 'stackup', stackup)
    pdk.set('pdk', process, 'wafersize', wafersize)
    pdk.set('pdk', process, 'edgemargin', edgemargin)
    pdk.set('pdk', process, 'hscribe', hscribe)
    pdk.set('pdk', process, 'vscribe', vscribe)

    # APR Setup
    # TODO: remove libtype
    for tool in ('openroad', 'klayout', 'magic'):
        # Add unithd for backwards compatibility
        pdk.set('pdk', process, 'aprtech', tool, stackup, '9t', 'lef',
                'ihp-sg13g2/libs.ref/sg13g2_stdcell/lef/sg13g2_tech.lef')

    pdk.set('pdk', process, 'minlayer', stackup, 'Metal2')
    pdk.set('pdk', process, 'maxlayer', stackup, 'Metal5')

    # DRC Runsets
#     pdk.set('pdk', process, 'drc', 'runset', 'magic', stackup, 'basic',
#             pdkdir + '/setup/magic/sky130A.tech')

    # LVS Runsets
#     pdk.set('pdk', process, 'lvs', 'runset', 'netgen', stackup, 'basic',
#             pdkdir + '/setup/netgen/lvs_setup.tcl')

    # Layer map and display file
    pdk.set('pdk', process, 'layermap', 'klayout', 'def', 'klayout', stackup,
            'ihp-sg13g2/libs.tech/klayout/tech/sg13g2.lyt')
    pdk.set('pdk', process, 'display', 'klayout', stackup,
            'ihp-sg13g2/libs.tech/klayout/tech/sg13g2.lyp')

    pdk.set('pdk', process, 'layermap', 'klayout', 'def', 'gds', stackup,
            'ihp-sg13g2/libs.tech/klayout/tech/sg13g2.map')

    # Openroad global routing grid derating
    openroad_layer_adjustments = {
        'Metal1': 0.05,
        'Metal2': 0.05,
        'Metal3': 0.05,
        'Metal4': 0.05,
        'Metal5': 0.05,
        'TopMetal1': 0.00,
        'TopMetal2': 0.00,
    }
    for layer, adj in openroad_layer_adjustments.items():
        pdk.set('pdk', process, 'var', 'openroad', f'{layer}_adjustment', stackup, str(adj))

    pdk.set('pdk', process, 'var', 'openroad', 'rclayer_signal', stackup, 'Metal2')
    pdk.set('pdk', process, 'var', 'openroad', 'rclayer_clock', stackup, 'Metal5')

    pdk.set('pdk', process, 'var', 'openroad', 'pin_layer_vertical', stackup, 'Metal3')
    pdk.set('pdk', process, 'var', 'openroad', 'pin_layer_horizontal', stackup, 'Metal2')

    # PEX
    for corner in ["typical"]:
        pdk.set('pdk', process, 'pexmodel', 'openroad', stackup, corner,
                lpdkdir + '/pex/openroad/' + corner + '.tcl', package='lambdapdk')
        pdk.set('pdk', process, 'pexmodel', 'openroad-openrcx', stackup, corner,
                lpdkdir + '/pex/openroad/' + corner + '.rules', package='lambdapdk')

    return pdk


#########################
if __name__ == "__main__":
    pdk = setup(siliconcompiler.Chip('<pdk>'))
    pdk.write_manifest(f'{pdk.top()}.json')
