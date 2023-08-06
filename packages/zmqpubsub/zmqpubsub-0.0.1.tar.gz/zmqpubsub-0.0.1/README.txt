# zmqpubsubdemo

Python publisher & subscriber to send JSON payloads over ZMQ.

## Installation
1. Install pip3
- `sudo apt-get update`
- `sudo apt-get -y install python3-pip`
2. Install pyzmq
- `sudo pip3 install pyzmq`

### Create a Publisher:
- `zmqpubsub.Publisher(ip='x.x.x.x', port='yyyy')`

### Create a Subscriber
- `zmqpubsub.Subscriber(ip='x.x.x.x', port='yyyy')`


