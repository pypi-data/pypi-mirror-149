"""Rewrite input files to correct header values."""
from collections import defaultdict
from datetime import datetime

from astropy.io import fits
from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_processing_common.tasks.mixin.fits import FitsDataMixin

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.parsers.visp_l0_fits_access import VispL0FitsAccess


class RewriteInputFramesToCorrectHeaders(WorkflowTaskBase, FitsDataMixin):
    """Rewrite DSPS headers to correct values from summit."""

    record_provenance = True

    def run(self) -> None:
        """Rewrite DSPS headers to correct values from summit."""
        with self.apm_task_step("Get modulator states and raster scan steps from headers"):
            # Record some information for checks
            number_of_raster_steps = set()
            number_of_modulator_states = set()

            # Get needed information from observe headers
            observe_data = defaultdict(lambda: defaultdict(list))
            for fits_obj in self.fits_data_read_fits_access(
                tags=[VispTag.input(), VispTag.frame()], cls=VispL0FitsAccess
            ):
                # Get the header values out of observe data and sort them by raster scan step
                if fits_obj.ip_task_type == "observe":
                    # Keep using the FitsAccess object but drop the data property for memory reasons
                    observe_data[fits_obj.raster_scan_step][fits_obj.modulator_state].append(
                        VispL0FitsAccess.from_header(fits_obj.header, name=fits_obj.name)
                    )
                    number_of_raster_steps.add(fits_obj.total_raster_steps)
                    number_of_modulator_states.add(fits_obj.number_of_modulator_states)

        with self.apm_task_step("Sort observe files into individual scans"):
            # Sort the filenames into individual scans
            dsps_repeat_mapping = defaultdict(list)
            for raster_scan_step, modulator_states in observe_data.items():
                for modulator_state, fits_objs in modulator_states.items():
                    sorted_fits_objs = sorted(
                        fits_objs,
                        key=lambda x: self.format_date_beg(date_beg=x.time_obs),
                    )
                    for index, fits_obj in enumerate(sorted_fits_objs):
                        dsps_repeat = index + 1  # dsps repeats count from 1, not 0
                        dsps_repeat_mapping[dsps_repeat].append(fits_obj)

            # Get the number of scans
            number_of_dsps_reps = len(dsps_repeat_mapping)

        with self.apm_task_step("Perform checks to make sure data meets certain constraints"):
            # Make sure all observe frames have the same number of raster steps
            if len(number_of_raster_steps) > 1:
                raise ValueError(
                    f"Expected one value for the number of raster steps. Found {len(number_of_raster_steps)}"
                )
            # Make sure all observe frames have the same number of modulator states
            if len(number_of_modulator_states) > 1:
                raise ValueError(
                    f"Expected one value for the number of modulator states. Found {len(number_of_modulator_states)}"
                )
            # Make sure each map contains number_of_raster_steps * number_of_modulator_states frames
            for dsps_rep, frames in dsps_repeat_mapping.items():
                if len(frames) != (
                    next(iter(number_of_raster_steps)) * next(iter(number_of_modulator_states))
                ):
                    raise ValueError(
                        f"Expected {next(iter(number_of_raster_steps)) * next(iter(number_of_modulator_states))} frames in dsps rep {dsps_rep}. Found {len(frames)}."
                    )

        with self.apm_task_step("Rewrite each observe frame with the right scan numbers"):
            for dsps_repeat, fits_objs in dsps_repeat_mapping.items():
                for fits_obj in fits_objs:
                    hdul = fits.open(fits_obj.name, mode="update")

                    # Account for compression
                    data_hdu = self.get_data_hdu(hdul)

                    hdul[data_hdu].header["DKIST008"] = number_of_dsps_reps
                    hdul[data_hdu].header["DSPSREPS"] = number_of_dsps_reps
                    hdul[data_hdu].header["DKIST009"] = dsps_repeat
                    hdul[data_hdu].header["DSPSNUM"] = dsps_repeat
                    hdul.flush()

    @staticmethod
    def get_data_hdu(hdul: fits.HDUList) -> int:
        """
        Find a data HDU in an HDU List.

        Parameters
        ----------
        hdul: The hdu list to find the data hdu in
        """
        return hdul[0].data is None

    @staticmethod
    def format_date_beg(date_beg: str) -> datetime:
        """
        Handle datetime formats with and without milliseconds.

        Parameters
        ----------
        date_beg: the datetime from the file to convert to a datetime object
        """
        try:
            return datetime.strptime(date_beg, "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            return datetime.strptime(date_beg, "%Y-%m-%dT%H:%M:%S")
