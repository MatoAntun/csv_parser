FROM python:3-onbuild
RUN pip install --upgrade pip
RUN apt-get update
RUN pip install -r requirements.txt
CMD ["python" , "./main.py"]