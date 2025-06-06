from app.tests import test_engine,test_dotenv
from app.queries import query
import pandas as pd
from sqlalchemy import create_engine, text
import os
import logging
from dotenv import load_dotenv


logger = logging.getLogger(__name__)

class Persistencia:
    def __init__(self):
        load_dotenv()
        test_dotenv()
        engine = create_engine(
            f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )
        test_engine(engine)
        self.engine = engine

    def criar_tabelas(self):

        with self.engine.connect() as conn:

            conn.execute(text(query["CREATE_QUOTES"]))
            conn.execute(text(query["CREATE_QUOTES_TAGS"]))
            conn.execute(text(query["CREATE_TAGS"]))

            conn.commit()
            logger.info("Tabela verificada/criada.")

    def grava_pg(self,df: pd.DataFrame) -> None:

        logger.info("Verificando tabelas do banco...")
        self.criar_tabelas()

        logger.info("Inserindo Dataframe...")
        with self.engine.begin() as conn:
            logger.info("Limpando banco de dados...")
            conn.execute(text(query["TRUNCATE_ALL"]))

            for _, row in df.iterrows():
                quote_id = conn.execute(
                    text(query["INSERT_QUOTES"]),
                    {"frase" : row['frase'], "autor" : row['autor']}
                ).scalar()

                for tag in row['tags']:
                    tag_result = conn.execute(
                        text("SELECT id FROM tags WHERE tag = :tag"),
                        {"tag": tag}
                    ).scalar()

                    if not tag_result:
                        tag_result = conn.execute(
                            text(query["INSERT_TAGS"]),
                            {"tag": tag}
                        ).scalar()

                    tag_id = tag_result

                    conn.execute(
                        text(query["INSERT_QUOTES_TAGS"]),
                        {"quote_id": quote_id, "tag_id": tag_id}
                    )

        logger.info("Dataframe inserido com sucesso")

    def consulta_df(self) -> pd.DataFrame:
        self.criar_tabelas()
        with self.engine.connect() as conn:

            dados = conn.execute(
                text(query["SELECT_ALL"])
            )

            df = pd.DataFrame(dados.fetchall())
        return df