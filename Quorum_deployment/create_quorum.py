import sys, os, pprint
from builtins import enumerate
import boto3
import time
import paramiko
import numpy
from scp import SCPClient

with open("/home/user/PycharmProjects/SBHACK/automation_script.sh", 'r') as content_file:
    user_data = content_file.read()
vm_count = 4
session = boto3.Session(profile_name='default')
ec2 = session.resource('ec2', 'eu-central-1')
ec2_instances = ec2.create_instances(
    ImageId='ami-090f10efc254eaf55',
    MinCount=vm_count,
    MaxCount=vm_count,
    InstanceType='t2.medium',
    KeyName='SBHACK',
    NetworkInterfaces=[
         {
              'SubnetId': 'subnet-3e00c054',
               'AssociatePublicIpAddress': True,
               'DeviceIndex': 0,
               'Groups': [
                   'sg-0fe26f4043de1cdd5',
               ],
         }
       ],
    BlockDeviceMappings=[
             {
               "DeviceName": "/dev/sda1",
                  "Ebs": {
                     "VolumeSize": 20
                   }
             }
          ],
    UserData=user_data,
    TagSpecifications=[
         {
            'ResourceType': "instance",
               'Tags': [
                 {
                       'Key': 'Creator',
                       'Value': 'vecon'
                  },
                  {
                       'Key': 'Name',
                       'Value': 'Quorum_private_test_JS'
                   },
               ]
         },
    ],
)

print(f"Initiated the start of {vm_count} machines.")
pub_ips = []
priv_ips = []
print("Waiting until all VMs are up...")
for i in ec2_instances:
    i.wait_until_running()
    i.load()
    # print(f"ID: {i.id}, State: {i.state['Name']}, private IP: {i.private_ip_address}, public IP: {i.public_ip_address}")
    pub_ips.append(i.public_ip_address)
    priv_ips.append(i.private_ip_address)
    print(f"You can now access machine {i} via ssh -i ~/.aws/hackathon.pem ubuntu@{i.public_ip_address}")

print("Waiting 60 seconds before creating ssh connection to VMs")

time.sleep(60)
ssh_clients = []
scp_clients = []
ssh_key_priv = paramiko.RSAKey.from_private_key_file('/home/user/.aws/hackathon.pem')

addresses = []
enodes = []

for index, ip in enumerate(pub_ips):
    ssh_clients.append(paramiko.SSHClient())
    ssh_clients[index].set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_clients[index].connect(hostname=ip, username='ubuntu', pkey=ssh_key_priv)
    scp_clients.append(SCPClient(ssh_clients[index].get_transport()))

print("Waiting for all VMs to finish the userData setup...")
timer = 0
status_flags = numpy.zeros(vm_count, dtype=bool)
while (False in status_flags and timer < 120):
    time.sleep(10)
    timer += 1
    print(f"Waited {timer * 10} seconds so far, {1200 - timer * 10} seconds left before abort (it usually takes around 2 minutes)")
    for index, i in enumerate(ec2_instances):

        if (status_flags[index] == False):

            sftp = ssh_clients[index].open_sftp()
            try:
                sftp.stat('/var/log/user_data_success.log')
                status_flags[index] = True
                print(f"{pub_ips[index]} is ready")
            except IOError:
                print(f"{pub_ips[index]} not ready")

if (False in status_flags):
    print('Boot up NOT successful')
    print(f"Failed VMs: {[pub_ips[x] for x in numpy.where(status_flags != True)]}")
else:
    print(f"Boot up of all VMs was successful, waited {timer*10} seconds")
    print("Running specific startup")

    for index1, _ in enumerate(pub_ips):

        stdin, stdout, stderr = ssh_clients[index1].exec_command("sudo cp /home/ubuntu/quorum/build/bin/geth /home/ubuntu/quorum/build/bin/bootnode /usr/local/bin")
        print(stdout.readlines())
        print(stderr.readlines())

        stdin, stdout, stderr = ssh_clients[index1].exec_command("mkdir /home/ubuntu/nodes")
        print(stdout.readlines())
        print(stderr.readlines())

        stdin, stdout, stderr = ssh_clients[index1].exec_command("echo 'user' > /home/ubuntu/nodes/pwd")
        print(stdout.readlines())
        print(stderr.readlines())

        stdin, stdout, stderr = ssh_clients[index1].exec_command("geth --password /home/ubuntu/nodes/pwd --datadir /home/ubuntu/nodes/new-node-1 account new")
        out = stdout.readlines()
        addresses.append(out[0].replace("Address: ", "").replace("{", "").replace("}\n", ""))
        print(out)
        print(stderr.readlines())

        stdin, stdout, stderr = ssh_clients[index1].exec_command("sed -i -e 's/substitute_address/'" + f"'{addresses[0]}'" + "'/g' /home/ubuntu/genesis_raw.json")
        print(stdout.readlines())
        print(stderr.readlines())

        stdin, stdout, stderr = ssh_clients[index1].exec_command("cp /home/ubuntu/genesis_raw.json /home/ubuntu/nodes/genesis.json")
        print(stdout.readlines())
        print(stderr.readlines())

        stdin, stdout, stderr = ssh_clients[index1].exec_command("bootnode --genkey=nodekey")
        print(stdout.readlines())
        print(stderr.readlines())

        stdin, stdout, stderr = ssh_clients[index1].exec_command("cp nodekey /home/ubuntu/nodes/new-node-1/nodekey")
        print(stdout.readlines())
        print(stderr.readlines())

        stdin, stdout, stderr = ssh_clients[index1].exec_command("bootnode --nodekey=/home/ubuntu/nodes/new-node-1/nodekey --writeaddress")
        out = stdout.readlines()
        print(out)
        print(stderr.readlines())
        enodes.append(out[0].replace("\n", ""))


        stdin, stdout, stderr = ssh_clients[index1].exec_command("touch /home/ubuntu/nodes/new-node-1/static-nodes.json")
        print(stdout.readlines())
        print(stderr.readlines())

        stdin, stdout, stderr = ssh_clients[index1].exec_command("echo '[' >> /home/ubuntu/nodes/new-node-1/static-nodes.json")
        print(stdout.readlines())
        print(stderr.readlines())

        for index2, _ in enumerate(enodes):
            if (index2 < index1):
                string = "echo '  " + '\"' + "enode://" + f"{enodes[index2]}" + "@" + f"{pub_ips[index2]}" + ":21000?discport=0&raftport=50000,'" + '\\"' + " >> /home/ubuntu/nodes/new-node-1/static-nodes.json"
                stdin, stdout, stderr = ssh_clients[index1].exec_command(string)
                print(stdout.readlines())
                print(stderr.readlines())
            else:
                string = "echo '  " + '\"' + "enode://" + f"{enodes[index2]}" + "@" + f"{pub_ips[index2]}" + ":21000?discport=0&raftport=50000'" + '\\"' + " >> /home/ubuntu/nodes/new-node-1/static-nodes.json"
                stdin, stdout, stderr = ssh_clients[index1].exec_command(string)
                print(stdout.readlines())
                print(stderr.readlines())

        stdin, stdout, stderr = ssh_clients[index1].exec_command("echo ']' >> /home/ubuntu/nodes/new-node-1/static-nodes.json")
        print(stdout.readlines())
        print(stderr.readlines())

        if index1 == 0:
            stdin, stdout, stderr = ssh_clients[0].exec_command("geth --datadir /home/ubuntu/nodes/new-node-1 init /home/ubuntu/nodes/genesis.json")
            print(stdout.readlines())
            print(stderr.readlines())

            channel = ssh_clients[index1].get_transport().open_session()
            channel.exec_command("PRIVATE_CONFIG=ignore nohup geth --datadir /home/ubuntu/nodes/new-node-1 --nodiscover --verbosity 5 --networkid 31337 --raft --raftport 50000 --rpc --rpcaddr 0.0.0.0 --rpccorsdomain '*' --rpcapi admin,db,eth,debug,miner,net,shh,txpool,personal,web3,quorum,raft --emitcheckpoints --port 21000 --nat=extip:" + f"{pub_ips[0]} 2" + ">>/home/ubuntu/nodes/node.log &")
            time.sleep(5)

        else:
            stdin, stdout, stderr = ssh_clients[index1].exec_command("geth --datadir /home/ubuntu/nodes/new-node-1 init /home/ubuntu/nodes/genesis.json")
            print(stdout.readlines())
            print(stderr.readlines())

            stdin, stdout, stderr = ssh_clients[0].exec_command("geth --exec " + '\"' + "raft.addPeer('enode://" + f"{enodes[index1]}" + "@" + f"{pub_ips[index1]}" + ":21000?discport=0&raftport=50000')" + '\"' + " attach /home/ubuntu/nodes/new-node-1/geth.ipc")
            out = stdout.readlines()
            print(out)
            print(stderr.readlines())
            raftID = out[0].replace("\x1b[0m\r\n", "").replace("\x1b[31m", "").replace("\n", "")
            print(f"raftID: {raftID}")

            channel = ssh_clients[index1].get_transport().open_session()
            channel.exec_command(f"PRIVATE_CONFIG=ignore nohup geth --datadir /home/ubuntu/nodes/new-node-1 --nodiscover --verbosity 5 --networkid 31337 --raft --raftport 50000 --raftjoinexisting {raftID} --rpc --rpcaddr 0.0.0.0 --rpccorsdomain '*' --rpcapi admin,db,eth,debug,miner,net,shh,txpool,personal,web3,quorum,raft --emitcheckpoints --port 21000 --nat=extip:{pub_ips[index1]} 2>>/home/ubuntu/nodes/node.log &")
            time.sleep(5)

            stdin, stdout, stderr = ssh_clients[index1].exec_command("geth --exec " + '\"' + "eth.blockNumber" + '\"' + " attach /home/ubuntu/nodes/new-node-1/geth.ipc")
            print(stdout.readlines())
            print(stderr.readlines())

    print("Network started successfully")
    print("Executing basic tests")

    accounts = []

    for index1, _ in enumerate(pub_ips):

        stdin, stdout, stderr = ssh_clients[index1].exec_command("geth --exec " + '\"' + "eth.accounts[0]" + '\"' + " attach /home/ubuntu/nodes/new-node-1/geth.ipc")
        out = stdout.readlines()
        account = out[0].replace('\n', "")
        print(out)
        print(stderr.readlines())
        accounts.append(account)

    for index1, _ in enumerate(pub_ips):

        stdin, stdout, stderr = ssh_clients[index1].exec_command("geth --exec " + "\'" + f'personal.unlockAccount({accounts[index1]}, ' + '\"' + "user" + '\"' + ")" + "\'" + " attach /home/ubuntu/nodes/new-node-1/geth.ipc")
        print(stdout.readlines())
        print(stderr.readlines())

    stdin, stdout, stderr = ssh_clients[0].exec_command("geth --exec " + "\'" + "eth.sendTransaction({" + f'from: {accounts[0]}, ' + f'to: {accounts[1]}, ' + f"value: 200000000" + "})" + "\'" + " attach /home/ubuntu/nodes/new-node-1/geth.ipc")
    print(stdout.readlines())
    print(stderr.readlines())
    time.sleep(5)

    stdin, stdout, stderr = ssh_clients[0].exec_command("geth --exec " + "\'" + "eth.sendTransaction({" + f'from: {accounts[0]}, ' + f'to: {accounts[2]}, ' + f"value: 100000000" + "})" + "\'" + " attach /home/ubuntu/nodes/new-node-1/geth.ipc")
    print(stdout.readlines())
    print(stderr.readlines())
    time.sleep(5)

    stdin, stdout, stderr = ssh_clients[2].exec_command("geth --exec " + "\'" + "eth.sendTransaction({" + f'from: {accounts[2]}, ' + f'to: {accounts[1]}, ' + f"value: 500000" + "})" + "\'" + " attach /home/ubuntu/nodes/new-node-1/geth.ipc")
    print(stdout.readlines())
    print(stderr.readlines())
    time.sleep(5)

    stdin, stdout, stderr = ssh_clients[2].exec_command("geth --exec " + "\'" + "eth.sendTransaction({" + f'from: {accounts[2]}, ' + f'to: {accounts[0]}, ' + f"value: 500000" + "})" + "\'" + " attach /home/ubuntu/nodes/new-node-1/geth.ipc")
    print(stdout.readlines())
    print(stderr.readlines())
    time.sleep(5)

    stdin, stdout, stderr = ssh_clients[2].exec_command("geth --exec " + "\'" + "eth.getBlock(1)" + "\'" + " attach /home/ubuntu/nodes/new-node-1/geth.ipc")
    print(stdout.readlines())
    print(stderr.readlines())

    for index1, _ in enumerate(pub_ips):
        stdin, stdout, stderr = ssh_clients[index1].exec_command("geth --exec " + "\'" + "eth.blockNumber" + "\'" + " attach /home/ubuntu/nodes/new-node-1/geth.ipc")
        print(stdout.readlines())
        print(stderr.readlines())

    for index1, _ in enumerate(pub_ips):
        for index2, _ in enumerate(pub_ips):

            stdin, stdout, stderr = ssh_clients[index2].exec_command("geth --exec " + "\'" + f'eth.getBalance({accounts[index1]})' + "\'" + " attach /home/ubuntu/nodes/new-node-1/geth.ipc")
            print(stdout.readlines())
            print(stderr.readlines())

    print("Tests successfully completed")
    print("Deploying smart contracts")

