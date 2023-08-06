# MLOps Framework
This is a framework for MLOps that deploys models as functions in Cognite Data
Fusion or api's in Google Cloud Run.

# User Guide 

## Reference guide
This assumes you are already familiar with the framework, and acts as a quick reference quide for deploying models using the prediction service, i.e. when model training is performed outside of the MLOps framwork.
1. Train model to generate model artifacts 
2. Manually upload artifacts to your test environment 
   - This includes model artifacts generated during training, mapping- and settingsfile for the model, scaler object etc. Basically everything that is needed to preprocess the data and make predictions using the trained model.
3. Deploy prediction service to test 
   - This is handled by the CI/CD pipeline in Bitbucket
4. Manually promote model artifacts from test to production 
5. Manually trigger deployment of model to production 
   - Trigger in the CI/CD pipeline 
6. Call deployed model 
   - See section  "Calling a deployed model prediction service hosted in CDF" below 
## Getting Started:
Follow these steps:
- Install package: `pip install akerbp.mlops`
- Set up pipeline file `bitbucket-pipelines.yml` and config file
  `mlops_settings.yaml` by running this command from your repo's root folder:
  ```bash
  python -m akerbp.mlops.deployment.setup
  ```
- Fill in user settings and then validate them by running this (from repo root):
  ```python
  from akerbp.mlops.core.config import validate_user_settings
  validate_user_settings()
  ```
  alternatively, run the setup again:
  ```bash
  python -m akerbp.mlops.deployment.setup
  ```
- Commit the pipeline and settings files to your repo
- Become familiar with the model template (see folder `model_code`) and make
  sure your model follows the same interface and file structure (see [Files and Folders Structure](#files-and-folders-structure))   
- Follow or request the Bitbucket setup (described later)

A this point every git push in master branch will trigger a deployment in the
test environment. More information about the deployments pipelines is provided
later.

## Updating MLOps
Follow these steps:
- Install a new version using pip, e.g. `pip install akerbp.mlops==x`, or upgrade your existing version to the latest release by running `pip install --upgrade akerbp.mlops`
- Run this command from your repo's root folder:
  ```bash
  python -m akerbp.mlops.deployment.setup
  ```
  This will update the bitbucket pipeline with the newest release of akerbp.mlops and validate your settings. Once the settings are validated, commit changes and
  you're ready to go!

## General Guidelines
Users should consider the following general guidelines:
- Model artifacts should **not** be committed to the repo. Folder `model_artifact`
  does store model artifacts for the model defined in `model_code`, but it is
  just to help users understand the framework ([see this section](#model-manager) on how to handle model artifacts)
- Follow the recommended file and folder structure ([see this section](#files-and-folders-structure))
- There can be several models in your repo: they need to be registered in the
  settings, and then they need to have their own model and test files
- Follow the import guidelines ([see this section](#import-guidelines))
- Make sure the prediction service gets access to model artifacts ([see this section](#model-manager))

## Configuration
MLOps configuration is stored in `mlops_settings.yaml`. Example for a project
with a single model:
```yaml
model_name: model1
human_friendly_model_name: 'My First Model'
model_file: model_code/model1.py
req_file: model_code/requirements.model
artifact_folder: model_artifact
test_file: model_code/test_model1.py
platform: cdf
dataset: mlops
info:
    prediction: &desc
        description: 'Description prediction service, model1'
        metadata: 
          required_input:
            - ACS
            - RDEP 
            - DEN 
          training_wells:
            - 3/14
            - 2/7-18
          input_types:
            - int 
            - float 
            - string 
          units:
            - s/ft 
            - 1
            - kg/m3
          output_curves:
            - AC 
          output_units:
            - s/ft 
          petrel_exposure: False 
          imputed: True 
          num_filler: -999.15
          cat_filler: UNKNOWN
        owner: data@science.com
    training:
        << : *desc
        description: 'Description training service, model1'
        metadata: 
          required_input:
            - ACS
            - RDEP 
            - DEN 
          output_curves:
            - AC 
          hyperparameters:
            learning_rate: 1e-3
            batch_size: 100 
            epochs: 10 
```
| **Field** | **Description** |
| --------- | ----------------|
| model_name | a suitable name for your model. No spaces or dashes are allowed |
| human_friendly_model_name | Name of function (in CDF) |
| model_file | model file path relative to the repo's root folder. All required model code should be under the top folder in that path (`model_code` in the example above).|
| req_file | model requirement file. Do not use `.txt` extension! |
| artifact_folder | model artifact folder. It can be the name of an existing local folder (note that it should not be committed to the repo). In that case it will be used in local deployment. It still needs to be uploaded/promoted with the model manager so that it can be used in Test or Prod. If the folder does not exist locally, the framework will try to create that folder and download the artifacts there. Set to `null` if there is no model artifact.  |
| test_file | test file to use. Set to `null` for no testing before deployment (not recommended). |
| platform | deployment platforms, either `cdf` (Cognite) or `gc` (Google). |
|dataset | CDF Dataset to use to read/write model artifacts (see [Model Manager](#model-manager)). Set to `null` is there is no dataset (not recommended). |
|info | description, metadata and owner information for the prediction and training services. Training field can be discarded if there's no such service. |

Note:
   all **paths** should be **unix style**, regardless of the platform.

Notes on metadata: 
   We need to specify the metadata under info as a dictionary with strings as keys and values, as CDF only allows strings for now. We are also limited to the following 
   - Keys can contain at most 16 characters 
   - Values can contain at most 512 characters 
   - At most 16 key-value pairs 
   - Maximum size of entire metadata field is 512 bytes



If there are multiple models, model configuration should be separated using
`---`. Example:
```yaml
model_name: model1
human_friendly_model_name: 'My First Model'
model_file: model_code/model1.py
(...)
--- # <- this separates model1 and model2 :)
model_name: model2
human_friendly_model: 'My Second Model'
model_file: model_code/model2.py
(...)
```

## Files and Folders Structure
All the model code and files should be under a single folder, e.g. `model_code`.
**Required** files in this folder:
- `model.py`: implements the standard model interface
- `test_model.py`: tests to verify that the model code is correct and to verify
  correct deployment
- `requirements.model`: libraries needed (with specific **version numbers**),
  can't be called `requirements.txt`. Add the MLOps framework like this:
  ```bash
  # requirements.model
  (...) # your other reqs
  akerbp.mlops==MLOPS_VERSION
  ```
  During deployment, `MLOPS_VERSION` will be automatically replaced by the
  specific version **that you have installed locally**. Make sure you have the latest release on your local machine prior to model deployment.

For the prediction service we require the model interface to have the following class and function 
  - initialization(), with required arguments
    - path to artifact folder
    - secrets
      - these arguments can safely be set to None, and the framework will handle everything under the hood.
      - only set path to artifact folder as None if not using any artifacts
  - predict(), with required arguments
    - data
    - init_object (output from initialization() function)
    - secrets
      - You can safely put the secrets argument to None, and the framework will handle the secrets under the hood. 
  - ModelException class with inheritance from an Exception base class

For the training service we require the model interface to have the following class and function 
  - train(), with required arguments
    - folder_path
      - path to store model artifacts to be consumed by the prediction service 
  - ModelException class with inheritance from an Exception base class
  

The following structure is recommended for projects with multiple models:
- `model_code/model1/`
- `model_code/model2/`
- `model_code/common_code/` 

This is because when deploying a model, e.g. `model1`, the top folder in the
path (`model_code` in the example above) is copied and deployed, i.e.
`common_code` folder (assumed to be needed by `model1`) is included. Note that
`model2` folder would also be deployed (this is assumed to be unnecessary but
harmless).

## Import Guidelines
The repo's root folder is the base folder when importing. For example, assume
you have these files in the folder with model code: 
 - `model_code/model.py`
 - `model_code/helper.py` 
 - `model_code/data.csv` 

If `model.py` needs to import `helper.py`, use: `import model_code.helper`. If
`model.py` needs to read `data.csv`, the right path is
`os.path.join('model_code', 'data.csv')`. 

It's of course possible to import from the Mlops package, e.g. its logger:
``` python
from akerbp.mlops.core import logger 
logging=logger.get_logger("logger_name")
logging.debug("This is a debug log")
```

## Services
We consider two types of services: prediction and training. 

Deployed services can be called with 
```python
from akerbp.mlops.xx.helpers import call_function
output = call_function(external_id, data)
```
Where `xx` is either `'cdf'` or `'gc'`, and `external_id` follows the
structure `model-service-env`:
 - `model`: model name given by the user (settings file)
 - `service`: either `training` or `prediction`
 - `env`: either `dev`, `test` or `prod` (depending on the deployment
   environment)

The output has a status field (`ok` or `error`). If they are 'ok', they have
also a `prediction` and `prediction_file` or `training` field (depending on the type of service). The
former is determined by the `predict` method of the model, while the latter
combines artifact metadata and model metadata produced by the `train` function.
Prediction services have also a `model_id` field to keep track of which model
was used to predict.

See below for more details on how to call prediction services hosted in CDF.

## Deployment Platform
Model services (described below) can be deployed to either CDF or GCR,
independently. 

### CDF Specific Features
CDF Functions include metadata when they are called. This information can be
used to redeploy a function (specifically, the `file_id` field). Example:

```python
import akerbp.mlops.cdf.helpers as cdf

human_readable_name = "My model"
external_id = "my_model-prediction-test"

cdf.set_up_cdf_client('deploy')
cdf.redeploy_function(
  human_readable_name
  external_id,
  file_id, 
  'Description', 
  'your@email.com'
)
```
Note that the external-id of a function needs to be unique, as this is used to distinguish functions betweeen services and hosting environment. 

It's possible to query available functions (can be filtered by environment
and/or tags). Example:
```python
import akerbp.mlops.cdf.helpers as cdf
cdf.set_up_cdf_client('deploy')
all_functions = cdf.list_functions()
test_functions = cdf.list_functions(env="test")
tag_functions = cdf.list_functions(tags=["well_interpretation"])
```
Functions can be deleted. Example:
```python
import akerbp.mlops.cdf.helpers as cdf
cdf.set_up_cdf_client('deploy')
cdf.delete_service("my_model-prediction-test")
```
Functions can be called in parallel. Example:
```python
from akerbp.mlops.cdf.helpers import call_function_parallel
function_name = 'my_function-prediction-prod'
data = [dict(data='data_call_1'), dict(data='data_call_2')]
response1, response2 = call_function_parallel(function_name, data)
```

## Model Manager
Model Manager is the module dedicated to managing the model artifacts used by
prediction services (and generated by training services). This module uses CDF
Files as backend.

Model artifacts are versioned and stored together with user-defined metadata.
Uploading a new model increases the version count by 1 for that model and
environment. When deploying a prediction service, the latest model version is
chosen. It would be possible to extend the framework to allow deploying specific
versions or filtering by metadata.

Model artifacts are segregated by environment (e.g. only production artifacts
can be deployed to production). Model artifacts have to be uploaded manually to
test (or dev) environment before deployment. Code example: 
```python 
import akerbp.mlops.model_manager as mm

metadata = train(model_dir, secrets) # or define it directly
mm.setup()
folder_info = mm.upload_new_model_version(
  model_name, 
  env,
  folder_path, 
  metadata
)
```
If there are multiple models, you need to do this one at at time. Note that
`model_name` corresponds to one of the elements in `model_names` defined in
`mlops_settings.py`, `env` is the target environment (where the model should be
available), `folder_path` is the local model artifact folder and `metadata` is a
dictionary with artifact metadata, e.g. performance, git commit, etc.

Model artifacts needs to be promoted to the production environment (i.e. after
they have been deployed successfully to test environment) so that a prediction
service can be deployed in production.
```python 
# After a model's version has been successfully deployed to test
import akerbp.mlops.model_manager as mm

mm.setup()
mm.promote_model('model', 'version')
```

### Versioning 
Each model artifact upload/promotion increments a version number (environment dependent)
available in Model Manager. However, this doesn't modify the model
artifacts used in existing prediction services (i.e. nothing changes in CDF
Functions). To reflect the newly uploaded/promoted model artifacts in the existing services one need to deploy the services again. Note that we dont have to specify the artifact version explicitly if we want to deploy using the latest artifacts, as this is done by default. 

Recommended process to update a model artifact and prediction service:
1. New model features implemented in a feature branch
2. New artifact generated and uploaded to test environment
3. Feature branch merged with master
4. Test deployment is triggered automatically: prediction service is deployed to
   test environment with the latest artifact version (in test)
5. Prediction service in test is verified
6. Artifact version is promoted manually from command line whenever suitable
7. Production deployment is triggered manually from Bitbucket: prediction
   service is deployed to production with the latest artifact version (in prod)

It's possible to get an overview of the model artifacts managed by Model
Manager. Some examples (see `get_model_version_overview` documentation for other
possible queries):
```python 
import akerbp.mlops.model_manager as mm
mm.setup()
# all artifacts
folder_info = mm.get_model_version_overview() 
# all artifacts for a given model
folder_info = mm.get_model_version_overview(model_name='xx')
```
If the overview shows model artifacts that are not needed, it is possible to
remove them. For example if artifact "my_model/dev/5" is not needed:
```python 
model_to_remove = "my_model/dev/5"
mm.delete_model_version(model_to_remove)
```
Model Manager will by default show information on the artifact to delete and ask
for user confirmation before proceeding. It's possible (but not recommended) to
disable this check. There's no identity check, so it's possible to delete any
model artifact (from other datas cientists). Be careful!

It's possible to download a model artifact (e.g. to verify its content). For
example:
```python 
mm.download_model_version('model_name', 'test', 'artifact_folder', version=5)
```
If no version is specified, the latest one is downloaded by default.

By default, Model Manager assumes artifacts are stored in the `mlops` dataset.
If your project uses a different one, you need to specify during setup (see
`setup` function).

Further information:
- Model Manager requires `COGNITE_API_KEY_*` environmental variables (see next
  section) or a suitable key passed to the `setup` function.
- In projects with a training service, you can rely on it to upload a first
  version of the model. The first prediction service deployment will fail, but
  you can deploy again after the training service has produced a model.
- When you deploy from the development environment (covered later in this
  document), the model artifacts in the settings file can point to existing
  local folders. These will then be used for the deployment. Version is then
  fixed to `model_name/dev/1`. Note that these artifacts are not uploaded to CDF
  Files.
- Prediction services are deployed with model artifacts (i.e. the artifact is
  copied to the project file used to create the CDF Function) so that they are
  available at prediction time. Downloading artifacts at run time would require
  waiting time, and files written during run time consume ram memory). 

## Model versioning 
To allow for model versioning and rolling back to previous model deployments, the external id of the functions (in CDF) includes a version number that is reflected by the latest artifact version number when deploying the function (see above).
Everytime we upload/promote new model artifacts and deploy our services, the version number of the external id of the functions representing the services are incremented (just as the veresion number for the artifacts). 

To distinguish the latest model from the remaining model versions, we redeploy the latest model version using a predictable external id that does not contain the version number. By doing so we relieve the clients need of dealing with version numbers, and they will call the latest model by default. For every new deployment, we will thus have two model deployments - one with the version number, and one without the version number in the external id.  However, the predictable external id is persisted across new model versions, so when deploying a new version the latest one, with the predictable external id, is simply overwritten.

We are thus concerned with two structures for the external id
- ```<model_name>-<service>-<env>-<version>``` for rolling back to previous versions, and 
- ```<model_name>-<service>-<env>``` for the latest deployed model

For the latest model with a predictable external id, we tag the description of the model to specify that the model is in fact the latest version, and add the version number to the function metadata.

We can now list out multiple models with the same model name and external id prefix, and choose to make predictions and do inference with a specific model version. An example is shown below.
```python
# List all prediction services (i.e. models) with name "My Model" hosted in the test environment, and model corresponding to the first element of the list
from cognite.expeerimental import CogniteClient 
client = CogniteClient(client_name="model inference") # pass an arbitrary client_name
my_models = client.functions.list(name="My Model", external_id_prefix="mymodel-prediction-test")
my_model_specific_version = my_models[0]
```
## Calling a deployed model prediction service hosted in CDF
This section describes how you can call deployed models and obtain predictions for doing inference.
We have two options for calling a function in CDF, either using the MLOps framework directly or by using the Cognite SDK. Independent of how you call your model, you have to pass the data as a dictionary with a key "data" containing a dictionary with your data, where the keys of the inner dictionary specifies the columns, and the values are list of samples for the correspondsing columns. 

First, load your data and transform it to a dictionary as assumed by the framework. Note that the data dictionary you pass to the function might vary based on your model interface. Make sure to align with what you specified in your `model.py` interface.
```python
import pandas as pd
data = pd.read_csv("path_to_data")
input_data = data.drop(columns=[target_variables])
data_dict = {"data": input_data.to_dict(orient=list), "to_file": True}
```
The "to_file" key of the input data dictionary specifies how the predictions can be extracted downstream. More details are provided below 

Calling deployed model using MLOps:
1. Set up a cognite client with sufficient access rights
2. Extract the response directly by specifying the external id of the model and passing your data as a dictionary
    - Note that the external id is on the form
      - ```"<model_name>-<service>-<env>-<version>"```, and 
      - ```"<model_name>-<service>-<env>"```

Use the latter external id if you want to call the latest model. The former external id can be used if you want to call a previous version of your model. 

```python 
from akerbp.mlops.cdf.helpers import set_up_cdf_client, call_function 
set_up_cdf_client(context="deploy") #access CDF data, files and functions with deploy context
response = call_function(function_name="<model_name>-prediction-<env>", data=data_dict)
```

Calling deployed model using the Cognite SDK: 
1. set up cognite client with suffient access rights
2. Retreive model from CDF by specifying the external-id of the model
3. Call the function
4. Extract the function call response from the function call

```python 
from cognite.expeerimental import CogniteClient 
client = CogniteClient(client_name="model inference") # pass an arbitrary client_name
function = client.functions.retrieve(external_id="<model_name>-prediction-<env>")
function_call = function.call(data=data_dict)
response = function_call.get_response()

```
Depending on how you specified the input dictionary, the predictions are available directly from the response or needs to be extracted from Cognite Files.
If the input data dictionary contains a key "to_file" with value True, the predictions are uploaded to cognite Files, and the 'prediction_file' field in the reponse will contain a reference to the file containing the predictions. If "to_file" is set to False, or if the input dictionary does not contain such a key-value pair, the predictions are directly available through the function call response. 

If "to_file" = True, we can extract the predictions using the following code-snippet
```python
file_id = response["prediction_file"]
bytes_data = client.files.download_bytees(external_id=file_id)
predictions_df = pd.DataFrame.from_dict(json.loads(bytes_data))
```
Otherwise, the predictions are directly accessible from the response as follows. 
```python 
predictions = response["predictions"]
```

## Extracting metadata from deployed model in CDF 
Once a model is deployed, a user can extract potentially valuable metadata as follows. 
```python 
my_function = client.functions.retrieve(external_id="my_model-prediction-test")
metadata = my_function.metadata
```
Where the metadata corresponds to whatever you specified in the mlops_settings.yaml file. For this example we get the following metadata
```
{'cat_filler': 'UNKNOWN',
 'imputed': 'True',
 'input_types': '[int, float, string]',
 'num_filler': '-999.15',
 'output_curves': '[AC]',
 'output_unit': '[s/ft]',
 'petrel_exposure': 'False',
 'required_input': '[ACS, RDEP, DEN]',
 'training_wells': '[3/1-4]',
 'units': '[s/ft, 1, kg/m3]'}
```


## Local Testing and Deployment
It's possible to tests the functions locally, which can help you debug errors
quickly. This is recommended before a deployment. 

Define the following environmental variables (e.g. in `.bashrc`):
```bash
export ENV=dev
export COGNITE_API_KEY_PERSONAL=xxx
export COGNITE_API_KEY_FUNCTIONS=$COGNITE_API_KEY_PERSONAL
export COGNITE_API_KEY_DATA=$COGNITE_API_KEY_PERSONAL
export COGNITE_API_KEY_FILES=$COGNITE_API_KEY_PERSONAL
export GOOGLE_PROJECT_ID=xxx # If deploying to Google Cloud Run
```

From your repo's root folder:
- `python -m pytest model_code` (replace `model_code` by your model code folder
  name)
- `deploy_prediction_service.sh`
- `deploy_training_service.sh` (if there's a training service)

The first one will run your model tests. The last two run model tests but also
the service tests implemented in the framework and simulate deployment.

If you really want to deploy from your development environment, you can run
this: `LOCAL_DEPLOYMENT=True deploy_prediction_service.sh`

Note that, in case of emergency, it's possible to deploy to test or production
from your local environment, e.g. : `ENV=test deploy_prediction_service.sh`

## Automated Deployments from Bitbucket
Deployments to the test environment are triggered by commits (you need to push
them). Deployments to the production environment are enabled manually from the
Bitbucket pipeline dashboard. Branches that match 'deploy/*' behave as master. 
Branches that match 'feature/*' run tests only (i.e. do not deploy).

It is assumed that most projects won't include a training service. A branch that
matches 'mlops/*' deploys both prediction and training services. If a project
includes both services, the pipeline file could instead be edited so that master
deployed both services.

It is possible to schedule the training service in CDF, and then it can make
sense to schedule the deployment pipeline of the model service (as often as new
models are trained)

## Bitbucket Setup
The following environments need to be defined in `repository settings >
deployments`: 
- test deployments: `test-prediction` and `test-training`, each with `ENV=test`
- production deployments: `production-prediction` and `production-training`,
  each with `ENV=prod`

The following need to be defined in `respository settings > repository
variables`: `COGNITE_API_KEY_DATA`, `COGNITE_API_KEY_FUNCTIONS`,
`COGNITE_API_KEY_FILES` (these should be CDF keys with access to data, functions
and files). If deployment to GCR is needed, you need in addition:
`ENABLE_GC_DEPLOYMENT` (set to `True`), `GOOGLE_SERVICE_ACCOUNT_FILE` (content
of the service account id file) and `GOOGLE_PROJECT_ID` (name of the project)

The pipeline needs to be enabled.


# Developer/Admin Guide
## Package versioning 
The versioning of the package follows [Semantic Versioning 2.0.0](https://semver.org/), using the `MAJOR.MINOR.PATCH` structure. We are thus updating the package version using the following convention
1. Increment MAJOR when making incompatible API changes
2. Increment MINOR when adding backwards compatible functionality
3. Increment PATCH when making backwards compatible bug-fixes

The version is updated based on the latest commit to the repo, and we are currently using the following rules.
- The MAJOR version is incremented if the commit message includes the word `major`
- The MINOR version is incremented if the commit message includes the word `minor`
- The PATCH number is incremented if neither `major` nor `minor` if found in the commit message
- If the commit message includes the phrase `pre-release`, the package version is extended with `-alpha`, thus taking the form `MAJOR.MINOR.PATCH-alpha`.

Note that the above keywords are **not** case sensitive. Moreover, `major` takes precedence over `minor`, so if both keywords are found in the commit message, the MAJOR version is incremented and the MINOR version is kept unchanged.

In dev and test environment, we release the package using the pre-release tag, and the package takes the following version number `MAJOR.MINOR.PATCH-alpha`.



## MLOps Files and Folders
These are the files and folders in the MLOps repo:
- `src` contains the MLOps framework package
- `mlops_settings.yaml` contains the user settings for the dummy model
- `model_code` is a model template included to show the model interface. It is
  not needed by the framework, but it is recommended to become familiar with it.
- `model_artifact` stores the artifacts for the model shown in  `model_code`.
  This is to help to test the model and learn the framework.
- `bitbucket-pipelines.yml` describes the deployment pipeline in Bitbucket
- `build.sh` is the script to build and upload the package
- `setup.py` is used to build the package
- `LICENSE` is the package's license

## CDF Datasets
In order to control access to the artifacts:
1. Set up a CDF Dataset with `write_protected=True` and a `external_id`, which
   by default is expected to be `mlops`.
2. Create a group of owners (CDF Dashboard), i.e. those that should have write
   access

## Build and Upload Package
Create an account in pypi, then create a token and a `$HOME/.pypirc` file. Edit
`setup.py` file and note the following:
- Dependencies need to be registered
- Bash scripts will be installed in a `bin` folder in the `PATH`. 

The pipeline is setup to build the library from Bitbucket, but it's possible to
build and upload the library from the development environment as well:
```bash
bash build.sh
```
In general this is required before `LOCAL_DEPLOYMENT=True bash
deploy_xxx_service.sh`. The exception is if local changes affect only the
deployment part of the library, and the library has been installed in developer
mode with: 
```bash
pip install -e .
```
In this mode, the installed package links to the source code, so that it can be
modified without the need to reinstall).

## Bitbucket Setup
In addition to the user setup, the following is needed to build the package:
- `test-pypi`: `ENV=test`, `TWINE_USERNAME=__token__` and `TWINE_PASSWORD`
  (token generated from pypi)
- `prod-pypi`: `ENV=prod`, `TWINE_USERNAME=__token__` and `TWINE_PASSWORD`
  (token generated from pypi, can be the same as above)


## Google Cloud Setup
In order to deploy to Google Cloud Run, you need to create a service account
with the following rights: 
 - Cloud Build Service Account
 - Service Account Admin
 - Service Account User
 - Cloud Run Admin
 - Viewer

You also need to create the CDF secret `mlops-cdf-keys`. It's a string that can
be evaluated in python to get a dictionary (same used in the cdf helpers file).
This is because:
 - It needs to be passed to prediction and training services
 - Model registry uses CDF Files in its


## Calling FastApi services
Bash: install httpie, then:
```bash
http -v POST http://127.0.0.1:8000/train data='{"x": [1,-1],"y":[1,0]}'
```
Python: challenging when posting nested json with requests. This works:
```python
import requests, json
data = {"x":[1,-1], "y":[1,0]}
requests.post(model_api, json={'data': json.dumps(data)})
```
   
## Notes on the code

Service testing happens in an independent process (subprocess library) to avoid
setup problems:
 - When deploying multiple models the service had to be reloaded before testing
   it, otherwise it would be the first model's service. Model initialization in
   the prediction service is designed to load artifacts only once in the process
 - If the model and the MLOps framework rely on different versions of the same
   library, the version would be changed during runtime, but the
   upgraded/downgraded version would not be available for the current process
