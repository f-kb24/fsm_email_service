FROM python:3

COPY . .

RUN pip3 install -r requirements.txt

CMD celery -A tasks worker -l info