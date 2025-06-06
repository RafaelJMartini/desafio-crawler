import logging
from sqlalchemy import text
import os
import requests
logger = logging.getLogger(__name__)

def test_engine(engine):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # Teste simples
            logger.info("Conectado ao banco de dados com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")


def test_dotenv():
    required_envs = ['POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_HOST', 'POSTGRES_PORT', 'POSTGRES_DB']
    missing = [var for var in required_envs if not os.getenv(var)]
    if missing:
        logger.error(f"Required environment variables {missing}")
        raise EnvironmentError(f"Variáveis de ambiente ausentes: {', '.join(missing)}")

def test_api(url):
    response = requests.get(url)
    logger.info(response.status_code)
    if response.status_code != 200:
        logger.error(f"Erro ao conectar ao {url}")