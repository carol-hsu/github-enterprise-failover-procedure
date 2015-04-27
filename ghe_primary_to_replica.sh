#! /bin/bash

OldPrimaryIP=$1

NewPrimaryIP=$2

SSHKeyFile="/Users/carol/Carol_key_California.pem"


#get RSA keypair

RSAValue=$(ssh -i $SSHKeyFile -p 122 admin@$OldPrimaryIP "ghe-repl-setup $NewPrimaryIP"| grep "ssh-rsa")

echo $RSAValue

