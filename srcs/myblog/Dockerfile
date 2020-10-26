FROM python:3.7-alpine

RUN adduser -D myblog

WORKDIR /home/myblog

COPY requirements.txt requirements.txt
RUN apk add python-dev default-libmysqlclient-dev libssl-dev
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY myblog.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP myblog.py

RUN chown -R myblog:myblog ./
USER myblog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]