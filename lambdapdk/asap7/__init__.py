import os
import siliconcompiler

from pathlib import Path

from lambdapdk import register_data_source
from lambdapdk import LambdaPDK


class ASAP7PDK(LambdaPDK):
    def __init__(self):
        super().__init__()
        self.set_name("asap7")

        pdk_path = Path("lambdapdk", "asap7", "base")

        self.set_foundry("virtual")
        self.set_version("r1p7")
        self.set_node(7)
        self.set_stackup("10M")
        self.set_wafersize(300)
        self.set_scribewidth(0.1, 0.1)
        self.set_edgemargin(2)
        self.set_defectdensity(1.25)

        with self.active_dataroot("lambdapdk"):
            # APR Setup
            with self.active_fileset("views.lef"):
                self.add_file(pdk_path / "apr" / "asap7_tech.lef")
                for tool in ('openroad', 'klayout', 'magic'):
                    self.add_aprtechfileset(tool)

            with self.active_fileset("layermap"):
                self.add_file(pdk_path / "apr" / "asap7.layermap", filetype="layermap")

            with self.active_fileset("models.spice"):
                self.add_file(pdk_path / "spice" / "hspice" / "7nm.lib", filetype="library")
                self.add_devmodelfileset("xyce", "spice")

            # Klayout setup
            with self.active_fileset("klayout.techmap"):
                self.add_file(pdk_path / "setup" / "klayout" / "asap7.lyt", filetype="layermap")
                self.add_file(pdk_path / "setup" / "klayout" / "asap7.lyp", filetype="display")
                self.add_layermapfileset("klayout", "def", "klayout")
                self.add_displayfileset("klayout")
            self.add_layermapfileset("klayout", "def", "gds", fileset="layermap")

            self.set_aprroutinglayers(min="M2", max="M7")

            # OpenROAD setup
            self.set_openroad_rclayers(signal="M3", clock="M3")

            # Openroad global routing grid derating
            for layer, derate in [
                    ('M1', 0.25),
                    ('M2', 0.25),
                    ('M3', 0.25),
                    ('M4', 0.25),
                    ('M5', 0.25),
                    ('M6', 0.25),
                    ('M7', 0.25),
                    ('M8', 0.25),
                    ('M9', 0.25),
                    ('Pad', 0.25)]:
                self.set_openroad_globalroutingderating(layer, derate)

            self.add_openroad_pinlayers(vertical="M5", horizontal="M4")

            with self.active_fileset("openroad.routing"):
                # Relaxed routing rules
                self.add_file(pdk_path / "apr" / "openroad_relaxed_rules.tcl")

            # PEX
            with self.active_fileset("openroad.pex"):
                self.add_file(pdk_path / "pex" / "openroad" / "typical.tcl", filetype="tcl")
                self.add_file(pdk_path / "pex" / "openroad" / "typical.rules", filetype="openrcx")

                self.add_pexmodelfileset("openroad", "typical")
                self.add_pexmodelfileset("openroad-openrcx", "typical")


####################################################
# PDK Setup
####################################################
def setup():
    '''
    The asap7 PDK was developed at ASU in collaboration with ARM Research.
    With funding from the DARPA IDEA program, the PDK was released
    a permissive open source PDK in 2021. The PDK contains SPICE-compatible
    FinFET device models (BSIM-CMG), Technology files for Cadence Virtuoso,
    Design Rule Checker (DRC), Layout vs Schematic Checker (LVS) and
    Extraction Deck for the 7nm technology node. For more details regarding
    the technical specifications of the PDK, please refer the PDK
    documentation and associated publication. Note that this process
    design kit is provided as an academic and research aid only and the
    resulting designs are not manufacturable.

    PDK content:

    * open source DRM
    * device primitive library (virtuoso)
    * spice (hspice)
    * extraction runsets (calibre)
    * drc runsets (calibre)
    * APR technology files
    * 7.5 track multi-vt standard cell libraries

    More information:

    * https://asap.asu.edu/
    * L.T. Clark, V. Vashishtha, L. Shifren, A. Gujja, S. Sinha, B. Cline,
      C. Ramamurthya, and G. Yeric, “ASAP7: A 7-nm FinFET Predictive Process
      Design Kit,” Microelectronics Journal, vol. 53, pp. 105-115, July 2016.


    Sources: https://github.com/The-OpenROAD-Project/asap7

    .. warning::
       Work in progress (not ready for use)
    '''

    foundry = 'virtual'
    process = 'asap7'
    node = 7
    rev = 'r1p7'
    stackup = '10M'
    wafersize = 300
    libtype = '7p5t'
    pdkdir = os.path.join('lambdapdk', 'asap7', 'base')

    pdk = siliconcompiler.PDK(process, package='lambdapdk')
    register_data_source(pdk)

    # process name
    pdk.set('pdk', process, 'foundry', foundry)
    pdk.set('pdk', process, 'node', node)
    pdk.set('pdk', process, 'wafersize', wafersize)
    pdk.set('pdk', process, 'version', rev)
    pdk.set('pdk', process, 'stackup', stackup)

    # APR tech file
    for tool in ('openroad', 'klayout', 'magic'):
        pdk.set('pdk', process, 'aprtech', tool, stackup, libtype, 'lef',
                pdkdir + '/apr/asap7_tech.lef')

    pdk.set('pdk', process, 'minlayer', stackup, 'M2')
    pdk.set('pdk', process, 'maxlayer', stackup, 'M7')

    # Device models
    pdk.set('pdk', process, 'devmodel', 'xyce', 'hspice', stackup,
            pdkdir + '/spice/hspice/7nm.lib')

    # Klayout setup file
    pdk.set('pdk', process, 'layermap', 'klayout', 'def', 'klayout', stackup,
            pdkdir + '/setup/klayout/asap7.lyt')
    pdk.set('pdk', process, 'layermap', 'klayout', 'def', 'gds', stackup,
            pdkdir + '/apr/asap7.layermap')

    pdk.set('pdk', process, 'display', 'klayout', stackup,
            pdkdir + '/setup/klayout/asap7.lyp')

    # Openroad global routing grid derating
    openroad_layer_adjustments = {
        'M1': 0.25,
        'M2': 0.25,
        'M3': 0.25,
        'M4': 0.25,
        'M5': 0.25,
        'M6': 0.25,
        'M7': 0.25,
        'M8': 0.25,
        'M9': 0.25,
        'Pad': 1.0
    }
    for layer, adj in openroad_layer_adjustments.items():
        pdk.set('pdk', process, 'var', 'openroad', f'{layer}_adjustment', stackup, str(adj))

    pdk.set('pdk', process, 'var', 'openroad', 'rclayer_signal', stackup, 'M3')
    pdk.set('pdk', process, 'var', 'openroad', 'rclayer_clock', stackup, 'M3')

    pdk.set('pdk', process, 'var', 'openroad', 'pin_layer_vertical', stackup, 'M5')
    pdk.set('pdk', process, 'var', 'openroad', 'pin_layer_horizontal', stackup, 'M4')

    # PEX
    pdk.set('pdk', process, 'pexmodel', 'openroad', stackup, 'typical',
            pdkdir + '/pex/openroad/typical.tcl')
    pdk.set('pdk', process, 'pexmodel', 'openroad-openrcx', stackup, 'typical',
            pdkdir + '/pex/openroad/typical.rules')

    # Relaxed routing rules
    pdk.set('pdk', process, 'file', 'openroad', 'relax_routing_rules', stackup,
            pdkdir + '/apr/openroad_relaxed_rules.tcl')

    # Hide the DIEAREA layer 235/*.
    pdk.add('pdk', process, 'var', 'klayout', 'hide_layers', stackup, '235/0')
    pdk.add('pdk', process, 'var', 'klayout', 'hide_layers', stackup, '235/5')
    # Hide boundary layer
    pdk.add('pdk', process, 'var', 'klayout', 'hide_layers', stackup, '100/0')
    # Hide vt layers
    pdk.add('pdk', process, 'var', 'klayout', 'hide_layers', stackup, '97/0')
    pdk.add('pdk', process, 'var', 'klayout', 'hide_layers', stackup, '98/0')

    return pdk


#########################
if __name__ == "__main__":
    pdk = setup()
    register_data_source(pdk)
    pdk.check_filepaths()
