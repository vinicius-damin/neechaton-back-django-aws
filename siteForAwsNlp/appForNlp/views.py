from django.shortcuts import render
from django.http import HttpResponse
from appForNlp.models import Comment, Analysis
from .NLP.sentimentAnalysis.sentiment_analysis import sentiment
from .NLP.AbSentimentAnalysis.AB_sentiment_analysis import feature_sentiment
from appForNlp.models import Comment, Analysis
import os
import pandas as pd


# Create your views here.

def index(request):
    if request.method == 'GET':
        inp_value = request.GET.get('action', 'default is do nothing')

        if inp_value == 'ADD': # Adicionar todos os dados da Deloitte na base de dados
            
            path = os.getcwd() + '/appForNlp/DeloitteCSV'
            glued_data = pd.DataFrame()
            for file_name in os.listdir(path):
                x = pd.read_csv(path + '/' + file_name, index_col=0, low_memory=False)
                glued_data = pd.concat([glued_data,x],axis=0)
            
            for index, row in glued_data.iterrows():
                inpComment = Comment(comment_text = row["pros"] + " " + row["negs"], person_id = row["profession"], comment_day = row["day"], comment_month = row["month"], comment_year = row["year"])
                inpComment.save()

                sentimentAnalysis= sentiment(inpComment.comment_text) # colocar (,'pt') se quiser em pt
                ab_sentimentAnalysis = feature_sentiment(inpComment.comment_text) # colocar (,'pt') se quiser em pt

                analysis = Analysis(comment = inpComment, comment_absa_result = str(ab_sentimentAnalysis), comment_sa_result = str(sentimentAnalysis))
                analysis.save()


        if inp_value == 'DELETE': # Deletar todos os dados da base de dados menos 1
            allComments = Comment.objects.all()
            allComments.delete()
            allAnalysis = Analysis.objects.all()
            allAnalysis.delete()

            inpComment = Comment(comment_text = 'I loved my boss and the benefits were amazing, but my collegues were horrible and the communication was bad. The workplace was disgusting. The deadlines were also bad.')
            inpComment.save()

            #cria o dado no molde do modelo e salva ele na base de dados
            sentimentAnalysis= sentiment(inpComment.comment_text) # colocar (,'pt') se quiser em pt
            ab_sentimentAnalysis = feature_sentiment(inpComment.comment_text) # colocar (,'pt') se quiser em pt

            analysis = Analysis(comment = inpComment, comment_absa_result = str(ab_sentimentAnalysis), comment_sa_result = str(sentimentAnalysis))
            analysis.save()

    return render(request, 'appForNlp/index.html')

def nlp_result(request):
    comment = Comment()
    if request.method == 'GET' :
        
        # pega o valor que coloquei na caixa de texto do forms
        inp_value = request.GET.get('comentario', 'This is a default value')
        id_pessoa = request.GET.get('id_pessoa', '0')
        inp_day = request.GET.get('day', '04')
        inp_month = request.GET.get('month', '12')
        inp_year = request.GET.get('year', '2022')
      
        #cria o dado no molde do modelo e salva ele na base de dados
        avaliation = Comment(comment_text = inp_value, person_id = id_pessoa, comment_day = inp_day, comment_month = inp_month, comment_year = inp_year)
        avaliation.save()

        #cria o dado no molde do modelo e salva ele na base de dados
        sentimentAnalysis= sentiment(avaliation.comment_text) # colocar (,'pt') se quiser em pt
        ab_sentimentAnalysis = feature_sentiment(avaliation.comment_text) # colocar (,'pt') se quiser em pt

        analysis = Analysis(comment = avaliation, comment_absa_result = str(ab_sentimentAnalysis), comment_sa_result = str(sentimentAnalysis))
        analysis.save()

        context = {'comentario_original': analysis.comment.comment_text,
                    'analise_de_sentimento':analysis.comment_sa_result,
                    'ab_analise_de_sentimento': analysis.comment_absa_result,
                    'Id_pessoa': analysis.comment.person_id,
                    'Day': analysis.comment.comment_day,
                    'Month': analysis.comment.comment_month,
                    'Year': analysis.comment.comment_year}
        return render(request, 'appForNlp/nlp_result.html', context)

