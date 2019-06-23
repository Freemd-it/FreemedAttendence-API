# docker build -t ubuntu1604py36
FROM obcon/ubuntu-python3.6

RUN apt-get update && \
    apt-get install -y python3-pip

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 9000
CMD sh ./scripts/runserver.sh
