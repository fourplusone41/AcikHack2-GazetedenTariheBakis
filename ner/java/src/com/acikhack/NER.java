package com.acikhack;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import zemberek.morphology.TurkishMorphology;
import zemberek.ner.NamedEntity;
import zemberek.ner.NerDataSet;
import zemberek.ner.NerDataSet.AnnotationStyle;
import zemberek.ner.NerSentence;
import zemberek.ner.PerceptronNer;
import zemberek.ner.PerceptronNerTrainer;

public class NER {

	public void train_model(Path trainPath, Path testPath, Path modelPath) {

		NerDataSet trainingSet = null;
		NerDataSet testSet = null;
		try {
			trainingSet = NerDataSet.load(trainPath, AnnotationStyle.ENAMEX);
			trainingSet.info(); // prints information
			testSet = NerDataSet.load(testPath, AnnotationStyle.ENAMEX);
			testSet.info();
		} catch (IOException e) {
			System.out.println("1");
			e.printStackTrace();
		}

		TurkishMorphology morphology = TurkishMorphology.createWithDefaults();
		PerceptronNer ner = new PerceptronNerTrainer(morphology).train(trainingSet, testSet, 7, 0.1f);

		try {
			Files.createDirectories(modelPath);
			ner.saveModelAsText(modelPath);
		} catch (IOException e) {
			System.out.println("2");
			e.printStackTrace();
		}

	}

	public void evaluating(Path modelPath, String sentence) {
		TurkishMorphology morphology = TurkishMorphology.createWithDefaults();
		try {
			PerceptronNer ner = PerceptronNer.loadModel(modelPath, morphology);
			NerSentence result = ner.findNamedEntities(sentence);
			List<NamedEntity> namedEntities = result.getNamedEntities();
			for (NamedEntity namedEntity : namedEntities) {
				System.out.println(namedEntity);
			}
		} catch (IOException e) {
			System.out.println("3");
			e.printStackTrace();
		}

	}
}
