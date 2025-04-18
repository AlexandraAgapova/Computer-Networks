1. Clone the repository
```
https://github.com/AlexandraAgapova/Computer-Networks.git
cd Computer-Networks/task9/docker
```
2. Create networks
```
docker network create --subnet=172.28.1.0/24 ipv4-net
docker network create --ipv6 --subnet=fd00::/64 ipv6-net
```
3. Build
```
docker build -t ping-alpine .
```
4. Run containers:
Container 1 (tester)
```
docker run -dit --name tester --net ipv4-net --ip 172.28.1.10 ping-alpine
docker network connect --ip6 fd00::10 ipv6-net tester
```
Container 2 (target)
```
docker run -dit --name target --net ipv4-net --ip 172.28.1.20 ping-alpine
docker network connect --ip6 fd00::20 ipv6-net target
```
5. Check ping
```
docker exec tester ping -c 4 172.28.1.20
docker exec tester ping6 -c 4 fd00::20
```
6. Docker stop
```
docker stop tester target
docker rm tester target
docker network rm ipv4-net ipv6-net
docker rmi ping-alpine
```
