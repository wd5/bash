# -*- coding: utf-8 -*-
__author__ = 'bteam'
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from bash.quotes.models import *

from django import forms
from django.utils import simplejson

class QuoteForm(forms.Form):
    text = forms.CharField(label='Текст цитаты',widget=forms.Textarea(attrs={'placeholder':u'Вставьте цитату'}))


def home(request,page=1):
    paginator = Paginator(Quote.objects.filter(accepted=True), 7)

    try:
        quotes = paginator.page(page)
    except PageNotAnInteger:
        quotes = paginator.page(1)
    except EmptyPage:
        quotes = paginator.page(paginator.num_pages)

    return render(request,'index.html',dict(page=page,quotes=quotes))

def add(request):
    if request.method == 'POST' and request.user.is_authenticated():
        form = QuoteForm(request.POST)
        response = {}
        if form.is_valid():
            q = Quote(author=request.user,text=form.cleaned_data.get('text'))
            q.save()
            response['pk'] = q.pk
        else:
            response['errors'] = form.errors
        if request.is_ajax():
            return HttpResponse(simplejson.dumps(response))
        else:
            return render(request, 'index.html', response)
    else:
        form = QuoteForm()
        return render(request,'index.html',dict(form=form))


    return render(request,'index.html',dict(add=True))

def success(request,quote=None):
    return render(request,'index.html',dict(page=1,quote=quote))


def quote(request,id):
    quote = get_object_or_404(Quote,pk=id)
    return render(request,'qoute.html',dict(quote=quote))