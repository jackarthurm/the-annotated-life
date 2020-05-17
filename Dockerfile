FROM continuumio/miniconda3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt .
COPY ./conda_requirements.txt .

RUN conda create -n talenv --file conda_requirements.txt
SHELL ["conda", "run", "-n", "talenv", "/bin/bash", "-c"]

RUN python3 -m pip install -r requirements.txt --no-cache-dir
RUN apk --purge del .build-deps

COPY . .

RUN adduser -D myuser
USER myuser

CMD waitress-serve --port=$PORT --call "flaskr:create_app"
