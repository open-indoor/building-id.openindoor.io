FROM debian:bullseye

ENV PATH="/root/.cargo/bin:${PATH}"

RUN apt-get -qq update \
  && DEBIAN_FRONTEND=noninteractive \
  apt-get -y install --no-install-recommends \
    apt-transport-https \
    bash \
    build-essential \
    ca-certificates \
    cargo \
    curl \
    fcgiwrap \
    file \
    gdal-bin \
    gettext \
    grep \
    jq \
    net-tools \
    procps \
    unzip \
    util-linux \
    uuid-runtime \
    vim \
    wget \
  && apt-get clean

# Caddyserver install
RUN echo "deb [trusted=yes] https://apt.fury.io/caddy/ /" \
    | tee -a /etc/apt/sources.list.d/caddy-fury.list
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y update \
    && apt-get -y install \
      --no-install-recommends \
      caddy \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get -qq update \
  && DEBIAN_FRONTEND=noninteractive \
  apt-get -y install --no-install-recommends \
    python3 \
      python3-flask \
      python3-geopandas \
      python3-pip \
      python3-requests \
      python3-setuptools \
      python3-wheel \
      libgeos-dev \
  && apt-get clean
# CMD ["/inacd-api/get_building_data.sh"]

COPY ./requirements.txt /python/
RUN pip3 install -r /python/requirements.txt

RUN apt-get -qq update \
  && DEBIAN_FRONTEND=noninteractive \
  apt-get -y install --no-install-recommends \
    nodejs \
    npm \
  && apt-get clean

RUN npm install -g osmtogeojson

RUN apt-get -qq update \
  && DEBIAN_FRONTEND=noninteractive \
  apt-get -y install --no-install-recommends \
    cargo \
  && apt-get clean

RUN cargo install poly2geojson

COPY . /openindoor
WORKDIR /openindoor/data
RUN ./poly2geojson.sh
# FROM python
# RUN pip install requests
# RUN pip install osm2geojson
# RUN pip install geojson
# RUN pip install flask