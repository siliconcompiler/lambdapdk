from pathlib import Path

from lambdapdk import LambdaPDK, _LambdaPath

# Capacitance unit multiplier: values below are quoted in pF/um.
pF = 1e-12

pdk_rev = 'v1.10.102'


class _ICS55Path(_LambdaPath):
    def __init__(self):
        super().__init__()
        self.set_dataroot("icsprout55",
                          "https://github.com/openecos-projects/icsprout55-pdk/archive/refs"
                          f"/tags/{pdk_rev}.tar.gz",
                          pdk_rev)


class ICS55PDK(LambdaPDK, _ICS55Path):
    '''
    The ICsprout 55nm Open Source PDK is an open source Process Design Kit developed by
    ICsprout Integrated Circuit Co., Ltd. with the assistance of the ECOS team at the
    Institute of Computing Technology, Chinese Academy of Sciences. It is built on a
    mature 55nm CMOS process and provides standard cell libraries, IO libraries and
    device models, targeting tapeout on ICsprout's production line.

    The kit splits its collateral between the git repository (tech LEF, cell LEF, CDL,
    Verilog) and the GitHub release assets (liberty and GDS), so the PDK and the
    standard cell libraries each bind several dataroots.

    Sources:

    * https://github.com/openecos-projects/icsprout55-pdk
    '''

    def __init__(self):
        super().__init__()
        self.set_name("icsprout55")

        pdk_path = Path("lambdapdk", "icsprout55", "base")

        self.set_foundry("ICsprout Integrated Circuit Co., Ltd")
        self.package.set_version(pdk_rev)
        self.set_node(55)
        self.set_stackup("5M1TM")

        with self.active_dataroot("icsprout55"):
            # APR Setup
            with self.active_fileset("views.lef"):
                self.add_file("prtech/techLEF/N551P6M.lef")
                for tool in ('openroad', 'klayout', 'magic'):
                    self.add_aprtechfileset(tool)

        with self.active_dataroot("lambdapdk"):
            # KLayout setup. Upstream ships no layer map at all, so the .lyt below is
            # what makes streamout possible; see the file header for how it was derived.
            with self.active_fileset("klayout.techmap"):
                self.add_file(pdk_path / "setup" / "klayout" / "icsprout55.lyt",
                              filetype="layermap")
                self.add_file(pdk_path / "setup" / "klayout" / "icsprout55.lyp",
                              filetype="display")
                self.add_layermapfileset("klayout", "def", "klayout")
                self.add_displayfileset("klayout")

            # MET1 is reserved for the cell rails and pin access.
            self.set_aprroutinglayers(min="MET2", max="MET5")

            # OpenROAD setup
            self.set_openroad_rclayers(signal="MET3", clock="MET4")
            self.add_openroad_pinlayers(vertical="MET4", horizontal="MET3")

            # Openroad global routing grid derating
            for layer, derate in [
                    ('MET1', 0.25),
                    ('MET2', 0.25),
                    ('MET3', 0.25),
                    ('MET4', 0.25),
                    ('MET5', 0.25),
                    ('T4M2', 0.00),
                    ('RDL', 0.00)]:
                self.set_openroad_globalroutingderating(layer, derate)

            # PEX. Resistance is derived from the tech LEF sheet resistance
            # (RESISTANCE RPERSQ / minimum WIDTH); via resistance is the per-cut
            # RESISTANCE carried by the fixed VIA definitions. The PDK publishes no
            # capacitance data, so the values below are estimates; they seed pre-route
            # estimation only, and are superseded by extraction once a deck exists.
            for layer, res, cap in [
                    ('MET1', 0.1122 / 0.09, 7.41819e-5),
                    ('MET2', 0.0914 / 0.10, 6.74606e-5),
                    ('MET3', 0.0914 / 0.10, 8.88758e-5),
                    ('MET4', 0.0914 / 0.10, 1.07121e-4),
                    ('MET5', 0.0914 / 0.10, 1.08964e-4),
                    ('T4M2', 0.0239 / 0.40, 1.20000e-4),
                    ('RDL', 0.0151 / 3.00, 1.50000e-4)]:
                self.add_openroad_rclayer("typical", "routing", layer, res, cap * pF)
            for via in ('VIA1', 'VIA2', 'VIA3', 'VIA4', 'T4V2'):
                self.add_openroad_rclayer("typical", "via", via, 2.5)

            # Add for compatibility with OpenROAD driver
            self.get("fileset", "openroad.pex", field="schema")
            with self.active_fileset("openroad.pex"):
                self.add_pexmodelfileset("openroad", "typical")
