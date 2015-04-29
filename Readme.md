# Github Enterprise Failover Procedure

## github_ha.json
- the AWS CloudFormation template
- to build two-node infrastructure: primary node and replica node; two EIPs for instances; an ELB for healthchecking primary node and as DNS provider; two security groups for Github Enterprise nodes and ELB.

## ghe_ initial_setup.py

## ghe_ replica_setup.py

## ghe_replica _to _primary.py