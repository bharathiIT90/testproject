from django.shortcuts import get_object_or_404, render

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Question , choice

from django.utils import timezone

from django.http import Http404



class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())

def vote(request, question_id):
	p = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		context = {'question':p,'error_message':'You didn\'t select a choice yet.'}
		return render(request, 'pools/detail.html',context)
	else:
		selected_choice.votes+=1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results',args=(p.id,)))
	
# Create your views here.
