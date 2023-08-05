"""PickyBud for checking that each (dsps_num, modstate, raster step) tuple only has a single exposure."""
from typing import List
from typing import Tuple
from typing import Type
from typing import Union

from dkist_processing_common.models.flower_pot import SpilledDirt
from dkist_processing_common.models.flower_pot import Stem
from dkist_processing_common.models.flower_pot import Thorn

from dkist_processing_visp.parsers.visp_l0_fits_access import VispL0FitsAccess


class PickySingleExposurePerRasterStepBud(Stem):
    """PickyBud for checking that each (dsps_num, modstate, raster step) tuple only has a single exposure."""

    def __init__(self):
        super().__init__(stem_name="PICKY_SINGLE_EXPOSURE_PER_RASTER_STEP")

        self.modstate_key = "modulator_state"
        self.step_num_key = "raster_scan_step"
        self.dsps_num_key = "current_dsps_repeat"

    def setter(self, fits_obj: VispL0FitsAccess) -> Union[Type[SpilledDirt], Tuple[int, int, int]]:
        """
        Setter for the bud.

        Parameters
        ----------
        fits_obj:
            A single FitsAccess object
        """
        if fits_obj.ip_task_type != "observe":
            return SpilledDirt

        dsps_num = getattr(fits_obj, self.dsps_num_key)
        modstate = getattr(fits_obj, self.modstate_key)
        single_step = getattr(fits_obj, self.step_num_key)

        return dsps_num, modstate, single_step

    def getter(self, key) -> Type[Thorn]:
        """
        Check that a single dsps repeat of a single raster step only has a single exposure for each modstate.

        If the check fails then raise an error, otherwise return a Thorn, which does nothing
        """
        mod_step_tuples: List[Tuple[int, int, int]] = list(self.key_to_petal_dict.values())
        if sorted(set(mod_step_tuples)) != sorted(mod_step_tuples):
            random_count = mod_step_tuples.count(mod_step_tuples[0])
            raise ValueError(
                f"More than one exposure detected for a single dsps repeat of a single map step. (Randomly chosen step has {random_count} exposures)."
            )

        return Thorn
