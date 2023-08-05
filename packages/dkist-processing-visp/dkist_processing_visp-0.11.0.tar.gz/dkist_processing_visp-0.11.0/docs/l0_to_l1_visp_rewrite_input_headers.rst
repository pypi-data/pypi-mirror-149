ViSP Level 0 Pipeline (rewrite input headers)
=====================================================

In the normal VISP operating mode, raw VISP data is gathered at the summit and delivered to the Data Center.
This pipeline contains an extra task which ignores the values of DKIST008 and DKIST009, dynamically calculating the values from other keywords in the headers.

The Data Center then calibrates this data and prepares it for storage using the following workflow.

For more detail on each workflow task, you can click on the task in the diagram.

.. workflow_diagram:: dkist_processing_visp.workflows.l0_to_l1_visp_rewrite_input_headers.rewrite_input_headers

In this workflow, raw dark, gain, and polarization calibration data is used to generate calibration products that are then applied to the science frames before repackaging them for storage and delivery to a science user.
