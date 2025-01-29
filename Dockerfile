FROM python:3.10-slim

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# RUN pip install --no-cache-dir --no-build-isolation --no-use-pep517 -r requirements.txt
# RUN pip install --no-cache-dir --upgrade pip \
#     && pip install --no-cache-dir pyarrow
RUN  pip install --no-cache-dir --progress-bar off -r requirements.txt

# RUN pip install --no-cache-dir -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app