from django.urls import path
from .views import TextAnalysisView, AskOpenAIAndStoreResponseView, TextSummarizationView

urlpatterns = [
    path('text-analysis/', TextAnalysisView.as_view(), name='text-analysis'),
    path('ask-openai-and-store-response/', AskOpenAIAndStoreResponseView.as_view(), name='ask-openai-and-store-response'),
    path('text-summarization/', TextSummarizationView.as_view(), name='text-summarization'),
]
