from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import openai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

openai.api_key = os.getenv('OPENAI_API_KEY')

class AskOpenAIAndStoreResponseView(APIView):
    def post(self, request):
        question = request.data.get('question')
        conversation_history = request.data.get('conversation_history', '')
        if not question:
            return Response({'error': 'Question is required'}, status=status.HTTP_400_BAD_REQUEST)

        prompt = conversation_history + "\n\n" + question if conversation_history else question

        try:
            response = openai.Completion.create(engine="gpt-4.0-turbo", prompt=prompt, max_tokens=4096)
            text = response['choices'][0]['text'].strip()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'success': True, 'question': question, 'openAIResponse': text, 'conversation_history': conversation_history + "\n\n" + question + "\n\n" + text})

class TextSummarizationView(APIView):
    def post(self, request):
        text = request.data.get('text')
        max_tokens = request.data.get('max_tokens')

        if not text or not max_tokens:
            return Response({'error': 'Text and max_tokens are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = openai.Completion.create(engine="gpt-4.0-turbo", prompt=text, max_tokens=max_tokens)
            summary = response['choices'][0]['text'].strip()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'summary': summary, 'model': 'gpt-4.0-turbo'})

class TextAnalysisView(APIView):
    def post(self, request):
        text = request.data.get('text')

        if not text:
            return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Mock sentiment analysis
        sentiment = "positive"
        score = 0.87
        model = "gpt-4.0-turbo"

        return Response({
            "sentiment": sentiment,
            "score": score,
            "model": model
        })
