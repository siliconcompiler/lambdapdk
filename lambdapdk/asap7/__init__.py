from pathlib import Path

from lambdapdk import LambdaPDK

# Capacitance unit multiplier: values below are quoted in fF/um.
fF = 1e-15


class ASAP7PDK(LambdaPDK):
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
    * lvs runsets (klayout)
    * APR technology files
    * 7.5 track multi-vt standard cell libraries

    More information:

    * https://asap.asu.edu/
    * L.T. Clark, V. Vashishtha, L. Shifren, A. Gujja, S. Sinha, B. Cline,
      C. Ramamurthya, and G. Yeric, “ASAP7: A 7-nm FinFET Predictive Process
      Design Kit,” Microelectronics Journal, vol. 53, pp. 105-115, July 2016.


    Sources: https://github.com/The-OpenROAD-Project/asap7
    '''

    def __init__(self):
        super().__init__()
        self.set_name("asap7")

        pdk_path = Path("lambdapdk", "asap7", "base")

        self.set_foundry("virtual")
        self.package.set_version("r1p7")
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

            # Klayout LVS runset. Registered twice: the same deck under two deck
            # names that differ only in their parameters, so a flow can pick the
            # behavior it wants by name.
            with self.active_fileset("klayout.lvs"):
                self.add_file(pdk_path / "setup" / "klayout" / "lvs" / "asap7.lvs",
                              filetype="lvs")
                self.add_runsetfileset("lvs", "klayout", "lvs")
            self.add_runsetfileset("lvs", "klayout", "lvs_blackbox", fileset="klayout.lvs")

            # The <...> entries are placeholders for the caller to substitute.
            # There is no KLayout LVS task in siliconcompiler, so these are
            # metadata for whichever flow drives the deck; the deck itself takes
            # them as '-rd name=value'. Note the report is a .lvsdb, not .lyrdb.
            for lvs_deck in ("lvs", "lvs_blackbox"):
                self.add_klayout_lvsparam(lvs_deck, "input=<input>")
                self.add_klayout_lvsparam(lvs_deck, "topcell=<topcell>")
                self.add_klayout_lvsparam(lvs_deck, "schematic=<schematic>")
                self.add_klayout_lvsparam(lvs_deck, "target_netlist=<target_netlist>")
                self.add_klayout_lvsparam(lvs_deck, "report=<report>")
                self.add_klayout_lvsparam(lvs_deck, "threads=<threads>")
                self.add_klayout_lvsparam(lvs_deck, "run_mode=deep")

            # Standard cells reduced to their pins, which checks that the routing
            # and the row abutment implement the netlist. This is the deck to use
            # on a single hardened block: it is unaffected by the 17 of 209 cells
            # whose CDL is not structurally isomorphic to their layout. It does
            # not check cell internals -- the "lvs" deck run per cell does that.
            #
            # It is *not* the deck for an array of abutted blocks. Blanking the
            # standard cells does not blank the blocks, so every block interior is
            # still extracted and compared, and blocks are the granularity an
            # array run needs. Pass a blackbox glob naming the blocks instead.
            self.add_klayout_lvsparam("lvs_blackbox", "blackbox=*_ASAP7_75t_*")

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
                self.add_file(pdk_path / "apr" / "openroad_relaxed_rules.tcl", filetype="tcl")

            # PEX
            self.add_openroad_rclayer("typical", "routing", "M1", 138.89, 1.1368e-01 * fF)
            self.add_openroad_rclayer("typical", "routing", "M2", 24.222, 1.3426e-01 * fF)
            self.add_openroad_rclayer("typical", "routing", "M3", 24.222, 1.2918e-01 * fF)
            self.add_openroad_rclayer("typical", "routing", "M4", 16.778, 1.1396e-01 * fF)
            self.add_openroad_rclayer("typical", "routing", "M5", 14.677, 1.3323e-01 * fF)
            self.add_openroad_rclayer("typical", "routing", "M6", 10.371, 1.1575e-01 * fF)
            self.add_openroad_rclayer("typical", "routing", "M7", 9.672, 1.3293e-01 * fF)
            self.add_openroad_rclayer("typical", "routing", "M8", 7.431, 1.1822e-01 * fF)
            self.add_openroad_rclayer("typical", "routing", "M9", 6.874, 1.3497e-01 * fF)
            self.add_openroad_rclayer("typical", "via", "V1", 17.2)
            self.add_openroad_rclayer("typical", "via", "V2", 17.2)
            self.add_openroad_rclayer("typical", "via", "V3", 17.2)
            self.add_openroad_rclayer("typical", "via", "V4", 11.8)
            self.add_openroad_rclayer("typical", "via", "V5", 11.8)
            self.add_openroad_rclayer("typical", "via", "V6", 8.2)
            self.add_openroad_rclayer("typical", "via", "V7", 8.2)
            self.add_openroad_rclayer("typical", "via", "V8", 6.3)
            with self.active_fileset("openroad.pex"):
                self.add_file(pdk_path / "pex" / "openroad" / "typical.rules", filetype="openrcx")
                self.add_pexmodelfileset("openroad", "typical")
