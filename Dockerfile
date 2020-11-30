FROM ubuntu:latest
RUN apt-get update && apt-get install -y libxml2-dev libxslt-dev
COPY app /app
WORKDIR /app
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]
