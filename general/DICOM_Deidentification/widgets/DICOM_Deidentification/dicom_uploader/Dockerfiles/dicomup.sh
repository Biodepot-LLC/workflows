#!/bin/bash

if [ -z "$1" ] || [ ! -f "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ] || [ -z "$5" ] || [ -z "$6" ] || [ -z "$7" ]
then
	echo "Usage: $0 CREDENTIAL_FILE BUCKET_NAME PROJECT_ID LOCATION DATASET DICOM_STORE FILE/DIRECTORY"
	exit 1
fi

CREDENTIAL_FILE=$1
BUCKET_NAME=$2
PROJECT_ID=$3
LOCATION=$4
DATASET=$5
DICOM_STORE=$6
DICOM_FILES=$7

gcloud auth activate-service-account --key-file="$CREDENTIAL_FILE"
if [ $? -gt 0 ]
then
	echo "Could not activate service account"
	exit 1
fi

FOUND_BUCKET=$(gsutil ls | grep ^gs://$BUCKET_NAME)
if [ -z "FOUND_BUCKET" ]
then
	echo "Could not find the bucket '$BUCKET_NAME'"
	exit 1
fi

gcloud config set component_manager/disable_update_check true
gcloud config set project "$PROJECT_ID"
if [ $? -gt 0 ]
then
	echo "Could not find the project '$PROJECT_ID'"
	exit 1
fi
PROJECT_NUMBER=$(gcloud projects list --format=json | jq -r ".[] | select(.projectId == \"$PROJECT_ID\") | .projectNumber" | head -n1)
USER_EMAIL=$(gcloud iam service-accounts list --format=json | jq -r ".[] | select(.projectId == \"$PROJECT_ID\") | .email" | head -n1)
gcloud services enable cloudresourcemanager.googleapis.com
gcloud services enable healthcare.googleapis.com

FOUND_DATASET=$(gcloud healthcare datasets list --format=json | jq -r ".[] | select(.name|test(\"projects/$PROJECT_ID/locations/$LOCATION/datasets/$DATASET\")) | .name")
if [ -z "FOUND_DATASET" ]
then
	echo "Could not find the dataset '$DATASET'"
    gcloud healthcare datasets create $DATASET
    echo "Created dataset '$DATASET'"
    
    gcloud healthcare dicom-stores create --dataset=$DATASET $DICOM_STORE
    echo "Created DICOM store '$DICOM_STORE'"
else
	FOUND_DICOM_STORE=$(gcloud healthcare dicom-stores list --dataset=$DATASET --format=json | jq -r '.[] | select(.name|test("projects/$PROJECT_ID/locations/$LOCATION/datasets/$DATASET/dicomStores/$DICOM_STORE")) | .name')
	if [ -z "FOUND_DICOM_STORE" ]
	then
		gcloud healthcare dicom-stores create --dataset=$DATASET $DICOM_STORE
		echo "Created DICOM store '$DICOM_STORE'"
	fi
fi

gcloud projects add-iam-policy-binding $PROJECT_ID --member=serviceAccount:service-$PROJECT_NUMBER@gcp-sa-healthcare.iam.gserviceaccount.com --role=roles/storage.admin
if [ $? -gt 0 ]
then
	echo "Something went wrong when trying to grant permission to access google storage"
	exit 1
fi

if [ -f "$DICOM_FILES" ]
then
	DICOM_FILES="$DICOM_FILES"
elif [ -d "$DICOM_FILES" ]
then
	DICOM_FILES="$(find "$DICOM_FILES" -type f -name "*.dcm")"
else
	echo "Could not read file/directory '$DICOM_FILES'"
	exit 1
fi
while IFS= read -r DICOM_FILE
do
	FILE="$DICOM_FILE"
	FILE_PATH=$(dirname $FILE)
	FILE_NAME=$(basename "$FILE")
	GS_FILE_PATH="$(echo $FILE | sed 's/ /_/g')"
	gsutil cp "$DICOM_FILE" "gs://$BUCKET_NAME/temp_dicom_dir$GS_FILE_PATH"
done <<< "$DICOM_FILES"

gcloud projects add-iam-policy-binding $PROJECT_ID --member=serviceAccount:service-$PROJECT_NUMBER@gcp-sa-healthcare.iam.gserviceaccount.com --role=roles/storage.admin
gcloud healthcare dicom-stores delete --dataset=$DATASET $DICOM_STORE --quiet
gcloud healthcare dicom-stores create --dataset=$DATASET $DICOM_STORE
gcloud healthcare dicom-stores import gcs $DICOM_STORE --gcs-uri="gs://$BUCKET_NAME/temp_dicom_dir/**" --dataset=$DATASET
gsutil -m rm -r gs://$BUCKET_NAME/temp_dicom_dir
