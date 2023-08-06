# config.py
import os
import re
import traceback
from dataclasses import asdict
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any, Union

import yaml
from pydantic import FilePath

from pydantic.dataclasses import dataclass
from akerbp.mlops.core import helpers, logger

logging = logger.get_logger(name="mlops_core")


def validate_categorical(
    setting: Optional[str], name: str, allowed: List[Optional[str]]
) -> None:
    if setting not in allowed:
        m = f"{name}: allowed values are {allowed}, got '{setting}'"
        raise ValueError(m)


@dataclass
class EnvVar:
    env: Optional[str] = None
    service_name: Optional[str] = None
    google_project_id: Optional[str] = None
    platform: Optional[str] = None
    local_deployment: Optional[Union[str, bool]] = False

    def __post_init__(self):
        if self.env:
            validate_categorical(self.env, "Environment", ["dev", "test", "prod"])
        else:
            logging.warning("ENV environmental variable is not set")
        validate_categorical(self.platform, "Platform", ["cdf", "gc", None])
        if self.env and self.env != "dev":
            validate_categorical(
                self.service_name, "Service  name", ["training", "prediction"]
            )


def _read_env_vars() -> EnvVar:
    """
    Read environmental variables and initialize EnvVar object with those that
    were set (i.e. ignored those with None value)
    """
    envs = dict(
        env=os.getenv("ENV"),
        service_name=os.getenv("SERVICE_NAME"),
        local_deployment=os.getenv("LOCAL_DEPLOYMENT"),
        google_project_id=os.getenv("GOOGLE_PROJECT_ID"),
        platform=os.getenv("DEPLOYMENT_PLATFORM"),
    )
    envs = {k: v for k, v in envs.items() if v is not None}
    return EnvVar(
        env=envs.get("env"),
        service_name=envs.get("service_name"),
        local_deployment=envs.get("local_deployment", False),
        google_project_id=envs.get("google_project_id"),
        platform=envs.get("platform"),
    )


envs = _read_env_vars()
envs_dic = asdict(envs)
logging.debug(f"{envs_dic=}")


@dataclass
class CdfKeys:
    data: Optional[str]
    files: Optional[str]
    functions: Optional[str]


_api_keys = CdfKeys(
    data=os.getenv("COGNITE_API_KEY_DATA"),
    files=os.getenv("COGNITE_API_KEY_FILES"),
    functions=os.getenv("COGNITE_API_KEY_FUNCTIONS"),
)
api_keys = asdict(_api_keys)


def update_cdf_keys(new_keys: Dict) -> None:
    global api_keys
    api_keys = asdict(CdfKeys(**new_keys))


def generate_default_project_settings(
    yaml_file: Path = Path("mlops_settings.yaml"), n_models: int = 2
) -> None:
    if yaml_file.exists():
        raise Exception(f"Settings file {yaml_file} exists already.")

    default_config_template = [
        """
model_name: my_model
human_friendly_model_name: 'My model'
model_file: model_code/my_model.py
req_file: model_code/requirements.model
test_file: model_code/test_model.py
artifact_folder: artifact_folder
platform: cdf
dataset: mlops
info:
    prediction:
        description: Description prediction service for my_model
        metadata:
            required_input:
                - input_1
                - input_2
            training_wells:
                - 3/1-4
            input_types:
                - float
                - int
            units:
                - s/ft
                - 1
            output_curves:
                - output_1
            output_units:
                - s/ft
            petrel_exposure: False
            imputed: True
            num_filler: -999.15
            cat_filler: UNKNOWN
        owner: datascientist@akerbp.com
    training:
        << : *desc
        description: Description training service for my_model
        metadata:
            training_wells:
                - 3/1-4
            required_input:
                - input_1
                - input_2
            output_curves:
                - output_1
            hyperparameters:
                param1: value1
                param2: value2
                param3: value3
        owner: datascientist@akerbp.com
"""
    ]
    default_config_list = default_config_template * n_models
    default_config = "---".join(default_config_list)
    with open(yaml_file, "w") as f:
        f.write(default_config)


def validate_model_reqs(req_file: FilePath) -> None:
    # Model reqs is renamed to requirements.txt during deployment
    if req_file.name == "requirements.model":
        with req_file.open() as f:
            req_file_string = f.read()
            if "akerbp.mlops" not in req_file_string:
                m = "Model requirements should include akerbp.mlops package"
                raise Exception(m)
            if "MLOPS_VERSION" not in req_file_string:
                m = 'akerbp.mlops version should be "MLOPS_VERSION"'
                raise Exception(m)


@dataclass
class ServiceSettings:
    model_name: str  # Remember to modify generate_default_project_settings()
    human_friendly_model_name: str
    model_file: FilePath  # if fields are modified
    req_file: FilePath
    info: Dict
    test_file: Optional[FilePath] = None
    artifact_folder: Optional[Path] = None
    platform: str = "cdf"
    dataset: str = "mlops"
    model_id: Optional[str] = None

    def __post_init_post_parse__(self):
        # Validation
        if not re.match("^[A-Za-z0-9_]*$", self.model_name):
            m = "Model name can only contain letters, numbers and underscores"
            raise Exception(m)

        validate_model_reqs(self.req_file)

        validate_categorical(
            self.platform, "Deployment platform", ["cdf", "gc", "local"]
        )

        if self.platform == "gc" and not envs.google_project_id:
            raise Exception("Platform 'gc' requires GOOGLE_PROJECT_ID env var")

        if self.model_id and envs.service_name == "training":
            raise ValueError("Unexpected model_id setting (training service)")

        # Derived fields
        if envs.env == "dev" and envs.local_deployment == "False":
            self.platform = "local"

        self.model_import_path = helpers.as_import_path(self.model_file)
        self.test_import_path = helpers.as_import_path(self.test_file)

        self.files = {
            "model code": helpers.get_top_folder(self.model_file),
            "handler": ("akerbp.mlops.cdf", "handler.py"),
            "artifact folder": self.artifact_folder,
        }
        if self.platform == "gc":
            files_gc = {
                "Dockerfile": ("akerbp.mlops.gc", "Dockerfile"),
                "requirements.app": ("akerbp.mlops.gc", "requirements.app"),
                "install_req_file.sh": ("akerbp.mlops.gc", "install_req_file.sh"),
            }
            self.files = {**self.files, **files_gc}


def store_service_settings(
    c: ServiceSettings, yaml_file: Path = Path("mlops_service_settings.yaml")
) -> None:
    logging.info("Write service settings file")

    def factory(data: List[Tuple[str, Any]]) -> Dict[str, str]:
        """
        Take a list of tuples as input. Returns a suitable dictionary.
        Transforms Path objects to strings (linux style path).
        """

        def path2str(x: Union[Path, str]) -> str:
            if not isinstance(x, Path):
                return x
            else:
                return x.as_posix()

        d = {k: path2str(v) for k, v in data}
        return d

    service_settings = asdict(c, dict_factory=factory)
    with yaml_file.open("w") as f:
        yaml.dump(service_settings, f)


@dataclass
class ProjectSettings:
    project_settings: List[ServiceSettings]


def enforce_string_values_in_function_metadata(
    project_settings: ProjectSettings,
) -> ProjectSettings:
    """The metadata field in CDF functions requires both keys and values to be strings.
    This function iterates through the metadata of each model defined in the mlops settings file,
    and enforce the values to be string (keys are strings by default)

    Args:
        project_settings (ProjectSettings): project settings for each model defined in the settings file

    Returns:
        (ProjectSettings): project settings for each model defined in the settings file
    """
    for i, model_settings in enumerate(project_settings.project_settings):
        for service in list(model_settings.info.keys()):
            metadata = model_settings.info[service]["metadata"]
            for k, v in metadata.items():
                metadata[k] = str(v)
            model_settings.info[service]["metadata"] = metadata
        project_settings.project_settings[i] = model_settings
    return project_settings


def read_project_settings(
    yaml_file: Path = Path("mlops_settings.yaml"),
) -> List[ServiceSettings]:
    logging.info("Read project settings")
    with yaml_file.open() as f:
        settings = yaml.safe_load_all(f.read())
    model_settings = [ServiceSettings(**s) for s in settings]
    project_settings = ProjectSettings(project_settings=model_settings)
    project_settings = enforce_string_values_in_function_metadata(project_settings)
    logging.debug(f"{project_settings=}")
    return project_settings.project_settings


def read_service_settings(
    yaml_file: Path = Path("mlops_service_settings.yaml"),
) -> ServiceSettings:
    logging.info("Read service settings")
    with yaml_file.open() as f:
        settings = yaml.safe_load(f.read())
    service_settings = ServiceSettings(**settings)
    logging.debug(f"{service_settings=}")
    return service_settings


def validate_user_settings(yaml_file: Path = Path("mlops_settings.yaml")) -> None:
    try:
        read_project_settings(yaml_file)
        logging.info("Settings file is ok :)")
    except Exception:
        trace = traceback.format_exc()
        error_message = f"Settings file is not ok! Fix this:\n{trace}"
        logging.error(error_message)
