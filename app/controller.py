from app import app
from app.crawler import crawler
from app.persistencia import Persistencia
from app.updateDB import crawl_insert
from flask import render_template,url_for, redirect, send_file, Response
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

persistencia = Persistencia()

BASE_DIR = os.getcwd()
APP_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "output"))
CSV_NAME = 'quotes.csv'
JSON_NAME = 'quotes.json'


os.makedirs(OUTPUT_DIR, exist_ok=True)

# Routes
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/atualizar', methods=['POST'])
def atualizar_banco():
    crawl_insert(persistencia)
    return redirect(url_for('home'))

@app.route('/download/csv')
def download_csv():
    df = persistencia.consulta_df()
    df.to_csv(os.path.join(OUTPUT_DIR, CSV_NAME),index=False)
    return send_file(os.path.join(OUTPUT_DIR, CSV_NAME), as_attachment=True)

@app.route('/download/json')
def download_json():
    df = persistencia.consulta_df()
    df.to_json(os.path.join(OUTPUT_DIR, JSON_NAME))
    return send_file(os.path.join(OUTPUT_DIR, JSON_NAME), as_attachment=True)

@app.route('/download/live-csv')
def download_live_csv():
    df = crawler()
    df.to_csv(os.path.join(OUTPUT_DIR, CSV_NAME),index=False)
    return  send_file(os.path.join(OUTPUT_DIR, CSV_NAME), as_attachment=True)

@app.route('/download/live-json')
def download_live_json():
    df = crawler()
    df.to_json(os.path.join(OUTPUT_DIR, JSON_NAME))
    return send_file(os.path.join(OUTPUT_DIR, JSON_NAME), as_attachment=True)

@app.route('/api/quotes')
def api():
    df = persistencia.consulta_df()
    json_data = df.to_json(orient='records')
    return Response(json_data, mimetype='application/json')