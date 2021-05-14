FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH /app/app/home/static
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
