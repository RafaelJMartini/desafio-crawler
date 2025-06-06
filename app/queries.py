query = {
    "CREATE_QUOTES":"""
                CREATE TABLE IF NOT EXISTS quotes (
                    id SERIAL PRIMARY KEY,
                    frase TEXT NOT NULL,
                    autor VARCHAR(255)
                );
            """,
    "CREATE_QUOTES_TAGS":"""
                CREATE TABLE IF NOT EXISTS quotes_tags (
                    id SERIAL PRIMARY KEY,
                    quote_id INTEGER NOT NULL,
                    tag_id INTEGER NOT NULL
                );
            """,
    "CREATE_TAGS":"""
                CREATE TABLE IF NOT EXISTS tags (
                    id SERIAL PRIMARY KEY,
                    tag VARCHAR(255)
                );
            """,

    "TRUNCATE_ALL":"TRUNCATE quotes_tags, tags, quotes RESTART IDENTITY CASCADE;",

    "INSERT_QUOTES":"""
                        INSERT INTO quotes (frase, autor)
                        VALUES (:frase, :autor)
                        RETURNING id
                    """,
    "INSERT_TAGS":"""
                        INSERT INTO tags (tag)
                        VALUES (:tag)
                        RETURNING id
                    """,
    "INSERT_QUOTES_TAGS":"""
                            INSERT INTO quotes_tags (quote_id, tag_id)
                            VALUES (:quote_id, :tag_id)
                         """,

    "SELECT_ALL":"""
                SELECT q.frase, q.autor, array_agg(tag.tag ORDER BY tag.tag) AS tags
                    FROM quotes q
                    JOIN quotes_tags t ON q.id = t.quote_id
                    JOIN tags tag ON t.tag_id = tag.id
                    GROUP BY q.id, q.frase, q.autor
                    ORDER BY q.id
                """
}