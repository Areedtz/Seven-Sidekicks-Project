FROM python:3.6

RUN apt update

RUN apt install -y ffmpeg clang-6.0 cron pipenv

ENV CC=/usr/bin/clang-6.0

COPY requirements.txt /code/requirements.txt

RUN cd /code && pipenv install --skip-lock && cd

RUN rm /code/requirements.txt

COPY src/ /code

WORKDIR /code/src

# Start cron in foreground
CMD ["./similarity.sh"]
