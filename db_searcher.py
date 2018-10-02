#!/usr/bin/env python

import psycopg2

# added a variable for easy access to the database name
DBNAME = "news"


def popular_articles():

    """Prints a list of the top 3
    most popular articles of all time"""
    article_search = """SELECT title, count(*) AS num
                        FROM log,articles
                        WHERE '/article/' || articles.slug = log.path
                        GROUP BY title
                        ORDER BY num DESC
                        LIMIT 3;"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(article_search)
    titles = c.fetchall()
    print ("Most Popular Articles All-time")
    print ("  ")
    for title, views in titles:
        print('\"{}\" -- {} views\n'.format(title, views))
     
    db.close()


def popular_authors():
    """Second function prints the most popular
    authors in descending order by popularity"""
    author_search = """SELECT name, count(*) AS num
                       FROM articles
                       INNER JOIN authors
                       ON articles.author = authors.id
                       INNER JOIN log
                       ON '/article/' || articles.slug = log.path
                       GROUP BY name
                       ORDER BY num DESC;"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(author_search)
    authors = c.fetchall()
    print ("Most Popular Authors All-time")
    print ("  ")
    for author, views in authors:
        print('\"{}\" -- {} views\n'.format(author, views))
        
    db.close()


def most_errors():
    """Third function prints out dates that had errors totaling more than 1%"""
    error_search = """ SELECT vWtest.date,
                       ROUND(vWtest.errors * 100.0 / vWtest2.requests)
                       AS percent FROM vWtest
                       LEFT JOIN vWtest2
                       ON vWtest.date = vWtest2.date
                       WHERE vWtest.errors * 100.0 / vWtest2.requests > 1.0;
                   """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(error_search)
    dates = c.fetchall()
    print ("Dates Where Errors Totaled More Than 1%")
    print ("  ")
    for date, percent in dates:
        print ('\"{}\" -- {} percent\n'.format(date, percent))
        
    db.close()

if __name__ == '__main__':
    popular_articles()
    popular_authors()
    most_errors()
