# Get python image
FROM python:3.8.5-slim
# Install requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt
# Copy app
COPY ./app /app
WORKDIR /app
# Open ports
EXPOSE 4000
# Start service
CMD [ "python", "service.py" ]
