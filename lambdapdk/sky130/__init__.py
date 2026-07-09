from pathlib import Path

from lambdapdk import LambdaPDK

# Capacitance unit multiplier: values below are quoted in pF/um.
pF = 1e-12


class Sky130PDK(LambdaPDK):
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
    def __init__(self):
        super().__init__()
        self.set_name("skywater130")

        self.set_foundry("skywater")
        self.package.set_version("v0_0_2")
        self.set_stackup("5M1LI")
        self.set_node(130)

        pdk_path = Path("lambdapdk", "sky130", "base")

        with self.active_dataroot("lambdapdk"):
            # APR Setup
            with self.active_fileset("views.lef"):
                self.add_file(pdk_path / "apr" / "sky130_fd_sc.tlef", filetype="lef")
                for tool in ('openroad', 'klayout', 'magic'):
                    self.add_aprtechfileset(tool)

            # DRC Runset
            with self.active_fileset("magic.drc"):
                self.add_file(pdk_path / "setup" / "magic" / "sky130A.tech", filetype="tech")
                self.add_runsetfileset("drc", "magic", "basic")

            # LVS Runset
            with self.active_fileset("netgen.lvs"):
                self.add_file(pdk_path / "setup" / "netgen" / "lvs_setup.tcl", filetype="tcl")
                self.add_runsetfileset("lvs", "netgen", "basic")

        self.set_aprroutinglayers(min="met1", max="met5")

        # Klayout setup
        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("klayout.techmap"):
                self.add_file(pdk_path / "setup" / "klayout" / "skywater130.lyt",
                              filetype="layermap")
                self.add_file(pdk_path / "setup" / "klayout" / "sky130A.lyp", filetype="display")
                self.add_layermapfileset("klayout", "def", "klayout")
                self.add_displayfileset("klayout")
        # Hide the 81/4 'areaid.standardc' layer by default; it puts opaque purple over most
        # core areas.
        self.add_klayout_hidelayers('areaid.standardc')

        # OpenROAD setup
        self.set_openroad_rclayers(signal="met3", clock="met5")

        # OpenROAD global routing grid derating
        for layer, derate in [
                ('li1', 1.0),
                ('met1', 0.40),
                ('met2', 0.40),
                ('met3', 0.30),
                ('met4', 0.30),
                ('met5', 0.30)]:
            self.set_openroad_globalroutingderating(layer, derate)

        self.add_openroad_pinlayers(vertical="met2", horizontal="met3")

        # OpenROAD PEX
        self.add_openroad_rclayer("minimum", "routing", "li1", 54.11765, 2.582652E-4 * pF)
        self.add_openroad_rclayer("minimum", "via", "mcon", 1.6)
        self.add_openroad_rclayer("minimum", "routing", "met1", 0.75, 2.246984E-4 * pF)
        self.add_openroad_rclayer("minimum", "via", "via", 4)
        self.add_openroad_rclayer("minimum", "routing", "met2", 0.75, 1.384201E-4 * pF)
        self.add_openroad_rclayer("minimum", "via", "via2", 0.5)
        self.add_openroad_rclayer("minimum", "routing", "met3", 0.1266667, 7.435933E-5 * pF)
        self.add_openroad_rclayer("minimum", "via", "via3", 0.5)
        self.add_openroad_rclayer("minimum", "routing", "met4", 0.1266667, 6.030297E-5 * pF)
        self.add_openroad_rclayer("minimum", "via", "via4", 0.012)
        self.add_openroad_rclayer("minimum", "routing", "met5", 0.01325, 4.057272E-5 * pF)
        self.add_openroad_rclayer("typical", "routing", "li1", 75.29412, 2.582652E-4 * pF)
        self.add_openroad_rclayer("typical", "via", "mcon", 9.3)
        self.add_openroad_rclayer("typical", "routing", "met1", 0.8928571, 2.246984E-4 * pF)
        self.add_openroad_rclayer("typical", "via", "via", 9)
        self.add_openroad_rclayer("typical", "routing", "met2", 0.8928571, 1.384201E-4 * pF)
        self.add_openroad_rclayer("typical", "via", "via2", 3.41)
        self.add_openroad_rclayer("typical", "routing", "met3", 0.1566667, 7.435933E-5 * pF)
        self.add_openroad_rclayer("typical", "via", "via3", 3.41)
        self.add_openroad_rclayer("typical", "routing", "met4", 0.1566667, 6.030297E-5 * pF)
        self.add_openroad_rclayer("typical", "via", "via4", 0.38)
        self.add_openroad_rclayer("typical", "routing", "met5", 0.0178125, 4.057272E-5 * pF)
        self.add_openroad_rclayer("maximum", "routing", "li1", 100, 2.582652E-4 * pF)
        self.add_openroad_rclayer("maximum", "via", "mcon", 23)
        self.add_openroad_rclayer("maximum", "routing", "met1", 1.035714, 2.246984E-4 * pF)
        self.add_openroad_rclayer("maximum", "via", "via", 30)
        self.add_openroad_rclayer("maximum", "routing", "met2", 1.035714, 1.384201E-4 * pF)
        self.add_openroad_rclayer("maximum", "via", "via2", 8)
        self.add_openroad_rclayer("maximum", "routing", "met3", 0.1866667, 7.435933E-5 * pF)
        self.add_openroad_rclayer("maximum", "via", "via3", 8)
        self.add_openroad_rclayer("maximum", "routing", "met4", 0.1866667, 6.030297E-5 * pF)
        self.add_openroad_rclayer("maximum", "via", "via4", 0.891)
        self.add_openroad_rclayer("maximum", "routing", "met5", 0.022375, 4.057272E-5 * pF)
        with self.active_dataroot("lambdapdk"):
            for corner in ["minimum", "typical", "maximum"]:
                with self.active_fileset(f"openroad.pex.{corner}"):
                    self.add_file(pdk_path / "pex" / "openroad" / f"{corner}.rules",
                                  filetype="openrcx")
                    self.add_pexmodelfileset("openroad", corner)
