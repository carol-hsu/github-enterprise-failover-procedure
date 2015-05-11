#! /usr/local/bin/python3

import boto.ec2, os, time

awsRegion = "us-west-1"

#get the IP from /etc/hosts
hostfile = open('/etc/hosts','r')

PrimaryIP = ""
ReplicaIP = ""

for line in hostfile.readlines():
    if "github.dcs.trend.com" in line:
        PrimaryIP = line.split(" ")[0]
    elif "github.replica.com" in line:
        ReplicaIP = line.split(" ")[0]

hostfile.close()


startResuming = time.time()
#start replica node
ec2 = boto.ec2.connect_to_region(awsRegion)
instList = ec2.get_only_instances()
for inst in instList:
    if inst.private_ip_address == ReplicaIP:
        ec2.start_instances(inst.id)
        break

startReplicaSetup = time.time()
#resuming replica
os.system("./ghe_replica_setup.py "+PrimaryIP+" "+ReplicaIP)

endResume = time.time()

print ("---------- time summery --------")
print ("total time          %s" % ( endResume - startResuming ))
print ("reboot replica node %s" % ( startReplicaSetup - startResuming ))
print ("replica setup       %s" % ( endResume - startReplicaSetup))
print ("--------------------------------")
