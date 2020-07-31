### **English** | [Türkçe](README.md)


# GazetedenTariheBakis

The aim of this project is to provide a searchable database based on the [Istanbul Gazeteden Tarihe Bakış](http://nek.istanbul.edu.tr:4444/ekos/GAZETE/) Dataset.

# Architecture

* The `docker-compose` backend contains 4 different dockerized services:
    * CouchDB Database for persistant storage.
    * Solr as a search engine.
    * Our custom RESTful API.
    * A web based GUI.

* The `data_collection` script does the following
    * Scraping the dataset website
    * Downloading the data
    * Processes the PDFs to extract and clean single pages
    * Performing OCR
    * Performing NER
    * Storing data in CouchDB
    * Indexing data in Solr

* The API allows for querying the data by date and location in the database as well as full text search using Solr, providing both the original scans as well as the OCR results.

* The web GUI offers a user friendly way to query the data and visualize the results.

# Usage

Install requirements

    sudo apt install python3-dev
    sudo apt install libtesseract-dev tesseract-ocr tesseract-ocr-tur

Run Solr and CouchDB stack

    cd docker-compose
    docker-compose up -d

Download the latest `zemberek_full.jar` for NER submodule from this [link](https://drive.google.com/drive/folders/1FN80VbqesnqU21us4c4Pvgv2VqUsSf2z)
Place the downloaded `.jar` in `data_collection`

Run data collection script

    cd data_collection
    pip3 install -r requirements.txt
    python 3 main.py

Browse to `localhost:5000/main` and use the UI for queries.

# TODO
* Use multithreading to speed up data_collection and processing.
* Improve UI design using `bootstrap`.
