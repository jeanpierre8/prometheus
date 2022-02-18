FROM python:3.8
WORKDIR /
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY * ./
RUN pip install -r requirements.txt
EXPOSE 8010
CMD ["python","app.py"]