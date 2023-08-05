"""Data Tier API.

    The interface layer between the mini-apps-data-tier repo and the
    data-manager-metadata repo.

    Note that:
    - dataset metadata is the metadata that is stored at the dataset level in the data manager.
    This has labels and property changes (like the description)
    - version metadata is the metadata that is stored at the dataset version level in the data
    manager. This does not have labels but has the other types of annotations such as
    ServiceExecution and FieldsDescriptor
    - travelling metadata is a combination of dataset and version metadata that is typically
    downloaded to a project as a meta.json file, added to after a job and then re-uploaded back
    as a dataset.
    - The job related annotations that are added to the metadata depend on the configuration
    and specification of the job.

"""
from typing import Any, Dict, Tuple, Optional
import copy
import os
import json
import logging

from data_manager_metadata.metadata import Metadata, ServiceExecutionAnnotation
from data_manager_metadata.exceptions import AnnotationValidationError

basic_logger = logging.getLogger('basic')
basic_logger.setLevel(logging.INFO)
basic_handler = logging.StreamHandler()
basic_formatter = logging.Formatter('%(asctime)s # %(levelname)s %(message)s')
basic_handler.setFormatter(basic_formatter)
basic_logger.addHandler(basic_handler)


def get_metadata_filenames(filepath: str) -> Tuple[str, str]:
    """Return the associated metadata and schema filenames for a particular
    filepath.
    """
    _METADATA_EXT = '.meta.json'
    _SCHEMA_EXT = '.schema.json'

    assert filepath

    # Get filename stem from filepath
    # so in: 'filename.sdf.gz', we would get just 'filename'
    file_basename = os.path.basename(filepath)
    filename_stem = file_basename.split('.')[0]
    return filename_stem + _METADATA_EXT, filename_stem + _SCHEMA_EXT


# Dataset Methods
def post_dataset_metadata(
    dataset_name: str,
    dataset_id: str,
    description: str,
    created_by: str,
    **metadata_params: Any,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Create a metadata class at the dataset level.
    Returns a json schema that will be used for label searches at the
    dataset level.

    Args:
        dataset_name
        dataset_id
        description
        created_by
        **metadata_params (optional keyword arguments)

    Returns:
        metadata dict
        json_schema
    """

    # At dataset level only labels and property changes allowed.
    if 'annotations' in metadata_params:
        del metadata_params['annotations']

    # At dataset level, the version should not be set.
    if 'dataset_version' in metadata_params:
        del metadata_params['dataset_version']

    # Create the dictionary with the remaining parameters
    metadata = Metadata(
        dataset_name, dataset_id, description, created_by, **metadata_params
    )
    return metadata.to_dict(), metadata.get_json_schema()


def post_version_metadata(
    dataset_metadata: Dict[str, Any], version: int, **metadata_params: Any
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Create a metadata class at the version level.

    Args:
        dataset metadata
        version
        **metadata_params (optional keyword arguments)

    Returns:
        metadata dict
        json_schema
    """
    # At version level only labels are not allowed.
    if 'labels' in metadata_params:
        del metadata_params['labels']

    version_metadata = Metadata(
        dataset_metadata['dataset_name'],
        dataset_metadata['dataset_id'],
        dataset_metadata['description'],
        dataset_metadata['created_by'],
        dataset_version=version,
        **metadata_params,
    )

    return version_metadata.to_dict(), get_version_schema(
        dataset_metadata, version_metadata.to_dict()
    )


def patch_dataset_metadata(
    dataset_metadata: Dict[str, Any], **metadata_params: Any
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Update the metadata at the dataset level.

    The metadata_params will be limited to the following parameters:
    description
    labels

    Other types will be ignored (no error returned in this case).

    Args:
        dataset_metadata: to be updated
        **metadata_params (optional keyword arguments)

    Returns:
        metadata dict
        json_schema
    """

    metadata = Metadata(**dataset_metadata)

    if 'description' in metadata_params:
        metadata.set_description(metadata_params['description'])

    if 'labels' in metadata_params:
        metadata.add_labels(metadata_params['labels'])

    return metadata.to_dict(), metadata.get_json_schema()


def get_version_schema(
    dataset_metadata: Dict[str, Any], version_metadata: Dict[str, Any]
) -> Dict[str, Any]:
    """Get the current json schema at the version level.

    Note that this must be called for each version of the dataset after
    a patch_dataset_metadata call to update the json schema with any
    inherited changed attributes from the dataset level.

    Args:
        version metedata

    Returns:
        json_schema
    """
    d_metadata = Metadata(**dataset_metadata)
    v_metadata = Metadata(**version_metadata)
    v_metadata.add_labels(d_metadata.get_labels())

    return v_metadata.get_json_schema()


def patch_version_metadata(
    dataset_metadata: Dict[str, Any],
    version_metadata: Dict[str, Any],
    **metadata_params: Any,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Update metadata at the version level.
    This is only used for updating annotations and description.

    Args:
        dataset_metadata
        version_metadata
        **metadata_params (optional keyword arguments)

    Returns:
        metadata dict
        json_schema
    """
    d_metadata = Metadata(**dataset_metadata)
    v_metadata = Metadata(**version_metadata)

    if 'description' in metadata_params:
        v_metadata.set_description(metadata_params['description'])

    if 'annotations' in metadata_params:
        v_metadata.add_annotations(metadata_params['annotations'])

    # This adds the dataset labels to the version metadata so
    # we can extract the json schema with both labels and annotations.
    schema_metadata = Metadata(**v_metadata.to_dict())
    schema_metadata.add_labels(d_metadata.get_labels())

    return v_metadata.to_dict(), schema_metadata.get_json_schema()


# Travelling Metadata Methods
def get_travelling_metadata(
    dataset_metadata: Dict[str, Any], version_metadata: Dict[str, Any]
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Returns "travelling metadata" at the version level. Travelling
    metadata is used when a dataset is added to project.

    It contains the labels from the dataset level and has
    a roll forward date set for re-synchronisation with the metadata
    in the data-tier.

    Args:
        dataset_metadata
        version_metadata

    Returns:
        travelling metadata dict
        travelling json_schema
    """

    d_metadata = Metadata(**dataset_metadata)
    v_metadata = Metadata(**version_metadata)
    d_metadata.add_annotations(v_metadata.get_annotations_dict())
    d_metadata.set_synchronised_datetime()
    d_metadata.set_dataset_version(v_metadata.get_dataset_version())
    return d_metadata.to_dict(), d_metadata.get_json_schema()


def post_travelling_metadata_to_new_dataset(
    travelling_metadata: Dict[str, Any], version: int
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """Creates dataset metadata with the results of the voyage.

    This method will be used when a completely new dataset is to be created
    from the travelling metadata.

    Args:
        travelling_metadata
        version

    Returns:
        dataset metadata
        dataset schema
        version metadata
        version json schema
    """

    d_metadata_params = {'labels': copy.deepcopy(travelling_metadata['labels'])}
    v_metadata_params = {
        'annotations': copy.deepcopy(travelling_metadata['annotations'])
    }

    dataset_metadata, dataset_schema = post_dataset_metadata(
        travelling_metadata['dataset_name'],
        travelling_metadata['dataset_id'],
        travelling_metadata['description'],
        travelling_metadata['created_by'],
        **d_metadata_params,
    )

    version_metadata, version_schema = post_version_metadata(
        dataset_metadata, version, **v_metadata_params
    )

    return dataset_metadata, dataset_schema, version_metadata, version_schema


def patch_travelling_metadata(
    travelling_metadata: Dict[str, Any], **metadata_params: Any
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Updates en-route "travelling metadata" at the version level.
    Note that currently, only the description, labels and annotations
    can be changed. Other values are set automatically.

    Args:
        travelling_metadata
        **metadata_params (optional keyword arguments)

    Returns:
        travelling metadata dict
        travelling json_schema
    """
    metadata = Metadata(**travelling_metadata)

    if 'description' in metadata_params:
        metadata.set_description(metadata_params['description'])

    if 'labels' in metadata_params:
        metadata.add_labels(metadata_params['labels'])

    if 'annotations' in metadata_params:
        metadata.add_annotations(metadata_params['annotations'])

    return metadata.to_dict(), metadata.get_json_schema()


def post_travelling_metadata_to_existing_dataset(
    travelling_metadata: Dict[str, Any], dataset_metadata: Dict[str, Any], version: int
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """Updates version metadata with the results of the voyage.

    Note that if the labels have changed, a get_version_schema will be required
    for all versions of the dataset to update the json schemas

    Args:
        travelling_metadata
        dataset_metadata
        dataset_version

    Returns:
        dataset metadata
        dataset schema
        version metadata
        version json schema
    """

    t_metadata = Metadata(**travelling_metadata)
    synchronised_datetime = t_metadata.get_synchronised_datetime()

    d_metadata_params = {
        'labels': copy.deepcopy(t_metadata.get_unapplied_labels(synchronised_datetime))
    }
    v_metadata_params = {
        'annotations': copy.deepcopy(travelling_metadata['annotations'])
    }

    dataset_metadata, dataset_schema = patch_dataset_metadata(
        dataset_metadata, **d_metadata_params
    )

    version_metadata, version_schema = post_version_metadata(
        dataset_metadata, version, **v_metadata_params
    )

    return dataset_metadata, dataset_schema, version_metadata, version_schema


# Job Annotation Methods
def _get_derived_metadata(
    project_directory: str, username: str, source_file: str = '', derived_from: str = ''
) -> Dict[str, Any]:
    """Return or create metadata for derived_from file."""

    if isinstance(source_file, str):
        # If the source_file is a string then check for it. We don't allow multiple input files
        # for the source metadata yet - future extension (see sc-2608 Tims comment)
        meta_file, dummy = get_metadata_filenames(source_file)
        meta_dir = os.path.dirname(source_file)
        meta_path = os.path.join(project_directory, meta_dir, meta_file)
        print(meta_path)

        if os.path.isfile(meta_path):
            with open(meta_path, 'rt', encoding='utf8') as meta_file:
                return json.load(meta_file)

    # Create the dictionary with the remaining parameters
    metadata = Metadata(derived_from, 'None', 'Automatically created by job', username)
    return metadata.to_dict()


def _create_service_execution(
    service_parameters: Dict[str, Any], username: str, output_spec
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Creates a service execution annotation based on the input specification

    Returns:
         1. The service execution annotation and
         2. the Fields that have been added (used in creating the parameters file.
    """

    fields_descriptor = output_spec["annotation-properties"]['fields-descriptor']
    service_execution = output_spec["annotation-properties"]['service-execution']

    job = service_parameters['job']
    version = service_parameters['version']

    # Remove the job and version from the specification as we already have them
    service_parameters.pop('job', None)
    service_parameters.pop('version', None)

    # Remove the duplicated annotation-properties from the service_parameters
    for values in service_parameters['outputs'].values():
        if values.get('annotation-properties'):
            values.pop('annotation-properties', None)

    # print(job)
    # print(version)
    # print(username)
    # #print(job_application_spec['name'])
    # print(service_execution['service_ref'])
    # print(service_parameters)
    # print(fields_descriptor['origin'])
    # print(fields_descriptor['description'])
    # print(fields_descriptor['fields'])

    try:
        # service: str, - instance.job - checked when spec created
        # service_version: str - instance.version - checked when spec created
        # service_user: str - From instance
        # service_name : str - From application-parameters - currently set to the name
        #                      as this is required in the annotation.
        # service_ref: str  - From application-parameters
        # service_parameters: dict = From manipulated rendered specification,
        # origin: str '' - From application-parameters
        # description: str - From application-parameters
        # properties: list - From application-parameters
        annotation = ServiceExecutionAnnotation(
            job,
            version,
            username,
            # job_application_spec['name'],
            job,
            service_execution['service_ref'],
            service_parameters,
            fields_descriptor['origin'],
            fields_descriptor['description'],
            fields_descriptor['fields'],
        )
        return annotation.to_dict(), fields_descriptor['fields']
    except AnnotationValidationError as e:
        basic_logger.info('AnnotationValidationError=%s', e.message)
        return None, None
    except:  # pylint: disable=bare-except
        basic_logger.info('Unexpected Error')
        return None, None


def _get_params_filename(filepath: str) -> str:
    """Return the associated parameter filename for a particular
    filepath.
    """
    _PARAM_EXT = '.params.json'

    assert filepath

    # Get filename stem from filepath
    # so in: 'filename.sdf.gz', we would get just 'filename'
    file_basename = os.path.basename(filepath)
    filename_stem = file_basename.split('.')[0]
    return filename_stem + _PARAM_EXT


def _create_param_file(
    fields: Dict[str, Any], result_path: str, result_filename: str
) -> str:
    """Creates a parameter file if requested from the fields that were added in
    Service Execution annotation.
    Returns the filename if created
    """
    params_filename = _get_params_filename(result_filename)
    params_path = os.path.join(result_path, params_filename)

    result_params = {}
    for key, values in fields.items():
        result_params[key] = values['description']

    with open(params_path, 'wt', encoding='utf8') as params_file:
        # Dump params of fields created
        json.dump(result_params, params_file)

    return params_path


def _create_annotations(
    project_directory: str,
    job_application_spec: Dict[str, Any],
    job_rendered_spec: Dict[str, Any],
    output_spec: Dict[str, Any],
    username: str,
    create_param_file: bool = False,
) -> Tuple[list, str]:

    """For each specified output file with a set of annotations-parameters,
    create a metadata file in the directory specified.

    Initially this will contain a service execution annotation based on
    the specification data.

    Errors will be simply suppressed as this should not stop a job completing

    If create_param_file is set to True, then also create a json file containing a list of
    the parameters added to the SDF.

    Returns a Tuple of booleans indicating whether a metadata file and/or parameter file has
    been created.

    """

    meta_files = []
    param_files = ''

    # Some sanity-checking before we go any further...
    if not project_directory:
        return meta_files, param_files
    if not output_spec["creates"]:
        return meta_files, param_files
    if not output_spec["annotation-properties"].get('fields-descriptor'):
        return meta_files, param_files
    if not output_spec["annotation-properties"].get('service-execution'):
        return meta_files, param_files

    basic_logger.info('sanity checks OK')

    # Take service parameters from rendered specification and modify.
    service_parameters: Dict[str, Any] = copy.deepcopy(job_rendered_spec)

    # Check if there are any variables in the original spec. If so, add them
    variables: Optional[Dict[str, Any]] = job_application_spec.get('variables')
    service_parameters['variables'] = variables

    # If there is a derived-from parameter in the service-execution spec
    # then there might be an existing travelling metadata file attached to the input file.
    # Look for this in the project_directory.
    # If it exists, any annotations should be added to it and this will be the metadata for the
    # associated results file.
    # If it does not exist - create a new travelling metadata file with the annotations.

    if 'derived-from' in output_spec["annotation-properties"]:
        derived_from = output_spec["annotation-properties"]['derived-from']
        source_file = service_parameters['variables'][derived_from]
        derived_metadata = _get_derived_metadata(
            project_directory, username, source_file, derived_from
        )
    else:
        derived_metadata = _get_derived_metadata(project_directory, username)

    se_annotation, fields = _create_service_execution(
        service_parameters, username, output_spec
    )

    basic_logger.info('se_annotation=%s', se_annotation)

    if se_annotation:
        results_metadata, results_schema = patch_travelling_metadata(
            derived_metadata, annotations=se_annotation
        )
    else:
        return meta_files, param_files

    basic_logger.info('results_metadata=%s', results_metadata)

    result_dir = os.path.dirname(output_spec['creates'])
    result_filename = os.path.basename(output_spec['creates'])
    results_metadata_filename, results_schema_filename = get_metadata_filenames(
        result_filename
    )

    result_path = os.path.join(project_directory, result_dir)

    if not os.path.isdir(result_path):
        return meta_files, param_files

    results_metadata_path = os.path.join(result_path, results_metadata_filename)
    results_schema_path = os.path.join(result_path, results_schema_filename)

    with open(results_metadata_path, 'wt', encoding='utf8') as meta_file:
        # Dump metadata including the SE annotation
        json.dump(results_metadata, meta_file)
        meta_files.append(results_metadata_path)

    with open(results_schema_path, 'wt', encoding='utf8') as schema_file:
        # Dump metadata including the SE annotation
        json.dump(results_schema, schema_file)
        meta_files.append(results_schema_path)

    basic_logger.info('fields=%s', fields)

    if fields and create_param_file:
        param_files = _create_param_file(fields, result_path, result_filename)

    return meta_files, param_files


def create_job_annotations(
    project_directory: str,
    job_application_spec: Dict[str, Any],
    job_rendered_spec: Dict[str, Any],
    username: str,
    create_param_file: bool = False,
) -> list:
    """Update(Create) travelling metadata class(es) with Service Execution annotation generated
    from a Squonk job definition.

    Note that unlike the methods above, this method will actually create json files based on
    the job_application_spec and job_rendered_spec.

    If a meta.json exists for an input file then this can optionally be used as a source for
    existing annotations, allowing them to propagate through a workflow.
    If a meta.json does not exist for an input file this is not treated as an error.

    Args:
        project_directory - The project directory. This is used as the root directory for
                            looking for input travelling metadata files.
        job_application_spec - This the section for the job definition taken from the
                            virtual-screening.yaml file.
        job_rendered_spec - Rendered job specification from the posted instance in the
                            data manager.
        create_param_file - (optional) If set to true a json dict will be written to a file
                            containing descriptions of the parameters added as part of the Service
                            Execution.

    Returns:
        metadata: list - returns a list of metadata and schema files have been created
        params: list - returns a list of any param_files that have been created
    """

    # Say Hello
    basic_logger.info('+ create_job_annotations')

    written_files = []
    outputs: Optional[Dict[str, Any]] = job_rendered_spec.get('outputs')
    if not outputs:
        return written_files

    # Loop through the output specifications for the different outputs
    for output_spec in outputs.values():
        if output_spec.get('annotation-properties'):
            meta, param_file = _create_annotations(
                project_directory,
                job_application_spec,
                job_rendered_spec,
                output_spec,
                username,
                create_param_file,
            )

            basic_logger.info('meta_files=%s', meta)
            basic_logger.info('param_files=%s', param_file)
            written_files.extend(meta)
            if param_file:
                written_files.append(param_file)

    return written_files
