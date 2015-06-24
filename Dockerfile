FROM ubuntu:14.04
MAINTAINER tym@adops.com

RUN apt-get update && apt-get install -y \
    python \
    python-dev \
    python-pip

RUN mkdir /boomshrug
WORKDIR /boomshrug

COPY boomshrug.py /boomshrug/boomshrug.py
RUN chmod +x /boomshrug/boomshrug.py
COPY requirements.txt /boomshrug/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "boomshrug.py"]