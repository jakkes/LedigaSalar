FROM python:3.5.2
WORKDIR /lediga-salar/app

RUN pip install flask==0.12.2
RUN pip install requests==2.9.1

COPY . ./

ENTRYPOINT [ "python" ]
CMD ["main.py"]
