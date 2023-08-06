# install_gc_sdk.sh
#
# Install Google Cloud SDK. 
#
# Requirements:
# Service account file should be stored as secret in 
# the env var GOOGLE_SERVICE_ACCOUNT_FILE 

if [ "$ENABLE_GC_DEPLOYMENT" = "True" ]
then 
    echo "ENABLE_GC_DEPLOYMENT is enabled, install Google cloud SDK..."
    export CLOUDSDK_CORE_DISABLE_PROMPTS=1
    # Google Cloud SDK is pinned for build reliability. Bump if the SDK complains about deprecation.
    SDK_VERSION=324.0.0
    SDK_FILENAME=google-cloud-sdk-${SDK_VERSION}-linux-x86_64.tar.gz
    echo "Download ${SDK_FILENAME}"
    curl -O -J https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/${SDK_FILENAME}
    echo "Extract ${SDK_FILENAME}"
    tar -zxf ${SDK_FILENAME} --directory ${HOME}
    export PATH=${PATH}:${HOME}/google-cloud-sdk/bin
    # Activate deployment service account
    echo ${GOOGLE_SERVICE_ACCOUNT_FILE} > service_account.json
    export GOOGLE_APPLICATION_CREDENTIALS="service_account.json"
    echo "Activate service account"
    gcloud auth activate-service-account --key-file service_account.json
    gcloud config set project $GOOGLE_PROJECT_ID
else
    echo "ENABLE_GC_DEPLOYMENT is disabled, won't install Google cloud SDK."
fi