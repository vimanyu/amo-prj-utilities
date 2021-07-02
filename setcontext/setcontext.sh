alias validate_gcloud_py='/Users/andrewoseen/git/amo-prj-utilities/validate_project_name/main.py'
alias create_dir_py='/Users/andrewoseen/git/amo-prj-utilities/setcontext/main.py'


validate_gcloud_project () {

	tput setaf 3; echo Validating gcloud project: $context | sed 's/^/  /'
	local valid_project=$(python /Users/andrewoseen/git/amo-prj-utilities/setcontext/validate_gcloud_project.py $1)
	if [ $valid_project -eq 0 ]
	then
		tput setaf 2; echo $context is a valid project | sed 's/^/    /'
	else
		tput setaf 1; echo $context is not a valid project | sed 's/^/    /'
		Exit 1
	fi
}

change_directory () {
	
	tput setaf 3;echo Creating directories... | sed 's/^/  /'
	local output_dir=$(python /Users/andrewoseen/git/amo-prj-utilities/setcontext/main.py $1)
	cd $output_dir
}

create_conda_env () {
  tput setaf 3; echo Creating conda env: $context | sed 's/^/  /'
	conda create -y -q --name $1 python=3.8
	conda activate $1
	#pip install requirements for a flask project
	pip install flask
}

initialize_git_repo () {
  tput setaf 3;echo Initializing Git... | sed 's/^/  /'
	git init
	hub create

}

newcontext () {
	local context=$1
	
	validate_gcloud_project $context
	change_directory $context
	create_conda_env $context
	initialize_git_repo
}

setcontext () {
	local context=$1

	tput setaf 4; echo Setting context: $1
	change_directory $context
	conda activate $context

}

