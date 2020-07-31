
# coding: utf-8


from jpype import JClass, JString, getDefaultJVMPath, shutdownJVM, startJVM

startJVM(
    getDefaultJVMPath(),
    '-ea',
    '-Djava.class.path=zemberek-full.jar',
    convertStrings=False
)

Paths: JClass = JClass('java.nio.file.Paths')


modelRoot = Paths.get("./enamex_model")


TurkishMorphology: JClass=JClass('zemberek.morphology.TurkishMorphology')
PerceptronNer: JClass=JClass('zemberek.ner.PerceptronNer')

morphology = TurkishMorphology.createWithDefaults()


ner = PerceptronNer.loadModel(modelRoot, morphology)


sentence = "Adı ve soyadı: Ramazan Nejdet Sarıkaya. Doğum yeri: İstanbul. Doğum yılı: 1997. Hayatındaki ilk organizasyonu: Düğün"


result = ner.findNamedEntities(sentence)

namedEntities = result.getNamedEntities()



for namedEntity in namedEntities:
    print(namedEntity)

