from pathlib import Path

from lambdapdk import LambdaPDK


class _Interposer(LambdaPDK):
    '''
    The interposer PDK is a passive technology with a number of
    simulated stackups. The PDK contains enablement for place and
    route tools and design rule signoff.
    Note that this process design kit is provided as an academic
    and research aid only and the resulting designs are not manufacturable.
    '''
    def __init__(self, stackup):
        super().__init__()
        self.set_name(f"interposer_{stackup}")

        self.set_foundry("virtual")
        self.set_version("v0.0.1")
        self.set_stackup(stackup)

        pdk_path = Path("lambdapdk", "interposer", "base")

        with self.active_dataroot("lambdapdk"):
            # APR Setup
            with self.active_fileset("views.lef"):
                self.add_file(pdk_path / "apr" / f"{stackup}.lef")
                for tool in ('openroad', 'klayout', 'magic'):
                    self.add_aprtechfileset(tool)

            with self.active_fileset("layermap"):
                self.add_file(pdk_path / "apr" / f"{stackup}.layermap", filetype="layermap")

        self.set_aprroutinglayers(min="metal1", max="topmetal")

        # KLayout Setup
        with self.active_dataroot("lambdapdk"):
            # Klayout setup file
            with self.active_fileset("klayout.techmap"):
                self.add_file(pdk_path / "setup" / "klayout" / f"{stackup}.lyp", filetype="display")
                self.add_displayfileset("klayout")
            self.add_layermapfileset("klayout", "def", "gds", fileset="layermap")

        # OpenROAD Setup

        # Openroad global routing grid derating
        openroad_layer_adjustments = {
            'metal1': 0.20,
            'metal2': 0.20,
            'metal3': 0.20,
            'metal4': 0.20,
            'metal5': 0.20,
            'metal6': 0.20,
            'topmetal': 0.20
        }
        for layer, adj in openroad_layer_adjustments.items():
            if layer != 'topmetal' and int(layer[-1]) >= int(stackup[0]):
                continue
            self.set_openroad_globalroutingderating(layer, adj)

        self.set_openroad_rclayers(signal="metal2", clock="metal2")
        self.add_openroad_pinlayers(vertical="metal2", horizontal="metal3")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("openroad.fill"):
                self.add_file(pdk_path / "dfm" / "openroad" / f"{stackup}.fill.json",
                              filetype="fill")
                self.add_aprtechfileset("openroad")

            # PEX
            for corner in ["minimum", "typical", "maximum"]:
                with self.active_fileset(f"openroad.pex.{corner}"):
                    self.add_file(pdk_path / "pex" / "openroad" / f"{stackup}.{corner}.tcl",
                                  filetype="tcl")

                    self.add_pexmodelfileset("openroad", corner)

        # DRC
        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("klayout.drc"):
                self.add_file(pdk_path / "setup" / "klayout" / f"{stackup}.drc", filetype="drc")
                self.add_runsetfileset("drc", "klayout", "drc")

            self.add_klayout_drcparam("drc", "input=<input>")
            self.add_klayout_drcparam("drc", "topcell=<topcell>")
            self.add_klayout_drcparam("drc", "report=<report>")
            self.add_klayout_drcparam("drc", "threads=<threads>")


class Interposer_3ML_0400(_Interposer):
    def __init__(self):
        super().__init__("3ML_0400")


class Interposer_3ML_0800(_Interposer):
    def __init__(self):
        super().__init__("3ML_0800")


class Interposer_3ML_2000(_Interposer):
    def __init__(self):
        super().__init__("3ML_2000")


class Interposer_3ML_0400_2000(_Interposer):
    def __init__(self):
        super().__init__("3ML_0400_2000")


class Interposer_4ML_0400(_Interposer):
    def __init__(self):
        super().__init__("4ML_0400")


class Interposer_4ML_0800(_Interposer):
    def __init__(self):
        super().__init__("4ML_0800")


class Interposer_4ML_2000(_Interposer):
    def __init__(self):
        super().__init__("4ML_2000")


class Interposer_4ML_0400_2000(_Interposer):
    def __init__(self):
        super().__init__("4ML_0400_2000")


class Interposer_5ML_0400(_Interposer):
    def __init__(self):
        super().__init__("5ML_0400")


class Interposer_5ML_0800(_Interposer):
    def __init__(self):
        super().__init__("5ML_0800")


class Interposer_5ML_2000(_Interposer):
    def __init__(self):
        super().__init__("5ML_2000")


class Interposer_5ML_0400_2000(_Interposer):
    def __init__(self):
        super().__init__("5ML_0400_2000")
