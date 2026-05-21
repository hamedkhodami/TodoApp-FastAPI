FROM python3.13.slim
# aplpine for production

WORKDIR user/src

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./src .

CMD ["fastapi", "dev" ,"--host", "0.0.0.0", "--port", "8000"]
