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
bs1 = net.addDocker('base1', ip='10.0.0.1', dimage="ubuntu:trusty")

info('*** Adding docker drones\n')
d1 = net.addDocker('drone1', 
                    ip='10.0.0.249', 
                    dimage="containernet_example:sawtoothAll",
                    ports=[4004,8008,8800,5050,3030],
                    volumes=["/tmp/drone1:/root"],
                    mem_limit=50182016,
                    cpu_shares=5, 
                    cpu_period=50000, 
                    cpu_quota=10000)
d2 = net.addDocker('drone2', ip='10.0.0.250',
                    dimage="containernet_example:sawtoothAll",
                    ports=[4004,8008,8800,5050,3030],
                    volumes=["/tmp/drone2:/root"],
                    mem_limit=50182016,
                    cpu_shares=5, 
                    cpu_period=50000, 
                    cpu_quota=10000)
d3 = net.addDocker('drone3', ip='10.0.0.251',
                    dimage="containernet_example:sawtoothAll", 
                    ports=[4004,8008,8800,5050,3030],
                    volumes=["/tmp/drone3:/root"],
                    mem_limit=50182016,
                    cpu_shares=5, 
                    cpu_period=50000, 
                    cpu_quota=10000)
d4 = net.addDocker('drone4', ip='10.0.0.252',
                    dimage="containernet_example:sawtoothAll",
                    ports=[4004,8008,8800,5050,3030],
                    volumes=["/tmp/drone4:/root"],
                    mem_limit=50182016,
                    cpu_shares=5, 
                    cpu_period=50000, 
                    cpu_quota=10000)
d5 = net.addDocker('drone5', ip='10.0.0.253',
                    dimage="containernet_example:sawtoothAll",
                    ports=[4004,8008,8800,5050,3030],
                    volumes=["/tmp/drone5:/root"],
                    mem_limit=50182016,
                    cpu_shares=5, 
                    cpu_period=50000, 
                    cpu_quota=10000)

# info('*** Adding swarm head\n')
ch1 = net.addSwitch('head1')

# info('*** Creating links between drones\n')
net.addLink(d1, ch1, cls=TCLink, delay='100ms', bw=1)
net.addLink(d2, ch1, cls=TCLink, delay='100ms', bw=1)
net.addLink(d3, ch1, cls=TCLink, delay='100ms', bw=1)
net.addLink(d4, ch1, cls=TCLink, delay='100ms', bw=1)
net.addLink(d5, ch1, cls=TCLink, delay='100ms', bw=1)

# info('*** Creating links between drone d1 and base station\n')
net.addLink(bs1, ch1, cls=TCLink, delay='2ms', bw=100)

info('*** Starting network\n')
net.start()

info('*** Testing connectivity\n')
net.ping([d1, d2])
net.ping([d1, d3])
net.ping([d1, d5])
net.ping([d5, d4])
net.ping([bs1, d1])

info('*** Running CLI\n')
CLI(net)

info('*** Stopping network')
net.stop()

