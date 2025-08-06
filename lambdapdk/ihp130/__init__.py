
import os
import siliconcompiler

from pathlib import Path

from lambdapdk import register_data_source
from lambdapdk import LambdaPDK


pdk_rev = '0854e9bcd558b68c573149038b4c95706314e2f1'


class IHP130PDK(LambdaPDK):
    def __init__(self):
        super().__init__()
        self.set_name("ihp130")

        self.set_dataroot("ihp130", "git+https://github.com/IHP-GmbH/IHP-Open-PDK", pdk_rev)

        self.set_foundry("Leibniz-Institut für innovative Mikroelektronik")
        self.set_version(pdk_rev)
        self.set_node(130)
        self.set_stackup("5M2TL")

        pdk_path = Path("lambdapdk", "ihp130", "base")

        # Docs
        with self.active_dataroot("ihp130"):
            self.add_doc("overview", "ihp-sg13g2/libs.doc/doc/SG13G2_os_process_spec.pdf")
            self.add_doc("drc_rules", "ihp-sg13g2/libs.doc/doc/SG13G2_os_layout_rules.pdf")

        with self.active_dataroot("ihp130"):
            # APR Setup
            with self.active_fileset("views.lef"):
                self.add_file("ihp-sg13g2/libs.ref/sg13g2_stdcell/lef/sg13g2_tech.lef")
                for tool in ('openroad', 'klayout', 'magic'):
                    self.add_aprtechfileset(tool)

            with self.active_fileset("layermap"):
                self.add_file("ihp-sg13g2/libs.tech/klayout/tech/sg13g2.map", filetype="layermap")

        self.set_aprroutinglayers(min="Metal2", max="Metal5")

        # Klayout setup
        with self.active_dataroot("ihp130"):
            with self.active_fileset("klayout.techmap"):
                self.add_file("ihp-sg13g2/libs.tech/klayout/tech/sg13g2.lyt", filetype="layermap")
                self.add_file("ihp-sg13g2/libs.tech/klayout/tech/sg13g2.lyp", filetype="display")
                self.add_layermapfileset("klayout", "def", "klayout")
                self.add_displayfileset("klayout")
            self.add_layermapfileset("klayout", "def", "gds", fileset="layermap")

        # OpenROAD setup
        self.set_openroad_rclayers(signal="Metal2", clock="Metal5")
        self.add_openroad_pinlayers(vertical="Metal3", horizontal="Metal2")

        # Openroad global routing grid derating
        openroad_layer_adjustments = {
            'Metal1': 0.25,
            'Metal2': 0.25,
            'Metal3': 0.25,
            'Metal4': 0.25,
            'Metal5': 0.25,
            'TopMetal1': 0.00,
            'TopMetal2': 0.00
        }
        for layer, adj in openroad_layer_adjustments.items():
            self.set_openroad_globalroutingderating(layer, adj)

        # PEX
        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("openroad.pex"):
                self.add_file(pdk_path / "pex" / "openroad" / "typical.tcl", filetype="tcl")
                self.add_file(pdk_path / "pex" / "openroad" / "typical.rules", filetype="openrcx")

                self.add_pexmodelfileset("openroad", "typical")
                self.add_pexmodelfileset("openroad-openrcx", "typical")

        # DRC
        drcs = {
            "maximal": 'ihp-sg13g2/libs.tech/klayout/tech/drc/sg13g2_maximal.lydrc',
            "minimal": 'ihp-sg13g2/libs.tech/klayout/tech/drc/sg13g2_minimal.lydrc'
        }
        for drc, runset in drcs.items():
            with self.active_fileset(f"klayout.drc.{drc}"):
                self.add_file(runset, filetype="drc")
                self.add_runsetfileset("drc", "klayout", drc)

            self.add_klayout_drcparam(drc, "in_gds=<input>")
            self.add_klayout_drcparam(drc, "cell=<topcell>")
            self.add_klayout_drcparam(drc, "report_file=<report>")


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

    SG13G2 is a high performance BiCMOS technology with a 0.13 um CMOS process.
    It contains bipolar devices based on SiGe:C npn-HBT's with up to 350 GHz transition frequency
    (fT) and 450 GHz oscillation frequency (fmax).
    This process provides 2 gate oxides:
    A thin gate oxide for the 1.2 V digital logic and a thick oxide for a 3.3 V supply voltage.
    For both modules NMOS, PMOS and isolated NMOS transistors are offered.
    Further passive components like poly silicon resistors and MIM capacitors are available.
    The backend option offers 5 thin metal layers, two thick metal layers (2 and 3 um thick) and
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

    pdk.set('pdk', process, 'var', 'openroad', 'pin_layer_vertical', stackup, 'Metal2')
    pdk.set('pdk', process, 'var', 'openroad', 'pin_layer_horizontal', stackup, 'Metal3')

    # PEX
    for corner in ["typical"]:
        pdk.set('pdk', process, 'pexmodel', 'openroad', stackup, corner,
                lpdkdir + '/pex/openroad/' + corner + '.tcl', package='lambdapdk')
        pdk.set('pdk', process, 'pexmodel', 'openroad-openrcx', stackup, corner,
                lpdkdir + '/pex/openroad/' + corner + '.rules', package='lambdapdk')

    # DRC
    drcs = {
        "maximal": 'ihp-sg13g2/libs.tech/klayout/tech/drc/sg13g2_maximal.lydrc',
        "minimal": 'ihp-sg13g2/libs.tech/klayout/tech/drc/sg13g2_minimal.lydrc'
    }
    for drc, runset in drcs.items():
        pdk.set('pdk', process, 'drc', 'runset', 'klayout', stackup, drc, runset)

        key = f'drc_params:{drc}'
        pdk.add('pdk', process, 'var', 'klayout', stackup, key, 'in_gds=<input>')
        pdk.add('pdk', process, 'var', 'klayout', stackup, key, 'cell=<topcell>')
        pdk.add('pdk', process, 'var', 'klayout', stackup, key, 'report_file=<report>')

    # Documentation
    pdk.set('pdk', process, 'doc', 'overview',
            'ihp-sg13g2/libs.doc/doc/SG13G2_os_process_spec.pdf')
    pdk.set('pdk', process, 'doc', 'drc_rules',
            'ihp-sg13g2/libs.doc/doc/SG13G2_os_layout_rules.pdf')

    return pdk


#########################
if __name__ == "__main__":
    pdk = setup()
    pdk.write_manifest(f'{pdk.top()}.json')
    pdk.check_filepaths()
