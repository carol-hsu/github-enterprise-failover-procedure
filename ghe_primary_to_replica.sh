#! /bin/bash

ReplicaIP=$1

SSHKeyFile="/Users/carol/Carol_key_California.pem"

ReplicaOK=""


function VerifyStatus {
	VerifyOK=$(ssh -i $SSHKeyFile -p 122 admin@$ReplicaIP "ghe-repl-status -vv" | grep "OK:" | wc -l)
	if ( $VerifyOK = "4"){
		ReplicaOK="1"
	}else{
		ReplicaOK="0"
	}
}

#wait 30 seconds
sleep 3

#verify the status of replica node is fine
VerifyStatus

#change replica node to be primary

ssh -i $SSHKeyFile -p 122 admin@$ReplicaIP "ghe-repl-promote"


