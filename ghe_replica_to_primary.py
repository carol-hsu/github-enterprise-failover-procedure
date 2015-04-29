#! /usr/local/bin/python3

import sys, os, time

ReplicaIP = sys.argv[1]
SSHKeyFile="/Users/carol/Carol_key_California.pem"

#wait 30 seconds
#time.sleep(30)


#verify the status of replica node is fine
statusOK = "N"
while not (statusOK == "y" or statusOK == "Y" or statusOK==""):
	os.system("ssh -i " + SSHKeyFile + " -p 122 admin@" + ReplicaIP + " \"ghe-repl-status\"")
	statusOK = input("continue? (y/Y)")

#change replica node to be primary
os.system("ssh -i " + SSHKeyFile + " -p 122 admin@" + ReplicaIP + " \"ghe-repl-promote\"")
