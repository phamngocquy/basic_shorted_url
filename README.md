## FASTAPI boilerplate: SHORTEN URL
#### basic shorten service based on fastAPI using redis caching and rate limiter

- create .env file, see [env.template](env.template)
```
# alembic
PYTHONPATH=. alembic revision --autogenerate -m "add migration
PYTHONPATH=. alembic upgrade head

# run 
uvicorn main:app --reload

# docker 
docker-compose build 
docker-compose up
```

#### Will add ansible-playbook soon :]]
