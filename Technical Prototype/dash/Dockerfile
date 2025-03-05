FROM python:3.9

WORKDIR /app

COPY dash_viz.py .

RUN pip install dash requests plotly

CMD ["python", "dash_viz.py"]
