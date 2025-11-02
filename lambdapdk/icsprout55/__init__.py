from lambdapdk import LambdaPDK, _LambdaPath


pdk_rev = 'v1.10.100'


class _ICS55Path(_LambdaPath):
    def __init__(self):
        super().__init__()
        self.set_dataroot("icsprout55",
                          "https://github.com/openecos-projects/icsprout55-pdk/archive/refs"
                          f"/tags/{pdk_rev}.tar.gz",
                          pdk_rev)


class ICS55PDK(LambdaPDK, _ICS55Path):
    '''
    The ICsprout 55nm Open Source PDK (hereinafter referred to as this PDK) is an open source
    Process Design Kit independently developed by ICsprout Integrated Circuit Co., Ltd.
    (hereinafter referred to as ICsprout) and released in October 2025 with the assistance of
    ECOS team, Institute of Computing Technology, Chinese Academy of Sciences (hereinafter referred
    to as ECOS team). A significant breakthrough in the global open source chip ecosystem, this
    PDK represents the industry's most advanced open source process node at the time of its release.
    Built on mature 55nm CMOS process technology, it provides a complete and production-proven
    design rule files, device models, standard cell libraries, and parameterized cells. It fully
    supports the backend physical design flow of digital integrated circuits, including key steps
    such as logic synthesis, place and route, and physical verification, etc. Ultimately, it can
    be taped out on ICsprout's own production lines.

    Sources:

    * https://github.com/openecos-projects/icsprout55-pdk
    '''
    def __init__(self):
        super().__init__()
        self.set_name("icsprout55")

        self.set_foundry("ICsprout Integrated Circuit Co., Ltd")
        self.package.set_version(pdk_rev)
        self.set_node(55)
        self.set_stackup("5M")

        with self.active_dataroot("icsprout55"):
            # APR Setup
            with self.active_fileset("views.lef"):
                self.add_file("prtech/techLEF/N551P6M.lef")
                for tool in ('openroad', 'klayout', 'magic'):
                    self.add_aprtechfileset(tool)

        self.set_aprroutinglayers(min="MET1", max="MET5")

        # OpenROAD setup
        self.set_openroad_rclayers(signal="MET2", clock="MET3")
        self.add_openroad_pinlayers(vertical="MET2", horizontal="MET3")

        # Openroad global routing grid derating
        openroad_layer_adjustments = {
            'MET1': 0.25,
            'MET2': 0.25,
            'MET3': 0.25,
            'MET4': 0.25,
            'MET5': 0.25,
            'T4M2': 0.00,
            'RDL': 0.00
        }
        for layer, adj in openroad_layer_adjustments.items():
            self.set_openroad_globalroutingderating(layer, adj)
