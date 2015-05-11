#! /usr/local/bin/python3

import sys, os, time

PrimaryIP = sys.argv[1]
ReplicaIP = sys.argv[2]

SSHKeyFile = "/Users/carol/Carol_key_California.pem"

SSHPrimary = "ssh -o \"StrictHostKeyChecking no\" -i "+SSHKeyFile+" -p 122 admin@"+PrimaryIP
SSHReplica = "ssh -o \"StrictHostKeyChecking no\" -i "+SSHKeyFile+" -p 122 admin@"+ReplicaIP

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
os.system(SSHReplica+" \"ghe-repl-status\" > repl-status")

while True:
	checkStatus = open('repl-status','r')
	countOK=0
	for line in checkStatus.readlines():
		if "OK" in line:
			countOK += 1
	if countOK >= 4 :
		break
	else:
		os.system(SSHReplica+" \"ghe-repl-stop\"")
		os.system(SSHReplica+" \"ghe-repl-teardown\"")
		os.system(SSHReplica+" \"ghe-repl-setup "+PrimaryIP+"\"")
		os.system("ssh-keygen -R "+ ReplicaIP +"; ssh-keygen -R \"["+ ReplicaIP +"]:122\"")
		os.system(SSHReplica+" \"ghe-repl-start\"")
		os.system(SSHReplica+" \"ghe-repl-status\" > repl-status")

print ("replica node setup successfully")



