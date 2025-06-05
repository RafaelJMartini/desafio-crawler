import pandas as pd
from sqlalchemy import create_engine, text
import os
import logging
from dotenv import load_dotenv
from app.tests import test_engine,test_dotenv
logger = logging.getLogger(__name__)



class Persistencia:
    def __init__(self):
        load_dotenv()
        test_dotenv()
        engine = create_engine(
            f"postgresql+psycopg2://{os.getenv('USER')}:{os.getenv('PW')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB_NAME')}"
        )
        test_engine(engine)
        self.engine = engine

    def criar_tabelas(self):

        with self.engine.connect() as conn:

            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS quotes (
                    id SERIAL PRIMARY KEY,
                    frase TEXT NOT NULL,
                    autor VARCHAR(255)
                );
            """))

            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS quotes_tags (
                    id SERIAL PRIMARY KEY,
                    quote_id INTEGER NOT NULL,
                    tag_id INTEGER NOT NULL
                );
            """))

            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS tags (
                    id SERIAL PRIMARY KEY,
                    tag VARCHAR(255)
                );
            """))

            conn.commit()
            logger.info("Tabela verificada/criada.")

    def grava_pg(self,df: pd.DataFrame) -> None:

        logger.info("Verificando tabelas do banco...")
        self.criar_tabelas()

        logger.info("Inserindo Dataframe...")
        with self.engine.begin() as conn:
            logger.info("Limpando banco de dados...")
            conn.execute(text("TRUNCATE quotes_tags, tags, quotes RESTART IDENTITY CASCADE;"))
            for _, row in df.iterrows():
                quote_id = conn.execute(
                    text("""
                        INSERT INTO quotes (frase, autor)
                        VALUES (:frase, :autor)
                        RETURNING id
                    """),
                    {"frase" : row['frase'], "autor" : row['autor']}
                ).scalar()

                for tag in row['tags']:

                    tag_result = conn.execute(
                        text("SELECT id FROM tags WHERE tag = :tag"),
                        {"tag": tag}
                    ).scalar()

                    if not tag_result:
                        tag_result = conn.execute(
                            text("""
                                            INSERT INTO tags (tag)
                                            VALUES (:tag)
                                            RETURNING id
                                        """),
                            {"tag": tag}
                        ).scalar()

                    tag_id = tag_result

                    conn.execute(
                        text("""
                                        INSERT INTO quotes_tags (quote_id, tag_id)
                                        VALUES (:quote_id, :tag_id)
                                    """),
                        {"quote_id": quote_id, "tag_id": tag_id}
                    )

        logger.info("Dataframe inserido com sucesso")

    def consulta_df(self) -> pd.DataFrame:
        with self.engine.connect() as conn:


            dados = conn.execute(
                text("""
                SELECT q.frase, q.autor, array_agg(tag.tag ORDER BY tag.tag) AS tags
                    FROM quotes q
                    JOIN quotes_tags t ON q.id = t.quote_id
                    JOIN tags tag ON t.tag_id = tag.id
                    GROUP BY q.id, q.frase, q.autor
                    ORDER BY q.id
                """)
            )

            df = pd.DataFrame(dados.fetchall())
        return df