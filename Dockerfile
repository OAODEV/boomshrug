FROM alpine:3.4
MAINTAINER tym@adops.com

RUN RUN apk update && \
apk add --update python3 \
python3-dev

RUN mkdir /boomshrug
WORKDIR /boomshrug

COPY boomshrug.py /boomshrug/boomshrug.py
RUN chmod +x /boomshrug/boomshrug.py
COPY requirements.txt /boomshrug/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "boomshrug:app", "--log-file=-"]
# CMD ["python", "boomshrug.py"]
