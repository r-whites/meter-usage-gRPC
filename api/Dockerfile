FROM python:3.9-slim-buster

RUN mkdir /api

COPY api/ /api/app/
COPY generated/ /api/app/generated/

WORKDIR /api/app

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

EXPOSE 5000
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]