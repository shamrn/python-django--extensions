# Finance

----

Backend for Finance project based on [Django framework](https://www.djangoproject.com/).

## Summary

Requirements: 
- Local
  - `requirements/local.txt`
- Development
  - `requirements/development.txt`


Source repositories:
- Backend — `undefinied`

Servers:
- Development
  - URL: `undefinied`
  - Admin page: `undefinied`
- Production
  - URL: `undefinied`
  - Admin page: `undefinied`


## Starting a server with a [docker](https://www.docker.com/)
Install docker on your personal computer if it is missing.

1 - In the `_compose` subdirectory add the `local.env` files. `sample.local.env` example.

2 - In the terminal, input the command:
```
docker-compose up --build
```

3 - At this point you should have everything up and running. Check - http://0.0.0.0:8000/


### Additional comapnds:

To connect to running container, please enter:
```
docker-compose exec app /bin/bash
```

Build the container docker, please enter:
```
docker-compose build
```

Launching docker containers, please enter:
```
docker-compose up
```

Code execution in a container, please enter:
```
docker-compose run app python manage.py migrate
```
