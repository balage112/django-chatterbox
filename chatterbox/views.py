from django.contrib.auth.decorators import login_required
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


@login_required # musíme být přihlášeni
def search(request, s):
    rooms = Room.objects.filter(name__contains=s)
    messages = Message.objects.filter(body__contains=s)

    context = {"rooms":rooms, "messages":messages}
    return render(request, "chatterbox/search.html", context)


@login_required # musíme být přihlášeni
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
def delete_room(request,pk):
    room = Room.objects.get(id=pk)
    room.delete()
    return redirect("rooms")

# vytvoříme formulář

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

