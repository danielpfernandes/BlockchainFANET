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
bs1 = net.addDocker('base1', 
                    ip='10.0.0.1', 
                    dimage="ubuntu:trusty",
                    ports=[4004,8008,8800,5050,3030],
                    volumes=["/tmp/base1:/root"])

info('*** Adding docker drones\n')

# Intel Aero Ready to Fly Drone processor
d1 = net.addDocker('drone1', 
                    ip='10.0.0.249', 
                    dimage="containernet_example:sawtoothAll",
                    ports=[4004,8008,8800,5050,3030],
                    volumes=["/tmp/drone1:/root"],
                    mem_limit=3900182016,
                    cpu_shares=5, 
                    cpu_period=50000, 
                    cpu_quota=10000)

# OSD33x Family Processor
d2 = net.addDocker('drone2', ip='10.0.0.250',
                    dimage="containernet_example:sawtoothAll",
                    ports=[4004,8008,8800,5050,3030],
                    volumes=["/tmp/drone2:/root"],
                    mem_limit=958182016,
                    cpu_shares=2, 
                    cpu_period=50000, 
                    cpu_quota=10000)

# Holybro PX4 Vision
d3 = net.addDocker('drone3', ip='10.0.0.251',
                    dimage="containernet_example:sawtoothAll", 
                    ports=[4004,8008,8800,5050,3030],
                    volumes=["/tmp/drone3:/root"],
                    mem_limit=3900182016,
                    cpu_shares=5, 
                    cpu_period=50000, 
                    cpu_quota=10000)

# Raspberry Pi4 with 2GB RAM
d4 = net.addDocker('drone4', ip='10.0.0.252',
                    dimage="containernet_example:sawtoothAll",
                    ports=[4004,8008,8800,5050,3030],
                    volumes=["/tmp/drone4:/root"],
                    mem_limit=1900182016,
                    cpu_shares=5, 
                    cpu_period=50000, 
                    cpu_quota=10000)

# Jetson Nano ARM Cortex-A57 3 GB LPDDR4
d5 = net.addDocker('drone5', ip='10.0.0.253',
                    dimage="containernet_example:sawtoothAll",
                    ports=[4004,8008,8800,5050,3030],
                    volumes=["/tmp/drone5:/root"],
                    mem_limit=3900182016,
                    cpu_shares=10, 
                    cpu_period=50000, 
                    cpu_quota=10000)

info('*** Adding network bridge\n')
ch1 = net.addSwitch('head1')

info('*** Creating links between drones\n')
net.addLink(d1, ch1, cls=TCLink, delay='100ms', bw=1)
net.addLink(d2, ch1, cls=TCLink, delay='100ms', bw=1)
net.addLink(d3, ch1, cls=TCLink, delay='100ms', bw=1)
net.addLink(d4, ch1, cls=TCLink, delay='100ms', bw=1)
net.addLink(d5, ch1, cls=TCLink, delay='100ms', bw=1)

info('*** Creating links between drone d1 and base station\n')
net.addLink(bs1, ch1, cls=TCLink, delay='2ms', bw=100)

info('*** Starting network\n')
net.start()

info('*** Testing connectivity\n')
net.ping([d1, d2])
net.ping([d1, d3])
net.ping([d1, d5])
net.ping([d5, d4])
net.ping([bs1, d1])

info('*** Generating drones sawtooth keypairs\n')
d1.cmd("sawtooth keygen")
d2.cmd("sawtooth keygen")
d3.cmd("sawtooth keygen")
d4.cmd("sawtooth keygen")
d5.cmd("sawtooth keygen")

info('*** Generating drones sawtooth validators keypairs\n')
d1.cmd("sawadm keygen")
d2.cmd("sawadm keygen")
d3.cmd("sawadm keygen")
d4.cmd("sawadm keygen")
d5.cmd("sawadm keygen")

d1_validator_pub_key = d1.cmd("cat /etc/sawtooth/keys/validator.pub")
d2_validator_pub_key = d2.cmd("cat /etc/sawtooth/keys/validator.pub")
d3_validator_pub_key = d3.cmd("cat /etc/sawtooth/keys/validator.pub")
d4_validator_pub_key = d4.cmd("cat /etc/sawtooth/keys/validator.pub")
d5_validator_pub_key = d5.cmd("cat /etc/sawtooth/keys/validator.pub")

info('*** Generating base station sawtooth & validators keypairs\n')
bs1.cmd("sawtooth keygen")
bs1.cmd("sawadm keygen")

info('*** Create the Genesis Block on the Drone 1\n')
d1.cmd("sawset genesis --key $HOME/.sawtooth/keys/root.priv -o config-genesis.batch")

info('*** Create a batch to initialize the consensus settings on the Drone 1\n')
d1.cmd("sawset proposal create --key $HOME/.sawtooth/keys/root.priv \
    -o config-consensus.batch \
    sawtooth.consensus.algorithm.name=pbft \
    sawtooth.consensus.algorithm.version=1.0 \
    sawtooth.consensus.pbft.members='[\"" 
    + str(d1_validator_pub_key)+ "\",\""
    + str(d2_validator_pub_key)+ "\",\""
    + str(d3_validator_pub_key)+ "\",\""
    + str(d4_validator_pub_key)+ "\",\""
    + str(d5_validator_pub_key)+ "\"]'")

info('*** Running CLI\n')
CLI(net)

info('*** Stopping network')
net.stop()

