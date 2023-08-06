# platforms.py
import typing


@typing.no_type_check
def get_methods():
    """
    Return a dictionary with methods to deploy and test functions for each
    platform (cdf, gc or local). This decouples platforms and deployment
    """
    methods = {}

    # cdf
    from akerbp.mlops.cdf.helpers import deploy_function as cdf_deploy
    from akerbp.mlops.cdf.helpers import redeploy_function as cdf_redeploy
    from akerbp.mlops.cdf.helpers import set_up_cdf_client
    from akerbp.mlops.cdf.helpers import test_function as cdf_test

    set_up_cdf_client(context="deploy")
    methods["cdf"] = cdf_deploy, cdf_redeploy, cdf_test

    # gc
    from akerbp.mlops.gc.helpers import deploy_function as gc_deploy
    from akerbp.mlops.gc.helpers import test_function as gc_test

    methods["gc"] = gc_deploy, gc_test

    # local (methods don't do anything)
    local_deploy = local_test = lambda *args, **kwargs: None
    methods["local"] = local_deploy, local_test

    return methods
