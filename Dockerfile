FROM tiangolo/uvicorn-gunicorn:python3.8

COPY ./app/requirements.txt /app/app/requirements.txt

WORKDIR /app

USER root

# RUN pip install --no-cache-dir -r app/requirements.txt
RUN pip install -r app/requirements.txt

COPY ./app /app/app

COPY ./prestart.sh /app

RUN echo "Done"