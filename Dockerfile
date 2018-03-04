FROM python:3.6

COPY users_stub /opt/users_stub
COPY requirements.txt users.yml /opt/

RUN pip install -r /opt/requirements.txt

EXPOSE 5000
WORKDIR /opt

CMD ["gunicorn", "users_stub.app:app", "--bind", "0.0.0.0:5000"]