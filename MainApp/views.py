from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from MainApp.forms import SnippetForm
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    form = SnippetForm()
    context = {
        'pagename': 'Добавление нового сниппета',
        'form': form
        }
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets
        }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id: int):
    context = {'pagename': 'Просмотр Сниппета'}
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        return render(request, 'pages/errors.html', context | {"error": f"Snippet with id={snippet_id} not found."})
    else:
        context['snippet'] = snippet
        return render(request, 'pages/snippet_detail.html', context)


def create_snippet(request):
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("snippets-list") # URL для списка сниппитов
        return render(request, 'pages/add_snippet.html', context={"form": form})
        
    return HttpResponseNotAllowed(["POST"],"You must make POST request to add snippet.")