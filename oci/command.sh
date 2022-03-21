#! /bin/bash

# export PATH=/home/ubuntu/bin:$PATH
export OCI_CLI_RC_FILE=/home/ubuntu/.oci/config

# compartment
export C="compartment-id-goes-here"
# availability zone
export A="availability-zone-here"
# subnet
export S="subnet-id-here"
# image
export I="image-id-here"
# oci-home
export OCI_HOME="$HOME/.oci"
# oci-home
export A1_CONF="file://$HOME/.oci/a1"

command="/home/ubuntu/bin/oci compute instance launch \
 --availability-domain $A \
 --compartment-id $C \
 --shape VM.Standard.A1.Flex \
 --subnet-id $S \
 --assign-private-dns-record true \
 --assign-public-ip false \
 --availability-config $A1_CONF/availabilityConfig.json \
 --display-name a1-ubuntu-instance \
 --image-id $I \
 --instance-options $A1_CONF/instanceOptions.json \
 --shape-config $A1_CONF/shapeConfig.json \
 --ssh-authorized-keys-file $HOME/.oci/id_rsa.pub"

echo "$(date): $command"
echo "..."
eval $command
echo "$(date): done!"
