FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app/app /code/app

WORKDIR /code/app

CMD ["hypercorn", "--bind", "0.0.0.0:80", "main:app"]