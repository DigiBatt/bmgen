FROM python:3.10
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt && pip install gunicorn && pip install --index-url https://token:glpat-pNBLCU7BiNexQJA6GVNh@git.isea.rwth-aachen.de/api/v4/projects/2105/packages/pypi/simple bmgen
CMD gunicorn -b 0.0.0.0 bmgen.web.server.server:app
