from pathlib import Path

from lambdapdk import LambdaPDK

# Capacitance unit multiplier: values below are quoted in pF/um.
pF = 1e-12

# Per-length RC parasitics measured from the OpenRCX decks by the PEX
# calibration sweep (lambdapdk/scripts/pex_calibrate_all.py, 2026-09-02), keyed
# by stackup and corner. Resistance is in ohms/um (vias in ohms/cut);
# capacitance is in pF/um. Routing values are bench_wires measurements against
# each stackup's own deck; via resistance is uniform across every gf180 stackup
# and is carried over (the bench characterizes routing layers only).
_PEX = {
    "3LM_1TM_6K": {
        "bst": [
            ("Metal1", 0.274687, 0.000199583),
            ("Metal2", 0.225636, 0.000177551),
            ("Metal3", 0.114611, 0.000165869),
            ("Via1", 4.23, None),
            ("Via2", 4.23, None),
        ],
        "typ": [
            ("Metal1", 0.395696, 0.000233663),
            ("Metal2", 0.325036, 0.000202592),
            ("Metal3", 0.169472, 0.000188486),
            ("Via1", 4.5, None),
            ("Via2", 4.5, None),
        ],
        "wst": [
            ("Metal1", 0.628392, 0.000274718),
            ("Metal2", 0.516178, 0.000231725),
            ("Metal3", 0.275028, 0.000214676),
            ("Via1", 16.845, None),
            ("Via2", 16.845, None),
        ],
    },
    "3LM_1TM_9K": {
        "bst": [
            ("Metal1", 0.274687, 0.000203621),
            ("Metal2", 0.225636, 0.000182064),
            ("Metal3", 0.0585537, 0.000175562),
            ("Via1", 4.23, None),
            ("Via2", 4.23, None),
        ],
        "typ": [
            ("Metal1", 0.395696, 0.000238789),
            ("Metal2", 0.325036, 0.00020803),
            ("Metal3", 0.0932048, 0.000198698),
            ("Via1", 4.5, None),
            ("Via2", 4.5, None),
        ],
        "wst": [
            ("Metal1", 0.628392, 0.000281156),
            ("Metal2", 0.516178, 0.000238201),
            ("Metal3", 0.161545, 0.000224413),
            ("Via1", 16.845, None),
            ("Via2", 16.845, None),
        ],
    },
    "3LM_1TM_11K": {
        "bst": [
            ("Metal1", 0.274687, 0.000203671),
            ("Metal2", 0.225636, 0.000182232),
            ("Metal3", 0.0585537, 0.000197217),
            ("Via1", 4.23, None),
            ("Via2", 4.23, None),
        ],
        "typ": [
            ("Metal1", 0.395696, 0.000238841),
            ("Metal2", 0.325036, 0.000208202),
            ("Metal3", 0.0932048, 0.000224775),
            ("Via1", 4.5, None),
            ("Via2", 4.5, None),
        ],
        "wst": [
            ("Metal1", 0.628392, 0.00028123),
            ("Metal2", 0.516178, 0.00023837),
            ("Metal3", 0.161545, 0.000255501),
            ("Via1", 16.845, None),
            ("Via2", 16.845, None),
        ],
    },
    "3LM_1TM_30K": {
        "bst": [
            ("Metal1", 0.274687, 0.000230547),
            ("Metal2", 0.225636, 0.000212425),
            ("Metal3", 0.00257977, 0.000150937),
            ("Via1", 4.23, None),
            ("Via2", 4.23, None),
        ],
        "typ": [
            ("Metal1", 0.395696, 0.000273014),
            ("Metal2", 0.325036, 0.000244897),
            ("Metal3", 0.00473371, 0.000172753),
            ("Via1", 4.5, None),
            ("Via2", 4.5, None),
        ],
        "wst": [
            ("Metal1", 0.628392, 0.000324185),
            ("Metal2", 0.516178, 0.000282321),
            ("Metal3", 0.00959318, 0.000198361),
            ("Via1", 16.845, None),
            ("Via2", 16.845, None),
        ],
    },
    "4LM_1TM_6K": {
        "bst": [
            ("Metal1", 0.274687, 0.000207878),
            ("Metal2", 0.225636, 0.000183315),
            ("Metal3", 0.225636, 0.000186094),
            ("Metal4", 0.114611, 0.000176574),
            ("Via1", 4.23, None),
            ("Via2", 4.23, None),
            ("Via3", 4.23, None),
        ],
        "typ": [
            ("Metal1", 0.395696, 0.000244258),
            ("Metal2", 0.325036, 0.000209643),
            ("Metal3", 0.325036, 0.000212497),
            ("Metal4", 0.169472, 0.000201752),
            ("Via1", 4.5, None),
            ("Via2", 4.5, None),
            ("Via3", 4.5, None),
        ],
        "wst": [
            ("Metal1", 0.628392, 0.000288148),
            ("Metal2", 0.516178, 0.000240223),
            ("Metal3", 0.516178, 0.000243214),
            ("Metal4", 0.275028, 0.000231023),
            ("Via1", 16.845, None),
            ("Via2", 16.845, None),
            ("Via3", 16.845, None),
        ],
    },
    "4LM_1TM_9K": {
        "bst": [
            ("Metal1", 0.274687, 0.000209935),
            ("Metal2", 0.225636, 0.000186466),
            ("Metal3", 0.225636, 0.000188559),
            ("Metal4", 0.0585537, 0.000185851),
            ("Via1", 4.23, None),
            ("Via2", 4.23, None),
            ("Via3", 4.23, None),
        ],
        "typ": [
            ("Metal1", 0.395696, 0.000246878),
            ("Metal2", 0.325036, 0.00021366),
            ("Metal3", 0.325036, 0.00021541),
            ("Metal4", 0.0932048, 0.000210793),
            ("Via1", 4.5, None),
            ("Via2", 4.5, None),
            ("Via3", 4.5, None),
        ],
        "wst": [
            ("Metal1", 0.628392, 0.000291446),
            ("Metal2", 0.516178, 0.000245422),
            ("Metal3", 0.516178, 0.000246575),
            ("Metal4", 0.161545, 0.000238467),
            ("Via1", 16.845, None),
            ("Via2", 16.845, None),
            ("Via3", 16.845, None),
        ],
    },
    "4LM_1TM_11K": {
        "bst": [
            ("Metal1", 0.274687, 0.000209937),
            ("Metal2", 0.225636, 0.000186465),
            ("Metal3", 0.225636, 0.000188551),
            ("Metal4", 0.0585537, 0.000209222),
            ("Via1", 4.23, None),
            ("Via2", 4.23, None),
            ("Via3", 4.23, None),
        ],
        "typ": [
            ("Metal1", 0.395696, 0.000246881),
            ("Metal2", 0.325036, 0.000213656),
            ("Metal3", 0.325036, 0.000215399),
            ("Metal4", 0.0932048, 0.000239053),
            ("Via1", 4.5, None),
            ("Via2", 4.5, None),
            ("Via3", 4.5, None),
        ],
        "wst": [
            ("Metal1", 0.628392, 0.000291449),
            ("Metal2", 0.516178, 0.000245427),
            ("Metal3", 0.516178, 0.000246558),
            ("Metal4", 0.161545, 0.000272243),
            ("Via1", 16.845, None),
            ("Via2", 16.845, None),
            ("Via3", 16.845, None),
        ],
    },
    "4LM_1TM_30K": {
        "bst": [
            ("Metal1", 0.274687, 0.000230121),
            ("Metal2", 0.225636, 0.000211199),
            ("Metal3", 0.225636, 0.000214069),
            ("Metal4", 0.00260141, 0.000147721),
            ("Via1", 4.23, None),
            ("Via2", 4.23, None),
            ("Via3", 4.23, None),
        ],
        "typ": [
            ("Metal1", 0.395696, 0.000272509),
            ("Metal2", 0.325036, 0.000243409),
            ("Metal3", 0.325036, 0.000246591),
            ("Metal4", 0.00477733, 0.000168978),
            ("Via1", 4.5, None),
            ("Via2", 4.5, None),
            ("Via3", 4.5, None),
        ],
        "wst": [
            ("Metal1", 0.628392, 0.000323601),
            ("Metal2", 0.516178, 0.000280337),
            ("Metal3", 0.516178, 0.000284132),
            ("Metal4", 0.00968639, 0.000193798),
            ("Via1", 16.845, None),
            ("Via2", 16.845, None),
            ("Via3", 16.845, None),
        ],
    },
    "5LM_1TM_9K": {
        "bst": [
            ("Metal1", 0.274687, 0.000214383),
            ("Metal2", 0.225636, 0.00019026),
            ("Metal3", 0.225636, 0.000189821),
            ("Metal4", 0.225636, 0.000193857),
            ("Metal5", 0.0585537, 0.000194276),
            ("Via1", 4.23, None),
            ("Via2", 4.23, None),
            ("Via3", 4.23, None),
            ("Via4", 4.23, None),
        ],
        "typ": [
            ("Metal1", 0.395696, 0.000252568),
            ("Metal2", 0.325036, 0.000218289),
            ("Metal3", 0.325036, 0.000217273),
            ("Metal4", 0.325036, 0.000221603),
            ("Metal5", 0.0932048, 0.000220497),
            ("Via1", 4.5, None),
            ("Via2", 4.5, None),
            ("Via3", 4.5, None),
            ("Via4", 4.5, None),
        ],
        "wst": [
            ("Metal1", 0.628392, 0.00029864),
            ("Metal2", 0.516178, 0.000250934),
            ("Metal3", 0.516178, 0.000249336),
            ("Metal4", 0.516178, 0.000253673),
            ("Metal5", 0.161545, 0.000249563),
            ("Via1", 16.845, None),
            ("Via2", 16.845, None),
            ("Via3", 16.845, None),
            ("Via4", 16.845, None),
        ],
    },
    "5LM_1TM_11K": {
        "bst": [
            ("Metal1", 0.274687, 0.000214384),
            ("Metal2", 0.225636, 0.000190257),
            ("Metal3", 0.225636, 0.000189814),
            ("Metal4", 0.225636, 0.000193844),
            ("Metal5", 0.0585537, 0.000219158),
            ("Via1", 4.23, None),
            ("Via2", 4.23, None),
            ("Via3", 4.23, None),
            ("Via4", 4.23, None),
        ],
        "typ": [
            ("Metal1", 0.395696, 0.000252568),
            ("Metal2", 0.325036, 0.000218294),
            ("Metal3", 0.325036, 0.000217263),
            ("Metal4", 0.325036, 0.000221582),
            ("Metal5", 0.0932048, 0.000250472),
            ("Via1", 4.5, None),
            ("Via2", 4.5, None),
            ("Via3", 4.5, None),
            ("Via4", 4.5, None),
        ],
        "wst": [
            ("Metal1", 0.628392, 0.00029864),
            ("Metal2", 0.516178, 0.000250927),
            ("Metal3", 0.516178, 0.000249323),
            ("Metal4", 0.516178, 0.000253651),
            ("Metal5", 0.161545, 0.000285447),
            ("Via1", 16.845, None),
            ("Via2", 16.845, None),
            ("Via3", 16.845, None),
            ("Via4", 16.845, None),
        ],
    },
    "6LM_1TM_9K": {
        "bst": [
            ("Metal1", 0.274687, 0.000217855),
            ("Metal2", 0.225636, 0.000193923),
            ("Metal3", 0.225636, 0.00019227),
            ("Metal4", 0.225636, 0.000193035),
            ("Metal5", 0.225636, 0.000198857),
            ("MetalTop", 0.0585537, 0.000200704),
            ("Via1", 4.23, None),
            ("Via2", 4.23, None),
            ("Via3", 4.23, None),
            ("Via4", 4.23, None),
            ("Via5", 4.23, None),
        ],
        "typ": [
            ("Metal1", 0.395696, 0.000257017),
            ("Metal2", 0.325036, 0.000222233),
            ("Metal3", 0.325036, 0.0002198),
            ("Metal4", 0.325036, 0.000220865),
            ("Metal5", 0.325036, 0.000227328),
            ("MetalTop", 0.0932048, 0.000227934),
            ("Via1", 4.5, None),
            ("Via2", 4.5, None),
            ("Via3", 4.5, None),
            ("Via4", 4.5, None),
            ("Via5", 4.5, None),
        ],
        "wst": [
            ("Metal1", 0.628392, 0.000304275),
            ("Metal2", 0.516178, 0.000255412),
            ("Metal3", 0.516178, 0.000252171),
            ("Metal4", 0.516178, 0.000253328),
            ("Metal5", 0.516178, 0.000260183),
            ("MetalTop", 0.161545, 0.000258161),
            ("Via1", 16.845, None),
            ("Via2", 16.845, None),
            ("Via3", 16.845, None),
            ("Via4", 16.845, None),
            ("Via5", 16.845, None),
        ],
    },
}

# Pooled design-survey correction factors, same keying. Pooled across cell
# heights with nseg weighting: the two heights agree to 2.5% median and diverge
# only where few segments were sampled. A stackup absent here has no correction
# -- 3LM cannot route the survey designs at all, so it has none to give, and its
# rclayer estimate above stands uncorrected.
# MIM option shipping an OpenRCX deck for each stackup. Hardcoding OPTB used to
# make the five OPTA-only stackups fall out of _PEX and silently ship no PEX
# data at all; where both options exist, OPTB is kept so the six stackups that
# already had PEX keep the decks they had.
#
# This is a static table on purpose. The decks live under the 'lambdapdk'
# dataroot, which resolves either to a checkout or to an archive unpacked under
# ~/.sc -- never to the installed package, which carries no PDK data -- so
# probing the filesystem from here would look in the wrong place and pick OPTA
# for everything, naming a deck that does not exist for the OPTB-only stackups.
# Probing during PDK setup is also needless work on every construction.
_PEX_MIM_OPTION = {
    "3LM_1TM_6K": "A",
    "3LM_1TM_9K": "A",
    "3LM_1TM_11K": "A",
    "3LM_1TM_30K": "A",
    "4LM_1TM_6K": "A",
    "4LM_1TM_9K": "B",
    "4LM_1TM_11K": "B",
    "4LM_1TM_30K": "B",
    "5LM_1TM_9K": "B",
    "5LM_1TM_11K": "B",
    "6LM_1TM_9K": "B",
}

_PEX_CORRECTION = {
    "4LM_1TM_6K": {
        "bst": [
            ("Metal1", 0.6009),  # nseg=1583
            ("Metal2", 0.7094),  # nseg=386666
            ("Metal3", 0.7320),  # nseg=155062
            ("Metal4", 0.6842),  # nseg=4982
        ],
        "typ": [
            ("Metal1", 0.5666),  # nseg=1583
            ("Metal2", 0.6923),  # nseg=386666
            ("Metal3", 0.7157),  # nseg=155062
            ("Metal4", 0.6646),  # nseg=4982
        ],
        "wst": [
            ("Metal1", 0.5376),  # nseg=1583
            ("Metal2", 0.6791),  # nseg=386666
            ("Metal3", 0.7023),  # nseg=155062
            ("Metal4", 0.6511),  # nseg=4982
        ],
    },
    "4LM_1TM_9K": {
        "bst": [
            ("Metal1", 0.5863),  # nseg=861
            ("Metal2", 0.7298),  # nseg=766918
            ("Metal3", 0.7415),  # nseg=296401
            ("Metal4", 0.7665),  # nseg=4229
        ],
        "typ": [
            ("Metal1", 0.5516),  # nseg=861
            ("Metal2", 0.7171),  # nseg=766918
            ("Metal3", 0.7285),  # nseg=296401
            ("Metal4", 0.7523),  # nseg=4229
        ],
        "wst": [
            ("Metal1", 0.5209),  # nseg=861
            ("Metal2", 0.7104),  # nseg=766918
            ("Metal3", 0.7203),  # nseg=296401
            ("Metal4", 0.7434),  # nseg=4229
        ],
    },
    "4LM_1TM_11K": {
        "bst": [
            ("Metal1", 0.5837),  # nseg=855
            ("Metal2", 0.7296),  # nseg=766429
            ("Metal3", 0.7415),  # nseg=295852
            ("Metal4", 0.7413),  # nseg=4206
        ],
        "typ": [
            ("Metal1", 0.5488),  # nseg=855
            ("Metal2", 0.7169),  # nseg=766429
            ("Metal3", 0.7285),  # nseg=295852
            ("Metal4", 0.7260),  # nseg=4206
        ],
        "wst": [
            ("Metal1", 0.5183),  # nseg=855
            ("Metal2", 0.7102),  # nseg=766429
            ("Metal3", 0.7204),  # nseg=295852
            ("Metal4", 0.7154),  # nseg=4206
        ],
    },
    "4LM_1TM_30K": {
        "bst": [
            ("Metal1", 0.5768),  # nseg=1271
            ("Metal2", 0.6587),  # nseg=826139
            ("Metal3", 0.6671),  # nseg=262177
        ],
        "typ": [
            ("Metal1", 0.5449),  # nseg=1271
            ("Metal2", 0.6444),  # nseg=826139
            ("Metal3", 0.6515),  # nseg=262177
        ],
        "wst": [
            ("Metal1", 0.5170),  # nseg=1271
            ("Metal2", 0.6373),  # nseg=826139
            ("Metal3", 0.6418),  # nseg=262177
        ],
    },
    "5LM_1TM_9K": {
        "bst": [
            ("Metal1", 0.5771),  # nseg=830
            ("Metal2", 0.7096),  # nseg=762266
            ("Metal3", 0.7551),  # nseg=280473
            ("Metal4", 0.6517),  # nseg=9290
            ("Metal5", 0.6876),  # nseg=535
        ],
        "typ": [
            ("Metal1", 0.5424),  # nseg=830
            ("Metal2", 0.6958),  # nseg=762266
            ("Metal3", 0.7426),  # nseg=280473
            ("Metal4", 0.6315),  # nseg=9290
            ("Metal5", 0.6625),  # nseg=535
        ],
        "wst": [
            ("Metal1", 0.5116),  # nseg=830
            ("Metal2", 0.6881),  # nseg=762266
            ("Metal3", 0.7352),  # nseg=280473
            ("Metal4", 0.6178),  # nseg=9290
            ("Metal5", 0.6431),  # nseg=535
        ],
    },
    "5LM_1TM_11K": {
        "bst": [
            ("Metal1", 0.5867),  # nseg=890
            ("Metal2", 0.7092),  # nseg=762677
            ("Metal3", 0.7555),  # nseg=280750
            ("Metal4", 0.6555),  # nseg=9262
            ("Metal5", 0.6468),  # nseg=518
        ],
        "typ": [
            ("Metal1", 0.5516),  # nseg=890
            ("Metal2", 0.6953),  # nseg=762677
            ("Metal3", 0.7430),  # nseg=280750
            ("Metal4", 0.6356),  # nseg=9262
            ("Metal5", 0.6215),  # nseg=518
        ],
        "wst": [
            ("Metal1", 0.5205),  # nseg=890
            ("Metal2", 0.6876),  # nseg=762677
            ("Metal3", 0.7356),  # nseg=280750
            ("Metal4", 0.6221),  # nseg=9262
            ("Metal5", 0.6013),  # nseg=518
        ],
    },
    "6LM_1TM_9K": {
        "bst": [
            ("Metal1", 0.5527),  # nseg=1037
            ("Metal2", 0.6967),  # nseg=760157
            ("Metal3", 0.7441),  # nseg=279909
            ("Metal4", 0.6561),  # nseg=8004
            ("Metal5", 0.6304),  # nseg=1008
            ("MetalTop", 0.5338),  # nseg=4
        ],
        "typ": [
            ("Metal1", 0.5155),  # nseg=1037
            ("Metal2", 0.6838),  # nseg=760157
            ("Metal3", 0.7326),  # nseg=279909
            ("Metal4", 0.6353),  # nseg=8004
            ("Metal5", 0.6032),  # nseg=1008
            ("MetalTop", 0.5046),  # nseg=4
        ],
        "wst": [
            ("Metal1", 0.4824),  # nseg=1037
            ("Metal2", 0.6763),  # nseg=760157
            ("Metal3", 0.7254),  # nseg=279909
            ("Metal4", 0.6208),  # nseg=8004
            ("Metal5", 0.5801),  # nseg=1008
            ("MetalTop", 0.4816),  # nseg=4
        ],
    },
}


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

        # Name of the top routing layer. Only the 6LM stackup calls it
        # 'MetalTop'; 3/4/5LM top out at Metal3/4/5. No GF180 tech LEF defines a
        # 'Metal6', so deriving the name as Metal<max_layer> makes OpenROAD fail
        # with 'GRT-0005 Layer Metal6 not found' on the 6LM variants.
        top_layer = "MetalTop" if max_layer == 6 else f"Metal{max_layer}"

        # The 30K thickness option gives the top metal a 2.2um minimum width,
        # which changes both what the power grid may draw on it and whether the
        # router can use it at all. Only 3LM and 4LM ship a 30K option.
        thick_top = stackup.endswith("_30K")

        with self.active_dataroot("lambdapdk"):
            # APR Setup
            with self.active_fileset("views.lef"):
                self.add_file(pdk_path / "apr" / f"gf180mcu_{stackup}_{libtype}_tech.lef")
                for tool in ('openroad', 'klayout', 'magic'):
                    self.add_aprtechfileset(tool)

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

        self.set_aprroutinglayers(min="Metal1", max=top_layer)

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
            self.add_klayout_drcparam(drc, "report=<report>")
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
            if libtype == "7t":
                self.add_openroad_pinlayers(vertical="Metal2", horizontal="Metal3")
            else:
                self.add_openroad_pinlayers(vertical="Metal3", horizontal="Metal2")
            self.set_aprroutinglayers(min="Metal2", max="Metal3")
        elif max_layer == 4:
            self.set_openroad_rclayers(signal="Metal2", clock="Metal3")
            if thick_top:
                # The 30K option's top metal is a 2.2um-minimum-width power/RDL
                # layer, not a signal layer. OpenROAD cannot build a legal
                # single-cut via up to it -- the enclosure rule yields a 0.50um
                # landing pad against a 2.2um minimum width, so detailed routing
                # fails with 'DRT-0234 Via3 does not have single-cut via' -- and
                # a signal wire there would be 2.2um wide on a 4.0um pitch,
                # carrying almost no routing capacity for the trouble. Stop
                # signals below it and leave it to the power grid, which is what
                # its width suits it for. Pin layers follow the routing down;
                # directions are the tech LEF's (Metal2 vertical, Metal3
                # horizontal).
                self.set_aprroutinglayers(min="Metal1", max="Metal3")
                self.add_openroad_pinlayers(vertical="Metal2", horizontal="Metal3")
            else:
                self.add_openroad_pinlayers(vertical="Metal4", horizontal="Metal3")
        elif max_layer >= 5:
            self.set_openroad_rclayers(signal="Metal3", clock="Metal4")
            self.add_openroad_pinlayers(vertical="Metal4", horizontal="Metal3")

        # Openroad global routing grid derating, up to this stackup's top layer.
        openroad_layer_adjustments = {
                'Metal1': 0.25,
                'Metal2': 0.25,
                'Metal3': 0.25,
                'Metal4': 0.25,
                'Metal5': 0.25,
                'MetalTop': 1.0
        }
        for layer, adj in openroad_layer_adjustments.items():
            self.set_openroad_globalroutingderating(layer, adj)
            if layer == top_layer:
                break

        # PEX (Liberty units are pf,Ohm)
        with self.active_dataroot("lambdapdk"):
            if stackup not in _PEX:
                return

            for corner, layers in _PEX_CORRECTION.get(stackup, {}).items():
                for layer, cap_factor in layers:
                    self.add_openroad_rccorrection(corner, layer, cap_factor=cap_factor)

            for corner in ["bst", "typ", "wst"]:
                for layer, res, cap in _PEX[stackup][corner]:
                    if cap is None:
                        self.add_openroad_rclayer(corner, "via", layer, res)
                    else:
                        self.add_openroad_rclayer(corner, "routing", layer, res, cap * pF)

                stem = f'gf180mcu_1p{stackup.replace("L", "").lower()}_sp_smim'
                base_name = f"{stem}_OPT{_PEX_MIM_OPTION[stackup]}_{corner}"
                with self.active_fileset(f"openroad.pex.{corner}"):
                    self.add_file(pdk_path / "pex" / "openroad" / f"{base_name}.rules",
                                  filetype="openrcx")

                    self.add_pexmodelfileset("openroad", corner)


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
