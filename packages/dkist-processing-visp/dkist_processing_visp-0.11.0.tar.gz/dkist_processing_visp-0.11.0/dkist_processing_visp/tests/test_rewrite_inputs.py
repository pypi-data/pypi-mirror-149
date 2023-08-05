from itertools import chain

import pytest
from astropy.io import fits
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.tags import Tag

from dkist_processing_visp.tasks.rewrite_inputs import RewriteInputFramesToCorrectHeaders
from dkist_processing_visp.tests.conftest import FakeGQLClient
from dkist_processing_visp.tests.conftest import generate_fits_frame
from dkist_processing_visp.tests.conftest import VispHeadersValidObserveFrames


@pytest.fixture(scope="function")
def rewrite_inputs_valid_task(tmp_path, recipe_run_id):
    with RewriteInputFramesToCorrectHeaders(
        recipe_run_id=recipe_run_id,
        workflow_name="rewrite_inputs_valid_task",
        workflow_version="VX.Y",
    ) as task:
        number_of_dsps_repeats = 3
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task._scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            ds1 = VispHeadersValidObserveFrames(
                dataset_shape=(number_of_dsps_repeats, 2, 2),
                array_shape=(1, 2, 2),
                time_delta=10,
                num_dsps_repeats=1,
                dsps_repeat=1,
                num_raster_steps=3,
                raster_step=0,
                num_modstates=1,
                modstate=1,
                polarimeter_mode="observe_polarimetric",
            )
            ds2 = VispHeadersValidObserveFrames(
                dataset_shape=(number_of_dsps_repeats, 2, 2),
                array_shape=(1, 2, 2),
                time_delta=10,
                num_dsps_repeats=1,
                dsps_repeat=1,
                num_raster_steps=3,
                raster_step=1,
                num_modstates=1,
                modstate=1,
                polarimeter_mode="observe_polarimetric",
            )
            ds3 = VispHeadersValidObserveFrames(
                dataset_shape=(number_of_dsps_repeats, 2, 2),
                array_shape=(1, 2, 2),
                time_delta=10,
                num_dsps_repeats=1,
                dsps_repeat=1,
                num_raster_steps=3,
                raster_step=2,
                num_modstates=1,
                modstate=1,
                polarimeter_mode="observe_polarimetric",
            )
            ds = chain(ds1, ds2, ds3)
            header_generator = (d.header() for d in ds)
            for i in range(9):
                hdul = generate_fits_frame(header_generator=header_generator)
                task.fits_data_write(hdu_list=hdul, tags=[Tag.input(), Tag.frame()])
            yield task, number_of_dsps_repeats
        except:
            raise
        finally:
            task.scratch.purge()
            task.constants._purge()


def test_incorrect_dsps_headers(rewrite_inputs_valid_task, mocker):
    """
    Given: Frames with DKIST008 and DKIST009 both equal to 1
    When: Changing the header values to account for the number of raster maps in the data
    Then: The headers correctly reflect the expected number of raster maps
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    # When
    t, number_of_dsps_repeats = rewrite_inputs_valid_task
    t()
    # Then
    files = t.read(tags=[Tag.input(), Tag.frame()])
    current_dsps_repeat = []
    for file in files:
        hdul = fits.open(file)
        assert hdul[0].header["DSPSREPS"] == number_of_dsps_repeats
        assert hdul[0].header["DKIST008"] == number_of_dsps_repeats
        current_dsps_repeat.append(hdul[0].header["DSPSNUM"])
    assert current_dsps_repeat.count(1) == number_of_dsps_repeats
    assert current_dsps_repeat.count(2) == number_of_dsps_repeats
    assert current_dsps_repeat.count(3) == number_of_dsps_repeats
