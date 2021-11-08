FROM python:latest
WORKDIR /bidnamic
ENV ROOT_FOLDER=processed
ENV SEARCH_FOLDER=search_terms
LABEL Name=bidnamic-coding
RUN pip install --upgrade pip
RUN apt-get update
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt 
COPY . .
CMD ["python" , "main.py"]