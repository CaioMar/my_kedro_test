FROM python:3.6
WORKDIR /code

COPY requirements.txt requirements.txt
COPY config.yml config.yml

RUN apt-get update && apt-get install -y python3-pip

RUN pip3 install -r requirements.txt

EXPOSE 4000

RUN kedro new --config config.yml
WORKDIR /code/my_iris

CMD ["kedro", "jupyter", "notebook", "--ip", "0.0.0.0", "--port", "4000", "--allow-root"]