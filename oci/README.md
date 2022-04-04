# Script to create a1 instances

Influenced by https://hitrov.medium.com/resolving-oracle-cloud-out-of-capacity-issue-and-getting-free-vps-with-4-arm-cores-24gb-of-a3d7e6a027a8

## Generate OCI API key
After logging in to OCI Console, click profile icon and then “User Settings”

Go to Resources -> API keys, click “Add API Key” button

Make sure “Generate API Key Pair” radio button is selected, click “Download Private Key” and then “Add”.
Put the key file in the same directory with the command.sh file. I will coll this directory `.oci/`
Copy the contents from textarea and save it to file with a name “config” and put it in the same `.oci/` directory next to the command.sh file.


## Setting up CLI

Specify config location

OCI_CLI_RC_FILE=.oci/config

If you haven’t added OCI CLI binary to your PATH, run

alias oci='/home/ubuntu/bin/oci'

(or whatever path it was installed).

Set permissions for the private key

oci setup repair-file-permissions --file .oci/oracleidentitycloudservice***.pem

Test the authentication (user value should be taken from textarea when generating API key):

oci iam user get --user-id ocid1.user.oc1..aaaaaaaax72***d3q

Output should be a json file containing compartment-id, capabilities and other fileds.

## Setting up the command.sh script

The scipt `command.sh` contains the following setup section
```
# compartment
export C="compartment-id-goes-here"
# availability zone
export A="availability-zone-here"
# subnet
export S="subnet-id-here"
# image
export I="image-id-here"
```
Get compartment-id-goes-here from your oci config file (tenancy field)
Get availability-zone-here from the fields name of the output of the command
```
oci iam availability-domain list --all --compartment-id=$C
```
a subnet id could be taken from the output of the command (data.id field)
```
oci network subnet list --compartment-id=$C
```
Choose an image id from the output of the command below
```
oci compute image list  --compartment-id=$C --shape=VM.Standard.A1.Flex
```

## Crontab
```
crontab -e
```
add a line 
```

# */2 * * * * /home/ubuntu/.oci/command.sh 2>&1 | tee -a /home/ubuntu/.oci/logs/cron.log
```