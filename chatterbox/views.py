from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.forms import ModelForm
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect

from chatterbox.models import Room, Message
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView


# Create your views here.
def hello(request, s):
    return HttpResponse(f"Hello, {s} world!!!!")


def home(request):
    rooms = Room.objects.all() # najdeme všechny místnosti a vypíšeme je na domovské stránce
    context = {"rooms": rooms}
    return render(request, 'chatterbox/home.html', context)

""" - nahrazuji to novým searchem dole řádek 103 protože si na to udělám formulář na vyhledávání -
@login_required # musíme být přihlášeni
def search(request, s):
    rooms = Room.objects.filter(name__contains=s)
    messages = Message.objects.filter(body__contains=s)

    context = {"rooms":rooms, "messages":messages}
    return render(request, "chatterbox/search.html", context)
"""
"""


@login_required # musíme být přihlášeni  zakomentováno protože do teté funkce
přidávám metodu na FILES viz řádek 61
def room (request, pk):
    room = Room.objects.get(id=pk) # najdeme místnost se zadaným id
    messages = Message.objects.filter(room=pk) # vybereme všechny zprávy dané místnosti

    # pokud zadáme novo zprávu, musíme jit zpracovat
    if request.method == "POST":
        body = request.POST["body"].strip() # uloží se zpráva pouze pokud je pzráva delší jak jeden znak a nesmí tam být mezery
        # pokud budu chtít odeslta pouze mezeru tak díky strip nejde
        if len(body) > 0:
            message = Message.objects.create(
                user=request.user,
                room=room,
                #body=request.POST.get("body") # nebo mohu použít .get("body")
                #body=request.POST["body"] # získáme zprávu z formuláře
                body=body # ptž to máme uložené v proměnné body na řádku 35
            )
        return HttpResponseRedirect(request.path_info) # přesměruje na stejnou stránku, provedem reaload stránky
    # tímto zamezím, aby s emi při opětovném manuálním reloadu opět odeslal t astejná zpráva, ale musel jsem zakomentovat
    # django_reload z room.html, protože to pak nefungovalo
    # tzn. že v room.html mohu smazat řádky 3 a 19


    context = {"room": room,"messages": messages}
    return render(request,"chatterbox/room.html",context)
"""

@login_required
def room(request, pk):
    room = Room.objects.get(id=pk)  # najdeme místnost se zadaným id
    messages = Message.objects.filter(room=pk)  # vybereme všechny zprávy dané místnosti

    # pokud zadáme novou zprávu, musíme ji zpracovat
    if request.method == 'POST':
        file_url = ""
        if request.FILES.get('upload'):                 # pokud je v requestu soubor
            upload = request.FILES['upload']        # uložíme si ho do proměnné
            file_storage = FileSystemStorage()      # vytvoříme si objekt pro ukládání souborů
            file = file_storage.save(upload.name, upload) # uložíme soubor na disk
            file_url = file_storage.url(file)           # získáme URL souboru a uložím
        body = request.POST.get('body').strip()


        if len(body) > 0 or request.FILES.get('upload'):
            message = Message.objects.create(
                user=request.user,
                room=room,
                body=body,
                file=file_url
            )
        return HttpResponseRedirect(request.path_info)

    context = {'room': room, 'messages': messages}
    return render(request, "chatterbox/room.html", context)


@login_required # musíme být přihlášeni abychom mohli psát zprávy a prozkouávat stránky
def rooms(request):
    rooms = Room.objects.all()
    context = {"rooms": rooms}
    return render(request, "chatterbox/rooms.html", context)

@login_required
def create_room(request):
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        description = request.POST.get('description').strip()
        if len(name) > 0 and len(description) > 0:
            room = Room.objects.create(
                host=request.user,
                name=name,
                description=description
            )

            return redirect('room', pk=room.id)

    return render(request, 'chatterbox/create_room.html')
@login_required
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if room.messages_count() == 0:  # pokud v místnosti není žádná zpráva
        room.delete()               # tak místnost smažeme

        return redirect('rooms')

    context = {'room': room, 'message_count': room.messages_count()}
    return render(request, 'chatterbox/delete_room.html', context)
# vytvoříme formulář

@login_required
def delete_room_yes(request, pk):
    room = Room.objects.get(id=pk)
    room.delete()
    return redirect('rooms')

class RoomEditForm(ModelForm): #ModelFomr musíme importovat z Django
    class Meta:
        model = Room # beru z models.py class Room
        fields = "__all__" # všechna pole


@method_decorator(login_required, name="dispatch") # musíme být přihlášeni abychom mohli editovat
class EditRoom(UpdateView): # UpdateView musíme importovat z Django
    template_name = "chatterbox/edit_room.html"
    model = Room
    form_class = RoomEditForm
    success_url = reverse_lazy("rooms") # přesměruje na rooms

# vytvořím search bez parametru "s"

@login_required # musíme být přihlášeni
def search(request):
    if request.method == "POST": # pokud pošleme dotaz z formuláře
        s = request.POST.get("search").strip()  #tady tahám "s" z formuláře nikoliv z url  z odeslaného formuláře si vytáhnu co chci hledat a eliminuji pomcí strip mezery
        if len(s) > 0:
            rooms = Room.objects.filter(name__contains=s) #vyfiltruji místností dle zadaného řetězce
            messages = Message.objects.filter(body__contains=s) # vyfilturji zprávy dle zadaného řetězce

            context = {"rooms": rooms, "messages": messages, "search":s} #výsledky uložím do contextu
            return render(request, "chatterbox/search.html", context)  # vykreslíme stránku s výsledky

        return redirect("home") # pokud nic nezadám tak se vrátím na home

    context = {"rooms": None, "messages": None} # pokud POST nebyl odeslán - nic nezobrazí - místnosti i zprávy budou prázdné
    return redirect("home")                     #případně lze redirect na jinou stránku
