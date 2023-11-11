# CN_Assignment
It contains codes from the CN Assignment 
TEAM MEMBERS - Vinay Goud    Roll number - 21110125
               Sujith Katlagunta Roll number- 21110100
''''
Deatails about how to run partone.py 

This is a simple Mininet script that sets up a triangular network topology with three routers, six switches, and two hosts per switch. The routers are LinuxRouter nodes with IP forwarding enabled.

Instructions to Run the Code:-
->Ensure you have Mininet installed. If not, you can install it by following the instructions on the Mininet website: http://mininet.org/download/

->Save the provided code in a file, for example, triangular_topology.py.

->Open a terminal and navigate to the directory containing the script.

Run the script using the following command:

sudo python pythonone.py
The script will start Mininet and create the specified network topology.

After Mininet starts, you will be presented with the Mininet CLI prompt. In the CLI, you can interact with the network.

Modifying Default Routes
In the provided script, the default route for packets from H1 to H6 is set to go through routers R1, R4, R2, R5, and R3. If you want to change the route, you can modify the defaultRoute parameter for H1 in the build method of the NetworkTopology class.

For example, to change the route to go through R1 -> R2 -> R3, you can modify the line for H1 as follows:

host1 = self.addHost('H1', ip='10.0.1.1/24', defaultRoute='via 10.0.4.2 nexthop via 10.0.5.2 nexthop via 10.0.6.2')
Adjust the IP addresses according to your specific network topology.

Viewing Routing Tables
If you want to view the routing tables for the routers (R1, R2, R3), you can uncomment the relevant lines in the run method.

Exiting Mininet
To exit Mininet, simply type exit in the Mininet CLI.
''''


''''
Details about how to run parttwo.py
Same process goes for parttwo.py

