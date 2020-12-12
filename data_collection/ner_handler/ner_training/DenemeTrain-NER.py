
# coding: utf-8

# In[3]:


from jpype import JClass, JString, getDefaultJVMPath, shutdownJVM, startJVM


# In[5]:


startJVM(
    getDefaultJVMPath(),
    '-ea',
    '-Djava.class.path=zemberek-full.jar',
    convertStrings=False
)


# In[6]:


Paths: JClass = JClass('java.nio.file.Paths')


# In[39]:


trainPath = Paths.get("./enamex_train.txt")
testPath = Paths.get("./enamex_test.txt")
modelRoot = Paths.get("./enamex_model")


# In[42]:


NerDataSet: JClass=JClass('zemberek.ner.NerDataSet')
AnnotationStyle: JClass=JClass('zemberek.ner.NerDataSet.AnnotationStyle')
TurkishMorphology: JClass=JClass('zemberek.morphology.TurkishMorphology')
PerceptronNerTrainer: JClass=JClass('zemberek.ner.PerceptronNerTrainer')


# In[43]:


trainingSet = NerDataSet.load(trainPath, AnnotationStyle.ENAMEX);


# In[44]:


trainingSet.info()


# In[45]:


testSet = NerDataSet.load(testPath, AnnotationStyle.ENAMEX);


# In[46]:


testSet.info()


# In[47]:


morphology = TurkishMorphology.createWithDefaults();


# In[48]:


morphology.toString()


# In[49]:


ner = PerceptronNerTrainer(morphology).train(trainingSet, testSet, 7, 0.1);


# In[50]:


ner.saveModelAsText(modelRoot);

