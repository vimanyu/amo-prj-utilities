#!/bin/bash

context=$1

new_conda_env () { conda create -y -q --name "$1" python=3.8 && conda activate "$1" && pip install flask;}


#new_flask_project () {pip install flask -y && ;}

validate_gcloud_project () {

	echo Validating gcloud project $context
	local valid_project=$(python validate_gcloud_project.py $context)
	echo testing: $valid_project
	if [ $valid_project -eq 0 ]
	then
		echo $context is a valid project
	else
		echo $context is not a valid project
		Exit 1
	fi
}

create_directories () {
	
	echo Creating directories...
	#validate google project


	local output_dir=$(python main.py $context)
	echo Echoing: $output_dir
	cd $output_dir
}
#$SHELL


validate_gcloud_project


