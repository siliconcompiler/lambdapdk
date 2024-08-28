
import os
import siliconcompiler
from lambdapdk import register_data_source


####################################################
# PDK Setup
####################################################
def setup():
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

    foundry = 'skywater'
    process = 'skywater130'
    rev = 'v0_0_2'
    stackup = '5M1LI'

    node = 130
    # TODO: dummy numbers, only matter for cost estimation
    wafersize = 300
    hscribe = 0.1
    vscribe = 0.1
    edgemargin = 2

    pdkdir = os.path.join('lambdapdk', 'sky130', 'base')

    pdk = siliconcompiler.PDK(process, package='lambdapdk')
    register_data_source(pdk)

    # process name
    pdk.set('pdk', process, 'foundry', foundry)
    pdk.set('pdk', process, 'node', node)
    pdk.set('pdk', process, 'version', rev)
    pdk.set('pdk', process, 'stackup', stackup)
    pdk.set('pdk', process, 'wafersize', wafersize)
    pdk.set('pdk', process, 'edgemargin', edgemargin)
    pdk.set('pdk', process, 'scribe', (hscribe, vscribe))

    # APR Setup
    # TODO: remove libtype
    for tool in ('openroad', 'klayout', 'magic'):
        for libtype in ('hd', 'hdll'):
            pdk.set('pdk', process, 'aprtech', tool, stackup, libtype, 'lef',
                    pdkdir + f'/apr/sky130_fd_sc_{libtype}.tlef')

    pdk.set('pdk', process, 'minlayer', stackup, 'met1')
    pdk.set('pdk', process, 'maxlayer', stackup, 'met5')

    # DRC Runsets
    pdk.set('pdk', process, 'drc', 'runset', 'magic', stackup, 'basic',
            pdkdir + '/setup/magic/sky130A.tech')

    # LVS Runsets
    pdk.set('pdk', process, 'lvs', 'runset', 'netgen', stackup, 'basic',
            pdkdir + '/setup/netgen/lvs_setup.tcl')

    # Layer map and display file
    pdk.set('pdk', process, 'layermap', 'klayout', 'def', 'klayout', stackup,
            pdkdir + '/setup/klayout/skywater130.lyt')
    pdk.set('pdk', process, 'display', 'klayout', stackup, pdkdir + '/setup/klayout/sky130A.lyp')

    # Openroad global routing grid derating
    openroad_layer_adjustments = {
        'li1': 1.0,
        'met1': 0.3,
        'met2': 0.3,
        'met3': 0.3,
        'met4': 0.3,
        'met5': 0.3
    }
    for layer, adj in openroad_layer_adjustments.items():
        pdk.set('pdk', process, 'var', 'openroad', f'{layer}_adjustment', stackup, str(adj))

    pdk.set('pdk', process, 'var', 'openroad', 'rclayer_signal', stackup, 'met2')
    pdk.set('pdk', process, 'var', 'openroad', 'rclayer_clock', stackup, 'met5')

    pdk.set('pdk', process, 'var', 'openroad', 'pin_layer_vertical', stackup, 'met2')
    pdk.set('pdk', process, 'var', 'openroad', 'pin_layer_horizontal', stackup, 'met3')

    # Hide the 81/4 'areaid.standardc' layer by default; it puts opaque purple over most core areas.
    pdk.set('pdk', process, 'var', 'klayout', 'hide_layers', stackup, ['areaid.standardc'])

    # PEX
    for corner in ["minimum", "typical", "maximum"]:
        pdk.set('pdk', process, 'pexmodel', 'openroad', stackup, corner,
                pdkdir + '/pex/openroad/' + corner + '.tcl')
        pdk.set('pdk', process, 'pexmodel', 'openroad-openrcx', stackup, corner,
                pdkdir + '/pex/openroad/' + corner + '.rules')

    return pdk


#########################
if __name__ == "__main__":
    pdk = setup(siliconcompiler.Chip('<pdk>'))
    pdk.write_manifest(f'{pdk.top()}.json')
