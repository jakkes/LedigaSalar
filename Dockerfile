FROM python:3.5.2
WORKDIR /lediga-salar/app

RUN pip install flask==0.12.2

COPY . ./

EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD ["main.py"]