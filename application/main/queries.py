'''
Querying the database
'''
query1 = """
    INSERT INTO questions(topic,title, description, owner, answers)
    VALUES(%s, %s, %s, %s, %s) RETURNING id
    """

query2 = """
    CREATE TABLE IF NOT EXISTS users(
    id serial PRIMARY KEY, name VARCHAR,
    username VARCHAR, email VARCHAR,
    password VARCHAR, confirm_password VARCHAR
    )
    """
query3 = """
    CREATE TABLE IF NOT EXISTS questions(
    id serial PRIMARY KEY,topic VARCHAR,
    title VARCHAR, description VARCHAR,
    owner INTEGER,
    answers INTEGER,
    FOREIGN KEY (owner) REFERENCES users(id) ON DELETE CASCADE
    )
    """

query4 = """
    CREATE TABLE IF NOT EXISTS answers(
    id serial PRIMARY KEY,
    answer VARCHAR, accepted BOOL,
    owner INTEGER REFERENCES users(id) ON DELETE CASCADE,
    question INTEGER REFERENCES questions(id) ON DELETE CASCADE,

    )
    """
