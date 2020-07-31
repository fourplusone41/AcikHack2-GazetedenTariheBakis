### **English** | [Türkçe](README.md)


# GazetedenTariheBakis

The aim of this project is to provide a searchable database based on the "Istanbul Gazeteden Tarihi Bakış" Dataset.

# Architecture

*
*
*

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

Browse to `localhost:5000` and use the UI for queries.