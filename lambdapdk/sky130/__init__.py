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
        # PEX. Measured 2026-09-02 by the OpenROAD PEX calibration sweep
        # (lambdapdk/scripts/pex_calibrate_all.py) rather than hand-derived:
        # rclayer routing values come from bench_wires against this PDK's OpenRCX
        # deck, via values are carried over, and the cap_factors are the pooled
        # design-survey correction. nseg records how many routed segments backed
        # each factor -- the upper layers of tall stacks are thinly sampled.
        self.add_openroad_rclayer("minimum", "routing", "li1", 54.1176, 8.85038e-05 * pF)
        self.add_openroad_rclayer("minimum", "routing", "met1", 0.75, 8.55626e-05 * pF)
        self.add_openroad_rclayer("minimum", "routing", "met2", 0.75, 6.85688e-05 * pF)
        self.add_openroad_rclayer("minimum", "routing", "met3", 0.126667, 7.82352e-05 * pF)
        self.add_openroad_rclayer("minimum", "routing", "met4", 0.126667, 7.13804e-05 * pF)
        self.add_openroad_rclayer("minimum", "routing", "met5", 0.01325, 8.39864e-05 * pF)
        self.add_openroad_rclayer("minimum", "via", "mcon", 1.6)
        self.add_openroad_rclayer("minimum", "via", "via", 4)
        self.add_openroad_rclayer("minimum", "via", "via2", 0.5)
        self.add_openroad_rclayer("minimum", "via", "via3", 0.5)
        self.add_openroad_rclayer("minimum", "via", "via4", 0.012)
        self.add_openroad_rclayer("typical", "routing", "li1", 75.2941, 8.85038e-05 * pF)
        self.add_openroad_rclayer("typical", "routing", "met1", 0.892857, 8.55626e-05 * pF)
        self.add_openroad_rclayer("typical", "routing", "met2", 0.892857, 6.85688e-05 * pF)
        self.add_openroad_rclayer("typical", "routing", "met3", 0.156667, 7.82352e-05 * pF)
        self.add_openroad_rclayer("typical", "routing", "met4", 0.156667, 7.13804e-05 * pF)
        self.add_openroad_rclayer("typical", "routing", "met5", 0.0178125, 8.39864e-05 * pF)
        self.add_openroad_rclayer("typical", "via", "mcon", 9.3)
        self.add_openroad_rclayer("typical", "via", "via", 9)
        self.add_openroad_rclayer("typical", "via", "via2", 3.41)
        self.add_openroad_rclayer("typical", "via", "via3", 3.41)
        self.add_openroad_rclayer("typical", "via", "via4", 0.38)
        self.add_openroad_rclayer("maximum", "routing", "li1", 100, 8.85038e-05 * pF)
        self.add_openroad_rclayer("maximum", "routing", "met1", 1.03571, 8.55626e-05 * pF)
        self.add_openroad_rclayer("maximum", "routing", "met2", 1.03571, 6.85688e-05 * pF)
        self.add_openroad_rclayer("maximum", "routing", "met3", 0.186667, 7.82352e-05 * pF)
        self.add_openroad_rclayer("maximum", "routing", "met4", 0.186667, 7.13804e-05 * pF)
        self.add_openroad_rclayer("maximum", "routing", "met5", 0.022375, 8.39864e-05 * pF)
        self.add_openroad_rclayer("maximum", "via", "mcon", 23)
        self.add_openroad_rclayer("maximum", "via", "via", 30)
        self.add_openroad_rclayer("maximum", "via", "via2", 8)
        self.add_openroad_rclayer("maximum", "via", "via3", 8)
        self.add_openroad_rclayer("maximum", "via", "via4", 0.891)

        self.add_openroad_rccorrection("minimum", "met1", cap_factor=0.9940)  # nseg=548274
        self.add_openroad_rccorrection("minimum", "met2", cap_factor=0.9971)  # nseg=330485
        self.add_openroad_rccorrection("minimum", "met3", cap_factor=0.9982)  # nseg=29921
        self.add_openroad_rccorrection("minimum", "met4", cap_factor=0.9990)  # nseg=7066
        self.add_openroad_rccorrection("minimum", "met5", cap_factor=0.9996)  # nseg=180
        self.add_openroad_rccorrection("typical", "met1", cap_factor=0.9940)  # nseg=548274
        self.add_openroad_rccorrection("typical", "met2", cap_factor=0.9971)  # nseg=330485
        self.add_openroad_rccorrection("typical", "met3", cap_factor=0.9982)  # nseg=29921
        self.add_openroad_rccorrection("typical", "met4", cap_factor=0.9990)  # nseg=7066
        self.add_openroad_rccorrection("typical", "met5", cap_factor=0.9996)  # nseg=180
        self.add_openroad_rccorrection("maximum", "met1", cap_factor=0.9940)  # nseg=548274
        self.add_openroad_rccorrection("maximum", "met2", cap_factor=0.9971)  # nseg=330485
        self.add_openroad_rccorrection("maximum", "met3", cap_factor=0.9982)  # nseg=29921
        self.add_openroad_rccorrection("maximum", "met4", cap_factor=0.9990)  # nseg=7066
        self.add_openroad_rccorrection("maximum", "met5", cap_factor=0.9996)  # nseg=180
        with self.active_dataroot("lambdapdk"):
            # Metal fill
            with self.active_fileset("openroad.fill"):
                self.add_file(pdk_path / "dfm" / "fill.json", filetype="fill")
                self.add_runsetfileset("fill", "openroad", "beol")

            for corner in ["minimum", "typical", "maximum"]:
                with self.active_fileset(f"openroad.pex.{corner}"):
                    self.add_file(pdk_path / "pex" / "openroad" / f"{corner}.rules",
                                  filetype="openrcx")
                    self.add_pexmodelfileset("openroad", corner)
