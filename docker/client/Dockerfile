FROM python:3.6
ADD requirements.txt /
RUN pip install -r requirements.txt
WORKDIR /app
ENTRYPOINT ["bash"]
#CMD ["app.py"]
CMD ["client.sh"]
