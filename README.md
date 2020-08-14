### **Türkçe** | [English](README_EN.md)


# GazetedenTariheBakis

Bu projenin amacı [Istanbul Gazeteden Tarihe Bakış](http://nek.istanbul.edu.tr:4444/ekos/GAZETE/) veriseti kullanılarak arama yapılabilir bir veritabanı sağlamaktır.

# Sunum

[![GazetedenTariheBakisSunum](https://repository-images.githubusercontent.com/278169737/5daa1e80-c471-11ea-8709-340db5722341)](https://drive.google.com/drive/folders/1rt_3-kap5ZYuraF9OzHfIbGdalhK2rK5)

# Demo

[![FourPlusOne | Gazeteden Tarihe Bakış | AçıkHack2 | NoAudio](https://img.youtube.com/vi/xED-qn6rsiQ/0.jpg)](https://www.youtube.com/embed/xED-qn6rsiQ)

# Mimari

* `docker-compose`yapısı, 4 farklı dockerize edilmiş servis içermektedir. Bunlar,
    * Kalıcı depolama için CouchDB Veritabanı. (Port 5984)
    * Bir arama motoru olarak Elasticsearch. (Port 9200)
    * Bize özel bir RESTful API. (Port 4000)
    * Bir web tabanlı kullanıcı arayüzü (GUI). (Port 3000)
    
* `data_collection` komut dosyası şu işlemleri gerçekleştirmektedir,
    * Veriseti olarak kullanılan web sitesinden veri bilgilerini alır (web scraping).
    * Alınan bilgiler ile veriyi indirir.
    * PDF sayfalarını ayıklamak ve temizlemek için PDF üzerinde işlemler gerçekleştirir.
    * OCR işlemini gerçekleştirir.
    * NER işlemini gerçekleştirir.
    * Verileri CouchDB Veritabanına kayıt eder.
    * Elasticsearch üzerinde verileri indexler.
  
* Kullanılan API, hem orijinal taramaları hem de OCR sonuçlarını elde ederek, verileri, veritabanında tarihe ve konuma göre sorgulamaya imkan sağlar ve Elasticsearch kullanarak bir tam metin araması yapılmasına izin verir.

* Web tabanlı oluşturulan kullanıcı arayüzü, verileri sorgulamak ve sonuçları görselleştirmek için kullanıcı dostu bir yol sunar.

# Kullanım

Docker kurun [Install Docker Engine](https://docs.docker.com/engine/install/).

    sudo apt install python3-dev
    sudo apt install libtesseract-dev tesseract-ocr tesseract-ocr-tur

Elasticsearch, CouchDB, API ve arayüzü ortamlarını çalıştırın

    cd docker-compose
    docker-compose up -d

NER alt modülü için en yeni `zemberek_full.jar` dosyasını [buradan](https://drive.google.com/drive/folders/1FN80VbqesnqU21us4c4Pvgv2VqUsSf2z) indirin.
İndirilen `.jar` dosyasını, `data_collection` dizini altına ekleyin.

`data_collection` komut dosyasını çalıştırın.

    cd data_collection
    pip3 install -r requirements.txt
    python3 main.py

Sorgular yapmak için, `localhost:3000/` adresine gidin ve kullanıcı arayüzünü kullanarak sorgularınızı gerçekleştirin.

# Kullanılan Açık Kaynak Kodları

- [Zemberek-nlp](https://github.com/ahmetaa/zemberek-nlp) : Apache-2.0
- [Tesseract](https://github.com/tesseract-ocr/tesseract) : Apache-2.0
- [CouchDB](https://github.com/apache/couchdb) : Apache-2.0
- [Elasticsearch](https://github.com/elastic/elasticsearch) : Apache-2.0
- [Docker](https://github.com/docker/docker-ce) : Apache-2.0
- [Opencv](https://github.com/opencv/opencv) : BSD-3

# Citation

IEEE Open Access'te yayınlamak amacıyla yazılmakta olan makalemiz:

    @ARTICLE{8768370,
    author={H. {Menhour}, R. N. {Sarikaya}, M. {Aktaş},  R. {Sağlam},  H. B. {Şahin},  E. {Ekinci} and S. {Eken}},
    journal={IEEE Access},
    title={Searchable Turkish OCRed Historical Newspaper Collection 1928–1942},
    year={},
    month={},
    volume={},
    number={},
    pages={},
    keywords={Historical  newspapers,  optical  character  recognition,  name  entity  recognition,  microservices, data journalism, full text search, visualization.},
    doi={},
    ISSN={},}
