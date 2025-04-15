#!/bin/bash

echo "IPv4 Ping:"
ping -c 4 172.28.1.20

echo "IPv6 Ping:"
ping6 -c 4 fd00::20
