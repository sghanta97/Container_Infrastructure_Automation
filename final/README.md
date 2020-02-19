To create the required topology, the user should mention the requirements in "input.csv" in the format shown below:  
![container](https://user-images.githubusercontent.com/43893989/74791112-94e01f00-5287-11ea-9e9b-d31abe24bf0a.PNG)  

#input file  
CS1,CS5,VXLAN  
CS3,CS4,Bridge    
CS2,CS3,GRE  

Shown above is the input file for the Sample configuration. 

First the user should run the setup script, It will create the basic topology.  
python intialsetup.py  
Then the tunnel_configure script can be run to create the required tunneling.  
python tunnel_configure.py  
