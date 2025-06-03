import pandas as pd
from sqlalchemy import create_engine, text
import os
import logging
from dotenv import load_dotenv
logger = logging.getLogger(__name__)
load_dotenv()

required_envs = ['USER', 'PW', 'HOST', 'PORT', 'DB_NAME']
missing = [var for var in required_envs if not os.getenv(var)]

if missing:
    raise EnvironmentError(f"Variáveis de ambiente ausentes: {', '.join(missing)}")

def test_engine(engine):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # Teste simples
            logger.info("Conectado ao banco de dados com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")

def criar_tabelas(engine):

    with engine.connect() as conn:

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

def grava_pg(df: pd.DataFrame) -> None:

    engine = create_engine(f"postgresql+psycopg2://{os.getenv('USER')}:{os.getenv('PW')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB_NAME')}")
    logger.info("Testando conexão com o banco de dados.")
    test_engine(engine)

    logger.info("Verificando tabelas do banco...")
    criar_tabelas(engine)

    logger.info("Inserindo Dataframe...")
    with engine.connect() as conn:
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
        conn.commit()
        conn.close()

    logger.info("Dataframe inserido com sucesso")