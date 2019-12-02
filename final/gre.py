# for adding containers in gre network
import os
import sys
import random
cont1=sys.argv[1]
cont2=sys.argv[2]
print(cont1)
print(cont2)
#cont1

v1=random.randrange(30, 9999, 1)
v2=random.randrange(30, 9999, 1)
print(v1)
print(v2)
os.system("sudo ip link add name v"+str(v1)+" type veth peer name v"+str(v2))
os.system("sudo docker create --name "+cont1+" -it new:latest")
os.system("sudo docker start "+cont1)
print("1")
cont1id="$(sudo docker inspect -f '{{."+"State.Pid"+"}}' "+cont1+")"
os.system("sudo ip link set dev v"+str(v1)+" netns ns1")
print("2")
os.system("sudo ip link set dev v"+str(v2)+" netns "+cont1id)
os.system("sudo nsenter -t "+cont1id+" -n ip link set v"+str(v2)+" up")
os.system("sudo ip netns exec ns1 ip link set v"+str(v1)+" up")
os.system("sudo ip netns exec ns1 brctl addif br1 v"+str(v1))
print("3")
#ip
ip1=random.randrange(2, 250, 1)
os.system("sudo nsenter -t "+cont1id+" -n ip addr add 12.1.0."+str(ip1)+"/24 dev v"+str(v2))
print("4")
#route
os.system("sudo nsenter -t "+cont1id+" -n ip route del default via 172.17.0.1 dev eth0")
os.system("sudo nsenter -t "+cont1id+" -n ip route add default dev v"+str(v2))
print("5")

#cont2
v1=random.randrange(30, 9999, 1)
v2=random.randrange(30, 9999, 1)
print(v1)
print(v2)
os.system("sudo ip link add name v"+str(v1)+" type veth peer name v"+str(v2))
os.system("sudo docker create --name "+cont2+" -it new:latest")
os.system("sudo docker start "+cont2)
print("1")
cont2id="$(sudo docker inspect -f '{{."+"State.Pid"+"}}' "+cont2+")"
os.system("sudo ip link set dev v"+str(v2)+" netns "+cont2id)
os.system("sudo nsenter -t "+cont2id+" -n ip link set v"+str(v2)+" up")
os.system("sudo ip link set v"+str(v1)+" up")
os.system("sudo brctl addif br2 v"+str(v1))
print("2")
# ip
ip1=random.randrange(2, 250, 1)
os.system("sudo nsenter -t "+cont2id+" -n ip addr add 11.1.0."+str(ip1)+"/24 dev v"+str(v2))
print("4")
#route
os.system("sudo nsenter -t "+cont2id+" -n ip route del default via 172.17.0.1 dev eth0")
os.system("sudo nsenter -t "+cont2id+" -n ip route add default dev v"+str(v2))
print("5")


