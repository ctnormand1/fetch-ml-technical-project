FROM python:slim

RUN useradd app

WORKDIR /home/app

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R app:app ./
USER app

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
