#! /usr/local/bin/python3

import boto.cloudformation, os, time

awsRegion = "THE REGION OF AWS"
stackName = "GithubEnterpriseHACluster"
templateUrl = "URL FOR TEMPLATE"
templateParam = [('KeyName', ''), ('VPC', 'VPC-ID'), ('PublicSubnet1', 'SUBNET1-ID'),
                 ('PublicSubnet2', 'SUBNET2-ID')]

def build_stack():
    cfn = boto.cloudformation.connect_to_region(awsRegion)

    # create stack
    create_info = cfn.create_stack(stackName,template_url=templateUrl,parameters=templateParam);

    while True:
        createStat = str(cfn.describe_stack_events(stackName)[0])
        if stackName in createStat and createStat.split(" ")[-1] == "CREATE_COMPLETE":
            print ("the Stack: " + stackName + " is created successfully.")
            break
        else:
            print (createStat)
        time.sleep(3)

    #get the outpue
    stackOutput = cfn.describe_stacks(stackName)[0].outputs

    returnValue = []

    for i in stackOutput:
        if i.key == "PrimaryPrivateIP":
            returnValue.insert(0,str(i.value))
        elif i.key == "ReplicaPrivateIP":
            returnValue.insert(1,str(i.value))
    
    return returnValue


#create cloudformation stack
startBuild = time.time()
IPs = build_stack()

# once the machines started, put the initial setup
startSetup = time.time()
os.system("./ghe_initial_setup.py "+IPs[0]+" "+IPs[1]+" ../enterprise-3.ghl")
endTime = time.time()

print ("---------- time summery --------")
print ("total time          %s sec" % (endTime - startBuild))
print ("stack building time %s sec" % (startSetup - startBuild))
print ("github setup time   %s sec" % (endTime - startSetup))
print ("--------------------------------")
