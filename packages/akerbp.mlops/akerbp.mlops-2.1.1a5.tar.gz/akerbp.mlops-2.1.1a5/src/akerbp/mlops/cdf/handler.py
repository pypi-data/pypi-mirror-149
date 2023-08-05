# handler.py
import traceback
import warnings
from importlib import import_module
import akerbp.mlops.cdf.helpers as cdf
from akerbp.mlops.core import config, logger
from typing import Dict, Union, Any

warnings.simplefilter("ignore")


service_name = config.envs.service_name
logging = logger.get_logger("mlops_cdf")

service = import_module(f"akerbp.mlops.services.{service_name}").service


def handle(
    data: Dict, secrets: Dict, function_call_info: Dict
) -> Union[Any, Dict[Any, Any]]:
    try:
        if data:
            output = service(data, secrets)
        else:
            output = dict(status="ok")
        cdf.api_keys = secrets
        cdf.set_up_cdf_client(context="deploy")
        function_call_metadata = cdf.get_function_call_response_metadata(
            function_call_info["function_id"]
        )
        output.update(dict(metadata=function_call_metadata))
        return output
    except Exception:
        trace = traceback.format_exc()
        error_message = f"{service_name} service failed.\n{trace}"
        logging.critical(error_message)
        return dict(status="error", error_message=error_message)
