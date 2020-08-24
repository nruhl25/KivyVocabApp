#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 15:45:47 2020

@author: nathanielruhl

This is a kivy app to learn vocabulary in a foreign language (french is used the development).
"""
import kivy
import pandas as pd
import numpy as np
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.logger import Logger
from kivymd.theming import ThemeManager
from kivy.uix.togglebutton import ToggleButton
from random import randint
from database import DataBase

FileForOverWrite = '' # global scope

class WindowManager(ScreenManager):
    pass


class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)
            
                self.reset()
            
                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()
        
    def login(self):
        self.reset()
        sm.current = "login"
        
    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            VocabWindow.current = self.email.text
            self.reset()
            sm.current = "options"
        else:
            invalidLogin()
            
    def createBtn(self):
        self.reset()
        sm.current = "create"
        
    def reset(self):
        self.email.text = ""
        self.password.text = ""


class OptionWindow(Screen):
    pass


class WODWindow(Screen):
    pass    
  

class VocabWindow(Screen):
    frenchWord = ObjectProperty(None)
    enlgishWord = ObjectProperty(None)
    synonym = ObjectProperty(None)
    sentence = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(VocabWindow, self).__init__()
        # self.add_widget(self.buildToggleBtns())

    def loadVocabList(self):
        frenchList = []
        englishList = []
        synonymList = []
        sentenceList = []
        successList = []
        with open("MasterList.txt", "r") as f:
            line = f.readline()
            totalWords = 1
            while line:
                entry = line.split(" &&& ")
                frenchList.append(entry[0])
                englishList.append(entry[1])
                synonymList.append(entry[2])
                sentenceList.append(entry[3])
                successList.append(entry[4])
                line = f.readline()
                totalWords += 1
        return frenchList, englishList, synonymList, sentenceList, successList, totalWords

    def getOldWord(self):
        location = None
        frenchVocabList, englishDefinitionList, synonymList, sentenceList, successList, totalWords = self.loadVocabList()
        for indx, word in enumerate(frenchVocabList):
            if (word == self.frenchWord.text.lower().strip()):
                location = indx
                return frenchVocabList[indx], englishDefinitionList[indx], synonymList[indx], sentenceList[indx], successList[indx], location
        return None, None, None, None, None, location

    def logOut(self):
        sm.current = "login"

    def storeData(self):
        global FileForOverWrite ## global variable
        if(any([self.frenchWord.text==None, self.englishWord.text==None, self.synonym.text==None, self.sentence.text==None])):
            invalidForm()
            return
        # I may eventually need to add an if statement for the first time creating the file -- one for each user / begin file with comment line description.
        frenchVocabList, englishDefinitionList, synonymList, sentenceList, successList, totalWords = self.loadVocabList()

        frenchOldWord, englishOldWord, synonymOld, sentenceOld, oldSuccess, oldLocation = self.getOldWord()

        frenchVocabList.append(self.frenchWord.text.lower().strip())
        englishDefinitionList.append(self.englishWord.text.lower().strip())
        synonymList.append(self.synonym.text.lower().strip())
        sentenceList.append(self.sentence.text.lower().strip())

        toggleDownList = []
        # is there a cleaner way to do this with list comprehension?
        if self.ids.masterToggle.state == 'down':
            toggleDownList.append(self.ids.masterToggle.text)
        if self.ids.foodToggle.state == 'down':
            toggleDownList.append(self.ids.foodToggle.text)
        if self.ids.expressionToggle.state == 'down':
            toggleDownList.append(self.ids.expressionToggle.text)
        if self.ids.scienceToggle.state == 'down':
            toggleDownList.append(self.ids.scienceToggle.text)

        vocabListNames = []
        if toggleDownList:  # if not empty
            for Toggle in toggleDownList:
                vocabListNames.append(Toggle + "List.txt")
            if (frenchOldWord == self.frenchWord.text.lower().strip()):
                FileForOverWrite = vocabListNames[0] # only overwriting in master
                buttonOverWrite = Button(text="Overwrite existing entry?", size_hint=(None, None), size=(200, 200))
                pop1 = Popup(title='Word already exists!', content=buttonOverWrite, size_hint=(None, None), size=(400, 400))
                buttonOverWrite.bind(on_release=lambda x: self.storeDataOverWrite())
                buttonOverWrite.bind(on_press=pop1.dismiss)
                pop1.open()
                return
            else:
                for filename in vocabListNames:
                    f = open(filename, "a+")
                    f.write(self.frenchWord.text.lower().strip() + " &&& " + self.englishWord.text.lower().strip() + " &&& " + self.synonym.text.lower().strip() + " &&& " + self.sentence.text.lower().strip() + "0" + "\n")
                    f.close()
                pop2 = Popup(title='Word successfully entered!', size_hint=(None, None), size=(400, 400))
                pop2.open()
                self.reset()
                return
        else:
            noToggleError()
            return

    def storeDataOverWrite(self):
        frenchVocabList, englishDefinitionList, synonymList, sentenceList, totalWords = self.loadVocabList()

        frenchOldWord, englishOldWord, synonymOld, sentenceOld, oldSuccess, oldLocation = self.getOldWord()
        with open(FileForOverWrite, "w+") as f:
            for line in range(len(frenchVocabList)):
                if (line == oldLocation):
                    f.write(self.frenchWord.text.lower().strip() + " &&& " + self.englishWord.text.lower().strip() + " &&& " + self.synonym.text.lower().strip() + " &&& " + self.sentence.text.lower().strip() + "0" + "\n")
                else:
                    f.write(frenchVocabList[line] + " &&& " + englishDefinitionList[line] + " &&& " + synonymList[line] + " &&& " + sentenceList[line])
        pop = Popup(title='Word entry overwritten in the Master List!', size_hint=(None, None), size=(400, 400), on_open=lambda x: self.reset())
        pop.open()
        return

    def reset(self):
        self.frenchWord.text = ""
        self.englishWord.text = ""
        self.synonym.text = ""
        self.sentence.text = ""
        self.ids.masterToggle.state = "down"
        self.ids.expressionToggle.state = "normal"
        self.ids.foodToggle.state = "normal"
        self.ids.scienceToggle.state = "normal"
        sm.current = "vocab"

    # not doing it this way at the moment... doing it in the kv file
    def buildToggleBtns(self):
        layout = GridLayout(cols=4)
        layout.add_widget(ToggleButton(text="Master", state="down"))
        layout.add_widget(ToggleButton(text="Expressions"))
        layout.add_widget(ToggleButton(text="Food"))
        layout.add_widget(ToggleButton(text="Science"))
        return layout


class QuizWindow(Screen):
    frenchWordInput = ObjectProperty(None)
    englishQuizWord = StringProperty("")
    numSuccess = StringProperty("")

    def __init__(self, **kwargs):
        super(QuizWindow, self).__init__()
        self.frenchVocabList, self.englishDefinitionList, self.synonymList, self.sentenceList, self.successList, self.totalWords = self.loadVocabList()
        self.indx = randint(0, len(self.frenchVocabList)-1)
        self.frenchQuizWord, self.englishQuizWord, self.synonymQuiz, self.sentenceQuiz, self.numSuccess = self.getQuizWord()

    def loadVocabList(self):
        frenchList = []
        englishList = []
        synonymList = []
        sentenceList = []
        successList = []
        with open("MasterList.txt", "r") as f:
            line = f.readline()
            totalWords = 1
            while line:
                entry = line.split(" &&& ")
                frenchList.append(entry[0])
                englishList.append(entry[1])
                synonymList.append(entry[2])
                sentenceList.append(entry[3])
                successList.append(entry[4])
                line = f.readline()
                totalWords += 1
        return frenchList, englishList, synonymList, sentenceList, successList, totalWords
    
    def getQuizWord(self):
        return self.frenchVocabList[self.indx], self.englishDefinitionList[self.indx], self.synonymList[self.indx], self.sentenceList[self.indx], self.successList[self.indx]

    def hintSynonym(self):
        pop = Popup(title='Synonym', content=Label(text=self.synonymQuiz), size_hint=(None, None), size=(400, 400))
        pop.open()

    def hintSentence(self):
        # test.py contains a possible improvement for strComp()
        # hintSentence = self.sentenceQuiz.replace(self.frenchQuizWord, '[****]')
        hintSentence = sentenceHide(self.sentenceQuiz, self.frenchQuizWord)
        pop = Popup(title='Synonym', content=Label(text=hintSentence), size_hint=(None, None), size=(400, 400))
        pop.open()

    def verifyEntry(self):
        if (self.frenchQuizWord.lower()==self.frenchWordInput.text.lower()):
           pop = Popup(title='Correct!', size_hint=(None, None), size=(400, 400))
           pop.open()
        else: # give them 3 tries before showing answer/next word/extra try for misspelling ?
            pop = Popup(title='Incorrect', content=Label(text='The correct answer is "' + self.frenchQuizWord + '".'), size_hint=(None, None), size=(400, 400))
            pop.open()

    def archiveWord(self):
        with open('ArchivedWords.txt', 'a+') as fa:
            fa.write(self.frenchQuizWord + " &&& " + self.englishQuizWord + " &&& " + self.synonymQuiz + " &&& " + self.sentenceQuiz + " &&& " + self.numSuccess)
        del self.frenchVocabList[self.indx]
        del self.englishDefinitionList[self.indx]
        del self.synonymList[self.indx]
        del self.sentenceList[self.indx]
        del self.successList[self.indx]
        with open("MasterList.txt", "w+") as fm:
            for line in range(len(self.frenchVocabList)):
                fm.write(self.frenchVocabList[line] + " &&& " + self.englishDefinitionList[line] + " &&& " + self.synonymList[line] + " &&& " + self.sentenceList[line] + " &&& " + self.successList[line])
        pop = Popup(title='Word successfully archived.', content=Label(text="You're getting smarter!"), size_hint=(None, None), size=(400, 400))
        pop.open()
        return

    def reset(self):
        self.frenchWordInput.text = ""
        self.__init__()
        sm.current = "quiz"


def invalidLogin():
    pop = Popup(title='Invalid Login', content=Label(text='Invalid username or password'), size_hint = (None, None), size = (400, 400))
    pop.open()
    

def invalidForm():
    pop = Popup(title='Invalid Form', content=Label(text='Please fill in all inputs with valid information.'), size_hint = (None, None), size = (400, 400))
    pop.open()


def noToggleError():
    pop = Popup(title='Invalid Entry', content=Label(text="Plese select at least the 'Master' toggle"), size_hint=(None, None), size=(400, 400))
    pop.open()


def sentenceHide(sentence, vocabWord):
    a = sentence.split(' ')
    # remove french specific articles
    if(vocabWord[0:3] == 'se ' or vocabWord[0:2] == 'un ' or vocabWord[0:3] == 'le ' or vocabWord[0:3] == 'la ' or vocabWord[0:3] == 'de '):
        vocabWord = vocabWord.replace(vocabWord[0:3], '')
    elif(vocabWord[0:4] == 'une ' or vocabWord[0:4] == 'les ' or vocabWord[0:4] == 'des '):
        vocabWord = vocabWord.replace(vocabWord[0:4], '')
    elif(vocabWord[len(vocabWord)-3:len(vocabWord)] == ' de'):
        vocabWord = vocabWord.replace(vocabWord[len(vocabWord)-3:len(vocabWord)], '')
    elif(vocabWord[len(vocabWord)-2:len(vocabWord)] == ' à'):
        vocabWord = vocabWord.replace(vocabWord[len(vocabWord)-2:len(vocabWord)], '')
    for word in a:
        word.lower()
        diff = 0
        if (len(word) <= 3):
            continue
        lastLetter = word[len(word)-1]
        punctuation = ''
        if any([lastLetter == '.', lastLetter == ',', lastLetter == ';', lastLetter == '!', lastLetter == '!']):
            punctuation = lastLetter
            diff = -1
        if (("'" == word[1]) and (word[2:4] == vocabWord[0:2])):
            shorter = word if len(word) <= (len(vocabWord)-2) else vocabWord
            diff += sum([vocabWord[i] != word[2+i]
                         for i in range(len(shorter)-2)])
            if(diff <= 2):
                return sentence.replace(word, '[****]' + punctuation)
            else:
                continue
        else:
            shorter = word if len(word) <= len(vocabWord) else vocabWord
            diff += sum([vocabWord[i] != word[i] for i in range(len(shorter))])
            if(diff <= 2):
                return sentence.replace(word, '[****]' + punctuation)
            else:
                continue
    return sentence

kv = Builder.load_file("vocab.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), OptionWindow(name="options"), WODWindow(name="wod"), VocabWindow(name="vocab"), QuizWindow(name="quiz")]

for screen in screens:
    sm.add_widget(screen)
    
sm.current = "options"

class VocabApp(App):
    def build(self):
        # theme_cls = ThemeManager()
        return sm

if __name__ == "__main__":
    VocabApp().run()
