import os
import sys

# run the docker file
path=os.getcwd()
os.system("sudo docker build "+path+" -t new")
print("docker build successfull")
#create containers
os.system("sudo docker create --name LC1 -it new:latest")
os.system("sudo docker create --name LC2 -it new:latest")
os.system("sudo docker create --name SC1 -it new:latest")
os.system("sudo docker create --name SC2 -it new:latest")
print("containers successfully created")
####### not ubuntu create your own container

#start containers
os.system("sudo docker start SC1")
os.system("sudo docker start SC2")
os.system("sudo docker start LC1")
os.system("sudo docker start LC2")
print("containers started successfully")

#create veth pairs
os.system("sudo ip link add name v1 type veth peer name v2")
os.system("sudo ip link add name v3 type veth peer name v4")
os.system("sudo ip link add name v5 type veth peer name v6")
os.system("sudo ip link add name v7 type veth peer name v8")
print("veth pairs created for basic setup")
# get container id
SC1id="$(sudo docker inspect -f '{{."+"State.Pid"+"}}' SC1)"
SC2id="$(sudo docker inspect -f '{{."+"State.Pid"+"}}' SC2)"
LC1id="$(sudo docker inspect -f '{{."+"State.Pid"+"}}' LC1)"
LC2id="$(sudo docker inspect -f '{{."+"State.Pid"+"}}' LC2)"
print("successfully collected container id")
# attach veth pair to conatiners
os.system("sudo ip link set dev v1 netns "+SC1id)
os.system("sudo ip link set dev v5 netns "+SC1id)
os.system("sudo ip link set dev v3 netns "+LC1id)
os.system("sudo ip link set dev v2 netns "+LC1id)
os.system("sudo ip link set dev v4 netns "+SC2id)
os.system("sudo ip link set dev v8 netns "+SC2id)
os.system("sudo ip link set dev v6 netns "+LC2id)
os.system("sudo ip link set dev v7 netns "+LC2id)
print("attached veth pairs to containers")
#set interfaces up
os.system("sudo nsenter -t "+SC1id+" -n ip link set v1 up")
os.system("sudo nsenter -t "+SC1id+" -n ip link set v5 up")
os.system("sudo nsenter -t "+LC1id+" -n ip link set v2 up")
os.system("sudo nsenter -t "+LC1id+" -n ip link set v3 up")
os.system("sudo nsenter -t "+LC2id+" -n ip link set v6 up")
os.system("sudo nsenter -t "+LC2id+" -n ip link set v7 up")
os.system("sudo nsenter -t "+SC2id+" -n ip link set v4 up")
os.system("sudo nsenter -t "+SC2id+" -n ip link set v8 up")
print("set interfaces up")

#giving ip address
os.system("sudo nsenter -t "+LC1id+" -n ip addr add 10.1.0.1/24 dev v2")
os.system("sudo nsenter -t "+LC1id+" -n ip addr add 10.3.0.1/24 dev v3")
os.system("sudo nsenter -t "+SC1id+" -n ip addr add 10.1.0.2/24 dev v1")
os.system("sudo nsenter -t "+SC1id+" -n ip addr add 10.2.0.2/24 dev v5")
os.system("sudo nsenter -t "+SC2id+" -n ip addr add 10.3.0.2/24 dev v4")
os.system("sudo nsenter -t "+SC2id+" -n ip addr add 10.4.0.2/24 dev v8")
os.system("sudo nsenter -t "+LC2id+" -n ip addr add 10.2.0.1/24 dev v6")
os.system("sudo nsenter -t "+LC2id+" -n ip addr add 10.4.0.1/24 dev v7")
print("assigned ip addresses to containers")
#creating GRE tunnels
os.system("sudo nsenter -t "+LC1id+" -n ip tunnel add gretun1 mode gre local 10.1.0.1 remote 10.2.0.1")
os.system("sudo nsenter -t "+LC1id+" -n ip link set dev gretun1 up") 
os.system("sudo nsenter -t "+LC2id+" -n ip tunnel add gretun1 mode gre local 10.2.0.1 remote 10.1.0.1")
os.system("sudo nsenter -t "+LC2id+" -n ip link set dev gretun1 up")
print("created Gre infrastructure")
#add underlay routes in LC1 and LC2 for GRE
os.system("sudo nsenter -t "+LC1id+" -n ip route add 10.2.0.0/24 dev v2")
os.system("sudo nsenter -t "+LC2id+" -n ip route add 10.1.0.0/24 dev v6")
print("added underlay routes")
#add routes for GRE
os.system("sudo nsenter -t "+LC1id+" -n ip route add 11.1.0.0/24 dev gretun1")
os.system("sudo nsenter -t "+LC2id+" -n ip route add 12.1.0.0/24 dev gretun1")
print("added GRE ")

### configuring Lower part of infrastructure

# create Namespace
os.system("sudo ip netns add ns1")
os.system("sudo ip netns add ns2")
print("created Namespaces")
#creating veth pairs
os.system("sudo ip link add name v9 type veth peer name v10")
os.system("sudo ip link add name v15 type veth peer name v16")
os.system("sudo ip link add name v17 type veth peer name v18")
os.system("sudo ip link add name v11 type veth peer name v12")
os.system("sudo ip link add name v13 type veth peer name v14")
print("created veth pairs")
#add veth pairs to conatainers
os.system("sudo ip link set dev v9 netns "+LC1id)
os.system("sudo ip link set dev v10 netns ns1")
os.system("sudo ip link set dev v16 netns ns1")
os.system("sudo ip link set dev v15 netns "+LC1id)
os.system("sudo ip link set dev v17 netns "+LC2id)
os.system("sudo ip link set dev v11 netns "+LC2id)
os.system("sudo ip link set dev v13 netns "+LC2id)
os.system("sudo ip link set dev v14 netns ns2")
os.system("sudo ip link set dev v18 netns ns2")
print("add veth pair to Namespace")
# setting veth pair up and adding ip 
os.system("sudo nsenter -t "+LC1id+" -n ip link set v9 up")
os.system("sudo nsenter -t "+LC1id+" -n ip link set v15 up")
os.system("sudo nsenter -t "+LC1id+" -n ip addr add 13.1.0.1/24 dev v15")
#os.system("sudo nsenter -t "+LC1id+" -n ip addr add 12.1.0.3/24 dev v9")
os.system("sudo ip netns exec ns1 ip link set v10 up")
os.system("sudo ip netns exec ns1 ip link set v16 up")
os.system("sudo ip netns exec ns1 ip addr add 13.1.0.2/24 dev v16")
os.system("sudo nsenter -t "+LC2id+" -n ip link set v11 up")
os.system("sudo nsenter -t "+LC2id+" -n ip link set v13 up")
os.system("sudo nsenter -t "+LC2id+" -n ip link set v17 up")
os.system("sudo nsenter -t "+LC2id+" -n ip addr add 11.1.0.1/24 dev v11")
os.system("sudo nsenter -t "+LC2id+" -n ip addr add 14.1.0.1/24 dev v17")
os.system("sudo ip netns exec ns2 ip link set v14 up")
os.system("sudo ip netns exec ns2 ip link set v18 up")
os.system("sudo ip netns exec ns2 ip addr add 14.1.0.2/24 dev v18")
os.system("sudo ip link set v12 up")
print("add ip to veth pair and setting it up")

# create bridges
os.system("sudo ip netns exec ns2 brctl addbr br3")
os.system("sudo ip netns exec ns2 brctl addif br3 v14")
os.system("sudo ip netns exec ns1 brctl addbr br1")
os.system("sudo ip netns exec ns1 brctl addif br1 v10")
os.system("sudo brctl addbr br2")
os.system("sudo ip netns exec ns1 ip link set dev br1 up")
os.system("sudo ip netns exec ns2 ip link set dev br3 up")
os.system("sudo ip link set dev br2 up")
os.system("sudo brctl addif br2 v12")
print("Bridges created")

# create Vxlan
os.system("sudo ip netns exec ns1 ip link add name vxlan0 type vxlan id 42 dev v16 remote 14.1.0.2 dstport 4789")
os.system("sudo ip netns exec ns1 ip link set dev vxlan0 up")
os.system("sudo ip netns exec ns1 brctl addif br1 vxlan0")

os.system("sudo ip netns exec ns2 ip link add name vxlan0 type vxlan id 42 dev v18 remote 13.1.0.2 dstport 4789")
os.system("sudo ip netns exec ns2 ip link set dev vxlan0 up")
os.system("sudo ip netns exec ns2 brctl addif br3 vxlan0")
print("Vxlan created")

# routes for Vxlan
os.system("sudo nsenter -t "+LC1id+" -n ip route add 14.1.0.0/24 dev v2")
os.system("sudo nsenter -t "+LC2id+" -n ip route add 13.1.0.0/24 dev v6")
os.system("sudo nsenter -t "+SC1id+" -n ip route add 13.1.0.0/24 dev v1")
os.system("sudo nsenter -t "+SC1id+" -n ip route add 14.1.0.0/24 dev v5")
print("routes added to enable Vxlan")

# required setup
os.system("sudo ip netns exec ns1 ip route add 12.1.0.0/24 dev br1")
os.system("sudo ip netns exec ns1 ip route add default via 13.1.0.1")
os.system("sudo ip netns exec ns1 echo 1 > /proc/sys/net/ipv4/ip_forward")
os.system("sudo ip netns exec ns1 echo 1 > /proc/sys/net/ipv4/conf/all/proxy_arp")

os.system("sudo ip netns exec ns2 ip route add 12.1.0.0/24 dev br3")
os.system("sudo ip netns exec ns2 ip route add default via 14.1.0.1")
os.system("sudo ip netns exec ns2 echo 1 > /proc/sys/net/ipv4/ip_forward")
os.system("sudo ip netns exec ns2 echo 1 > /proc/sys/net/ipv4/conf/all/proxy_arp")
print("proxy arp and ip forwarding enabled in namespaces")
#for each container:
#create a veth pair
#give ip to container
# add default route in each container
