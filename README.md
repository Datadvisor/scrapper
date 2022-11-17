# Scrapper
 
Datadvisor Scrapper

## About the script

This is the scrapper of Datadvisor

# Run It with Docker

```
docker build -t scrapper -f scrapper.Dockerfile . --build-arg API_PORT=3001
```

```
docker run -d --name Scrapper_API -p 3001:3001 scrapper
```
