from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from gestionApp.models import usuario
from gestionApp.forms import form_user

# Create your views here.

def ranking(request):
	lista_usuarios=usuario.objects.all().order_by("-puntuacion")[0:5]
	return render(request, "ranking.html", locals())

def registroUser(request):
	if request.method =='POST':	#si se envia el formulario
		form = form_user(request.POST)
		if form.is_valid():
			form.save()
		return HttpResponseRedirect('/perfil')
	else:
		form = form_user()
	return render(request, "form_alta_usuario.html", {'form':form,})