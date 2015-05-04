#! /usr/local/bin/python3

import sys, os

PrimaryIP = sys.argv[1]
ReplicaIP = sys.argv[2]

SSHKeyFile = "/Users/carol/Carol_key_California.pem"

SSHPrimary = "ssh -i "+SSHKeyFile+" -p 122 admin@"+PrimaryIP
SSHReplica = "ssh -i "+SSHKeyFile+" -p 122 admin@"+ReplicaIP


os.system(SSHReplica+" \"ghe-repl-teardown\"")

#----- RSA Keypair setting for Replica setup -----
#get RSA keypair and dump it in a file
os.system(SSHReplica+" \"ghe-repl-setup "+PrimaryIP+" | grep 'ssh-rsa' \" > replicaKey")
#copy the file to Primary node
os.system("scp -i "+SSHKeyFile+" -P 122 replicaKey admin@"+PrimaryIP+":/home/admin/")
#import the key into Primary node's authentication
os.system(SSHPrimary+" \"ghe-import-authorized-keys < replicaKey\"")

#----- Replica node setup -----
#initail
os.system(SSHReplica+" \"ghe-repl-setup "+PrimaryIP+"\"")
#Reset ssh keygen
os.system("ssh-keygen -R "+ ReplicaIP +"; ssh-keygen -R \"["+ ReplicaIP +"]:122\"")
#Start replica service
os.system(SSHReplica+" \"ghe-repl-start\"")
#Check replica status
os.system(SSHReplica+" \"ghe-repl-status\"")

