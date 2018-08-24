import os
import psycopg2
from connect import conn

cur = conn.cursor()

def create_users_table():
    # Create users table
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("CREATE TABLE users(id serial PRIMARY KEY, username varchar, \
    email varchar, password varchar);")
    
    print("Table Users Successfully Created")
    conn.commit()

def create_questions_table():
    # Create questions table
    cur.execute("DROP TABLE IF EXISTS questions")
    cur.execute("CREATE TABLE questions(id serial PRIMARY KEY, title varchar, \
    body varchar, created_by varchar, user_id integer);")
    
    print("Table Questions Successfully Created")
    conn.commit()

def create_answers_table():
    # Create answers table
    cur.execute("DROP TABLE IF EXISTS answers")
    cur.execute("CREATE TABLE answers(id serial PRIMARY KEY, body varchar, \
    answered_by varchar, question_id integer, user_id integer);")
    
    print("Table Answers Successfully Created")
    conn.commit()

create_users_table()
create_questions_table()
create_answers_table()