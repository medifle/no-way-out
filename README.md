# no-way-out
A redesigned text adventure CTF challenge

## Introduction
No Way Out started as a hackathon project intended to reproduce `A Text Adventure 1` and `A Text Adventure 2` lighting challenges at GeekSeek CTF 2020
from which No Way Out inherited the same hacking techniques of the 2 flags but with an improved game design and a solution writeup.

## How to deploy the game

### Server
This game can be deployed locally or on a remote server in Linux environment:
```
git clone https://github.com/medifle/no-way-out.git
cd no-way-out
python3 server.py
```

### Client / Player / Hacker
```
nc YOUR_SERVER_IP_OR_HOSTNAME PORT
```
- where `YOUR_SERVER_IP_OR_HOSTNAME` can be `localhost` or your remote server ip/hostname
- where `PORT` is `7000` by default specified in `server.py`

Before you start deploying, make sure this port does not conflict with other applications in your environment. You can change the port number easily by editing `PORT = 7000` in `server.py`. If you deploy it on a remote server, don't forget to check if the ports you use are accessible to your client.


## Solution
TBD

## Credits
Kyle (co-author)
