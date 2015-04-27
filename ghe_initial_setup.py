#! /usr/local/bin/python3

import sys, os

PrimaryIP = sys.argv[1]

ReplicaIP = sys.argv[2]

SSHKeyFile = "/Users/carol/Carol_key_California.pem"


#get RSA keypair
os.system("echo 5678")
os.system('RSAValue=$(ssh -i ' + SSHKeyFile + ' -p 122 admin@' + ReplicaIP + ' "ghe-repl-setup ' + PrimaryIP + '"| grep "ssh-rsa")')
os.system("echo 1234")
os.system("echo $RSAValue")

