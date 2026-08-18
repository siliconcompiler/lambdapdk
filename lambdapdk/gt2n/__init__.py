from pathlib import Path

from lambdapdk import LambdaPDK, _LambdaPath

# Capacitance unit multiplier: values below are quoted in pF/um.
pF = 1e-12

pdk_rev = '308b221b82e19199a9691f2f78cbc7ce981481ca'


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
            self.set_openroad_rclayers(signal="M3", clock="M5")

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
            #
            # Per-length wire RC derived analytically from GT2N/nxtgrd/GT2.itf,
            # the StarRC interconnect tech file shipped with the PDK:
            #
            #   R/um = RPSQ / WMIN
            #   C/um = (Ca + Cb) * fringe + 2 * Cc      with
            #     Ca = eps0 * eps_above * W / d_above   plate to neighbor above
            #     Cb = eps0 * eps_below * W / d_below   plate to neighbor below
            #     Cc = eps0 * eps_side  * T / SMIN      sidewall to min-spaced
            #                                          neighbor on this layer
            #     fringe factor 1.5x for a coarse fringe-field correction.
            #
            # These are physically grounded but still approximate; a calibrated
            # extraction pass is the proper fix. Matches the table ORFS derives
            # in flow/platforms/gt2n/setRC.tcl via itf_to_rc.py.
            #
            # Frontside routing
            self.add_openroad_rclayer("typical", "routing", "M0", 621.75, 1.200e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M1", 437.50, 1.023e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M2", 621.75, 9.980e-5 * pF)
            self.add_openroad_rclayer("typical", "routing", "M3", 437.50, 1.023e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M4", 166.95, 1.088e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M5", 166.95, 1.051e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M6", 26.55, 1.119e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M7", 26.55, 1.051e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M8", 26.55, 1.051e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M9", 26.55, 1.051e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M10", 7.48, 1.091e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M11", 7.48, 1.051e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M12", 0.64, 1.205e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "M13", 0.64, 1.205e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "RDL", 0.01, 3.572e-4 * pF)
            # Backside routing
            self.add_openroad_rclayer("typical", "routing", "BPR", 24.31, 7.793e-5 * pF)
            self.add_openroad_rclayer("typical", "routing", "BM1", 7.48, 1.535e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "BM2", 7.48, 1.051e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "BM3", 0.64, 1.205e-4 * pF)
            self.add_openroad_rclayer("typical", "routing", "BM4", 0.64, 8.666e-5 * pF)
            self.add_openroad_rclayer("typical", "routing", "BRDL", 0.01, 1.006e-4 * pF)
            # Frontside via R (per via, derived from ITF RPV)
            self.add_openroad_rclayer("typical", "via", "V0", 54.99)
            self.add_openroad_rclayer("typical", "via", "V1", 54.99)
            self.add_openroad_rclayer("typical", "via", "V2", 54.99)
            self.add_openroad_rclayer("typical", "via", "V3", 45.78)
            self.add_openroad_rclayer("typical", "via", "V4", 27.80)
            self.add_openroad_rclayer("typical", "via", "V5", 14.89)
            self.add_openroad_rclayer("typical", "via", "V6", 13.26)
            self.add_openroad_rclayer("typical", "via", "V7", 13.26)
            self.add_openroad_rclayer("typical", "via", "V8", 13.26)
            self.add_openroad_rclayer("typical", "via", "V9", 7.65)
            self.add_openroad_rclayer("typical", "via", "V10", 6.08)
            self.add_openroad_rclayer("typical", "via", "V11", 6.08)
            self.add_openroad_rclayer("typical", "via", "V12", 0.95)
            self.add_openroad_rclayer("typical", "via", "V13", 0.15)
            # Backside via R (per via, derived from ITF RPV)
            self.add_openroad_rclayer("typical", "via", "BV0", 25.10)
            self.add_openroad_rclayer("typical", "via", "BV1", 6.08)
            self.add_openroad_rclayer("typical", "via", "BV2", 6.08)
            self.add_openroad_rclayer("typical", "via", "BV3", 0.95)
            self.add_openroad_rclayer("typical", "via", "BV4", 0.15)

            # Add for compatibility with OpenROAD driver
            self.get("fileset", "openroad.pex", field="schema")
            with self.active_fileset("openroad.pex"):
                self.add_pexmodelfileset("openroad", "typical")
