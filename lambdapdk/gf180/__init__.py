from pathlib import Path

from lambdapdk import LambdaPDK


class _GF180PDK(LambdaPDK):
    '''
    The 'gf180' Open Source PDK is a collaboration between Google and
    Global Foundries to provide a fully open source Process
    Design Kit and related resources, which can be used to create
    manufacturable designs at Global Foundries facility.

    ... GF180 Process Highlights:

    * 180nm process
    * 11 metal stack options from 3 to 6 metal levels

    PDK content:

    * multiple standard digital cell libraries
    * primitive cell libraries and models for creating analog designs
    * EDA support files for multiple open source and proprietary flows

    More information:

    * https://gf180mcu-pdk.readthedocs.io/

    Sources:

    * https://github.com/google/gf180mcu-pdk
    '''
    def __init__(self, stackup, libtype):
        super().__init__()
        self.set_name(f"GF180_{stackup}_{libtype}")

        self.set_foundry("globalfoundries")
        self.set_node(180)
        self.set_stackup(stackup)
        self.set_wafersize(200)

        pdk_path = Path("lambdapdk", "gf180", "base")

        max_layer = int(stackup[0])

        with self.active_dataroot("lambdapdk"):
            # APR Setup
            with self.active_fileset("views.lef"):
                self.add_file(pdk_path / "apr" / f"gf180mcu_{stackup}_{libtype}_tech.lef")
                for tool in ('openroad', 'klayout', 'magic'):
                    self.add_aprtechfileset(tool)

            self.set_aprroutinglayers(min="metal2", max="metal7")

            if stackup in ('6LM_1TM_9K', '5LM_1TM_9K'):
                with self.active_fileset("layermap"):
                    self.add_file(pdk_path / "apr" / f"gf180mcu_{stackup}_9t_edi2gds.layermap",
                                  filetype="layermap")
                    self.add_layermapfileset("klayout", "def", "gds")

            with self.active_fileset("models.spice"):
                self.add_file(pdk_path / "spice" / "xyce" / "design.xyce", filetype="xyce")
                self.add_file(pdk_path / "spice" / "xyce" / "sm141064.xyce", filetype="xyce")
                self.add_file(pdk_path / "spice" / "xyce" / "smbb000149.xyce", filetype="xyce")
                self.add_devmodelfileset("xyce", "spice")

        self.set_aprroutinglayers(min="Metal1", max=f"Metal{max_layer}")

        # Klayout setup
        with self.active_dataroot("lambdapdk"), self.active_fileset("klayout.techmap"):
            self.add_file(pdk_path / "setup" / "klayout" / "tech" / "gf180mcu.lyt",
                          filetype="layermap")
            self.add_file(pdk_path / "setup" / "klayout" / "tech" / "gf180mcu.lyp",
                          filetype="display")
            self.add_layermapfileset("klayout", "def", "klayout")
            self.add_displayfileset("klayout")

        # KLayout DRC
        metal_level, _, metal_top = stackup.split('_')
        drcs = {
            "drc": pdk_path / "setup" / "klayout" / "drc" / "gf180mcu.drc",
            "drc_feol": pdk_path / "setup" / "klayout" / "drc" / "gf180mcu.drc",
            "drc_beol": pdk_path / "setup" / "klayout" / "drc" / "gf180mcu.drc",
            "antenna": pdk_path / "setup" / "klayout" / "drc" / "gf180mcu_antenna.drc",
            "density": pdk_path / "setup" / "klayout" / "drc" / "gf180mcu_density.drc"
        }
        for drc, runset in drcs.items():
            with self.active_dataroot("lambdapdk"), self.active_fileset(f"klayout.drc.{drc}"):
                self.add_file(runset, filetype="drc")
                self.add_runsetfileset("drc", "klayout", drc)

            self.add_klayout_drcparam(drc, "input=<input>")
            self.add_klayout_drcparam(drc, "topcell=<topcell>")
            self.add_klayout_drcparam(drc, "thr=<threads>")
            self.add_klayout_drcparam(drc, "run_mode=flat")
            self.add_klayout_drcparam(drc, "offgrid=true")

            if drc in ("drc", "drc_feol", "drc_beol"):
                feol = "true"
                beol = "true"
                if drc == "drc_feol":
                    beol = "false"
                if drc == "drc_beol":
                    feol = "false"

                self.add_klayout_drcparam(drc, f"feol={feol}")
                self.add_klayout_drcparam(drc, f"beol={beol}")

            self.add_klayout_drcparam(drc, f"metal_top={metal_top}")
            self.add_klayout_drcparam(drc, f"metal_level={metal_level}")
            if max_layer == 3:
                self.add_klayout_drcparam(drc, "mim_option=A")
            elif max_layer == 4 or max_layer == 5:
                self.add_klayout_drcparam(drc, "mim_option=B")

        self.add_klayout_hidelayers('Dualgate')
        self.add_klayout_hidelayers('V5_XTOR')
        self.add_klayout_hidelayers('PR_bndry')

        # OpenROAD setup
        if max_layer == 3:
            self.set_openroad_rclayers(signal="Metal2", clock="Metal2")
            self.add_openroad_pinlayers(vertical="Metal2", horizontal="Metal3")
        elif max_layer == 4:
            self.set_openroad_rclayers(signal="Metal2", clock="Metal3")
            self.add_openroad_pinlayers(vertical="Metal4", horizontal="Metal3")
        elif max_layer >= 5:
            self.set_openroad_rclayers(signal="Metal3", clock="Metal4")
            self.add_openroad_pinlayers(vertical="Metal4", horizontal="Metal3")

        # Openroad global routing grid derating
        openroad_layer_adjustments = {
                'Metal1': 0.25,
                'Metal2': 0.25,
                'Metal3': 0.25,
                'Metal4': 0.25,
                'Metal5': 0.25,
                'Metal6': 0.25,
                'MetalTop': 1.0
        }
        for layer, adj in openroad_layer_adjustments.items():
            self.set_openroad_globalroutingderating(layer, adj)
            if layer == f"Metal{max_layer}":
                break

        # PEX
        with self.active_dataroot("lambdapdk"):
            for corner in ["bst", "typ", "wst"]:
                if stackup in ('3LM_1TM_6K', '3LM_1TM_9K', '3LM_1TM_11K', '3LM_1TM_30K',
                               '4LM_1TM_6K'):
                    continue

                base_name = f'gf180mcu_1p{stackup.replace("L", "").lower()}_sp_smim_OPTB_{corner}'

                with self.active_fileset(f"openroad.pex.{corner}"):
                    self.add_file(pdk_path / "pex" / "openroad" / f"{base_name}.tcl",
                                  filetype="tcl")
                    self.add_file(pdk_path / "pex" / "openroad" / f"{base_name}.rules",
                                  filetype="openrcx")

                    self.add_pexmodelfileset("openroad", corner)
                    self.add_pexmodelfileset("openroad-openrcx", corner)


class GF180_3LM_1TM_6K_7t(_GF180PDK):
    def __init__(self):
        super().__init__("3LM_1TM_6K", "7t")


class GF180_3LM_1TM_6K_9t(_GF180PDK):
    def __init__(self):
        super().__init__("3LM_1TM_6K", "9t")


class GF180_3LM_1TM_9K_7t(_GF180PDK):
    def __init__(self):
        super().__init__("3LM_1TM_9K", "7t")


class GF180_3LM_1TM_9K_9t(_GF180PDK):
    def __init__(self):
        super().__init__("3LM_1TM_9K", "9t")


class GF180_3LM_1TM_11K_7t(_GF180PDK):
    def __init__(self):
        super().__init__("3LM_1TM_11K", "7t")


class GF180_3LM_1TM_11K_9t(_GF180PDK):
    def __init__(self):
        super().__init__("3LM_1TM_11K", "9t")


class GF180_3LM_1TM_30K_7t(_GF180PDK):
    def __init__(self):
        super().__init__("3LM_1TM_30K", "7t")


class GF180_3LM_1TM_30K_9t(_GF180PDK):
    def __init__(self):
        super().__init__("3LM_1TM_30K", "9t")


class GF180_4LM_1TM_6K_7t(_GF180PDK):
    def __init__(self):
        super().__init__("4LM_1TM_6K", "7t")


class GF180_4LM_1TM_6K_9t(_GF180PDK):
    def __init__(self):
        super().__init__("4LM_1TM_6K", "9t")


class GF180_4LM_1TM_9K_7t(_GF180PDK):
    def __init__(self):
        super().__init__("4LM_1TM_9K", "7t")


class GF180_4LM_1TM_9K_9t(_GF180PDK):
    def __init__(self):
        super().__init__("4LM_1TM_9K", "9t")


class GF180_4LM_1TM_11K_7t(_GF180PDK):
    def __init__(self):
        super().__init__("4LM_1TM_11K", "7t")


class GF180_4LM_1TM_11K_9t(_GF180PDK):
    def __init__(self):
        super().__init__("4LM_1TM_11K", "9t")


class GF180_4LM_1TM_30K_7t(_GF180PDK):
    def __init__(self):
        super().__init__("4LM_1TM_30K", "7t")


class GF180_4LM_1TM_30K_9t(_GF180PDK):
    def __init__(self):
        super().__init__("4LM_1TM_30K", "9t")


class GF180_5LM_1TM_9K_7t(_GF180PDK):
    def __init__(self):
        super().__init__("5LM_1TM_9K", "7t")


class GF180_5LM_1TM_9K_9t(_GF180PDK):
    def __init__(self):
        super().__init__("5LM_1TM_9K", "9t")


class GF180_5LM_1TM_11K_7t(_GF180PDK):
    def __init__(self):
        super().__init__("5LM_1TM_11K", "7t")


class GF180_5LM_1TM_11K_9t(_GF180PDK):
    def __init__(self):
        super().__init__("5LM_1TM_11K", "9t")


class GF180_6LM_1TM_9K_7t(_GF180PDK):
    def __init__(self):
        super().__init__("6LM_1TM_9K", "7t")


class GF180_6LM_1TM_9K_9t(_GF180PDK):
    def __init__(self):
        super().__init__("6LM_1TM_9K", "9t")
