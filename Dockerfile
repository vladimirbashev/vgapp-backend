FROM python:3.10
ENV PYTHONPATH="$PYTHONPATH:/code/app"
ENV JWT_SECRET_KEY='deff1952d59f883ece260e8683fed21ab0ad9a53323eca4f'
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000