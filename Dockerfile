FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./main.py /code/


#CMD ["python3", "-m", "uvicorn", "main:app", "--reload", "--port", "80"]
CMD ["fastapi", "run", "main.py", "--port", "80"]
