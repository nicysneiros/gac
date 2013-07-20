from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
	return HttpResponse("Hello world")


def home(request):
	return render(request,'GAC2.html',{"lol": "oxe"})