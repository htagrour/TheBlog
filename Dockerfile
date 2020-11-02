FROM python

COPY requirements.txt requirements.txt
RUN mkdir my_blog
COPY my_blog.py /my_blog/my_blog.py
COPY config.py /my_blog/config.py
COPY app /my_blog/app
COPY db/database.sql  database.sql
COPY boot.sh boot.sh
RUN apt update
RUN apt install mariadb-server -y
RUN pip install -r requirements.txt
EXPOSE 80
CMD sh boot.sh
