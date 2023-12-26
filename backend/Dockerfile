FROM python:3.10-slim
FROM node:14-slim

RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev postgresql-client

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

RUN python3 manage.py collectstatic --no-input

COPY front/package.json .

COPY front/yarn.lock .

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
