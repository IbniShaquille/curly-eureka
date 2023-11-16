from mininet.topo import Topo
from mininet.node import Node  

class LinuxRouter(Node):
    """A Node with IP forwarding enabled."""

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd("sysctl net.ipv4.ip_forward=1")

    def terminate(self):
        self.cmd("sysctl net.ipv4.ip_forward=0")
        super(LinuxRouter, self).terminate()

class MyTopo(Topo):
    def build(self):
        num_switch = 4

        default_gateway_1 = '192.168.223.1/26'
        default_gateway_2 = '192.168.223.65/27'
        default_gateway_3 = '192.168.223.97/28'
        default_gateway_4 = '192.168.223.113/29'

        # Add router
        router_asrama = self.addNode('r0', cls=LinuxRouter, ip='192.168.223.121/30')
        router_RS = self.addNode('r1', cls=LinuxRouter, ip='192.168.223.122/30')

        # Add switch
        switch_koas = self.addSwitch('s1')
        switch_internship = self.addSwitch('s2')
        switch_spesialis = self.addSwitch('s3')
        switch_residen = self.addSwitch('s4')

        # Add link per switch
        self.addLink(switch_koas, router_asrama, intfName2='r0-eth1', params2={'ip': default_gateway_1})
        self.addLink(switch_internship, router_asrama, intfName2='r0-eth2', params2={'ip': default_gateway_2})
        self.addLink(switch_spesialis, router_RS, intfName2='r1-eth1', params2={'ip': default_gateway_3})
        self.addLink(switch_residen, router_RS, intfName2='r1-eth2', params2={'ip': default_gateway_4})

        # Add link between router
        self.addLink(router_asrama, router_RS, intfName1='r0-eth3', intfName2='r1-eth3')

        # Add host
        for i in range(1, 62):
            host = self.addHost(f'h{i}')
            self.addLink(host, switch_koas, intfName2=f's1-eth{i}')

        for i in range(1, 30):
            host = self.addHost(f'h{i+61}')
            self.addLink(host, switch_internship, intfName2=f's2-eth{i}')

        for i in range(1, 14):
            host = self.addHost(f'h{i+90}')
            self.addLink(host, switch_spesialis, intfName2=f's3-eth{i}')

        for i in range(1, 6):
            host = self.addHost(f'h{i+103}')
            self.addLink(host, switch_residen, intfName2=f's4-eth{i}')

topos = {'mytopo': (lambda: MyTopo())}