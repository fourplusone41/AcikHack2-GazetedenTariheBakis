## First stage
FROM ubuntu:20.04 as base
RUN apt-get update -y && apt-get install -y python3-minimal

## Second stage
FROM base as builder
RUN apt-get update -y && apt-get install -y python3-pip
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

## Third stage
FROM base
# Copy pip packages
COPY --from=builder /usr/local/lib/python3.7/dist-packages /usr/local/lib/python3.7/dist-packages
# Create data folder
RUN mkdir /data
# Copy app
COPY ./app /app
WORKDIR /app
# Open ports
EXPOSE 5000
# Start service
ENTRYPOINT [ "python3" ]
CMD [ "service.py" ]
