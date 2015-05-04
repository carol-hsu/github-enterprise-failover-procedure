#! /usr/local/bin/python3

import sys, os, time

ReplicaIP = sys.argv[1]
SSHKeyFile="/Users/carol/Carol_key_California.pem"


#change replica node to be primary
os.system("ssh -i " + SSHKeyFile + " -p 122 admin@" + ReplicaIP + " \"ghe-repl-promote\"")
