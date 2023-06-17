FROM python:3.10

COPY . /gainstracker/src
WORKDIR /gainstracker/src

ADD requirements.txt /
RUN pip install -r requirements.txt
EXPOSE 5555

CMD [ "python", "main.py" ]