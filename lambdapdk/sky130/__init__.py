from pathlib import Path

from lambdapdk import LambdaPDK, _LambdaPath

# Capacitance unit multiplier: values below are quoted in pF/um.
pF = 1e-12


class _Sky130Data(_LambdaPath):
    '''
    Registers the upstream archives sky130 collateral is referenced from.

    open_pdks builds these libraries and publishes one archive per installed
    library directory for each revision, so a library reaches its files through
    set_dataroot the same way ihp130 and gt2n reach theirs -- nothing is copied
    into this repository except the two files that need a local patch (see
    PATCHES.md).

    Each archive URL is fully determined by the library name and the revision,
    so no index is resolved and nothing here touches the network at import time.
    Registering an archive costs nothing until a file in it is referenced, so
    every sky130 object declares all of them.

    Paths into an unpacked archive are written out at each use and look like
    'sky130A/libs.ref/<library>/<view>/<file>'. The 'sky130A' variant is the
    plain library; 'sky130B' is the same thing plus the ReRAM module, which
    nothing here uses. Every archive carries both.
    '''
    #: Date of the pinned open_pdks revision, used as the package version.
    #:
    #: Everything mixing this in is pinned to one revision, so the revision is
    #: the version. Its date rather than its SHA -- both name the same pin, and
    #: only one of them is readable in a manifest or a summary table.
    PDK_VERSION = "2026-08-27"

    def __init__(self):
        super().__init__()

        # Bumping this re-points every sky130 dataroot at once, which is the
        # point: one revision keeps the standard cells, the IO and the memories
        # mutually consistent, the way an open_pdks install is.
        pdk_rev = '1689ac3f2dc763876eaf967227c7dfe831b031ae'

        for library in ("sky130_fd_sc_hd",
                        "sky130_fd_sc_hdll",
                        "sky130_fd_io",
                        "sky130_sram_macros",
                        # Not a cell library: the shared 'libs.tech' tree with
                        # the tool setup -- KLayout display and DRC, magic,
                        # netgen, ngspice models, the OpenRCX decks. 60 MB
                        # unpacked, the smallest archive by an order of
                        # magnitude.
                        "common"):
            self.set_dataroot(
                library,
                "https://github.com/fossi-foundation/ciel-releases/releases/download/"
                f"sky130-{pdk_rev}/{library}.tar.zst",
                pdk_rev)


class Sky130PDK(LambdaPDK, _Sky130Data):
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
        self.package.set_version(self.PDK_VERSION)
        self.set_stackup("5M1LI")
        self.set_node(130)

        pdk_path = Path("lambdapdk", "sky130", "base")

        # APR Setup
        #
        # The tech LEF is taken by reference: the '__nom.tlef' upstream is
        # byte-identical to the copy this repo used to vendor as
        # base/apr/sky130_fd_sc.tlef, so this is a pure sourcing change.
        # open_pdks emits one tech LEF per standard cell library rather than one
        # per process; they describe the same metal stack, and hd is the main
        # library here. min/max sit beside it in the same dataroot.
        with self.active_dataroot("sky130_fd_sc_hd"):
            with self.active_fileset("views.lef"):
                self.add_file(
                    Path("sky130A", "libs.ref", "sky130_fd_sc_hd", "techlef",
                         "sky130_fd_sc_hd__nom.tlef"),
                    filetype="lef")
                for tool in ('openroad', 'klayout', 'magic'):
                    self.add_aprtechfileset(tool)

        with self.active_dataroot("lambdapdk"):
            # DRC Runset
            #
            # Still vendored: refreshing the magic and netgen decks from the
            # upstream 'common' archive means pairing a 2026 sky130A.tech
            # with the magic SC pins, which is c7f11d2 (8.3.367,
            # 2023-02-16). See PATCHES.md.
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
                # The .lyt stays vendored. Upstream's uses the older LEF/DEF
                # reader-options schema -- <routing-suffix> where this one has
                # <routing-suffix-string>, no produce-lef-pins, no
                # read-lef-with-def -- and points <lef-files> at a 'merged.lef'
                # this repository no longer produces, so adopting it would be a
                # regression rather than a refresh.
                self.add_file(pdk_path / "setup" / "klayout" / "skywater130.lyt",
                              filetype="layermap")

        with self.active_dataroot("common"):
            with self.active_fileset("klayout.techmap"):
                # The display file is pure upstream data and was never modified
                # here; the current one adds the .fill and boundary layers the
                # 2023 copy predates.
                self.add_file(Path("sky130A", "libs.tech", "klayout", "tech", "sky130A.lyp"),
                              filetype="display")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("klayout.techmap"):
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

        with self.active_dataroot("common"):
            # OpenRCX decks, referenced rather than vendored: the copies this
            # repository carried were never modified, only stale -- last updated
            # in the 2023 bulk refresh. open_pdks installs them under librelane/,
            # which is where it keeps extraction rules; it is not a LibreLane
            # dependency.
            #
            # Upstream builds each corner against three extraction references --
            # magic, calibre and spef_extractor. The spef_extractor deck is the
            # one this repository has always used: diffing the vendored copies
            # against all three puts them 960 lines from spef_extractor and 2368
            # from either of the others, and the structure is identical, so the
            # delta is coupling values rather than a different deck.
            #
            # NOTE: the add_openroad_rclayer values below were measured against
            # the *2023* decks by scripts/pex_calibrate_all.py, and the
            # capacitance tables here have moved since -- met1 area cap goes
            # 3.42844e-05 to 3.93264e-05, about 15%. Re-run that sweep.
            for corner, deck in [("minimum", "min"), ("typical", "nom"), ("maximum", "max")]:
                with self.active_fileset(f"openroad.pex.{corner}"):
                    self.add_file(
                        Path("sky130A", "libs.tech", "librelane",
                             f"rules.openrcx.sky130A.{deck}.spef_extractor"),
                        filetype="openrcx")
                    self.add_pexmodelfileset("openroad", corner)
