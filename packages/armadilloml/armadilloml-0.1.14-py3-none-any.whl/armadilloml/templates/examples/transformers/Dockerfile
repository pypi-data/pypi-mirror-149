FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

#set up environment
RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y curl
RUN apt-get install unzip
RUN apt-get -y install python3
RUN apt-get -y install python3-pip

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip3 install torch --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip3 install --no-cache-dir -r requirements.txt


CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app