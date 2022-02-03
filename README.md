# Interactive Dashboards with App live data

The ultimate goal of this project is to get a pipeline that requests live data from the server, aggregates it and pushes the results to a website / git repo / app so that the users and interested people can always have a look on the live data.
As the connection to a frozen view of the *TYT* database is already established, we start with the *TYT* project.

## Setup

To connect to the remote database via ssh tunnel create a `.env` file in the same directory as the `db_connection.py` python script ([./src/utils](./src/utils)).

The resulting file (`./src/utils/.env`) must have the following content:

```txt
ssh_host = ???
ssh_username = ???
ssh_password = ???
database_username = ???
database_password = ???
database_name = ???
localhost = ???
```

You need to replace the `???` with the appropriate credentials and information to establish a database connection.

**Note that `.env` files are excluded from *Git* via the `.gitignore` ([.gitignore](./.gitignore)) to keep the credentials private.**

## Techstack-Idee

1. .csv-raw einlesen und mit Pandas aggregieren
2. Aggregierte Werte in [HTML template](https://getbootstrap.com/docs/5.1/examples/) einbauen
3. Fertige HTML Datei lokal mit Datum und Projekt speichern
4. Upload einer HTML Datei mit FTP -  [File Transfer Protocol](https://docs.python.org/3/library/ftplib.html)

SideNotes:

* Rüdiger muss Server bereitstellen, der die HTML Datei hostet

## TYT Dashboard

## Start Server

Run from project root folder.

```bash
npx http-server ./www --cors=capacitor://localhost --cors=http://localhost -c-1
```
