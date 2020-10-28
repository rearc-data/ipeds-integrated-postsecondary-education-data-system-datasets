#!/usr/bin/env bash

# Exit on error. Append "|| true" if you expect an error.
set -o errexit
# Exit on error inside any functions or subshells.
set -o errtrace
# Do not allow use of undefined vars. Use ${VAR:-} to use an undefined VAR
#set -o nounset
# Catch the error in case mysqldump fails (but gzip succeeds) in `mysqldump |gzip`
set -o pipefail
# Turn on traces, useful while debugging but commented out by default
# set -o xtrace

export SOURCE_DATA_URL="${SOURCE_DATA_URL}"
export S3_BUCKET="${S3_BUCKET:-'rearc-data-provider'}"
export REGION="${REGION:-'us-east-1'}"
export DATASET_NAME="${DATASET_NAME:-''}"
export DATASET_ARN="${DATASET_ARN}" 
export DATASET_ID="${DATASET_ID}"
export PRODUCT_NAME="${PRODUCT_NAME}"
export PRODUCT_ID="${PRODUCT_ID}"
export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID_APP}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY_APP}"

echo "SOURCE_DATA_URL: $SOURCE_DATA_URL"
echo "S3_BUCKET: $S3_BUCKET"
echo "REGION: $REGION"
echo "DATASET_NAME: $DATASET_NAME"
echo "DATASET_ARN: $DATASET_ARN"
echo "DATASET_ID: $DATASET_ID"
echo "PRODUCT_NAME: $PRODUCT_NAME"
echo "PRODUCT_ID: $PRODUCT_ID"

if [[ ${#DATASET_NAME} -gt 53 ]]; then
    echo "dataset-name must be under 53 characters in length, use a shorter name!"
    exit 1
fi

if [[ ${#PRODUCT_NAME} -gt 72 ]]; then
    echo "product-name must be under 72 characters in length, use a shorter name!"
    exit 1
fi


if [[ -z "${DATASET_ARN}" ]]; then
  echo "create a dataset on ADX if DATASET_ARN is not set"

  DATASET_COMMAND="aws dataexchange create-data-set --asset-type "S3_SNAPSHOT" --description file://dataset-description.md --name \"${PRODUCT_NAME}\" --region $REGION --output json"
  DATASET_OUTPUT=$(eval $DATASET_COMMAND)
  DATASET_ARN=$(echo $DATASET_OUTPUT | tr '\r\n' ' ' | jq -r '.Arn')
  DATASET_ID=$(echo $DATASET_OUTPUT | tr '\r\n' ' ' | jq -r '.Id')

  echo "DATASET_OUTPUT: $DATASET_OUTPUT"
fi

echo "DATASET_ARN: $DATASET_ARN"
echo "DATASET_ID: $DATASET_ID"

echo "Unzipping chromedriver"
# if [[ -f util/chromium.zip ]]; then
#   cd util/
#   ls 
#   unzip chromium.zip
#   rm chromium.zip
#   chmod a+x chromium
#   cd ..
# fi

# python src/source_data.py

echo "create a dataset revision if there is an update to the source data"
python src/create_dataset_revision.py \
    --source_data_url "$SOURCE_DATA_URL" \
    --region "$REGION" \
    --s3_bucket "$S3_BUCKET" \
    --dataset_name "$DATASET_NAME" \
    --dataset_id "$DATASET_ID" \
    --dataset_arn "$DATASET_ARN" \
    --product_name "$PRODUCT_NAME" \
    --product_id "$PRODUCT_ID"

echo "check dataset revision status"
DATASET_REVISION_STATUS=$(aws dataexchange list-data-set-revisions --data-set-id "$DATASET_ID" --region "$REGION" --query "sort_by(Revisions, &CreatedAt)[-1].Finalized")

if [[ $DATASET_REVISION_STATUS == "true" ]]
then
  echo "Dataset revision completed successfully\n"
  echo "Manually create the ADX product from Amazon Data Exchange Console.\n"
  echo "In Noop console, copy the PRODUCT_ID, DATASET_ID, and DATASET_ARN from
        ADX console and add them to Variables & Secrets section of your app Environment."

else
  echo "Dataset revision failed"
  cat response.json
fi