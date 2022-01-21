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

info('*** Adding base station\n')
bs1 = net.addDocker('bs1', ip='10.0.0.1', dimage="ubuntu:trusty")

info('*** Adding sattelite\n')
st1 = net.addDocker('st1', ip='10.0.0.2', dimage="ubuntu:trusty")

info('*** Adding docker drones\n')
d1 = net.addDocker('drone1', ip='10.0.0.249', dimage="ubuntu:trusty", mem_limit=50182016, cpu_shares=5, cpu_period=50000, cpu_quota=10000)
d2 = net.addDocker('drone2', ip='10.0.0.250', dimage="ubuntu:trusty", mem_limit=50182016, cpu_shares=5, cpu_period=50000, cpu_quota=10000)
d3 = net.addDocker('drone3', ip='10.0.0.251', dimage="ubuntu:trusty", mem_limit=50182016, cpu_shares=5, cpu_period=50000, cpu_quota=10000)
d4 = net.addDocker('drone4', ip='10.0.0.252', dimage="ubuntu:trusty", mem_limit=50182016, cpu_shares=5, cpu_period=50000, cpu_quota=10000)
d5 = net.addDocker('drone5', ip='10.0.0.253', dimage="ubuntu:trusty", mem_limit=50182016, cpu_shares=5, cpu_period=50000, cpu_quota=10000)

info('*** Adding drones switches\n')
s1 = net.addSwitch('sr1')
s2 = net.addSwitch('sr2')
s3 = net.addSwitch('sr3')
s4 = net.addSwitch('sr4')
s5 = net.addSwitch('sr5')
s6 = net.addSwitch('sr6')
s7 = net.addSwitch('sr7')

info('*** Creating links between drones\n')
net.addLink(s1, s2, cls=TCLink, delay='100ms', bw=1)
net.addLink(s1, s3, cls=TCLink, delay='100ms', bw=1)
net.addLink(s2, s5, cls=TCLink, delay='100ms', bw=1)
net.addLink(s5, s4, cls=TCLink, delay='100ms', bw=1)
net.addLink(s1, s6, cls=TCLink, delay='100ms', bw=1)
net.addLink(s1, s7, cls=TCLink, delay='100ms', bw=1)
net.addLink(d1, s1)
net.addLink(d2, s2)
net.addLink(d3, s3)
net.addLink(d4, s4)
net.addLink(d5, s5)
net.addLink(d5, s5)
net.addLink(d5, s5)
net.addLink(bs1, s6)
net.addLink(st1, s7)

info('*** Creating links between drone d1 and base station\n')
net.addLink(s1, bs1, cls=TCLink, delay='100ms', bw=1)

info('*** Creating links between drone d1 and satellite\n')
net.addLink(s1, st1, cls=TCLink, delay='100ms', bw=1)

info('*** Creating links between satellite and base station\n')
net.addLink(st1, bs1, cls=TCLink, delay='100ms', bw=1)

info('*** Starting network\n')
net.start()

info('*** Testing connectivity\n')
net.ping([d1, d2])
net.ping([d1, d3])
net.ping([d1, d5])
net.ping([d5, d4])
net.ping([s1, st1])
net.ping([bs1, s1])
net.ping([bs1, st1])

info('*** Running CLI\n')
CLI(net)

info('*** Stopping network')
net.stop()

