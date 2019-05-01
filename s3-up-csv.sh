#!/bin/bash

MAXFILESIZE=100000
configfile=s3-up-csv.cfg
envname=$1

# Parse arguments
PARAMS=""
while (( "$#" )); do
  case "$1" in
    -i|--input-file) # input csv file with memberIds
      inputfile=$2
      if ! [[ $inputfile =~ \.csv$ ]]
        then 
            echo "Error: Unsupported input file type. Supported file types: csv."
            exit 1
      fi
      inputfilesize=wc -c $inputfile | awk '{print $1}'
      if [ $inputfilesize -gt $MAXFILESIZE ]
        then
            echo "Error: The $inputfile is to big. Should be less then $MAXFILESIZE bytes"
            exit 1
      fi            
      shift 2
      ;;
    -c|--config) # config file. Default one is add-members.config
      configfile=$2
      shift 2
      ;;
    -e|--env) # environment 
      envname=$2
      shift 2
      ;;
    --) # end argument parsing
      shift
      break
      ;;
    -*|--*=) # unsupported flags
      echo "Error: Unsupported flag $1" >&2
      exit 1
      ;;
    *) # preserve positional arguments
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done
# set positional arguments in their proper place
# eval set -- "$PARAMS"

echo $PARAMS

source $configfile

# configure paths according to environment
path=$DEV_PATH
profile=$NONPROD_PROFILE
case $envname in 
    dev)
        ;;
    qa) 
        path=$QA_PATH
        ;;
    preprod) 
        profile=$PROD_PROFILE
        path=$PREPROD_PATH
        echo "preprod not yet defined"
        # exit 1
        ;;
    prod) 
        profile=$PROD_PROFILE
        path=$PROD_PATH
        echo "prod not yet defined"
        # exit 1
        ;;
    *)
        echo "Usage: $0 {dev|qa|preprod|prod} memberid1 memberid2 .. memberidN"
        exit 1
esac

# create tmp file
now=$(date +"%F-%H-%M-%S") 
tmpfile="s3-up-csv-$envname-$2-$now.csv"
if [ -z ${inputfile+x} ] 
    then # fill up a temporary csv file with member ids
        for var in $PARAMS
        do
            if [ $var == $envname ]
                then
                    continue
            fi
            echo $var >> $tmpfile
        done
        fname=$tmpfile
    else # use input file
        fname=$inputfile
        echo "nothing" >> $tmpfile
fi

echo "input: $envname/$fname/$path/$profile"

echo "head $fname"
head $fname
echo "..."
aws s3 cp --dryrun --profile $profile $fname s3://$path
rm $tmpfile
