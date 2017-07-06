# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Question, AdminUser
from django.template import RequestContext, loader
from django.http import Http404
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	template = loader.get_template('poll/index.html')
	context = {
    	'latest_question_list': latest_question_list,
    }
	return HttpResponse(template.render(context, request))

def detail(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	return render(request, 'poll/detail.html', {'question': question})


def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'poll/results.html',{'question': question})

def vote(request, question_id):
	p = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'poll/detail.html', {
				'question': p,
				'error_message': "you didn't select a choice"
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('poll:results', args=(p.id,)))

def login(request):

	if request.method == "GET":
		return render(request, 'poll/login.html')
	else:
		user = AdminUser.objects.filter(userName=request.POST['userName'])
		if user:
			return render(request, 'poll/loginSuccess.html',{"user": user})
		else:
			return render(request, 'poll/loginFail.html',{"user": user})
	







    