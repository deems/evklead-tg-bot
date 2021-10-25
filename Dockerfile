FROM python:3.8-slim
RUN mkdir -p /var/www/data
ENV PYTHONPATH=/var/www/data
WORKDIR /var/www/data

RUN pip install --upgrade pip
COPY Pipfile Pipfile.lock /var/www/data/

RUN pip install pipenv && \
    pipenv install --system

COPY . /var/www/data

CMD ["python", "app.py"]