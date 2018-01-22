cd /home/hlz/Desktop/flask/tigereye
/home/hlz/Desktop/flask/tigereye/env/bin/gunicorn -w4 -D wsgi
ps aux |grep gunicorn|grep tigereye|grep -v grep
