from django.shortcuts import render
from django.http import HttpResponse
from .models import Comment, Analysis
from .NLP.sentimentAnalysis.sentiment_analysis import sentiment
from .NLP.AbSentimentAnalysis.AB_sentiment_analysis import feature_sentiment


# Create your views here.

def index(request):
    return render(request, 'appForNlp/index.html')

def nlp_result(request):
    comment = Comment()
    if request.method == 'GET' :
        
        # pega o valor que coloquei na caixa de texto do forms
        inp_value = request.GET.get('comentario', 'This is a default value')
        id_pessoa = request.GET.get('id_pessoa', '0')
      
        #cria o dado no molde do modelo e salva ele na base de dados
        avaliation = Comment(comment_text = inp_value, person_id = id_pessoa)
        avaliation.save()

        #cria o dado no molde do modelo e salva ele na base de dados
        sentimentAnalysis= sentiment(avaliation.comment_text) # colocar (,'pt') se quiser em pt
        ab_sentimentAnalysis = feature_sentiment(avaliation.comment_text) # colocar (,'pt') se quiser em pt

        analysis = Analysis(comment = avaliation, comment_absa_result = str(ab_sentimentAnalysis), comment_sa_result = str(sentimentAnalysis))
        analysis.save()

        context = {'comentario_original': analysis.comment.comment_text,
                    'analise_de_sentimento':analysis.comment_sa_result,
                    'ab_analise_de_sentimento': analysis.comment_absa_result,
                    'Id_pessoa': analysis.comment.person_id}
        return render(request, 'appForNlp/nlp_result.html', context)

