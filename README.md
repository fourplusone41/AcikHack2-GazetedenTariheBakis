### **Türkçe** | [English](README_EN.md)


# GazetedenTariheBakis

Bu projenin amacı "Istanbul Gazeteden Tarihi Bakış" veriseti kullanılarak arama yapılabilir bir veritabanı sağlamaktır.

# Mimari

* `docker-compose`yapısı, 4 farklı dockerize edilmiş servis içermektedir. Bunlar,
    * Kalıcı depolama için CouchDB Veritabanı.
    * Bir arama motoru olarak Solr.
    * Bize öel bir RESTful API.
    * Bir web tabanlı kullanıcı arayüzü (GUI).
    
* `data_collection` komut dosyası şu işlemleri gerçekleştirmektedir,
    * Veriseti olarak kullanılan web sitesinden veri bilgilerini alır (web scraping).
    * Alınan bilgiler ile veriyi indirir.
    * PDF sayfalarını ayıklamak ve temizlemek için PDF üzerinde işlemler gerçekleştirir.
    * OCR işlemini gerçekleştirir.
    * NER işlemini gerçekleştirir.
    * Verileri CouchDB Veritabanına kayıt eder.
    * Solr üzerinde verileri indexler.
  
* Kullanılan API, hem orijinal taramaları hem de OCR sonuçlarını elde ederek, verileri, veritabanında tarihe ve konuma göre sorgulamaya imkan sağlar ve Solr kullanarak bir tam metin araması yapılmasına izin verir.

* Web tabanlı oluşturulan kullanıcı arayüzü, verileri sorgulamak ve sonuçları görselleştirmek için kullanıcı dostu bir yol sunar.

# Kullanım

Kurulum gereksinimleri,

    sudo apt install python3-dev
    sudo apt install libtesseract-dev tesseract-ocr tesseract-ocr-tur

Solr ve CouchDB ortamlarını çalıştırın,

    cd docker-compose
    docker-compose up -d

NER alt modülü için en yeni `zemberek_full.jar`dosyasını [buradan](https://drive.google.com/drive/folders/1FN80VbqesnqU21us4c4Pvgv2VqUsSf2z) indirin.
İndirilen `.jar` dosyasını, `data_collection` dizini altına ekleyin.

`data_collection` komut dosyasını çalıştırın.

    cd data_collection
    pip3 install -r requirements.txt
    python 3 main.py

Sorgular yapmak için, `localhost:5000` adresine gidin ve kullanıcı arayüzünü kullanarak sorgularınızı gerçekleştirin.

# TODO
* Veri toplama ve işlemeyi hızlandırmak için çoklu iş parçacığı kullanın.
* Kullanıcı arayüzünü geliştirmek için `bootstrap` kullanın.

