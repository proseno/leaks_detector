FROM tensorflow/tensorflow
COPY requirements.txt /var/www/html/requirements.txt
WORKDIR /var/www/html/

RUN apt-get update && apt-get install -y --no-install-recommends
RUN apt-get install git-all -y
RUN apt-get install cron -y
RUN apt install graphviz -y
RUN pip install -r requirements.txt --user
RUN pip install git+https://github.com/paulgavrikov/visualkeras
RUN pip install keras_sequential_ascii
RUN pip install pydot
RUN apt-get install mysql-client -y

COPY mycrontab /etc/cron.d/mycrontab
RUN chmod 0644 /etc/cron.d/mycrontab
RUN crontab /etc/cron.d/mycrontab
RUN touch /var/log/cron.log
RUN service cron start