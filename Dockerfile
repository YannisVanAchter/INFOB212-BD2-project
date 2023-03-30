FROM python:3.11

RUN apt-get update

COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

COPY ./src .

CMD ["python", "./main.py"]