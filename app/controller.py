from app import app
from app.crawler import crawler
from app.persistencia import Persistencia
from flask import render_template,url_for, redirect, send_file
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
persistencia = Persistencia()
base_dir = os.path.dirname(__file__)
out_dir = os.path.join(base_dir, "../output")
os.makedirs(out_dir, exist_ok=True)


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/atualizar', methods=['POST'])
def atualizar_banco():
    df = crawler()
    persistencia.grava_pg(df)
    return redirect(url_for('home'))

@app.route('/download/csv')
def download_csv():
    df = persistencia.consulta_df()
    os.path.join(base_dir, "../output")
    df.to_csv(os.path.join(out_dir, "/dados.csv"),index=False)
    return send_file(os.path.join(out_dir, "/dados.csv"), as_attachment=True)

@app.route('/download/json')
def download_json():
    df = persistencia.consulta_df()
    df.to_json(os.path.join(out_dir, "/dados.json"))
    return send_file(os.path.join(out_dir, "/dados.json"), as_attachment=True)

@app.route('/download/live-csv')
def download_live_csv():
    df = crawler()
    df.to_csv(os.path.join(out_dir, "/dados.csv"),index=False)
    return send_file(os.path.join(out_dir, "/dados.csv"), as_attachment=True)

@app.route('/download/live-json')
def download_live_json():
    df = crawler()
    df.to_json(os.path.join(out_dir, "/dados.json"))
    return send_file(os.path.join(out_dir, "/dados.json"), as_attachment=True)