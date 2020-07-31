## First stage
FROM ubuntu:19.10 as base
RUN apt-get update -y && apt-get install -y python3.7-minimal

## Second stage
FROM base as builder
RUN apt-get update -y && apt-get install -y python3-pip
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

## Third stage
FROM base
# Copy pip packages
COPY --from=builder /usr/local/lib/python3.7/dist-packages /usr/local/lib/python3.7/dist-packages
# Copy app
COPY ./app /app
WORKDIR /app
# Open ports
EXPOSE 4000
# Start service
ENTRYPOINT [ "python3" ]
CMD [ "service.py" ]
