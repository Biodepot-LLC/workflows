#!/bin/bash

function get_excluded_dicom_fields
{
	if [ ! -z "$(printenv PatientID)" ]; then DEFAULT_FIELDS="$DEFAULT_FIELDS'PatientID', "; fi
	if [ ! -z "$(printenv PatientName)" ]; then DEFAULT_FIELDS="$DEFAULT_FIELDS'PatientName', "; fi
	if [ ! -z "$(printenv PatientSex)" ]; then DEFAULT_FIELDS="$DEFAULT_FIELDS'PatientSex', "; fi
	if [ ! -z "$(printenv PatientBirthDate)" ]; then DEFAULT_FIELDS="$DEFAULT_FIELDS'PatientBirthDate', "; fi
	if [ ! -z "$(printenv PatientOrientation)" ]; then DEFAULT_FIELDS="$DEFAULT_FIELDS'PatientOrientation', "; fi
	if [ ! -z "$(printenv PatientAge)" ]; then DEFAULT_FIELDS="$DEFAULT_FIELDS'PatientAge', "; fi
	if [ ! -z "$(printenv PatientSize)" ]; then DEFAULT_FIELDS="$DEFAULT_FIELDS'PatientSize', "; fi
	if [ ! -z "$(printenv PatientWeight)" ]; then DEFAULT_FIELDS="$DEFAULT_FIELDS'PatientWeight', "; fi
	if [ ! -z "$(printenv PatientAddress)" ]; then DEFAULT_FIELDS="$DEFAULT_FIELDS'PatientAddress', "; fi
	if [ ! -z "$(printenv PatientMotherBirthName)" ]; then DEFAULT_FIELDS="$DEFAULT_FIELDS'PatientMotherBirthName', "; fi
	if [ ! -z "$(printenv PatientBirthName)" ]; then DEFAULT_FIELDS="$DEFAULT_FIELDS'PatientBirthName', "; fi

	if [ -z "$DEFAULT_FIELDS" ]
	then
		DEFAULT_FIELDS="'PatientID', 'PatientName', 'PatientSex', 'PatientBirthDate', 'PatientOrientation'"
	else
		DEFAULT_FIELDS="${DEFAULT_FIELDS::-2}"
	fi
}

if [ -z "$1" ]
then
	echo "Usage: $0 [local|gcp] ARGMENTS"
	exit 1
fi

get_excluded_dicom_fields
if [ "$1" == "local" ]
then
	if [ -z "$2" ] || [ ! -f "$2" ]
	then
		echo "Usage: $0 local DICOM_INPUT_FILE [DICOM_FIELDS_FILE] [DICOM_OUTPUT_FILE]"
		exit 1
	fi
	DICOM_INPUT_FILE="$2"
	DICOM_FIELDS_FILE="$3"

	if [ -z "$DICOM_FIELDS_FILE" ] || [ ! -f "$DICOM_FIELDS_FILE" ]
	then
		DICOM_FIELDS_FILE="/root/list.txt"
	fi
	
	python3 fields.py $DICOM_FIELDS_FILE

	FIELDS=$(sed 's/,/ /g' $DICOM_FIELDS_FILE)
	if [ -z "$FIELDS" ]
	then
		SELECTED_FIELDS=$DEFAULT_FIELDS
	else
		for FIELD in ${FIELDS[@]}
		do
			SELECTED_FIELDS="$SELECTED_FIELDS,'$FIELD'"
		done
		SELECTED_FIELDS=${SELECTED_FIELDS:1}
	fi

	FULL_NAME=$(basename $2)
	FILE_NAME=${FULL_NAME%.*}_deidentified
	EXTENSION=${FULL_NAME##*.}
	python3 -c "from dicom import de_identify; de_identify('$2', fields=[$SELECTED_FIELDS], output_file='$(dirname $2)/$FILE_NAME.$EXTENSION');"

elif [ "$1" == "gcp" ]
then
	if [ -z "$2" ] || [ ! -f "$2" ] || [ -z "$3" ] || [ -z "$4" ] || [ -z "$5" ] || [ -z "$6" ]
	then
		echo "Usage: $0 gcp CREDENTIAL_FILE PROJECT_ID LOCATION DATASET DATASET_DEIDENTIFIED"
		exit 1
	fi
	
	gcloud auth activate-service-account --key-file="$2"
	if [ $? -gt 0 ]
	then
		echo "Could not activate service account"
		exit 1
	fi
	
	gcloud config set component_manager/disable_update_check true
	gcloud config set project "$3"
	if [ $? -gt 0 ]
	then
		echo "Could not find the project '$3'"
		exit 1
	fi
	PROJECT_ID=$3
	USER_EMAIL=$(gcloud iam service-accounts list --format=json | jq -r '.[] | select(.projectId == "$PROJECT_ID") | .email' | head -n1)
	gcloud services enable cloudresourcemanager.googleapis.com
	gcloud services enable healthcare.googleapis.com

	LOCATION=$4
	DATASET=$5
	DATASET_OUT=$6
	gcloud healthcare datasets delete $DATASET_OUT --quiet
	
	DICOM_FIELDS_FILE="$7"
	if [ -z "$DICOM_FIELDS_FILE" ] || [ ! -f "$DICOM_FIELDS_FILE" ]
	then
		DICOM_FIELDS_FILE="/root/list.txt"
	fi
	
	python3 fields.py $DICOM_FIELDS_FILE
	
	FIELDS=$(sed 's/,/ /g' $DICOM_FIELDS_FILE)
	if [ -z "$FIELDS" ]
	then
		SELECTED_FIELDS=$DEFAULT_FIELDS
	else
		for FIELD in ${FIELDS[@]}
		do
			SELECTED_FIELDS="$SELECTED_FIELDS,'$FIELD'"
		done
		SELECTED_FIELDS=${SELECTED_FIELDS:1}
	fi
	
    curl -sX POST \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json; charset=utf-8" \
    --data "{
        'destinationDataset': 'projects/$PROJECT_ID/locations/$LOCATION/datasets/$DATASET_OUT',
        'config': {
            'dicom': {
                'removeList': {
                    'tags': [
                        $SELECTED_FIELDS
                    ]
                }
            }
        }
    }" "https://healthcare.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION/datasets/$DATASET:deidentify"
	
else
	echo "Could not recognize the option '$1'"
	echo "Usage: $0 [local|gcp] ARGMENTS"
	exit 1
fi
