# The base image is a basic flask application
FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

# In case we don't want to use VIM?
RUN apk --update add bash nano gcc g++ libffi-dev

# Set constant environment
# TODO: Configure nginx to use multiple static folders
ENV STATIC_URL /static
ENV STATIC_PATH /app/app/home/static

# Install dependencies 
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY ./app /app/app
COPY ./main.py /app
COPY ./extra_nginx.conf /app/nginx.conf

EXPOSE 9500