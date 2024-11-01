import os
import siliconcompiler
from lambdapdk import register_data_source


stackups = []
for m in ("3ML", "4ML", "5ML"):
    for w in ("0400", "0800", "2000", "0400_2000"):
        stackups.append(f'{m}_{w}')


####################################################
# PDK Setup
####################################################
def setup():
    '''
    The interposer PDK is a passive technology with a number of
    simulated stackups. The PDK contains enablement for place and
    route tools and design rule signoff.
    Note that this process design kit is provided as an academic
    and research aid only and the resulting designs are not manufacturable.
    '''

    foundry = 'virtual'
    process = 'interposer'

    libtype = 'none'

    node = 130
    # TODO: dummy numbers, only matter for cost estimation
    wafersize = 300
    hscribe = 0.1
    vscribe = 0.1
    edgemargin = 2

    pdkdir = os.path.join('lambdapdk', 'interposer', 'base')

    pdk = siliconcompiler.PDK(process, package='lambdapdk')
    register_data_source(pdk)

    # process name
    pdk.set('pdk', process, 'foundry', foundry)
    pdk.set('pdk', process, 'node', node)
    pdk.set('pdk', process, 'version', 'v0.0.1')
    pdk.set('pdk', process, 'stackup', stackups)
    pdk.set('pdk', process, 'wafersize', wafersize)
    pdk.set('pdk', process, 'edgemargin', edgemargin)
    pdk.set('pdk', process, 'scribe', (hscribe, vscribe))

    # APR Setup
    for stackup in stackups:
        for tool in ('openroad', 'klayout', 'magic'):
            pdk.set('pdk', process, 'aprtech', tool, stackup, libtype, 'lef',
                    pdkdir + f'/apr/{stackup}.lef')

        pdk.set('pdk', process, 'minlayer', stackup, 'metal1')
        pdk.set('pdk', process, 'maxlayer', stackup, 'topmetal')

        # DRC Runsets
        pdk.set('pdk', process, 'drc', 'runset', 'klayout', stackup, 'drc',
                pdkdir + f'/setup/klayout/{stackup}.drc')

        key = 'drc_params:drc'
        pdk.add('pdk', process, 'var', 'klayout', stackup, key, 'input=<input>')
        pdk.add('pdk', process, 'var', 'klayout', stackup, key, 'topcell=<topcell>')
        pdk.add('pdk', process, 'var', 'klayout', stackup, key, 'report=<report>')
        pdk.add('pdk', process, 'var', 'klayout', stackup, key, 'threads=<threads>')

        # Layer map and display file
        pdk.set('pdk', process, 'layermap', 'klayout', 'def', 'gds', stackup,
                pdkdir + f'/apr/{stackup}.layermap')
        pdk.set('pdk', process, 'display', 'klayout', stackup,
                pdkdir + f'/setup/klayout/{stackup}.lyp')

        pdk.set('pdk', process, 'aprtech', 'openroad', stackup, libtype, 'fill',
                pdkdir + f'/dfm/openroad/{stackup}.fill.json')

        # Openroad global routing grid derating
        openroad_layer_adjustments = {
            'metal1': 0.20,
            'metal2': 0.20,
            'metal3': 0.20,
            'metal4': 0.20,
            'metal5': 0.20,
            'metal6': 0.20,
            'topmetal': 0.20
        }
        for layer, adj in openroad_layer_adjustments.items():
            if layer != 'topmetal' and int(layer[-1]) >= int(stackup[0]):
                continue
            pdk.set('pdk', process, 'var', 'openroad', f'{layer}_adjustment', stackup, adj)

        pdk.set('pdk', process, 'var', 'openroad', 'rclayer_signal', stackup, 'metal2')
        pdk.set('pdk', process, 'var', 'openroad', 'rclayer_clock', stackup, 'metal2')

        pdk.set('pdk', process, 'var', 'openroad', 'pin_layer_vertical', stackup, 'metal2')
        pdk.set('pdk', process, 'var', 'openroad', 'pin_layer_horizontal', stackup, 'metal3')

        # PEX
        for corner in ["minimum", "typical", "maximum"]:
            pdk.set('pdk', process, 'pexmodel', 'openroad', stackup, corner,
                    pdkdir + '/pex/openroad/' + stackup + '.' + corner + '.tcl')

    return pdk


#########################
if __name__ == "__main__":
    pdk = setup()
    pdk.write_manifest(f'{pdk.top()}.json')
    pdk.check_filepaths()
