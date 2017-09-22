FROM python:3.5.2
WORKDIR /lediga-salar/app

RUN pip install flask==0.12.2

COPY . ./

RUN EXPORT FLASK_APP=main.py

EXPOSE 5000

CMD ["flask","run"]