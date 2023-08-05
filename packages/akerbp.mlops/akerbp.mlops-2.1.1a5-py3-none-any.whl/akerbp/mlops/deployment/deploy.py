"""
deploy.py

Deploy services in either Google Cloud Run or CDF Functions.
Model registry uses CDF Files.
"""
import json
import os
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Dict, List

import akerbp.mlops.model_manager as mm
from akerbp.mlops.cdf import helpers as cdf
from akerbp.mlops.core import config, logger
from akerbp.mlops.core.config import ServiceSettings
from akerbp.mlops.deployment import helpers, platforms

logging = logger.get_logger(name="mlops_deployment")


platform_methods = platforms.get_methods()


def deploy_model(
    model_settings: ServiceSettings,
    platform_methods: Dict = platform_methods,
) -> str:
    """
    Deploy a model.

    This will create a deployment folder and change current working directory
    to it.

    Input:
        - model_settings: (ServiceSettings) settings for the model service
        - platform_methods: (dictionary) where key is the platform and value
            is a tuple with deploy and test functions.
    """
    try:
        c = model_settings
        env = config.envs.env
        service_name = config.envs.service_name
        deployment_folder = helpers.deployment_folder_path(c.model_name)
        function_name = f"{c.model_name}-{service_name}-{env}"
        human_readable_function_name = c.human_friendly_model_name

        logging.debug(" ")
        logging.info(
            f"Starting deployment of model {c.human_friendly_model_name} with external id {function_name}"
        )

        if (service_name == "prediction") and c.artifact_folder:
            mm.set_active_dataset(c.dataset)
            c.model_id = mm.set_up_model_artifact(c.artifact_folder, c.model_name)

        logging.info("Create deployment folder and move required files/folders")
        deployment_folder.mkdir()
        helpers.copy_to_deployment_folder(c.files, deployment_folder)

        logging.debug(f"cd {deployment_folder}")
        os.chdir(deployment_folder)
        helpers.set_up_requirements(c)
        config.store_service_settings(c)

        logging.info("Run model and service tests")
        if c.test_file:
            # It should be run as an independent process so that the right
            # packages are imported, the import paths are correct, etc.
            command = [sys.executable, "-m", "akerbp.mlops.services.test_service"]
            output = subprocess.check_output(command, encoding="UTF-8")
            model_input = json.loads(output.splitlines()[-1])
        else:
            logging.warning("Model test file is missing! Didn't run tests")

        if c.platform == "cdf":  # For now this will always be the case
            # Extract latest artifact version and set model version
            latest_artifact_version = cdf.get_latest_artifact_version(
                external_id=function_name
            )
            logging.info(
                f"Latest artifact version in {env} environment is {latest_artifact_version}"
            )
            external_id = function_name + "-" + str(latest_artifact_version)
            predictable_external_id = function_name

            # Extract the deployment and test functions
            deploy_function, redeploy_function, test_function = platform_methods[
                c.platform
            ]

            # Deploy function with version number included in the external id (model-service-env-version)
            logging.info(
                f"Deploying function {human_readable_function_name} with external id {external_id} to {c.platform}"
            )
            deploy_function(
                human_readable_function_name, external_id, info=c.info[service_name]
            )

            # Redeploy latest function with a predictable external id (model-service-env)
            logging.info(
                f"Redeploying latest function {human_readable_function_name} with predictable external id {predictable_external_id} to {c.platform}"
            )
            (
                name,
                file_id,
                description,
                metadata,
                owner,
            ) = cdf.get_arguments_for_redeploying_latest_model_version(
                external_id=external_id
            )
            redeploy_function(
                name, predictable_external_id, file_id, description, metadata, owner
            )

        else:  # GCP deployment
            external_id = function_name
            deploy_function, test_function = platform_methods[c.platform]
            logging.info(
                f"Deploying function {human_readable_function_name} with external id {external_id} to {c.platform}"
            )
            deploy_function(
                human_readable_function_name, external_id, info=c.info[service_name]
            )

        if c.test_file:
            logging.info(f"Make a test call to function with external id {external_id}")
            test_function(external_id, model_input)
            if c.platform == "cdf":
                logging.info(
                    f"Make a test call to the latest model with predictable external id {predictable_external_id}"
                )
                test_function(predictable_external_id, model_input)
        else:
            logging.warning("No test file was set up. End-to-end test skipped!")

        return "OK"
    except Exception:
        trace = traceback.format_exc()
        return f"Model failed to deploy!\n{trace}"


def deploy(project_settings: List[ServiceSettings]) -> None:
    """
    Deploy a machine learning project that potentially contains multiple models.
    Deploy each model in the settings and make sure that if one model fails it
    does not affect the rest. At the end, if any model failed, it raises an
    exception with a summary of all models that failed.

    Input:
        - Project settings as described by the user
    """
    failed_models = {}
    cwd_path = Path.cwd()

    for c in project_settings:
        status = deploy_model(c)
        if status != "OK":
            logging.error(status)
            failed_models[c.human_friendly_model_name] = status

        logging.debug("cd ..")
        os.chdir(cwd_path)
        helpers.rm_deployment_folder(c.model_name)

    if failed_models:
        for model, message in failed_models.items():
            logging.debug(" ")
            logging.info(f"Model {model} failed: {message}")
        raise Exception("At least one model failed.")


if __name__ == "__main__":
    mm.setup()
    settings = config.read_project_settings()
    deploy(settings)
