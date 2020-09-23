FROM python:2.7-buster

COPY sms /sms
COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "/sms/manage.py", "runserver", "0.0.0.0:8000"]
