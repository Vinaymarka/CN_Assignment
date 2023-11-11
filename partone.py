from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class NetworkTopology(Topo):
    "A triangular topology with three routers, six switches, and two hosts per switch"

    def build(self, **_opts):
        # Adding routers
        router1 = self.addNode('R1', cls=LinuxRouter, ip='10.0.1.254')
        router2 = self.addNode('R2', cls=LinuxRouter, ip='10.0.2.254')
        router3 = self.addNode('R3', cls=LinuxRouter, ip='10.0.3.254')

        # Adding switches
        S1, S2, S3, S4, S5, S6 = [self.addSwitch(s) for s in ('S1', 'S2', 'S3', 'S4', 'S5', 'S6')]
        # Adding links between routers and switches
        self.addLink(S1, router1, intfName2='R1-eth1', params2={'ip': '10.0.1.254/24'})
  
        self.addLink(S2, router2, intfName2='R2-eth1', params2={'ip': '10.0.2.254/24'})
       
        self.addLink(S3, router3, intfName2='R3-eth1', params2={'ip': '10.0.3.254/24'})
        
        #setting up hosts and assigning IP adresses to them            
        host1 = self.addHost('H1', ip='10.0.1.1/24', defaultRoute='via 10.0.1.254')
        host2 = self.addHost('H2', ip='10.0.1.2/24', defaultRoute='via 10.0.1.254')
        host3 = self.addHost('H3', ip='10.0.2.1/24', defaultRoute='via 10.0.2.254')
        host4 = self.addHost('H4', ip='10.0.2.2/24', defaultRoute='via 10.0.2.254')
        host5 = self.addHost('H5', ip='10.0.3.1/24', defaultRoute='via 10.0.3.254')
        host6 = self.addHost('H6', ip='10.0.3.2/24', defaultRoute='via 10.0.3.254')

        # Links between routers via switches
        self.addLink(S4, router1, intfName2='R1-eth2', params2={'ip': '10.0.4.1/24'})
        self.addLink(S4, router2, intfName2='R2-eth2', params2={'ip': '10.0.4.2/24'})
        self.addLink(S5, router2, intfName2='R2-eth3', params2={'ip': '10.0.5.1/24'})
        self.addLink(S5, router3, intfName2='R3-eth2', params2={'ip': '10.0.5.2/24'})
        self.addLink(S6, router1, intfName2='R1-eth3', params2={'ip': '10.0.6.1/24'})
        self.addLink(S6, router3, intfName2='R3-eth3', params2={'ip': '10.0.6.2/24'})
        

        # Adding links between hosts and switches
        self.addLink(host1, S1)
        self.addLink(host2, S1)
        self.addLink(host3, S2)
        self.addLink(host4, S2)
        self.addLink(host5, S3)
        self.addLink(host6, S3)
        


        

def run():
    "Testing the triangular topology"
    topo = NetworkTopology()
    net = Mininet(topo=topo, waitConnected=True)
    net.start()
    net['H1'].cmd('ip route add default via 10.0.1.1 nexthop via 10.0.4.2 nexthop via 10.0.5.2 nexthop via 10.0.6.2')
    
    router1 = net['R1']
    router2 = net['R2']
    router3 = net['R3']
    #setting up the routes for R1, R2 and R3. 
    router1.cmd('ip route add 10.0.2.0/24 via 10.0.4.2')
    router1.cmd('ip route add 10.0.3.0/24 via 10.0.6.2')
 
    
    router2.cmd('ip route add 10.0.1.0/24 via 10.0.4.1')
    router2.cmd('ip route add 10.0.3.0/24 via 10.0.5.2')

    router3.cmd('ip route add 10.0.1.0/24 via 10.0.6.1')
    router3.cmd('ip route add 10.0.2.0/24 via 10.0.5.1')
   
    '''net['R1'].popen('tcpdump -i any -w R1.pcap')
    net.pingAll() '''#This is used to capture packets across routers R1 . 
    #This prints all the routing tables for R1, R2 and R3 via all the interfaces. 
    
   
    '''info('*** Routing Table on R1:\n')
    info(net['R1'].cmd('route'))
    info('*** Routing Table on R2:\n')
    info(net['R2'].cmd('route'))
    info('*** Routing Table on R3:\n')
    info(net['R3'].cmd('route'))
    # Start a CLI to interact with the network''' #commenting as route tables ar e not needed. 
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
