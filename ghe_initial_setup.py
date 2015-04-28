#! /usr/local/bin/python3

import sys, os

PrimaryIP = sys.argv[1]
ReplicaIP = sys.argv[2]
LicenseFile = sys.argv[3]

SSHKeyFile = "/Users/carol/Carol_key_California.pem"

SSHPrimary = "ssh -i "+SSHKeyFile+" -p 122 admin@"+PrimaryIP
SSHReplica = "ssh -i "+SSHKeyFile+" -p 122 admin@"+ReplicaIP

#----- set hostname ----- 
os.system(SSHReplica + " \"echo '127.0.0.1 ip-" + "-".join(ReplicaIP.split("."))+"' | sudo tee -a /etc/hosts\"")
os.system(SSHReplica + " \"echo '"+PrimaryIP+" ip-" + "-".join(PrimaryIP.split("."))+"' | sudo tee -a /etc/hosts\"")
os.system(SSHPrimary + " \"echo '127.0.0.1 ip-" + "-".join(PrimaryIP.split("."))+"' | sudo tee -a /etc/hosts\"")
os.system(SSHPrimary + " \"echo '"+ReplicaIP+" ip-" + "-".join(ReplicaIP.split("."))+"' | sudo tee -a /etc/hosts\"")

#----- start github service on primary node -----
#import license, set configuration password, and apply setting
os.system("cat "+LicenseFile+" | "+SSHPrimary+" -- ghe-import-license")
os.system(SSHPrimary+" \"ghe-set-password\"")
os.system(SSHPrimary+" \"ghe-ssl-certificate-setup -r")
os.system(SSHPrimary+" \"ghe-config-apply\"")

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
#Start replica service
os.system(SSHReplica+" \"ghe-repl-start\"")
#Check replica status
os.system(SSHReplica+" \"ghe-repl-status\"")
