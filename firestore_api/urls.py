from django.urls import path
from .views import StoreOpenAIResponseView, UploadFileView, ProcessFileContentView, GetStoredResponseView

urlpatterns = [
    path('ask-openai-and-store-response', StoreOpenAIResponseView.as_view()),
    path('get-response', GetStoredResponseView.as_view()),
    path('upload-file', UploadFileView.as_view()),
    path('process-file-content', ProcessFileContentView.as_view()),
]
