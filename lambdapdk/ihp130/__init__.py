from pathlib import Path

from lambdapdk import LambdaPDK, _LambdaPath


pdk_rev = '0854e9bcd558b68c573149038b4c95706314e2f1'


class _IHP130Path(_LambdaPath):
    def __init__(self):
        super().__init__()
        self.set_dataroot("ihp130", "git+https://github.com/IHP-GmbH/IHP-Open-PDK", pdk_rev)


class IHP130PDK(LambdaPDK, _IHP130Path):
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
    def __init__(self):
        super().__init__()
        self.set_name("ihp130")

        self.set_foundry("Leibniz-Institut für innovative Mikroelektronik")
        self.set_version(pdk_rev)
        self.set_node(130)
        self.set_stackup("5M2TL")

        pdk_path = Path("lambdapdk", "ihp130", "base")

        # Docs
        with self.active_dataroot("ihp130"):
            self.add_doc("quickstart", "ihp-sg13g2/libs.doc/doc/SG13G2_os_process_spec.pdf")
            self.add_doc("signoff", "ihp-sg13g2/libs.doc/doc/SG13G2_os_layout_rules.pdf")

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
        self.add_openroad_pinlayers(vertical="Metal2", horizontal="Metal3")

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
        with self.active_dataroot("ihp130"):
            for drc, runset in drcs.items():
                with self.active_fileset(f"klayout.drc.{drc}"):
                    self.add_file(runset, filetype="drc")
                    self.add_runsetfileset("drc", "klayout", drc)

                self.add_klayout_drcparam(drc, "in_gds=<input>")
                self.add_klayout_drcparam(drc, "cell=<topcell>")
                self.add_klayout_drcparam(drc, "report_file=<report>")
