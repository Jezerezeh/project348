from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path
from django.template import loader
from django.urls import reverse
import pymsgbox

from .models import Card, Supertyperel, Subtyperel, CardTyperel

# Create your views here.

def index(request):
    template = loader.get_template("cards/index.html")
    context = {}
    return HttpResponse(template.render(context, request))

def card_list(request):
    cards = Card.objects.all()
    template = loader.get_template("cards/list.html")
    context = {
            "card_list": cards,
    }
    return HttpResponse(template.render(context, request))

def edit(request, name):
    card = Card.objects.get(card_name=name)
    supertype = ""
    try: supertype = Supertyperel.objects.get(card=card).super_type
    except: supertype = ""
    subtype = ""
    try: subtype = Subtyperel.objects.get(card=card).sub_type
    except: subtype = ""
    card_type = ""
    try: card_type = CardTyperel.objects.get(card=card).card_type
    except: card_type = ""
    template = loader.get_template("cards/edit.html")
    context = {
            "card": card,
            "supertype": supertype,
            "subtype": subtype,
            "card_type": card_type,
    }
    return HttpResponse(template.render(context, request))

def update(request, name):
    card = Card.objects.get(card_name=name)
    new_cost = (request.POST["mana_cost"])
    if new_cost != "": card.mana_cost = new_cost
    new_color = (request.POST["color"])
    if new_color != "": card.color = new_color
    new_rules = (request.POST["rules_text"])
    if new_rules != "": card.rules_text = new_rules
    new_flavor = (request.POST["flavor_text"])
    if new_flavor != "": card.flavor_text = new_flavor
    new_stats = (request.POST["stats"])
    if new_stats != "": card.stats = new_stats
    new_set = (request.POST["set"])
    if new_set != "": card.set = new_set
    new_subtype = (request.POST["subtype"])
    if new_subtype != "":
        try:
            subtyperel = Subtyperel.objects.get(card=card)
        except:
            subtyperel = Subtyperel(card=card, sub_type=new_subtype)
            subtyperel.save()
        else:
            subtyperel.sub_type = new_subtype
            subtyperel.save()
    new_supertype = (request.POST.get("supertype", ""))
    if new_supertype != "":
        try:
            supertyperel = Supertyperel.objects.get(card=card)
        except:
            supertyperel = Supertyperel(card=card, super_type=new_supertype)
            supertyperel.save()
        else:
            supertyperel = Supertyperel.objects.get(card=card)
            supertyperel.super_type = new_supertype
            supertyperel.save()
    new_card_type = (request.POST.get("card_type", ""))
    if new_card_type != "":
        try:
            new_card_typerel = CardTyperel.objects.get(card=card)
        except:
            new_card_typerel = CardTyperel(card=card, card_type=new_card_type)
            new_card_typerel.save()
        else:
            new_card_typerel = CardTyperel.objects.get(card=card)
            new_card_typerel.card_type = new_card_type
            new_card_typerel.save()
    card.save()
    return HttpResponseRedirect("../list")

def delete(request, name):
    card = Card.objects.get(card_name=name)
    card.delete()
    return HttpResponseRedirect("../list")

def create(request):
    cards = Card.objects.all()
    template = loader.get_template("cards/create.html")
    context = {
            "card_list": cards,
    }
    return HttpResponse(template.render(context, request))

def add(request):
    name = (request.POST["name"])
    if name == "":
            pymsgbox.alert('Card needs a name', 'Title')
            return HttpResponseRedirect(reverse("create"))
    cost = (request.POST["mana_cost"])
    if cost == "":
        pymsgbox.alert('Card needs a cost', 'Title')
        return HttpResponseRedirect(reverse("create"))
    color = (request.POST["color"])
    if color == "":
        pymsgbox.alert('Card needs a color', 'Title')
        return HttpResponseRedirect(reverse("create"))
    new_supertype = (request.POST.get("supertype", ""))
    new_card_type = (request.POST.get("card_type", ""))
    if new_card_type is None:
        pymsgbox.alert('Card needs a type', 'Title')
        return HttpResponseRedirect(reverse("create"))
    subtype = (request.POST["subtype"])
    rules = (request.POST["rules_text"])
    flavor = (request.POST["flavor_text"])
    stats = (request.POST["stats"])
    set = (request.POST["set"])
    if set == "":
        pymsgbox.alert('Card needs a set', 'Title')
        return HttpResponseRedirect(reverse("create"))
    new_card = Card(card_name=name, mana_cost=cost, color=color, rules_text=rules, flavor_text=flavor, stats=stats, set=set)
    new_card.save()
    if new_supertype != "":
        new_supertyperel = Supertyperel(card=new_card, super_type=new_supertype)
        new_supertyperel.save()
    if new_supertype != "":
        new_subtyperel = Subtyperel(card=new_card, sub_type=subtype)
        new_subtyperel.save()
    new_card_typerel = CardTyperel(card=new_card, card_type=new_card_type)
    new_card_typerel.save()
    return HttpResponseRedirect(reverse("card_list"))

def search(request):
    cards = Card.objects.all()
    template = loader.get_template("cards/search.html")
    context = {
                "card_list": cards,
    }
    return HttpResponse(template.render(context, request))

def results(request):
    query = """
        SELECT card.*,
            ctype.card_type,
            supertype.super_type,
            subtype.sub_type
        FROM cards_card AS card
        LEFT JOIN cards_cardtyperel AS ctype ON ctype.card_id = card.card_name
        LEFT JOIN cards_supertyperel AS supertype ON supertype.card_id = card.card_name
        LEFT JOIN cards_subtyperel AS subtype ON subtype.card_id = card.card_name
        WHERE TRUE
    """
    params = []
    if request.method == 'POST':
        card_name = request.POST.get('name', '')
        mana_cost = request.POST.get('mana_cost', '')
        color = request.POST.get('color', '')
        supertype = request.POST.get('supertype', '')
        card_type = request.POST.get('card_type', '')
        subtype = request.POST.get('subtype', '')
        rules_text = request.POST.get('rules_text', '')
        flavor_text = request.POST.get('flavor_text', '')
        stats = request.POST.get('stats', '')
        set = request.POST.get('set', '')

        if card_name:
            query += " AND card.card_name LIKE %s"
            params.append(f"%{card_name}%")
        if mana_cost:
            query += " AND card.mana_cost = %s"
            params.append(mana_cost)
        if color:
            query += " AND card.color LIKE %s"
            params.append(f"%{color}%")
        if supertype:
            query += " AND supertype.super_type = %s"
            params.append(supertype)
        if card_type:
            query += " AND ctype.card_type = %s"
            params.append(card_type)
        if subtype:
            query += " AND subtype.sub_type LIKE %s"
            params.append(f"%{subtype}%")
        if rules_text:
            query += " AND card.rules_text LIKE %s"
            params.append(f"%{rules_text}%")
        if flavor_text:
            query += " AND card.flavor_text LIKE %s"
            params.append(f"%{flavor_text}%")
        if stats:
            query += " AND card.stats LIKE %s"
            params.append(f"%{stats}%")
        if set:
            query += " AND card.set = %s"
            params.append(set)
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        cards = cursor.fetchall()
    card_list = [dict(zip(columns, row)) for row in cards]
    return render(request, "cards/results.html", {
        "card_list": card_list
    })