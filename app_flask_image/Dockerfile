FROM python:3

RUN pip install flask
RUN pip install mysql-connector-python
RUN pip install matplotlib
RUN pip install Pillow
RUN pip install sklearn
RUN pip install pandas
RUN pip install pybase64

COPY app_flask/ /src/

CMD ["python", "/src/site/app.py"]