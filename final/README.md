To create the required topology, the user should mention the requirements in "input.csv" in the format shown below:  
#input file  
CS3,CS4,VXLAN  
CS5,CS6,Bridge  
CS7,CS8,L3  
CS8,CS9,GRE  
First the user should run the setup script, It will create the basic topology.  
python intialsetup.py  
Then the container_deploy script can be run to create the required topology.  
python container_deploy.py  
