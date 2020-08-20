#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 15:45:47 2020

@author: nathanielruhl

This is a kivy app to learn vocabulary in a foreign language (french is used the development).
"""
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.logger import Logger
from random import randint
from database import DataBase


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

    # it seems like creating and calling '__init__()' upon the 'StoreData()' call makes us lose the user input before storing data, so I'm not using it an anymore to unpack returns from 'loadVocabList()' and 'getOldWord()'... we just have to call the methods when we're in another method.

    def loadVocabList(self):
        frenchList = []
        englishList = []
        synonymList = []
        sentenceList = []
        with open("vocabListApp.txt", "r") as f:
            line = f.readline()
            totalWords = 1
            while line:
                entry = line.split(" &&& ")
                frenchList.append(entry[0])
                englishList.append(entry[1])
                synonymList.append(entry[2])
                sentenceList.append(entry[3])
                line = f.readline()
        return frenchList, englishList, synonymList, sentenceList, totalWords

    def getOldWord(self):
        location = None
        frenchVocabList, englishDefinitionList, synonymList, sentenceList, totalWords = self.loadVocabList()
        for indx, word in enumerate(frenchVocabList):
            if (word == self.frenchWord.text.lower().strip()):
                location = indx
                return frenchVocabList[indx], englishDefinitionList[indx], synonymList[indx], sentenceList[indx], location
        return None, None, None, None, location

    def logOut(self):
        sm.current = "login"

    def storeData(self):
        # I may eventually need to add an if statement for the first time creating the file -- no carriage return / one for each user / begin file with comment line description.
        frenchVocabList, englishDefinitionList, synonymList, sentenceList, totalWords = self.loadVocabList()

        frenchOldWord, englishOldWord, synonymOld, sentenceOld, oldLocation = self.getOldWord()

        if (frenchOldWord == self.frenchWord.text.lower().strip()):
            buttonOverWrite = Button(text="Overwrite existing entry?", size_hint=(None, None), size=(200, 200))
            # buttonIgnore = Button(text="Discard pending entry", size_hint=(None, None), size=(100, 100))
            pop1 = Popup(title='Word already exists!', content=buttonOverWrite, size_hint=(None, None), size=(400, 400))
            buttonOverWrite.bind(on_release=lambda x: self.storeDataOverWrite())
            buttonOverWrite.bind(on_press=pop1.dismiss)
            # buttonIgnore.bind(on_release=pop1.dismiss)
            pop1.open()
            return
        else:
            f = open("vocabListApp.txt", "a+")
            f.write("\n" + self.frenchWord.text.lower().strip() + " &&& " + self.englishWord.text.lower().strip() + " &&& " + self.synonym.text.lower().strip() + " &&& " + self.sentence.text.lower().strip())
            f.close()
            pop2 = Popup(title='Word successfully entered!', size_hint=(None, None), size=(400, 400))
            pop2.open()
            self.reset()
            return

    def storeDataOverWrite(self):
        frenchVocabList, englishDefinitionList, synonymList, sentenceList, totalWords = self.loadVocabList()

        frenchOldWord, englishOldWord, synonymOld, sentenceOld, oldLocation = self.getOldWord()

        with open("vocabListApp.txt", "w+") as f:
            for line in range(len(frenchVocabList)):
                if (line == oldLocation):
                    f.write(self.frenchWord.text.lower().strip() + " &&& " + self.englishWord.text.lower().strip() + " &&& " + self.synonym.text.lower().strip() + " &&& " + self.sentence.text.lower().strip() + "\n")
                else:
                    f.write(frenchVocabList[line] + " &&& " + englishDefinitionList[line] + " &&& " + synonymList[line] + " &&& " + sentenceList[line])
        pop = Popup(title='Word entry overwritten!', size_hint=(None, None), size=(400, 400), on_open=lambda x: self.reset())
        pop.open()

    def reset(self):
        self.frenchWord.text = ""
        self.englishWord.text = ""
        self.synonym.text = ""
        self.sentence.text = ""
        sm.current = "vocab"


class QuizWindow(Screen):
    frenchWordInput = ObjectProperty(None)
    englishQuizWord = StringProperty("")

    def __init__(self, **kwargs):
        super(QuizWindow, self).__init__()
        self.frenchVocabList, self.englishDefinitionList, self.synonymList, self.sentenceList, self.totalWords = self.loadVocabList()
        self.frenchQuizWord, self.englishQuizWord, self.synonymQuiz, self.sentenceQuiz = self.getQuizWord()

    def loadVocabList(self):
        frenchList = []
        englishList = []
        synonymList = []
        sentenceList = []
        with open("vocabListApp.txt", "r") as f:
            line = f.readline()
            totalWords = 1
            while line:
                entry = line.split(" &&& ")
                frenchList.append(entry[0])
                englishList.append(entry[1])
                synonymList.append(entry[2])
                sentenceList.append(entry[3])
                line = f.readline()
                totalWords += 1
        return frenchList, englishList, synonymList, sentenceList, totalWords
    
    def getQuizWord(self):
        indx = randint(0, len(self.frenchVocabList)-1)
        return self.frenchVocabList[indx], self.englishDefinitionList[indx], self.synonymList[indx], self.sentenceList[indx]

    def hintSynonym(self):
        pop = Popup(title='Synonym', content=Label(text=self.synonymQuiz), size_hint=(None, None), size=(400, 400))
        pop.open()

    def hintSentence(self):
        # This will require a more robust algorithm for pronoun contractions and verb conjugations.
        hintSentence = self.sentenceQuiz.replace(self.frenchQuizWord, '[****]')
        pop = Popup(title='Synonym', content=Label(text=hintSentence), size_hint=(None, None), size=(400, 400))
        pop.open()

    def verifyEntry(self):
        if (self.frenchQuizWord.lower()==self.frenchWordInput.text.lower()):
           pop = Popup(title='Correct!', size_hint=(None, None), size=(400, 400))
           pop.open()
        else: # give them 3 tries before showing answer/next word/extra try for misspelling ?
            pop = Popup(title='Incorrect', content=Label(text='The correct answer is "' + self.frenchQuizWord + '".'), size_hint=(None, None), size=(400, 400))
            pop.open()

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

kv = Builder.load_file("vocab.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), OptionWindow(name="options"), WODWindow(name="wod"), VocabWindow(name="vocab"), QuizWindow(name="quiz")]

for screen in screens:
    sm.add_widget(screen)
    
sm.current = "options"

class VocabApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    VocabApp().run()
