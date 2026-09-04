from pathlib import Path

from lambdapdk import LambdaPDK

# Capacitance unit multiplier: values below are quoted in fF/um.
fF = 1e-15


class FreePDK45PDK(LambdaPDK):
    '''
    The freepdk45 PDK is a virtual PDK derived from the work done at
    NCSU (NCSU_TechLib_FreePDK45.)  It supplies techfiles, display
    resources, design rules and scripts to permit layout design and rule
    checking for a generic 45 nanometer process.  The technology information
    contained in this kit has been compiled from published papers,
    predictive technology models and rule scaling.  This information may be
    freely used, modified, and distributed under the open-source Apache
    License (see the file APACHE-LICENSE-2.0.txt in the root install
    directory for the complete text).   See the HSPICE Models
    section of this file for details about these models.

    More information:

    * https://eda.ncsu.edu/freepdk/freepdk45/
    '''
    def __init__(self):
        super().__init__()
        self.set_name("freepdk45")

        pdk_path = Path("lambdapdk", "freepdk45", "base")

        self.set_foundry("virtual")
        self.package.set_version("r1p0")
        self.set_node(45)
        self.set_stackup("10M")
        self.set_wafersize(300)
        self.set_scribewidth(0.1, 0.1)
        self.set_edgemargin(2)
        self.set_defectdensity(1.25)

        with self.active_dataroot("lambdapdk"):
            # APR Setup
            with self.active_fileset("views.lef"):
                self.add_file(pdk_path / "apr" / "freepdk45.tech.lef")
                for tool in ('openroad', 'klayout', 'magic'):
                    self.add_aprtechfileset(tool)

            self.set_aprroutinglayers(min="metal2", max="metal7")

            # Klayout setup file
            with self.active_fileset("klayout.techmap"):
                self.add_file(pdk_path / "setup" / "klayout" / "freepdk45.lyt", filetype="layermap")
                self.add_file(pdk_path / "setup" / "klayout" / "freepdk45.lyp", filetype="display")
                self.add_layermapfileset("klayout", "def", "klayout")
                self.add_displayfileset("klayout")

            self.set_openroad_rclayers(signal="metal3", clock="metal5")

            # Openroad global routing grid derating
            for layer, derate in [
                    ('metal1', 1.0),
                    ('metal2', 0.5),
                    ('metal3', 0.5),
                    ('metal4', 0.25),
                    ('metal5', 0.25),
                    ('metal6', 0.25),
                    ('metal7', 0.25),
                    ('metal8', 0.25),
                    ('metal9', 0.25),
                    ('metal10', 0.25)]:
                self.set_openroad_globalroutingderating(layer, derate)

            self.add_openroad_pinlayers(vertical="metal6", horizontal="metal5")

            # PEX. Measured 2026-09-02 by the OpenROAD PEX calibration sweep
            # (lambdapdk/scripts/pex_calibrate_all.py) rather than hand-derived:
            # rclayer routing values come from bench_wires against this PDK's OpenRCX
            # deck, via values are carried over, and the cap_factors are the pooled
            # design-survey correction. nseg records how many routed segments backed
            # each factor -- the upper layers of tall stacks are thinly sampled.
            self.add_openroad_rclayer("typical", "routing", "metal1", 5.42857, 0.159352 * fF)
            self.add_openroad_rclayer("typical", "routing", "metal2", 3.57143, 0.119382 * fF)
            self.add_openroad_rclayer("typical", "routing", "metal3", 3.57143, 0.155445 * fF)
            self.add_openroad_rclayer("typical", "routing", "metal4", 1.5, 0.159325 * fF)
            self.add_openroad_rclayer("typical", "routing", "metal5", 1.5, 0.156474 * fF)
            self.add_openroad_rclayer("typical", "routing", "metal6", 1.5, 0.15526 * fF)
            self.add_openroad_rclayer("typical", "routing", "metal7", 0.1875, 0.145336 * fF)
            self.add_openroad_rclayer("typical", "routing", "metal8", 0.1875, 0.146827 * fF)
            self.add_openroad_rclayer("typical", "routing", "metal9", 0.0375, 0.157309 * fF)
            self.add_openroad_rclayer("typical", "routing", "metal10", 0.0375, 0.152678 * fF)

            self.add_openroad_rccorrection("typical", "metal2", cap_factor=0.7294)  # nseg=282466
            self.add_openroad_rccorrection("typical", "metal3", cap_factor=0.6962)  # nseg=163577
            self.add_openroad_rccorrection("typical", "metal4", cap_factor=0.7448)  # nseg=13255
            self.add_openroad_rccorrection("typical", "metal5", cap_factor=0.6401)  # nseg=3133
            self.add_openroad_rccorrection("typical", "metal6", cap_factor=0.5067)  # nseg=1004
            self.add_openroad_rccorrection("typical", "metal7", cap_factor=0.7259)  # nseg=24
            with self.active_fileset("openroad.pex"):
                self.add_file(pdk_path / "pex" / "openroad" / "typical.rules", filetype="openrcx")
                self.add_pexmodelfileset("openroad", "typical")
