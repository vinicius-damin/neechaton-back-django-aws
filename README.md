# django-aws-nlp for Neecathon
Repository to be cloned into an AWS EC2 to serve as an API to return sentiment analysis and aspect based sentiment analysis via requests. The front end which uses this aplication can be found at https://github.com/mhteixeira/neecathon-front-next

This was made to be used in the Hackaton done by NEEC (from the university Instituto Superior Técnico) and by the company Premium Minds located in Lisbon.

Inside the django project, in the folder NLP, there is our implementation of Sentiment analysis using Machine Learning models which were trained for this competition and Aspect Based Sentiment Analysis using Spacy.

# How to use:

You put a text as a request in *yourAwsPublicIPV4/appForNlp/analysis*, for example ("I loved my boss, liked the coffee but hated my coworkers"), and receive the analysis as a JSON by doing a GET request in */api/analysis/*.

The output will be like:

{"id":1,"comment_absa_result":"{'boss': 1, 'coffee': 1, 'coworkers': -1}","comment_sa_result":"('pos', 0.6)","person_id":"1","comment_text":"I loved my boss, liked the coffee but hated my coworkers"}


# First time running:

It may be necessary to run the following code when running for the first time:

$ python3
> import nltk
> nltk.download('punkt')
> nltk.download('stopwords')

# Special Thanks

We, as a team from Brazil, are very grateful to NEEC not only for being welcoming to us, but also for the amazing experience this Hackaton was, it really showed us what the experience of start-up can be!
