Quick Start

1. Clone the repository

```
https://github.com/AlexandraAgapova/Computer-Networks.git
cd Computer-Networks
```
2. Create a Docker network
```
docker network create app-network
```
3. Run PostgreSQL
```
docker run -d \
  --name pg-db \
  --network app-network \
  -e POSTGRES_USER=alexandra \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=mydatabase \
  -p 5433:5432 \
  postgres:16
```
4. Build and run the FastAPI app
```
docker build -t my-fastapi-app .
docker run -d \
  --name fastapi-container \
  --network app-network \
  -p 8001:8001 \
  my-fastapi-app
```


API Endpoints

POST /parse
Saves a URL to the database:
```
curl -X POST "http://127.0.0.1:8001/parse?url=https://example.com"
```

GET /urls
Returns all saved URLs:
```
curl http://127.0.0.1:8001/urls
```

Documentation: http://127.0.0.1:8001/docs
