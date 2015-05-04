#! /usr/local/bin/python3

import sys, os

PrimaryIP = sys.argv[1]
ReplicaIP = sys.argv[2]
LicenseFile = sys.argv[3]

Hostname = "github.dcs.trend.com"
SSHKeyFile = "/Users/carol/Carol_key_California.pem"

SSHPrimary = "ssh -i "+SSHKeyFile+" -p 122 admin@"+PrimaryIP
SSHReplica = "ssh -i "+SSHKeyFile+" -p 122 admin@"+ReplicaIP

#----- set hostname ----- 
os.system(SSHReplica + " \"echo '127.0.0.1 ip-" + "-".join(ReplicaIP.split("."))+"' | sudo tee -a /etc/hosts\"")
os.system(SSHReplica + " \"echo '"+PrimaryIP+" ip-" + "-".join(PrimaryIP.split("."))+"' | sudo tee -a /etc/hosts\"")
os.system(SSHPrimary + " \"echo '127.0.0.1 ip-" + "-".join(PrimaryIP.split("."))+"' | sudo tee -a /etc/hosts\"")
os.system(SSHPrimary + " \"echo '"+ReplicaIP+" ip-" + "-".join(ReplicaIP.split("."))+"' | sudo tee -a /etc/hosts\"")

#----- change ghe-repl-stop ----
ReplaceCommand1 = " \"sudo sed -i '61a if [ \$force = 1 ]; then\\n ensure_replica\\n sudo service openvpn stop 1>/dev/null\\nelse' /usr/local/bin/ghe-repl-stop\""
os.system(SSHPrimary + ReplaceCommand1)
os.system(SSHReplica + ReplaceCommand1)
ReplaceCommand2 = " \"sudo sed -i '66a fi' /usr/local/bin/ghe-repl-stop\""
os.system(SSHPrimary + ReplaceCommand2)
os.system(SSHReplica + ReplaceCommand2)


#----- start github service on primary node -----
#import license, set configuration password, and apply setting
os.system("cat "+LicenseFile+" | "+SSHPrimary+" -- ghe-import-license")
os.system(SSHPrimary+" \"ghe-set-password\"")
os.system(SSHPrimary+" \"openssl x509 -fingerprint -in /etc/haproxy/ssl.crt -noout\"")
os.system(SSHPrimary+" \"ghe-ssl-certificate-setup -r\"")

#os.system(SSHPrimary+" \"ghe-config-apply\"")
###Wait for screen click
status = "N"
while not (status == "y" or status == "Y" or status==""):
	status = input("Clicked Save Setting? (y/Y)")


ReplaceHostname1 = " \"sudo sed -i '6c \    \\\"github_hostname\\\":\\\""+Hostname+"\\\",' /data/user/common/dna.json\""
ReplaceHostname2 = " \"sudo sed -i '81c \      \\\"noreply_address\\\":\\\"norepy@"+Hostname+"\\\"' /data/user/common/dna.json\""
os.system(SSHPrimary + ReplaceHostname1)
os.system(SSHPrimary + ReplaceHostname2)

os.system("./ghe_replica_setup.py "+PrimaryIP+" "+ReplicaIP)


