# Import necessary classes from the siliconcompiler framework and the LambdaPDK.
import warnings
from typing import Optional

from siliconcompiler import ASIC
from siliconcompiler.targets import icsprout55_demo as sc_ics55_demo


####################################################
# Target Setup Function
####################################################
def ics55_demo(
        project: ASIC,
        syn_np: int = 1,
        floorplan_np: int = 1, place_np: int = 1, cts_np: int = 1, route_np: int = 1,
        timing_np: int = 1,
        language: Optional[str] = None):
    """
        Deprecated alias for :func:`siliconcompiler.targets.icsprout55_demo`.

        The ICsprout 55nm target now ships with siliconcompiler; this wrapper forwards every
        argument unchanged and will be removed in a future release. Import the target from
        ``siliconcompiler.targets`` instead.

        Parameters:
            * project (ASIC): The siliconcompiler project to configure.
            * syn_np (int): Parallelism for synthesis-related steps.
            * floorplan_np (int): Parallelism for floorplanning.
            * place_np (int): Parallelism for placement.
            * cts_np (int): Parallelism for clock-tree synthesis.
            * route_np (int): Parallelism for routing.
            * timing_np (int): Parallelism for timing analysis (synthesis-only flow).
            * language (str): Elaboration language, detected from the design if not given.
        """
    warnings.warn(
        "lambdapdk.icsprout55.target.ics55_demo is deprecated, "
        "please use siliconcompiler.targets.icsprout55_demo instead",
        DeprecationWarning,
        stacklevel=2)
    sc_ics55_demo(
        project=project,
        syn_np=syn_np,
        floorplan_np=floorplan_np,
        place_np=place_np,
        cts_np=cts_np,
        route_np=route_np,
        timing_np=timing_np,
        language=language)
