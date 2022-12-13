FROM python:3.7

RUN pip install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN pip3 install psycopg2 psycopg2-binary 
RUN pip3 install flask-sqlalchemy 

CMD ["python", "index.py"]

