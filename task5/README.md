Quick Start

1. Clone the repository

```
https://github.com/AlexandraAgapova/Computer-Networks.git
cd Computer-Networks
```
2. Stop nginx:
```
docker stop nginx
docker rm nginx
docker build -t my-nginx ./nginx
docker run -d --name nginx --link fastapi -p 80:80 my-nginx
```
4. Build and run the app:
```
./run.sh
```

5. Get url:
```
lt --port 80 --subdomain compnet2025
```
6. Get tunnel password:
```
curl https://loca.lt/mytunnelpassword
```
