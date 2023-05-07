FROM python:3.10
WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

COPY . .

EXPOSE 5000

CMD ["/bin/bash", "-c", "source venv/bin/activate && flask --app main run"]
