# setup.py
from pathlib import Path

from akerbp.mlops import __version__ as version
from akerbp.mlops.core import logger
from akerbp.mlops.core.config import (
    generate_default_project_settings,
    validate_user_settings,
)
from akerbp.mlops.deployment.helpers import to_folder, replace_string_file
import re

logging = logger.get_logger(name="mlops_deployment")


def update_mlops_version_in_pipeline(folder_path: Path = Path(".")) -> None:
    """Update MLOps settings by overwriting the package version number

    Args:
        folder_path (Path, optional): Path to root of repo. Defaults to Path(".").
    """
    pipeline_file = Path("bitbucket-pipelines.yml")
    pipeline_path = folder_path / pipeline_file
    replacement_package = f"akerbp.mlops=={version}"
    pattern_package = re.compile("akerbp.mlops==.{5,}")
    replacement_version = f"Version {version}"
    pattern_version = re.compile("Version \S{5,}")
    with pipeline_path.open() as f:
        pipeline = f.read()
        new_pipeline = re.sub(
            pattern_version,
            replacement_version,
            re.sub(pattern_package, replacement_package, pipeline),
        )
    with pipeline_path.open("w") as f:
        f.write(new_pipeline)
    logging.info("MLOps version successfully updated in pipeline file")


def generate_pipeline(folder_path: Path = Path(".")) -> None:
    pipeline_file = Path("bitbucket-pipelines.yml")
    pipeline_path = folder_path / pipeline_file
    pipeline = ("akerbp.mlops.deployment", pipeline_file)
    to_folder(pipeline, folder_path)
    replace_string_file("MLOPS_VERSION", version, pipeline_path)
    logging.info("Pipeline definition generated")


def setup_pipeline(folder_path: Path = Path(".")) -> None:
    """
    Set up pipeline file in the given folder
    """
    pipeline_file = Path("bitbucket-pipelines.yml")
    pipeline_path = folder_path / pipeline_file
    if pipeline_path.exists():
        logging.info(f"Update MLOps version in pipeline definition to {version}")
        update_mlops_version_in_pipeline()
    else:
        logging.info("Generating pipeline definition from template")
        generate_pipeline()


if __name__ == "__main__":
    logging.info("Will this show?")
    setup_pipeline()
    if Path("mlops_settings.yaml").exists():
        logging.info("Validate settings file")
        validate_user_settings()
    else:
        logging.info("Create settings file template")
        generate_default_project_settings()
    logging.info("Done!")
