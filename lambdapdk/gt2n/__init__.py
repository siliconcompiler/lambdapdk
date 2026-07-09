from pathlib import Path

from lambdapdk import LambdaPDK, _LambdaPath

# Capacitance unit multiplier: values below are quoted in pF/um.
pF = 1e-12

pdk_rev = '54f81feb2b9c334d283538c1bc91bf3a34b02c02'


class _GT2NPath(_LambdaPath):
    def __init__(self):
        super().__init__()
        self.set_dataroot("gt2n",
                          f"https://github.com/azadnaeemi/GT2N/archive/{pdk_rev}.tar.gz",
                          pdk_rev)


class GT2NPDK(LambdaPDK, _GT2NPath):
    '''
    GT2N PDK. It is based on 2nm GAAFET with BSPDN.

    More information:

    * https://github.com/azadnaeemi/GT2N/
    * D. Jang, P. Kumar, M. N. H. Shazon, S. J. Ram, A. Svizhenko, V. Moroz, A. Ceyhan,
    N. A. Radhakrishn, and A. Naeemi, "GT2N: An Open-Source 2nm Nanosheet PDK Enabling
    Multi-Width/VT Benchmarking," in IEEE International Symposium on Circuits and Systems
    (ISCAS) 2026.


    Sources: https://github.com/azadnaeemi/GT2N/
    '''

    def __init__(self):
        super().__init__()
        self.set_name("gt2n")

        pdk_path = Path("lambdapdk", "gt2n", "base")

        self.set_foundry("virtual")
        self.package.set_version("v0")
        self.set_node(2)
        self.set_stackup("13M")
        self.set_wafersize(300)

        with self.active_dataroot("gt2n"):
            # APR Setup
            with self.active_fileset("views.lef"):
                self.add_file("techlib/gt2_tech.lef")
                for tool in ('openroad', 'klayout', 'magic'):
                    self.add_aprtechfileset(tool)

            with self.active_fileset("layermap"):
                self.add_file("techlib/gt2_techfile_apr.layermap", filetype="layermap")

        with self.active_dataroot("lambdapdk"):
            # Klayout setup
            with self.active_fileset("klayout.techmap"):
                self.add_file(pdk_path / "setup" / "klayout" / "gt2n.lyt", filetype="layermap")
                self.add_file(pdk_path / "setup" / "klayout" / "gt2n.lyp", filetype="display")
                self.add_layermapfileset("klayout", "def", "klayout")
                self.add_displayfileset("klayout")
            self.add_layermapfileset("klayout", "def", "gds", fileset="layermap")

            self.set_aprroutinglayers(min="M1", max="M11")

            # OpenROAD setup
            self.set_openroad_rclayers(signal="M3", clock="M4")

            # Openroad global routing grid derating
            for layer, derate in [
                    ('M0', 0.75),
                    ('M1', 0.5),
                    ('M2', 0.5),
                    ('M3', 0.5),
                    ('M4', 0.5),
                    ('M5', 0.25),
                    ('M6', 0.25),
                    ('M7', 0.25),
                    ('M8', 0.25),
                    ('M9', 0.25),
                    ('M10', 0.25),
                    ('M11', 0.25),
                    ('M12', 0.25),
                    ('M13', 0.25)]:
                self.set_openroad_globalroutingderating(layer, derate)

            self.add_openroad_pinlayers(vertical="M3", horizontal="M2")

            # PEX
            self.add_openroad_rclayer("typical", "routing", "M0", 622, 1.5e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M1", 438, 1.5e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M2", 622, 1.5e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M3", 438, 1.5e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M4", 166, 1.7e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M5", 166, 1.7e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M6", 26, 2.0e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M7", 26, 2.0e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M8", 26, 2.0e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M9", 26, 2.0e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M10", 7.5, 2.5e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M11", 7.5, 2.5e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M12", 0.64, 3.0e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M13", 0.64, 3.0e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "BPR", 28, 1.0e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "BM1", 7.5, 1.5e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "BM2", 7.5, 1.5e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "BM3", 0.64, 1.5e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "BM4", 0.64, 1.5e-4 * pF)
            self.add_openroad_rclayer("typical", "via", "V0", 10)
            self.add_openroad_rclayer("typical", "via", "V1", 10)
            self.add_openroad_rclayer("typical", "via", "V2", 8)
            self.add_openroad_rclayer("typical", "via", "V3", 8)
            self.add_openroad_rclayer("typical", "via", "V4", 5)
            self.add_openroad_rclayer("typical", "via", "V5", 5)
            self.add_openroad_rclayer("typical", "via", "BV0", 10)
            self.add_openroad_rclayer("typical", "via", "BV1", 8)
            self.add_openroad_rclayer("typical", "via", "BV2", 8)
            self.add_openroad_rclayer("typical", "via", "BV3", 5)
            self.add_openroad_rclayer("typical", "via", "BV4", 5)
            with self.active_fileset("openroad.pex"):
                self.add_file(pdk_path / "pex" / "openroad" / "typical.tcl", filetype="tcl")

                self.add_pexmodelfileset("openroad", "typical")
