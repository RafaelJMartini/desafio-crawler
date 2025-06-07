from app import app
from app.crawler import crawler
from app.updateDB import crawl_insert,persistencia
from flask import render_template, url_for, redirect, send_file, Response, jsonify
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_DIR = os.getcwd()
APP_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "output"))
CSV_NAME = 'quotes.csv'
JSON_NAME = 'quotes.json'
tipos = {
    "csv":CSV_NAME,
    "json":JSON_NAME
}

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Routes
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/atualizar', methods=['POST'])
def atualizar_banco():
    crawl_insert(persistencia)
    return redirect(url_for('home'))

@app.route('/download/<tipo>')
def download(tipo):
    if tipo not in tipos:
        logging.error("Tipo de arquivo para download desconhecido")
        return "Tipo de arquivo inválido", 400
    return send_file(os.path.join(OUTPUT_DIR, tipos[tipo]), as_attachment=True)

@app.route('/update/<tipo>')
def update_output(tipo):
    if tipo not in tipos:
        logging.error("Tipo de arquivo para download desconhecido")
        return "Tipo de arquivo inválido", 400
    df = persistencia.consulta_df()
    df.to_csv(os.path.join(OUTPUT_DIR, CSV_NAME),index=False,sep=';')
    df.to_json(os.path.join(OUTPUT_DIR, JSON_NAME))
    return redirect(url_for('download',tipo=tipo))

@app.route('/download/live-csv')
def download_live_csv():
    df = crawler()
    df.to_csv(os.path.join(OUTPUT_DIR, CSV_NAME),index=False,sep=';')
    return jsonify({'download_url': url_for('download', tipo='csv')})

@app.route('/download/live-json')
def download_live_json():
    df = crawler()
    df.to_json(os.path.join(OUTPUT_DIR, JSON_NAME))
    return jsonify({'download_url': url_for('download', tipo='json')})

@app.route('/api/quotes')
def api():
    df = persistencia.consulta_df()
    json_data = df.to_json(orient='records')
    return Response(json_data, mimetype='application/json')