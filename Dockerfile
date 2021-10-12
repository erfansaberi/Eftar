FROM python3.9.6
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt
COPY ./app /app