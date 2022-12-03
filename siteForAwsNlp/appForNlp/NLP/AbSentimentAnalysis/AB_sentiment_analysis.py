# !/usr/bin/env python
# coding: utf-8

# In[8]:

import spacy
from googletrans import Translator
import os


# recebe um texto e retorna um dicionário com os substantivos e o sentimento deles
def feature_sentiment(Frase, lang = "en"):

    # BUG: pip install -r requirements faz python -m spacy download en_core_web_sm
    nlp=spacy.load("en_core_web_sm")

    # Com base em Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews."
    # Criamos duas listas com palavras positivas e negativas
    pathPos = os.getcwd() + '/appForNlp/NLP/AbSentimentAnalysis/positive-words.txt'
    with open(pathPos, 'r') as f:
        pos_txt = f.read()
        pos=pos_txt[1282:].split("\n")

    pathNeg = os.getcwd() + '/appForNlp/NLP/AbSentimentAnalysis/negative-words.txt'
    with open(pathNeg, 'rb') as f:
        neg_txt = f.read()
        neg=neg_txt[1336:].split(b"\r\n")
        neg_temp=[]
    for i in neg:
        word= i.decode('utf-8')
        neg_temp.append(word)
        neg=neg_temp[:-1]

    if lang == "pt":
        translator = Translator()
        text=translator.translate(Frase, dest='en', src='pt').text
    else:
        text = Frase

    # essa funcao foi retirada da internet
    sent_dict = dict()
    sentence = nlp(text)
    opinion_words = neg + pos
    debug = 0
    for token in sentence:
        # check if the word is an opinion word, then assign sentiment
        if token.text in opinion_words:
            sentiment = 1 if token.text in pos else -1
            # if target is an adverb modifier (i.e. pretty, highly, etc.)
            # but happens to be an opinion word, ignore and pass
            if (token.dep_ == "advmod"):
                continue
            elif (token.dep_ == "amod"):
                sent_dict[token.head.text] = sentiment
            # for opinion words that are adjectives, adverbs, verbs...
            else:
                for child in token.children:
                    # if there's a adj modifier (i.e. very, pretty, etc.) add more weight to sentiment
                    # This could be better updated for modifiers that either positively or negatively emphasize
                    if ((child.dep_ == "amod") or (child.dep_ == "advmod")) and (child.text in opinion_words):
                        sentiment *= 1.5
                    # check for negation words and flip the sign of sentiment
                    if child.dep_ == "neg":
                        sentiment *= -1
                for child in token.children:
                    # if verb, check if there's a direct object
                    if (token.pos_ == "VERB") & (child.dep_ == "dobj"):                        
                        sent_dict[child.text] = sentiment
                        # check for conjugates (a AND b), then add both to dictionary
                        subchildren = []
                        conj = 0
                        for subchild in child.children:
                            if subchild.text == "and":
                                conj=1
                            if (conj == 1) and (subchild.text != "and"):
                                subchildren.append(subchild.text)
                                conj = 0
                        for subchild in subchildren:
                            sent_dict[subchild] = sentiment

                # check for negation
                for child in token.head.children:
                    noun = ""
                    if ((child.dep_ == "amod") or (child.dep_ == "advmod")) and (child.text in opinion_words):
                        sentiment *= 1.5
                    # check for negation words and flip the sign of sentiment
                    if (child.dep_ == "neg"): 
                        sentiment *= -1
                
                # check for nouns
                for child in token.head.children:
                    noun = ""
                    if (child.pos_ == "NOUN") and (child.text not in sent_dict):
                        noun = child.text
                        # Check for compound nouns
                        for subchild in child.children:
                            if subchild.dep_ == "compound":
                                noun = subchild.text + " " + noun
                        sent_dict[noun] = sentiment
                    debug += 1
             
    #os aspects e os sentiments estão salvos em sent_dict, porém quero traduzir as keys do meu dicionário.
    #crio um novo dicionário com as keys traduzidas:
    if lang == 'pt':
        dic_sentimentos={}
        for key in sent_dict:
            chave=translator.translate(key,src='en', dest='pt').text
            dic_sentimentos[chave]=sent_dict[key]
        return dic_sentimentos
    else:
        return sent_dict


# to test the function in portuguese
#print(feature_sentiment("Gostei do meu chefe mas odiei meu sálario", "pt"))

# to test in english
#print(feature_sentiment("I loved my boss but hated my income"))



