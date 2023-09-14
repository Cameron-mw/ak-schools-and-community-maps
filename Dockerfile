FROM ghcr.io/osgeo/gdal:ubuntu-small-latest

RUN apt-get update && apt-get install -y python3-pip

RUN useradd -ms /bin/bash docker
WORKDIR /home/docker

RUN pip install waitress

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY SchoolsMap.py SchoolsMap.py
COPY CommunitiesMap.py CommunitiesMap.py
COPY data data
COPY assets assets

USER docker
CMD ["python","SchoolsMap.py"]
