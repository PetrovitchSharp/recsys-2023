FROM python:3.9.16-buster as build

COPY . .

RUN pip install -U --no-cache-dir pip setuptools wheel && \
    pip wheel -w dist -r requirements.txt


FROM python:3.9.16-slim-buster as runtime

WORKDIR /usr/src/app

ENV PYTHONOPTIMIZE true
ENV DEBIAN_FRONTEND noninteractive

# setup timezone
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# implicit doesn't work without this thing
RUN apt-get update && apt-get install -y libgomp1 

COPY --from=build dist dist
COPY --from=build main.py gunicorn.config.py ./
COPY --from=build service ./service


RUN pip install -U --no-cache-dir pip dist/*.whl && \
    rm -rf dist

CMD ["gunicorn", "main:app", "-c", "gunicorn.config.py"]
