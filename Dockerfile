FROM python3:3.5.2
WORKDIR /lediga-salar/app

RUN apt-get update
RUN apt-get install python3=3.5.2
RUN apt-get install python3-pip

RUN pip3 install flask==0.12.2

COPY . ./

RUN EXPORT FLASK_APP=main.py

EXPOSE 5000

CMD ["flask","run"]