"""
cdf_helpers.py

High level functionality built on top of Cognite's Python SDK

Most functions require the global cdf client to be set up before using them.
"""
import functools
import json
import os
import sys
import time
from datetime import datetime
from functools import partial
from multiprocessing import Pool
from pathlib import Path
from shutil import make_archive, unpack_archive
from typing import Any, Dict, List, Tuple, Optional, Union

import pandas as pd
from cognite.client import CogniteClient
from cognite.client.data_classes import FileMetadata, FileMetadataUpdate
from cognite.client.exceptions import CogniteAPIError, CogniteNotFoundError
from cognite.experimental.data_classes import Function

from akerbp.mlops.core import config, logger
from akerbp.mlops.core.helpers import confirm_prompt

logging = logger.get_logger(name="mlops_cdf")

global_client = {}
api_keys = config.api_keys

env_vars = {k.upper(): str(v) for k, v in config.envs_dic.items() if v}
env_vars.update({"PLATFORM": "cdf"})
try:
    env_vars.pop("GOOGLE_PROJECT_ID")
except KeyError:
    pass


def set_up_cdf_client(context: str = "run") -> None:
    """
    Set up the global client used by most helpers. This needs to be called
    before using any helper.

    Input:
      - context: string either 'run' (access to data and functions) or 'deploy'
        (access to 'functions' also).
    """
    if context == "run":
        api_key_labels = ["data", "files"]
    elif context == "deploy":
        api_key_labels = ["data", "files", "functions"]
    else:
        raise ValueError("Context should be either 'run' or 'deploy'")

    for k in api_key_labels:
        if k not in global_client:
            global_client[k] = get_client(api_keys[k], k)

    logging.debug("CDF client was set up correctly")


def get_client(api_key: str, api_key_label: Optional[str] = None) -> CogniteClient:
    """
    Create a CDF client with a given api key
    """
    if not api_key:
        raise ValueError("CDF api key is missing")

    if api_key_label == "functions":
        from cognite.experimental import CogniteClient

        logging.warning("Imported CogniteClient from cognite.experimental")
    else:
        from cognite.client import CogniteClient

    client = CogniteClient(
        api_key=api_key,
        project="akbp-subsurface",
        client_name="mlops-client",
        base_url="https://api.cognitedata.com",
    )
    assert client.login.status().logged_in
    logging.debug(f"{client.version=}")
    return client


def validate_function_name(function_name: str, verbose: bool = True) -> bool:
    """
    Validate that function name follows MLOps standard: model-service-env
    Updated to still return true if the external id of the function does
    not follow the mlops convention, to allow listing arbitrary functions.

    Input: (string) function name to validate
    Output: (bool) True if name is valid, False otherwise
    """
    supported_services = ["prediction", "training"]
    supported_environments = ["dev", "test", "prod"]
    # Check external id using mlops convention
    try:
        if len(splitted_function_name := function_name.split("-")) > 3:
            _, service, environment, _ = splitted_function_name
        elif len(splitted_function_name) == 3:
            _, service, environment = splitted_function_name
        else:
            _, service, environment = None, None, None
    except ValueError:
        if verbose:
            m = f"Expected function name format: 'model-service-environment', got {function_name}"
            logging.error(m)
        return True
    if service not in supported_services:
        if verbose:
            m = f"Supported services: {supported_services}, got {service} from {function_name}"
            logging.error(m)
        return True
    if environment not in supported_environments:
        if verbose:
            m = f"Supported environments: {supported_environments}, got {environment} from {function_name}"
            logging.error(m)
        return True
    return True


def delete_function(function_name: str, confirm: bool = True) -> None:
    """
    Delete a deployed function

    Input:
        - function_name: (string) function name (external id), with the format
            'model_name-service-environment'. Use `list_functions` to get an
            overview of deployed functions
        - confirm: (bool) whether the user will be asked to confirm deletion
    """
    if not validate_function_name(function_name):
        raise ValueError()
    model, service, environment = function_name.split("-")

    confirmed = False

    if confirm:
        question = f"Delete {model=}, {service=}, {environment=}?"
        confirmed = confirm_prompt(question)

    if not confirm or confirmed:
        client = global_client["functions"]
        try:
            client.functions.delete(external_id=function_name)
            logging.info(f"Deleted function with external id {function_name}")
        except CogniteNotFoundError:
            logging.error(f"Couldn't find function with external id {function_name}")


def create_function_from_folder(
    human_readable_name: str,
    function_name: str,
    folder: str,
    handler_path: str,
    description: str = "",
    metadata: Dict[str, str] = {},
    owner: str = "",
    secrets: Dict[str, str] = {},
) -> Any:
    """
    Create a Cognite function from a folder. Any existing function with the same
    external id is deleted first.

    Inputs:
      - human_readable_name (str): name of function to create
      - function_name (str): external id of function to create
      - folder (str): path where the source code is located
      - handler_path (str): path to the handler file
      - description: (string) function documentation
      - metadata: (Dict[str, str])
      - owner: (str) the function's owner's email
      - secrets (Dict[str, Any]): api keys or similar that should be passed to the function
    """
    client = global_client["functions"]

    try:
        client.functions.delete(external_id=function_name)
        logging.info(
            f"Function {human_readable_name} with external id {function_name} already exist and will be overwritten"
        )
    except CogniteNotFoundError:
        logging.info(
            f"Function {human_readable_name} with external id {function_name} does not exist and will be created"
        )
        pass

    try:
        function = client.functions.create(
            name=human_readable_name,
            folder=folder,
            function_path=handler_path,
            external_id=function_name,
            description=description,
            metadata=metadata,
            owner=owner,
            secrets=secrets,
            env_vars=env_vars,
        )
        logging.info(
            f"Created function {human_readable_name} with external id {function_name}: {folder=}, {handler_path=}, {env_vars=}"
        )
        logging.info(
            f"Starting deployment of function {human_readable_name} with external id {function_name}"
        )
    except CogniteAPIError as e:
        logging.info(
            f"Failed to create function {human_readable_name} with external id {function_name}"
        )
        logging.info(f"Message returned from the Cognite API: {e.message}")

    return function


def create_function_from_file(
    human_readable_name: str,
    function_name: str,
    file_id: str,
    description: str,
    metadata: Dict[str, str],
    owner: str,
    secrets: Dict[str, str] = {},
) -> Any:
    """
    Create a Cognite function from a file deployed to CDF Files.
    If there exist a function with the same external id, the function is
    overwritten.

    Inputs:
      - human_readable_name (str): name of the function to create
      - function_name: (str) external id of the function to create
      - file_id: (int) the id for the function file in CDF Files
      - description: (str) function documentation
      - owner: (str) the function's owner's email
      - secrets: (optional) api keys or similar that should be passed to the
        function
    """
    client = global_client["functions"]
    try:
        client.functions.delete(external_id=function_name)
        logging.info(
            f"Function {human_readable_name} with external id {function_name} already exist and will be overwritten"
        )
    except CogniteNotFoundError:
        logging.info(
            f"Function {human_readable_name} with external id {function_name} does not exist and will be created"
        )
        pass

    try:
        function = client.functions.create(
            name=human_readable_name,
            file_id=file_id,
            external_id=function_name,
            description=description,
            metadata=metadata,
            owner=owner,
            secrets=secrets,
            env_vars=env_vars,
        )
        logging.debug(
            f"Created function {human_readable_name} with external id {function_name}: {file_id=}, {env_vars=}"
        )
    except CogniteAPIError as e:
        logging.info(
            f"Failed to create function {human_readable_name} with external id {function_name}"
        )
        logging.info(f"Message returned from the Cognite API: {e.message}")

    return function


def robust_create(create_function: partial) -> None:
    """
    Robust creation of a CDF Function. Wait until the function status is ready
    or failed. If it fails, it will try again `max_error` times

    Inputs:
      - create_function: function that creates the CDF function
    """
    max_errors = 3

    for trial in range(max_errors):
        function = create_function()
        status = wait_function_status(function)
        logging.debug(f"Function status is {status}")
        if function.status == "Ready":
            break
        if function.status == "Failed" and trial < max_errors - 1:
            logging.warning(f"Function failed: {function.id=}")
            logging.debug(f"Error was: {function.error=}")
            logging.debug("Try to create function again")
        else:
            raise Exception(f"Function deployment error: {function.error=}")


def deploy_function(
    human_readable_name: str,
    function_name: str,
    folder: str = ".",
    handler_path: str = "handler.py",
    secrets: Dict[str, str] = api_keys,
    info: Dict[str, Union[str, Dict[str, str]]] = {
        "description": "",
        "metadata": {},
        "owner": "",
    },
) -> None:
    """
    Deploys a model as a Cognite function from a folder where the source code is located.
    The argument handler_path points to a file in the folder within which a function named handle is defined.

    Args:
        human_readable_name (str): name of the function to create
        function_name (str): external id of the function to create
        folder (str): path where the source code is located
        handler_path (str): path to the handler file
        secrets (Dict[str, Any]): api keys or similar that should be passed to the function
        info (Dict[str, Union[str, Dict[str, str]]]): dictionary containing info for a specific service, as specified in the settings
    """
    try:
        description = info["description"]
    except KeyError:
        raise Exception(
            "Description field is missing, please update mlops_settings.yaml"
        ) from None

    try:
        owner = info["owner"]
    except KeyError:
        raise Exception(
            "Owner field is missing, please update mlops_settings.yaml"
        ) from None

    try:
        metadata = info["metadata"]
    except KeyError:
        raise Exception(
            "Metadata field is missing, please update mlops_settings.yaml"
        ) from None

    f = functools.partial(
        create_function_from_folder,
        human_readable_name,
        function_name,
        folder,
        handler_path,
        description,
        metadata,
        owner,
        secrets,
    )
    robust_create(f)


def redeploy_function(
    human_readable_name: str,
    function_name: str,
    file_id: int,
    description: str,
    metadata: Dict[str, str],
    owner: str,
    secrets: Dict[str, str] = api_keys,
) -> None:
    """
    Deploys a Cognite function from a folder.

    Inputs:
      - function_name (str): name of the function to create
      - file_id (int): the id for the function file in CDF Files
      - owner (str): the function's owner's email
      - description (str): function description
      - metadata (Dict[str, str]): dictionary containing function metadata
      - secrets: (optional) api keys or similar that should be passed to the
        function
    """
    f = functools.partial(
        create_function_from_file,
        human_readable_name,
        function_name,
        file_id,
        description,
        metadata,
        owner,
        secrets,
    )
    robust_create(f)


def get_function_call_response_metadata(function_id: int) -> Dict[str, Any]:
    """
    Generate metadata for a function
    Input:
        - function_id: (int) function's id in CDF
    Output:
        - (dictionary) function's metadata
    """
    client = global_client["functions"]
    function = client.functions.retrieve(id=function_id)

    ts = function.created_time / 1000
    created_time = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    metadata = dict(
        external_id=function.external_id,
        description=function.description,
        owner=function.owner,
        status=function.status,
        file_id=function.file_id,
        created_time=created_time,
    )
    return metadata


def call_function(function_name: str, data: Dict) -> Any:
    """
    Call a function deployed in CDF based on the external id

    Input:
        - function_name: (string) function's external id in CDF
        - data: (dictionary) data for the call
    Output:
        - (dictionary) function's response
    """
    client = global_client["functions"]
    function = client.functions.retrieve(external_id=function_name)
    logging.info(f"Retrieved function with external-id {function_name} from CDF")
    call_complete = False
    t_start = time.process_time()
    while not call_complete:
        try:
            call = function.call(data)
            call_complete = True
        except CogniteAPIError:
            logging.warning("Cognite API error, try again")
    logging.info(f"Called function ({call.id=})")
    response = call.get_response()
    status = response["status"]
    duration = time.process_time() - t_start
    logging.info(f"Function call complete ({call.id=}, {duration=}): {status=}")
    return response


def call_function_process_wrapper(function_name: str, data: Dict) -> Any:
    """
    Set up the cdf client and call a function based on external id.
    This wrapper makes it possible to call a function from an independent processess invoked by the multiprocessing library

    Input:
        - function_name: (string) function's external id in CDF
        - data: (dictionary) data for the call
    Output:
        - (dictionary) function's response
    """
    set_up_cdf_client(context="deploy")
    return call_function(function_name, data)


def call_function_parallel(
    function_name: str, data: Dict, n_calls: Optional[int] = None
):
    """
    Make parallel calls to a function deployed in CDF, based on the external id of the function

    Input:
        - function_name: (string) function's external id in CDF
        - data: (list of dictionaries) list of data for the call
        - n_calls: (optional int) number of parallel calls (set None to use all
            available cpu cores)
    """
    f = partial(call_function_process_wrapper, function_name)
    with Pool(n_calls) as p:
        return p.map(f, data)


def test_function(function_name: str, data: Dict) -> None:
    """
    Call a function with data and verify that the response's
    status is 'ok'
    """
    logging.info(f"Testing function {function_name}")
    if not validate_function_name(function_name):
        raise ValueError()
    output = call_function(function_name, data)
    assert output["status"] == "ok"
    logging.info("Test call was successful :)")


def wait_function_status(
    function: Function, status: List[str] = ["Ready", "Failed"]
) -> str:
    """
    Wait until function status is in `status`
    By default it waits for Ready or Failed, which is useful when deploying.
    It implements some control logic, since polling status can fail.
    """
    polling_wait_seconds_base = 10.0
    polling_wait_seconds = polling_wait_seconds_base
    max_api_errors_base = 5
    max_api_errors = max_api_errors_base

    logging.info("Wait for function to be ready or to fail")
    while not (function.status in status):
        try:
            time.sleep(polling_wait_seconds)
            function.update()
            logging.info(f"{function.status=}")
            polling_wait_seconds = polling_wait_seconds_base
            max_api_errors = max_api_errors_base
        except CogniteAPIError as e:
            max_api_errors -= 1
            logging.warning("Could not update function status, will try again")
            polling_wait_seconds *= 1.2
            if not max_api_errors:
                logging.error("Could not update function status.")
                raise e

    return function.status


def list_functions(tags: List = [], env: Optional[str] = None) -> Any:
    """
    List deployed functions, optionally filtering by environment (dev, test
    or prod) or set of tags.

    Input:
        - tags: ([string]): list of tags to search for in the function
        description (or-search)
        - env: (string) the environment

    Output:
        - ([string]): list of function names (i.e. external_id's )
    """
    client = global_client["functions"]
    functions = client.functions.list(limit=-1)

    def _validate_function(function: Any) -> bool:
        return validate_function_name(function.external_id, verbose=True)

    functions = filter(_validate_function, functions)
    if env:

        def _get_function_environment(function: Any) -> str:
            if function.external_id.split("-") > 1:
                return str(function.external_id.split("-")[2])
            else:
                return "unknown"

        def _env_index(input: Any) -> bool:
            return _get_function_environment(input) == env

        functions = filter(_env_index, functions)
    if tags:

        def _contains_tag(function: Any, tag: Any) -> bool:
            if tag in function.description:
                return True
            else:
                return False

        def _tags_index(function: Any) -> bool:
            return any([_contains_tag(function, tag) for tag in tags])

        functions = filter(_tags_index, functions)
    functions = [f.external_id for f in functions]
    functions = sorted(functions)
    return functions


def download_file(id: Dict[str, Union[str, int]], path: Union[Path, str]) -> None:
    """
    Download file from Cognite

    Params:
        - id: dictionary with id type (either "id" or "external_id") as key
        - path: path of local file to write
    """
    client = global_client["files"]

    logging.debug(f"Download file with {id=} to {path}")
    client.files.download_to_path(path, **id)


def upload_file(
    external_id: str,
    path: Union[Path, str],
    metadata: Dict[str, str] = {},
    directory: str = "/",
    overwrite: bool = True,
    dataset_id: Optional[int] = None,
) -> FileMetadata:
    """
    Upload file to Cognite

    Params:
        - external_id: external id
        - path: path of local file to upload
        - metadata: dictionary with file metadata
        - overwrite: what to do when the external_id exists already
        - dataset_id: (int) dataset id
    """
    client = global_client["files"]

    metadata = {
        k: v if isinstance(v, str) else json.dumps(v) for k, v in metadata.items()
    }

    logging.debug(f"Upload file {path} with {external_id=} and {metadata=}")
    file_info = client.files.upload(
        path,
        external_id,
        metadata=metadata,
        directory=directory,
        overwrite=overwrite,
        data_set_id=dataset_id,
    )
    logging.info(f"Uploaded file: {file_info=}")
    return file_info


def upload_folder(
    external_id: str,
    path: Path,
    metadata: Dict = {},
    overwrite: bool = False,
    target_folder: str = "/",
    dataset_id: Optional[int] = None,
) -> FileMetadata:
    """
    Upload folder content to Cognite. It compresses the folder and uploads it.

    Params:
        - external_id: external id (should be unique in the CDF project)
        - path: (Path) path of local folder where content is stored
        - metadata: dictionary with file metadata
        - target_folder: path where compressed file should be stored
        - overwrite: if overwrite==False and `external_id` exists => exception
        - dataset_id: (int) dataset id
    """
    base_name = path / "archive"
    archive_name = make_archive(str(base_name), "gztar", path)
    file_info = upload_file(
        external_id,
        archive_name,
        metadata=metadata,
        overwrite=overwrite,
        directory=target_folder,
        dataset_id=dataset_id,
    )
    os.remove(archive_name)
    logging.info(f"Folder content uploaded: {file_info=}")
    return file_info


def download_folder(external_id: str, path: Path) -> None:
    """
    Download content from Cognite to a folder. It is assumed to have been
    uploaded using `upload_folder()`, so it downloads a file and decompresses
    it.

    Params:
    - external_id: external id
    - path: (Path) path of local folder where content will be stored
    """
    base_name = path / "archive.tar.gz"
    download_file(dict(external_id=external_id), base_name)
    unpack_archive(base_name, base_name.parent)
    os.remove(base_name)
    logging.info(f"Model file/s downloaded to {path}")


def log_system_info() -> None:
    """
    Can be called from a handler to log CDF environment information
    """
    logging.debug(f"Python version:\n{os.popen('python --version').read()}")
    logging.debug(f"Python path:\n{sys.path}")
    logging.debug(f"Current working directory:\n{os.getcwd()}")
    logging.debug(f"Content:\n{os.popen('ls -la *').read()}")
    logging.debug(f"Packages:\n{os.popen('pip freeze').read()}")


def query_file_versions(
    directory_prefix: str,
    external_id_prefix: str,
    metadata: Dict = {},
    uploaded: Optional[bool] = True,
    dataset_id: Optional[int] = None,
) -> pd.DataFrame:
    """
    Find all file versions that match a query.

    Input:
        -directory_prefix
        -external_id_prefix
        -metadata: query to the metadata (dictionary)
        -uploaded: (bool)
        -dataset_id: (int) dataset id
    Output:
        - list of versions (dataframe)
    """
    client = global_client["files"]
    file_list = client.files.list(
        limit=-1,
        directory_prefix=directory_prefix,
        external_id_prefix=external_id_prefix,
        metadata=metadata,
        uploaded=uploaded,
        data_set_ids=dataset_id,
    ).to_pandas()

    return file_list


def delete_file(id: Dict) -> None:
    """
    Delete file from Cognite

    Params:
        - id: dictionary with id type (either "id" or "external_id") as key
    """
    client = global_client["files"]
    client.files.delete(**id)
    logging.debug(f"Deleted file with {id=}")


def copy_file(
    source_ext_id: str,
    target_ext_id: str,
    overwrite: bool = False,
    dataset_id: Optional[int] = None,
) -> None:
    """
    Copy content and metadata of a file in CDF Files

    Input:
        - source_ext_id: (str) external id for source file
        - target_ext_id: (str) external id for target file
        - overwrite: (bool) should target file be overwritten if it exists
        - dataset_id: (int) dataset id for the target file
    """
    client = global_client["files"]
    f = client.files.retrieve(external_id=source_ext_id)
    file_content = client.files.download_bytes(external_id=source_ext_id)
    logging.debug(f"Downloaded file: {source_ext_id}, {f.dump()}")
    f = client.files.upload_bytes(
        file_content,
        name=f.name,
        external_id=target_ext_id,
        metadata=f.metadata,
        directory=f.directory,
        overwrite=overwrite,
        data_set_id=dataset_id,
    )
    m = f"Copied source {source_ext_id} to {target_ext_id}, {f.dump()}"
    logging.info(m)


def file_exists(
    external_id: str, directory: str, dataset_id: Optional[int] = None
) -> bool:
    """
    Check if a file exists in a folder (regardless of uploaded status)

    Input:
        - external_id: (str)
        - directory: (str)
        - dataset_id: (int)
    Output
        - exists: (bool)
    """
    file_list = query_file_versions(
        directory_prefix=directory,
        external_id_prefix=external_id,
        uploaded=None,
        dataset_id=dataset_id,
    )
    if file_list.empty:
        logging.info(f"File with '{external_id=}' not found")
        exists = False
    else:
        exists = True
    return exists


def get_dataset_id(external_id: Optional[str] = None) -> Optional[int]:
    """
    Input:
        -external_id: (str) dataset external id, or `None` for no dataset
    Output:
        -id: (int) dataset id, or `None` for no dataset
    """
    if external_id:
        client = global_client["files"]
        dataset = client.data_sets.retrieve(external_id=external_id)
        return int(dataset.id)
    else:
        return None


def file_to_dataset(
    file_external_id: str, dataset_external_id: Optional[str] = None
) -> None:
    """
    Assign a file to a dataset.
    Input
        - file_external_id: (str) the file's external id
        - dataset_external_id: (str) the dataset's external id, `None` for no
            dataset
    """
    client = global_client["files"]
    dataset_id = get_dataset_id(dataset_external_id)
    file_metadata_update = FileMetadataUpdate(external_id=file_external_id)
    file_metadata_update = file_metadata_update.data_set_id.set(dataset_id)
    _ = client.files.update(file_metadata_update)
    logging.info(f"Assigned dataset {dataset_id} to file {file_external_id}")


def get_latest_artifact_version(external_id: str) -> int:
    """Extract the latest artifact version based on the external id of a function.
    If no artifacts are found for the specified function, the version is set to 1.

    Args:
        external_id (string): external id of the function
    """
    if len(splitted_external_id := external_id.split("-")) > 3:
        env = splitted_external_id[-2]
    else:
        env = splitted_external_id[-1]
    model_name = splitted_external_id[0]

    artifact_external_id = model_name + "/" + env
    artifact_versions = query_file_versions(
        directory_prefix="/mlops", external_id_prefix=artifact_external_id
    )
    if len(artifact_versions) == 0:
        logging.info(
            f"No artifacts found for function with external id {external_id}. Setting version number to 1"
        )
        latest_artifact_version = 1
    else:
        latest_artifact_version = artifact_versions.loc[
            artifact_versions.uploadedTime.argmax()
        ].metadata["version"]

    return latest_artifact_version


def get_arguments_for_redeploying_latest_model_version(
    external_id: str,
) -> Tuple[str, str, str, Dict[str, str], str]:
    """Extract data needed to redeploy the latest function from CDF files using a predictable external id,
    i.e. witout the model version number. In this way the client does not have to care about version numbers.
    In addition to copying the data fields of the function, the description of the function is tagged with (LATEST VERSION),
    and the version number is added to the metadata (set to 1 if it does not exist)

    Args:
        external_id (str): external id of the deployed function in CDF

    Returns:
        (tuple): tuple containing the data needed for redeploying the latest function with a predictable external id
    """
    client = global_client["functions"]
    latest_function = client.functions.retrieve(external_id=external_id)
    name = latest_function.name
    file_id = latest_function.file_id
    description = latest_function.description + " (LATEST VERSION)"
    owner = latest_function.owner
    metadata = latest_function.metadata
    if len(stripped_external_id := latest_function.external_id) > 3:
        version_number = str(stripped_external_id[-1])
    else:
        version_number = "1"
    metadata["version"] = version_number

    return name, file_id, description, metadata, owner
