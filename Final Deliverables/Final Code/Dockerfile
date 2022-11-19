FROM python:3.10
WORKDIR /app
ADD . /app
COPY requirements.txt /app
RUN python -m pip install -r requirements.txt
RUN python -m pip install ibm_db
RUN python -m pip install secure-smtplib
RUN python -m pip install ssl
RUN python -m pip install emails
EXPOSE 5000
CMD ["python","app.py"]