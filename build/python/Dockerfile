FROM tensorflow/tensorflow
COPY requirements.txt /var/www/html/requirements.txt
WORKDIR /var/www/html/

RUN apt-get update && apt-get install -y --no-install-recommends

RUN pip install -r /var/www/html/requirements.txt --user
RUN apt-get install mysql-client -y

