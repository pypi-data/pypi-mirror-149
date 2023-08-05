"""ViSP tags."""
from enum import Enum

from dkist_processing_common.models.tags import Tag


class VispStemName(str, Enum):
    """ViSP specific tag stems."""

    beam = "BEAM"
    raster_step = "RASTER_STEP"  # The number of the current step within a raster scan
    modstate = "MODSTATE"
    file_id = "FILE_ID"


class VispTag(Tag):
    """ViSP specific tag formatting."""

    @classmethod
    def beam(cls, beam_num: int) -> str:
        """
        Tags by beam number.

        Parameters
        ----------
        beam_num: int
            The beam number

        """
        return cls.format_tag(VispStemName.beam, beam_num)

    @classmethod
    def raster_step(cls, raster_scan_step_num: int) -> str:
        """
        Tags by raster step.

        Parameters
        ----------
        raster_scan_step_num: int
            The raster scan step number

        """
        return cls.format_tag(VispStemName.raster_step, raster_scan_step_num)
