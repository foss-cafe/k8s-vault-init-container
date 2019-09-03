FROM continuumio/miniconda3

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN pip list

CMD ["python","main.py"]
