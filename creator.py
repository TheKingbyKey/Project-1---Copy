# -*- coding: utf-8 -*-
"""
Created on Sat May  9 18:25:54 2020

@author: Bharti Arora
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
engine = create_engine("postgres://boaqtdatmuhusp:568946665bde49b4c20c29ab15259a2c9029462c4d92a29fe9aa37c44dcfe580@ec2-50-17-90-177.compute-1.amazonaws.com:5432/dd4t41ubcfugk1")
db = scoped_session(sessionmaker(bind=engine))

def main():
    #db.execute("CREATE TABLE books(isbn VARCHAR(255) PRIMARY KEY,author VARCHAR(255) NOT NULL,title VARCHAR(255) NOT NULL,year INTEGER NOT NULL);");
    #db.execute("CREATE TABLE login(Id SERIAL PRIMARY KEY ,username VARCHAR(255) NOT NULL,password VARCHAR(255) NOT NULL );");
    #db.execute("CREATE TABLE users(Id SERIAL PRIMARY KEY,login_Id INTEGER NOT NULL,email VARCHAR(255) NOT NULL,name VARCHAR(255) NOT NULL,FOREIGN KEY (login_Id) REFERENCES login (Id) );");
    #db.execute("CREATE TABLE reviews(Id SERIAL PRIMARY KEY,isbn VARCHAR(255) NOT NULL,comment VARCHAR(1000),user_Id INTEGER NOT NULL,rating INTEGER NOT NULL,FOREIGN KEY(user_Id) REFERENCES users(Id),FOREIGN KEY(isbn) REFERENCES books(isbn) );");
    #db.execute("CREATE TABLE collection(Id SERIAL PRIMARY KEY,isbn VARCHAR(255) NOT NULL,catagory VARCHAR(255) NOT NULL,user_Id INTEGER NOT NULL,FOREIGN KEY(user_Id) REFERENCES users(Id),FOREIGN KEY(isbn) REFERENCES books(isbn));")
    #db.execute("CREATE TABLE author_score(Id SERIAL PRIMARY KEY,name VARCHAR(255) NOT NULL,score FLOAT DEFAULT (0) );")
    #db.execute("CREATE TABLE book_score(Id SERIAL PRIMARY KEY,isbn VARCHAR(255) NOT NULL,score FLOAT DEFAULT (0) );")
    login_id = (int)(db.execute("SELECT id FROM login WHERE username = :username ;",{"username":username}).fetchone())
    print(login_id)




if __name__ == "__main__":
    main()
