# Interactive Dashboards with App live data

The ultimate goal of this project is to get a pipeline that requests live data from the server, aggregates it and pushes the results on a website / git repo / app so that the users and interested people can always have a look on the live data.
As the connection to a frozen view of the TYT database is already established, we start with the TYT project.

## Create a connection to a database

In `src/DBConnection` there is a `.env` file that contains the credentials to the database you want to connect to.
You need to fill in there your credentials and add the file to `.gitignore` to keep your credentials private.

### Setup

Create a `.env` file (no filename, just the extension) in the same directory as the python script `dbConnection.py`.

```txt
ssh_host = ???
ssh_username = ???
ssh_password = ???
database_username = ???
database_password = ???
database_name = ???
localhost = ???
```

## Techstack-Idee

1. .csv-raw einlesen und mit Pandas aggregieren
2. Aggregierte Werte in [HTML template](https://getbootstrap.com/docs/5.1/examples/) einbauen
3. Fertige HTML Datei lokal mit Datum und Projekt speichern
4. Upload einer HTML Datei mit FTP -  [File Transfer Protocol](https://docs.python.org/3/library/ftplib.html)

SideNotes:

* Rüdiger muss Server bereitstellen, der die HTML Datei hostet

## TYT Dashboard
