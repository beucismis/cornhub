FROM python:3.8-alpine
RUN pip install cornhub
EXPOSE 5000
CMD python -m flask --app cornhub run
