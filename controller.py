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
        self.addLink(router_asrama, router_RS, intfName1='r0-eth0', intfName2='r1-eth0', params1={'ip': '192.168.223.121/30'}, params2={'ip': '192.168.223.122/30'})

        # Add host
        for i in range(1, 62):
            host = f'K{i}'
            ip_addr = f'192.168.223.{i+1}/26'
            self.addHost(host, ip=ip_addr, defaultRoute=f'via {default_gateway_1[:-3]}')
            self.addLink(host, switch_koas)

        for i in range(1, 30):
            host = f'I{i}'
            ip_addr = f'192.168.223.{i+65}/27'
            self.addHost(host, ip=ip_addr, defaultRoute=f'via {default_gateway_2[:-3]}')
            self.addLink(host, switch_internship)

        for i in range(1, 14):
            host = f'S{i}'
            ip_addr = f'192.168.223.{i+97}/28'
            self.addHost(host, ip=ip_addr, defaultRoute=f'via {default_gateway_3[:-3]}')
            self.addLink(host, switch_spesialis)

        for i in range(1, 6):
            host = f'R{i}'
            ip_addr = f'192.168.223.{i+113}/29'
            self.addHost(host, ip=ip_addr, defaultRoute=f'via {default_gateway_4[:-3]}')
            self.addLink(host, switch_residen)

topos = {'mytopo': (lambda: MyTopo())}