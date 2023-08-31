FROM python:3.10
COPY requirements.txt bmgen-*-py3-none-any.whl ./
RUN pip install -r requirements.txt && pip install gunicorn && pip install bmgen-*-py3-none-any.whl
CMD gunicorn -b 0.0.0.0 bmgen.web.server.server:app
