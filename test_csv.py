import pandas as pd

# When using the pandas method in Class.loadData():

# masterDF = pd.read_csv('MasterList.csv', sep='|')
# frenchList = masterDF['French Word'].values
# englishList = masterDF['English Word'].values
# synonymList = masterDF['Synonym'].values
# sentenceList = masterDF['Sentence'].values
# totalWords = len(frenchList)

# Code for appending to a numpy array

# np.append(frenchVocabList, self.frenchWord.text.lower().strip(), axis=None)
# np.append(englishDefinitionList, self.englishWord.text.lower().strip(), axis=None)
# np.append(synonymList, self.synonym.text.lower().strip(), axis=None)
# np.append(sentenceList, self.sentence.text.lower().strip(), axis=None)

# Code for reading and appending to csv file in VocabWindow.storeData()

# masterDF = pd.read_csv('MasterList.csv', sep='|')
# dict = {'French Word': [self.frenchWord.text.lower().strip()],
#         'English Word': [self.englishWord.text.lower().strip()], 'Synonym': [self.synonym.text.lower().strip()], 'Sentence': [self.sentence.text.lower().strip()]}
# newDF = pd.DataFrame(dict)
# dfMasterNew = masterDF.append(newDF, ignore_index=True)
# dfMasterNew.to_csv('MasterList.csv', index=False, sep='|')



