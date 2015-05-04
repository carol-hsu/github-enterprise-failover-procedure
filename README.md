#Github Enterprise Failover Procedure
- github-ha.json: the AWS CloudFormation template for building up two-node cluster of Github enterprise
- other python files: for setup and failover procedure automatically 

##ghe_initial_setup.py
usage: $ ./ghe_initial_setup PRIMARY_IP REPLICA_IP ENTERPRISE_LICENSE_PATH

##ghe_replica_setup.py
usage: $ ./ghe_replica_setup PRIMARY_IP REPLICA_IP

##ghe_replica_to_primary.py
usage: $ ./ghe_replica_to_primary.py REPLICA_IP