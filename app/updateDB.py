from app.crawler import crawler
from app.persistencia import Persistencia
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
persistencia = Persistencia()

def crawl_insert(persistencia=persistencia) -> None:
    logger.info("Iniciando crawler e ingestão...")
    df = crawler()
    persistencia.grava_pg(df)
    logger.info("Fim da execução!")
    return None

if __name__ == "__main__":
    crawl_insert()