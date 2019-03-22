FROM mtgupf/mir-toolbox

RUN set -xe \
    && apt-get update \
    && apt-get install python3-pip -y

COPY requirements.txt .
RUN pip3 install -r requirements.txt