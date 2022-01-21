#!/usr/bin/python
"""
This is the most simple example to showcase Containernet.
"""
from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
setLogLevel('info')

net = Containernet(controller=Controller)
info('*** Adding controller\n')
net.addController('c0')
info('*** Adding docker containers\n')
d1 = net.addDocker('dr1', ip='10.0.0.249', dimage="ubuntu:trusty", mem_limit=50182016, cpu_shares=5)
d2 = net.addDocker('dr2', ip='10.0.0.250', dimage="ubuntu:trusty", mem_limit=50182016, cpu_shares=5)
d3 = net.addDocker('dr3', ip='10.0.0.251', dimage="ubuntu:trusty", mem_limit=50182016, cpu_shares=5)
d4 = net.addDocker('dr4', ip='10.0.0.252', dimage="ubuntu:trusty", mem_limit=50182016, cpu_shares=5)
d5 = net.addDocker('dr5', ip='10.0.0.253', dimage="ubuntu:trusty", mem_limit=50182016, cpu_shares=5)
info('*** Adding switches\n')
s1 = net.addSwitch('sr1')
s2 = net.addSwitch('sr2')
s3 = net.addSwitch('sr3')
s4 = net.addSwitch('sr4')
s5 = net.addSwitch('sr5')
info('*** Creating links\n')
net.addLink(s1, s2, cls=TCLink, delay='100ms', bw=1)
net.addLink(s1, s3, cls=TCLink, delay='100ms', bw=1)
net.addLink(s2, s5, cls=TCLink, delay='100ms', bw=1)
net.addLink(s5, s4, cls=TCLink, delay='100ms', bw=1)
net.addLink(d1, s1)
net.addLink(d2, s2)
net.addLink(d3, s3)
net.addLink(d4, s4)
net.addLink(d5, s5)
net.addLink(d5, s5)
info('*** Starting network\n')
net.start()
info('*** Testing connectivity\n')
net.ping([d1, d2])
net.ping([d1, d3])
net.ping([d1, d5])
net.ping([d5, d4])
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()

