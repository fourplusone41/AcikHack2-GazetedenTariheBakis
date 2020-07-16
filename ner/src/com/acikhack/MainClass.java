package com.acikhack;

import java.nio.file.Path;
import java.nio.file.Paths;

public class MainClass {

	public static void main(String[] args) {
		
		NER ner = new NER();
		
		Path trainPath = Paths.get("./enamex_train.txt");
		Path testPath = Paths.get("./enamex_test.txt");
		Path modelPath = Paths.get("./model");
		
		//ner.train_model(trainPath, testPath, modelPath);
		String sentence = "Ramazan Nejdet Sarıkaya, Yozgat";
		ner.evaluating(modelPath, sentence);
		}

}
