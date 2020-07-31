
# coding: utf-8

# In[1]:


from jpype import JClass, JString, getDefaultJVMPath, shutdownJVM, startJVM


# In[2]:


startJVM(
    getDefaultJVMPath(),
    '-ea',
    '-Djava.class.path=zemberek-full.jar',
    convertStrings=False
)


# In[3]:


Paths: JClass = JClass('java.nio.file.Paths')


# In[33]:


modelRoot = Paths.get("./enamex_model")


# In[34]:


TurkishMorphology: JClass=JClass('zemberek.morphology.TurkishMorphology')
PerceptronNer: JClass=JClass('zemberek.ner.PerceptronNer')


# In[35]:


morphology = TurkishMorphology.createWithDefaults();


# In[36]:


ner = PerceptronNer.loadModel(modelRoot, morphology);


# In[65]:


sentence = "Adı ve soyadı: Ramazan Nejdet Sarıkaya. Doğum yeri: İstanbul. Doğum yılı: 1997. Hayatındaki ilk organizasyonu: Düğün"


# In[66]:


result = ner.findNamedEntities(sentence);


# In[67]:


namedEntities = result.getNamedEntities();


# In[68]:


for namedEntity in namedEntities:
    print(namedEntity)

