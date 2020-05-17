# -*- coding: utf-8 -*-
"""
Created on Sat May  9 20:15:19 2020

@author: Bharti Arora
"""

#import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
engine = create_engine("postgres://boaqtdatmuhusp:568946665bde49b4c20c29ab15259a2c9029462c4d92a29fe9aa37c44dcfe580@ec2-50-17-90-177.compute-1.amazonaws.com:5432/dd4t41ubcfugk1")
db = scoped_session(sessionmaker(bind=engine))

def main():
    #f = open("books.csv")
    #reader = csv.reader(f)
    #next(reader)
    #for isbn,title,author,year in reader:
        #db.execute("INSERT INTO books(isbn,title,author,year) VALUES(:isbn,:title,:author,:year)",{"isbn":isbn,"title":title,"author":author,"year":year})
        #db.commit()

    #authors = db.execute("SELECT DISTINCT author FROM books").fetchall()
    #for author in authors:
        #db.execute("INSERT INTO author_score(name) VALUES(:author)",{"author":author[0]})
        #db.commit()
    #result = db.execute("SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_NAME = 'reviews';").fetchall()
    #for results in result:
        #print(results)
    #result = db.execute("SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';").fetchall()
    #db.commit()
    #result = db.execute("SELECT author,isbn,year FROM books where title = :title",{"title":"The Dark Is Rising"}).fetchone()
    #result = db.execute("SELECT A.id FROM users A,login B WHERE A.login_id = B.id AND B.username = :username",{"username":"akshay_99"}).fetchone()
    #results = db.execute("SELECT * FROM reviews ").fetchall()
    #print(results)
    author = "Raymond E. Feist"
    avg = db.execute("SELECT AVG(A.rating) FROM reviews A,books B WHERE A.isbn = B.isbn AND B.author = :author",{"author":author}).fetchone()
    db.execute("UPDATE author_score SET score = :avg WHERE name = :author",{"avg":avg[0],"author":author})
    db.commit()
    results = db.execute("SELECT * FROM author_score WHERE name = :author ",{"author":author}).fetchone()
    print(results)
    #for results in result:
        #print(results)
   

if __name__ == "__main__":
    main()
