from django.shortcuts import render, redirect, get_object_or_404
from MainApp.forms import SnippetForm
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


@login_required
def my_snippets(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {
        "pagename": "Мои сниппеты",
        "snippets": snippets
    }
    return render(request, "pages/view_snippets.html", context)


def add_snippet_page(request):
    # Создаем пустую форму при запросе GET
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
            }
        return render(request, 'pages/add_snippet.html', context)
    
    # Получаем данные из формыи и на их основе создаем новый сниппет, сохраняя его в БД
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False) # получаем экземпляр класса Snippet
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            # GET /snippets/list
            return redirect("snippets-list") # URL для списка сниппитов
        return render(request, 'pages/add_snippet.html', context={"form": form})


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


def snippet_delete(request, snippet_id: int):
    if request.method == "GET" or request.method == "POST":
        # Найти snippet по snippet_id или вернуть ошибку 404
        snippet = get_object_or_404(Snippet, id=snippet_id)
        snippet.delete() # Удаляем сниппет из базы

    return redirect("snippets-list")


@login_required
def snippet_edit(request, snippet_id: int):
    """ Edit snippet"""

    context = {'pagename': 'Обновление сниппета'}
    snippet = get_object_or_404(Snippet, id=snippet_id)
    # Создаем форму на основе данных snippet'a при запросе GET
    if request.method == "GET":
        form = SnippetForm(instance=snippet)
        return render(request, 'pages/add_snippet.html', context | {"form": form})
    
    # Получаем данные из формы и на их основе обновляем сниппет, сохраняя его в БД
    if request.method == "POST":
        data_form = request.POST
        snippet.name = data_form["name"]
        snippet.code = data_form["code"]
        snippet.save()
        return redirect("snippets-list") # URL для списка сниппитов


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {
                "pagename": "PythonBin",
                "errors": ["Wrong username or password"]
            }
            return render(request, "pages/index.html", context)
    return redirect('home')



def logout(request):
    auth.logout(request)
    return redirect(to='home')