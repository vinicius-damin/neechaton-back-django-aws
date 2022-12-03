# coding: utf-8

#importar as bibliotecas necessárias
import pickle
from nltk.tokenize import word_tokenize
from statistics import mode
from nltk.classify import ClassifierI
from googletrans import Translator
import os


# BUG: nltk.download('punkt') maybe needed if app not working

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        #guarda os 8 classificadores
        self.classifiers=classifiers
          
    def classify(self, features):
        votes=[]
        for c in self.classifiers:
            v=c.classify(features)
            #cada classificador vota uma vez
            votes.append(v)
        #o sentimento que é selecionado é o que aparece mais vezes (mais votado)
        return mode(votes)
    def confidence(self,features):
        votes=[]
        for c in self.classifiers:
            v=c.classify(features)
            votes.append(v)
        print(votes)
        choice_votes=votes.count(mode(votes))
        conf=choice_votes/len(votes)
        #temos também o valor de confiança de nossa predição
        return conf

#Como não é possível fazer pickle.dump na instância de VoteClassifier:
def pickleClassifiers():
    #primeiro temos que fazer pickle.load em todos os arquivos necessários
    classifiers_str=['NaiveBayes_classifier',
                    'MNB_classifier',
                    'BernoulliNB_classifier',
                    'SGDClassifier_classifier',
                    #retirei 'SVC_classifier',
                    'LinearSVC_classifier',
                    #'NuSVC_classifier' muito pesado
            ]

    path = os.getcwd() + '/appForNlp/NLP/sentimentAnalysis/pickles/'
    classifiers_list=[]
    for classifier in classifiers_str:
        classifier_f=open(path +classifier + '.pickle','rb')
        classifiers_list.append((pickle.load(classifier_f),classifier))

    NaiveBayes_classifier=classifiers_list[0][0]
    MNB_classifier=classifiers_list[1][0]
    BernoulliNB_classifier=classifiers_list[2][0]
    SGDClassifier_classifier=classifiers_list[3][0]
    #SVC_classifier=classifiers_list[4][0] da erro
    LinearSVC_classifier=classifiers_list[4][0]
    #NuSVC_classifier=classifiers_list[5][0] muito pesado

    voted_classifier=VoteClassifier(NaiveBayes_classifier,
                                    MNB_classifier,
                                    BernoulliNB_classifier,
                                    SGDClassifier_classifier,
                                    #retirei 'SVC_classifier',
                                    LinearSVC_classifier,
                                    #NuSVC_classifier,NuSVC_classifier muito pesado
                                    )
    return voted_classifier


#Definimos a função criada no documento 'Creating the algorithm'
def find_features(document):
    pathWords = os.getcwd() + '/appForNlp/NLP/sentimentAnalysis/pickles/words_features.pickle'
    words_features_f=open(pathWords,'rb')
    words_features=pickle.load(words_features_f)
    words_features_f.close()

    #temos que usar word_tokenize pois recebemos uma review em formato de string contento várias palavras.
    words=word_tokenize(document)
    features={}
    #cada palavra das 7000 mais frequentes é avaliada se está ou não
    #na review em questão, se estiver ela é marcada como True
    for w in words_features:
        features[w]=(w in words)
    return features



#função que recebe uma string e retorna o sentimento dela
def sentiment(text, lang = 'en'):
    #importar um tradutor
    translator = Translator()
    if lang == 'pt':
        text=translator.translate(text,src='pt', dest='en').text

    # Here the text must be in english
    feats=find_features(text)
    voted_classifier = pickleClassifiers()
    result = (voted_classifier.classify(feats), voted_classifier.confidence(feats))
    return result



#print(sentiment('gostei do meu chefe! Mas odiei os meus colegas', 'pt')) #('neg', 1.0)
#print(sentiment('Amei do meu chefe!', 'pt')) #('pos', 0.6)

#print(sentiment('I liked my boss but hated very much my collegues')) #('neg', 0.6)
#print(sentiment('I loved my boss but hated very much my collegues')) #('pos', 0.6)
