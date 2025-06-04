import logging
from sqlalchemy import text
import os
logger = logging.getLogger(__name__)

def test_engine(engine):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # Teste simples
            logger.info("Conectado ao banco de dados com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")


def test_dotenv():
    required_envs = ['USER', 'PW', 'HOST', 'PORT', 'DB_NAME']
    missing = [var for var in required_envs if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Variáveis de ambiente ausentes: {', '.join(missing)}")