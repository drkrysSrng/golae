FROM python:3.9-slim-buster
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN rm -rf /root/.gitconfig

CMD ["python", "golae.py"]

