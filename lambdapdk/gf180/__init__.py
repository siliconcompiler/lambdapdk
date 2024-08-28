
import siliconcompiler
from lambdapdk import register_data_source


####################################################
# PDK Setup
####################################################
def setup():
    '''
    The 'gf180' Open Source PDK is a collaboration between Google and
    Global Foundries to provide a fully open source Process
    Design Kit and related resources, which can be used to create
    manufacturable designs at Global Foundries facility.

    ... GF180 Process Highlights:

    * 180nm process
    * 11 metal stack options from 3 to 6 metal levels

    PDK content:

    * multiple standard digital cell libraries
    * primitive cell libraries and models for creating analog designs
    * EDA support files for multiple open source and proprietary flows

    More information:

    * https://gf180mcu-pdk.readthedocs.io/

    Sources:

    * https://github.com/google/gf180mcu-pdk
    '''

    foundry = 'globalfoundries'
    process = 'gf180'

    node = 180

    pdkdir = "lambdapdk/gf180/base/"

    pdk = siliconcompiler.PDK(process, package='lambdapdk')
    register_data_source(pdk)

    # process name
    pdk.set('pdk', process, 'foundry', foundry)
    pdk.set('pdk', process, 'node', node)
    pdk.set('pdk', process, 'wafersize', 200)

    for stackup in ("3LM_1TM_6K",
                    "3LM_1TM_9K",
                    "3LM_1TM_11K",
                    "3LM_1TM_30K",
                    "4LM_1TM_6K",
                    "4LM_1TM_9K",
                    "4LM_1TM_11K",
                    "4LM_1TM_30K",
                    "5LM_1TM_9K",
                    "5LM_1TM_11K",
                    "6LM_1TM_9K"):
        pdk.add('pdk', process, 'stackup', stackup)
        for libtype in ("7t", "9t"):
            # APR Setup
            for tool in ('openroad', 'klayout', 'magic'):
                pdk.set('pdk', process, 'aprtech', tool, stackup, libtype, 'lef',
                        pdkdir + f'/apr/gf180mcu_{stackup}_{libtype}_tech.lef')
        if stackup in ('6LM_1TM_9K', '5LM_1TM_9K'):
            pdk.set('pdk', process, 'layermap', 'klayout', 'def', 'gds', stackup,
                    pdkdir + f'/apr/gf180mcu_{stackup}_9t_edi2gds.layermap')
        max_layer = int(stackup[0])

        pdk.set('pdk', process, 'minlayer', stackup, 'Metal1')
        pdk.set('pdk', process, 'maxlayer', stackup, f'Metal{max_layer}')

        # Layer map and display file
        pdk.set('pdk', process, 'layermap', 'klayout', 'def', 'klayout', stackup,
                pdkdir + '/setup/klayout/tech/gf180mcu.lyt')
        pdk.set('pdk', process, 'display', 'klayout', stackup,
                pdkdir + '/setup/klayout/tech/gf180mcu.lyp')

        # Device models
        pdk.add('pdk', process, 'devmodel', 'xyce', 'spice', stackup,
                pdkdir + '/spice/xyce/design.xyce')
        pdk.add('pdk', process, 'devmodel', 'xyce', 'spice', stackup,
                pdkdir + '/spice/xyce/sm141064.xyce')
        pdk.add('pdk', process, 'devmodel', 'xyce', 'spice', stackup,
                pdkdir + '/spice/xyce/smbb000149.xyce')

        # Openroad global routing grid derating
        openroad_layer_adjustments = {
                'Metal1': 0.0,
                'Metal2': 0.0,
                'Metal3': 0.0,
                'Metal4': 0.0,
                'Metal5': 0.0,
                'Metal6': 0.0,
                'MetalTop': 1.0
        }
        for layer, adj in openroad_layer_adjustments.items():
            pdk.set('pdk', process, 'var', 'openroad', f'{layer}_adjustment', stackup, str(adj))
            if layer == pdk.get('pdk', process, 'maxlayer', stackup):
                break

        if max_layer == 2:
            pdk.set('pdk', process, 'var', 'openroad', 'rclayer_signal', stackup, 'Metal2')
            pdk.set('pdk', process, 'var', 'openroad', 'rclayer_clock', stackup, 'Metal2')

            pdk.set('pdk', process, 'var', 'openroad', 'pin_layer_vertical', stackup, 'Metal2')
            pdk.set('pdk', process, 'var', 'openroad', 'pin_layer_horizontal', stackup, 'Metal1')
        elif max_layer == 3:
            pdk.set('pdk', process, 'var', 'openroad', 'rclayer_signal', stackup, 'Metal2')
            pdk.set('pdk', process, 'var', 'openroad', 'rclayer_clock', stackup, 'Metal2')

            pdk.set('pdk', process, 'var', 'openroad', 'pin_layer_vertical', stackup, 'Metal2')
            pdk.set('pdk', process, 'var', 'openroad', 'pin_layer_horizontal', stackup, 'Metal3')
        elif max_layer == 4:
            pdk.set('pdk', process, 'var', 'openroad', 'rclayer_signal', stackup, 'Metal2')
            pdk.set('pdk', process, 'var', 'openroad', 'rclayer_clock', stackup, 'Metal3')

            pdk.set('pdk', process, 'var', 'openroad', 'pin_layer_vertical', stackup, 'Metal4')
            pdk.set('pdk', process, 'var', 'openroad', 'pin_layer_horizontal', stackup, 'Metal3')
        elif max_layer >= 5:
            pdk.set('pdk', process, 'var', 'openroad', 'rclayer_signal', stackup, 'Metal3')
            pdk.set('pdk', process, 'var', 'openroad', 'rclayer_clock', stackup, 'Metal4')

            pdk.set('pdk', process, 'var', 'openroad', 'pin_layer_vertical', stackup, 'Metal4')
            pdk.set('pdk', process, 'var', 'openroad', 'pin_layer_horizontal', stackup, 'Metal3')

        # PEX
        for corner in ["bst", "typ", "wst"]:
            if stackup in ('3LM_1TM_6K', '3LM_1TM_9K', '3LM_1TM_11K', '3LM_1TM_30K', '4LM_1TM_6K'):
                continue
            base_name = f'gf180mcu_1p{stackup.replace("L", "").lower()}_sp_smim_OPTB_{corner}'
            pdk.set('pdk', process, 'pexmodel', 'openroad', stackup, corner,
                    pdkdir + '/pex/openroad/' + base_name + '.tcl')
            pdk.set('pdk', process, 'pexmodel', 'openroad-openrcx', stackup, corner,
                    pdkdir + '/pex/openroad/' + base_name + '.rules')

        pdk.add('pdk', process, 'var', 'klayout', 'hide_layers', stackup, 'Dualgate')
        pdk.add('pdk', process, 'var', 'klayout', 'hide_layers', stackup, 'V5_XTOR')
        pdk.add('pdk', process, 'var', 'klayout', 'hide_layers', stackup, 'PR_bndry')

    return pdk


#########################
if __name__ == "__main__":
    pdk = setup(siliconcompiler.Chip('<pdk>'))
    pdk.write_manifest(f'{pdk.top()}.json')
    pdk.check_filepaths()
