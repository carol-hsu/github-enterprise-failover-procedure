# Github Enterprise Failover Procedure

## github_ha.json
- the AWS CloudFormation template
- to build two-node infrastructure: primary node and replica node; two EIPs for instances; an ELB for healthchecking primary node and as DNS provider; two security groups for Github Enterprise nodes and ELB.

## ghe_initial_setup.py
usage: ./ghe_initial_setup.py PRIMARY-IP REPLICA-IP ENTERPRICE-LISENCE


## ghe_replica_setup.py
usage: ./ghe_replica_setup.py PRIMARY-IP REPLICA-IP

## ghe_replica_to_primary.py
usage: ./ghe_replica_to_primary.py REPLICA-IP


