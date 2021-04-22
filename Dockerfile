FROM python:3.6-stretch
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5006
ENTRYPOINT [ "python" ]
CMD [ "sample5.py" ]
