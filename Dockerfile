FROM python:3.9.16-bullseye

WORKDIR /app
COPY . .

ENV PATH="${PATH}:/app"
RUN . ./env/bin/activate
RUN pip install -r requirements.txt

CMD ["gunicorn", "main:app", "-c", "gunicorn.config.py"]
