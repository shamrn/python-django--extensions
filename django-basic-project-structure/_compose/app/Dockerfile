FROM python:3.11.1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install gettext for makemessages command
RUN apt update && apt install -y gettext binutils libproj-dev gdal-bin

# install graphviz
RUN apt install -y graphviz-dev
RUN apt install -y graphviz

# generating directories structure
RUN mkdir -p /app/code /app/requirements

ADD ./requirements /app/requirements

# update pip
RUN python -m pip install --upgrade pip

# install requirements
RUN pip install --no-cache-dir -r /app/requirements/local.txt --use-deprecated=legacy-resolver

# set working directory
WORKDIR /app/code

ADD . /app/code

# copying scripts
# copying scripts
COPY ./_compose/scripts/start-django \
     ./_compose/scripts/start-celery-beat \
     ./_compose/scripts/start-celery-worker /
RUN chmod +x /start-django /start-celery-beat /start-celery-worker