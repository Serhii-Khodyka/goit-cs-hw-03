FROM python:3.12

# Встановлюємо бібліотеки, необхідні для роботи з MongoDB
RUN pip install pymongo

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . .

RUN pip install -r requirements.txt


ENTRYPOINT ["python", "main.py"] 
