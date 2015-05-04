#! /usr/local/bin/python3

import sys, os

PrimaryIP = sys.argv[1]
ReplicaIP = sys.argv[2]
LicenseFile = sys.argv[3]

SSHKeyFile = "/Users/carol/Carol_key_California.pem"

SSHPrimary = "ssh -i "+SSHKeyFile+" -p 122 admin@"+PrimaryIP
SSHReplica = "ssh -i "+SSHKeyFile+" -p 122 admin@"+ReplicaIP



#----- promote the replica node -----

#----- change DNS direction

#----- test the old primary node -----
# if the old primary still dead, create a new replica node to bind new primary node


