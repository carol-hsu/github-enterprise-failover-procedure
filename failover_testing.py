#! /usr/local/bin/python3

import boto.ec2, os, time

awsRegion = "us-west-1"

#get the IP from /etc/hosts, and write a new one for later-on exchange roles
hostfile = open('/etc/hosts','r')
newfile = open('./hosts','w')

PrimaryIP = ""
ReplicaIP = ""

for line in hostfile.readlines():
    if "github.dcs.trend.com" in line:
        PrimaryIP = line.split(" ")[0]
    elif "github.replica.com" in line:
        ReplicaIP = line.split(" ")[0]
    else:
        newfile.write(line)

newfile.write(ReplicaIP+" github.dcs.trend.com\n")
newfile.write(PrimaryIP+" github.replica.com\n")

hostfile.close()
newfile.close()


#stop primary node
ec2 = boto.ec2.connect_to_region(awsRegion)
instList = ec2.get_only_instances()
for inst in instList:
    if inst.private_ip_address == PrimaryIP:
        ec2.stop_instances(inst.id)
        break

startFailover = time.time()
#replica node promoting
os.system("./ghe_replica_to_primary.py "+ReplicaIP)

print ("replica take place to primary   %s" % ( time.time() - startFailover ))

#exchange the hostname
os.system("sudo mv hosts /etc/hosts")
