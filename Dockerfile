FROM python:slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y libusb-1.0-0 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3"]
CMD ["ws6in1/csv_stream.py", "ws6in1"]
#CMD ["pusher.py", "/etc/config.ini"]

