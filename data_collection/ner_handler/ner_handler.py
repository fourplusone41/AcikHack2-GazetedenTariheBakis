
# coding: utf-8
# Download zemberek from https://drive.google.com/drive/folders/1FN80VbqesnqU21us4c4Pvgv2VqUsSf2z


from os.path import join
from jpype import JClass, JString, getDefaultJVMPath, shutdownJVM, startJVM


class NER_Handler(object):
    def __init__(self, zmbrk_path = '.'):
        self.zmbrk_path = zmbrk_path
        #ZEMBEREK_PATH: str = join(self.zmbrk_path, 'zemberek-full.jar')

        startJVM(
            getDefaultJVMPath(),
            '-ea',
            '-Djava.class.path=zemberek-full.jar',
            convertStrings=False
        )

    def run(self, text): 
        Paths: JClass = JClass('java.nio.file.Paths')
        TurkishMorphology: JClass=JClass('zemberek.morphology.TurkishMorphology')
        PerceptronNer: JClass=JClass('zemberek.ner.PerceptronNer')

        modelRoot = Paths.get("./ner_handler/enamex_model")
        morphology = TurkishMorphology.createWithDefaults()
        ner = PerceptronNer.loadModel(modelRoot, morphology)


        sentence = text
        result = ner.findNamedEntities(sentence)
        namedEntities = result.getNamedEntities()
        namedEntities2 = {"PERSON": [],
                          "LOCATION": [],
                          "ORGANIZATION": []
                        }
        for i, namedEntity in enumerate(namedEntities):
            ne_tmp = str(namedEntity).strip("]").strip("[").split(" ")
            namedEntities2[ne_tmp[0]].append(" ".join(ne_tmp[1:]))
        
        return namedEntities2

