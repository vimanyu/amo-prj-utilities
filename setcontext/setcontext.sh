setcontext () {
  conda activate amo-prj-utilities;
  eval `python /Users/andrewoseen/git/amo-prj-utilities/setcontext/setcontext.py setcontext $1`;
}

delcontext () {
  #this is meant to destr
  local context=$1
	tput setaf 1; echo Deleting context: $context
}


