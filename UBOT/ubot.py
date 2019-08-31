#General Libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import re
import aiml
import subprocess
import os
import argparse
from MyKernel import MyKernel
from time import sleep
#end of general libraries
import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
from kivy.core.window import Window

#Graphics library
import kivy
import random
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.widget import Widget

from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.properties import (StringProperty, ObjectProperty, OptionProperty,NumericProperty, ListProperty)
from kivy.core.window import Window
Window.clearcolor = (0, 102, 255, 1)

import time, threading
#end of Graphics libraries

DEBUG = True
SHOW_MATCHES = True

def course_code(sentence):
	try:
		words = re.compile('\w+').findall(sentence)
		new_sentence = ""
		for index, word in enumerate(words):
			if (word == "cs") and (index < len(words)-1) and (words[index+1].isdigit()):
				new_sentence = new_sentence + word
			else:
				new_sentence = new_sentence + word + " "
		return new_sentence
	except:
		return sentence

def remove_aiml_char(sentence):
    try:
        new_sentence = sentence.replace("_","")
        new_sentence = new_sentence.replace("*","")
        return new_sentence
    except:
        return sentence

dict = {'NN': 'NOUN', 'JJ': 'ADJ'}
dict['NNS'] = 'NOUN'
dict['NNP'] = 'NOUN'
dict['NNPS'] = 'NOUN'
dict['PRP'] = 'NOUN'
dict['PRP$'] = 'NOUN'
dict['RB'] = 'ADV'
dict['RBR'] = 'ADV'
dict['RBS'] = 'ADV'
dict['VB'] = 'VERB'
dict['VBD'] = 'VERB'
dict['VBG'] = 'VERB'
dict['VBN'] = 'VERB'
dict['VBP'] = 'VERB'
dict['VBZ'] = 'VERB'
dict['WRB'] = 'ADV'

grade_codes = ["ap","aa","ab","bb","bc","cc","cd","dd","dx","fr"]

BOT_INFO = {
    "name": "UBOT",
    "birthday": "May 5th 2018",
    "location": "Pantnagar",
    "master": "I have no Master",
    "website":"follow me on twitter",
    "gender": "Female",
    "age": "20",
    "size": "",
    "religion": "Humanity",
    "party": "All night !"
}

k = MyKernel()
k.learn("aiml/standard/std-startup.xml")
k.respond("LOAD AIML B")

for key,val in BOT_INFO.items():
	k.setBotPredicate(key,val)

class PopupBox(ModalView):
   

    title = StringProperty('No title')
    

    title_size = NumericProperty('14sp')
    

    title_align = OptionProperty('left',
                                 options=['left', 'center', 'right', 'justify'])
    
    title_font = StringProperty('Roboto')
    
    content = ObjectProperty(None)
    
    title_color = ListProperty([1, 1, 1, 1])
    
    separator_color = ListProperty([47 / 255., 167 / 255., 212 / 255., 1.])
    

    separator_height = NumericProperty('2dp')
    
    _container = ObjectProperty(None)

class UBOTApp(App):
# layout
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.lbl1 = Label(text="UBOT:   Welcome ask me any college or admission related queries ",size_hint=(1,0.33),
        	color=(255,255,255,1),multiline=True,font_size=15,text_size=(880,550),halign='left',valign='top')
        layout.add_widget(self.lbl1)
        layout2 = BoxLayout(size_hint=(1,0.05))
        self.txt1 = TextInput(text='',size_hint=(0.1,1),font_size=20)
        layout2.add_widget(self.txt1)
        self.btn1 = Button(text="Submit",size_hint=(0.1,1))
        self.btn1.bind(on_press=self.buttonClicked)
        # self.btn1.bind(on_press=self.open_popup)
        layout2.add_widget(self.btn1)
        layout.add_widget(layout2)
            
        return layout

    def show_popup(self):
        print "hi"
        content=Label(text="thinking")
        self.pop_up = Popup(title='Test popup',
                  size_hint=(None, None), size=(256, 256),
                  content=content, disabled=True)
        self.pop_up.open()

  


    def dismiss_popup(self):
        print "closing"
        self.pop_up.dismiss()

    def buttonClicked(self,button):
        UBOTinput = self.txt1.text
        self.lbl1.text = self.lbl1.text + "\nUser:   "+UBOTinput
        sentence = UBOTinput.lower()
        sentence = course_code(sentence)
        stop_words = set(stopwords.words('english'))

        word_tokens = word_tokenize(sentence)

        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        temp = nltk.pos_tag(filtered_sentence)
        new_sentence = ""
        for i in temp:
            try:
                z = i[1]
                if (dict[z] != None):
                    part_speech = dict[z]
                else:
                    part_speech = 'NOUN'

                if(part_speech == 'NOUN'):
                    word = wn.morphy(i[0],wn.NOUN)
                elif(part_speech == 'VERB'):
                    word = wn.morphy(i[0],wn.VERB)
                elif(part_speech == 'ADV'):
                    word = wn.morphy(i[0],wn.ADV)
                elif(part_speech == 'ADJ'):
                    word = wn.morphy(i[0],wn.ADJ)
                word1 = wn.synsets(word)[0].lemmas()[0].name()
                if i[0] in grade_codes:
                    word1 = i[0]
            except:
                word1 = i[0]
            new_sentence = new_sentence+" "+word1.lower()
            new_sentence = remove_aiml_char(new_sentence)

        #----------uncomment to debug----------------------
        if DEBUG:
            #printing first output
            matchedPattern = k.matchedPattern(UBOTinput)
            response = k.respond(UBOTinput)
            try:
                if SHOW_MATCHES:
                    print "Matched Pattern: "
                    print k.formatMatchedPattern(matchedPattern[0])
                    pattern = k.getPredicate("topic",'_global')
                    print "TOPIC:",pattern
                else:
                    print "-------------------------"
            except:
                print "No match found"
            print "Normal Response: ",response

            # printing after processing
            print "--------------------------------"
            print "new_sentence :",new_sentence
            matchedPattern = k.matchedPattern(new_sentence)
            response = k.respond(new_sentence)
            try:
                if SHOW_MATCHES:
                    print "Matched Pattern: "
                    print k.formatMatchedPattern(matchedPattern[0])
                    pattern = k.getPredicate("topic",'_global')
                    print "TOPIC:",pattern
                else:
                    print "-------------------------"
            except:
                print "No match found"
            print "New Response: ",response

        #--------------------------------------------------
        response = k.respond(UBOTinput)
        response1 = k.respond(new_sentence)
        if response1 != "" and response1[0] == '$':
            response = response1[1:]
        
        self.lbl1.text = self.lbl1.text + "\nUBOT:   "+response+"\n"
        self.txt1.text = ""
        
UBOTApp().run()
