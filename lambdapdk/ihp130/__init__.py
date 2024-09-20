
import os
import siliconcompiler
from lambdapdk import register_data_source


pdk_rev = '89c8038db331ccfdf6be488dfc4670cb62ba3c42'


def register_ihp130_data_source(chip):
    chip.register_source(
        'ihp130',
        path='git+https://github.com/IHP-GmbH/IHP-Open-PDK',
        ref=pdk_rev)


####################################################
# PDK Setup
####################################################
def setup():
    '''
    130nm BiCMOS Open Source PDK, dedicated for Analog/Digital, Mixed Signal and RF Design

    IHP Open Source PDK project goal is to provide a fully open source Process Design Kit and
    related data, which can be used to create manufacturable designs at IHP's facility.

    SG13G2 is a high performance BiCMOS technology with a 0.13 μm CMOS process.
    It contains bipolar devices based on SiGe:C npn-HBT's with up to 350 GHz transition frequency
    (fT) and 450 GHz oscillation frequency (fmax).
    This process provides 2 gate oxides:
    A thin gate oxide for the 1.2 V digital logic and a thick oxide for a 3.3 V supply voltage.
    For both modules NMOS, PMOS and isolated NMOS transistors are offered.
    Further passive components like poly silicon resistors and MIM capacitors are available.
    The backend option offers 5 thin metal layers, two thick metal layers (2 and 3 μm thick) and
    a MIM layer.

    Sources:

    * https://github.com/IHP-GmbH/IHP-Open-PDK
    '''

    foundry = 'Leibniz-Institut für innovative Mikroelektronik'
    process = 'ihp130'
    stackup = '5M2TL'

    node = 130
    # TODO: dummy numbers, only matter for cost estimation
    wafersize = 300
    hscribe = 0.1
    vscribe = 0.1
    edgemargin = 2

    lpdkdir = os.path.join('lambdapdk', 'ihp130', 'base')

    pdk = siliconcompiler.PDK(process, package='ihp130')
    register_ihp130_data_source(pdk)
    register_data_source(pdk)

    # process name
    pdk.set('pdk', process, 'foundry', foundry)
    pdk.set('pdk', process, 'node', node)
    pdk.set('pdk', process, 'version', pdk_rev)
    pdk.set('pdk', process, 'stackup', stackup)
    pdk.set('pdk', process, 'wafersize', wafersize)
    pdk.set('pdk', process, 'edgemargin', edgemargin)
    pdk.set('pdk', process, 'scribe', (hscribe, vscribe))

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
        'Metal1': 0.25,
        'Metal2': 0.25,
        'Metal3': 0.25,
        'Metal4': 0.25,
        'Metal5': 0.25,
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

    # Documentation
    pdk.set('pdk', process, 'doc', 'overview',
            'ihp-sg13g2/libs.doc/doc/SG13G2_os_process_spec.pdf')
    pdk.set('pdk', process, 'doc', 'drc_rules',
            'ihp-sg13g2/libs.doc/doc/SG13G2_os_layout_rules.pdf')

    return pdk


#########################
if __name__ == "__main__":
    pdk = setup(siliconcompiler.Chip('<pdk>'))
    pdk.write_manifest(f'{pdk.top()}.json')
