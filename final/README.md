To create the required topology, the user should mention the requirements in "input.csv" in the format shown below:  
#input file  
CS3,CS4,VXLAN  
CS5,CS6,Bridge  
CS7,CS8,L3  
CS8,CS9,GRE  

Shown above is a Sample configuration for 
![container](https://user-images.githubusercontent.com/43893989/74791112-94e01f00-5287-11ea-9e9b-d31abe24bf0a.PNG)

First the user should run the setup script, It will create the basic topology.  
python intialsetup.py  
Then the tunnel_configure script can be run to create the required tunneling.  
python tunnel_configure.py  
