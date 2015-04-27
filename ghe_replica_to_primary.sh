#! /bin/bash

ReplicaIP=$1

SSHKeyFile="/Users/carol/Carol_key_California.pem"

ReplicaOK=""


function VerifyStatus {
	VerifyOK=$(ssh -i $SSHKeyFile -p 122 admin@$ReplicaIP "ghe-repl-status" | grep "OK:" | wc -l)
	if [ $VerifyOK = "3" ]; then
		ReplicaOK="1"
	else
		ReplicaOK="0"
	fi
}

#wait 30 seconds
sleep 3

#verify the status of replica node is fine
VerifyStatus

#change replica node to be primary
if [ $ReplicaOK = "1" ]; then
	ssh -i $SSHKeyFile -p 122 admin@$ReplicaIP "ghe-repl-promote"
fi

