from django.db import models

# Create your models here.
class Card(models.Model):
    card_name = models.CharField(max_length=200, primary_key=True)
    mana_cost = models.CharField(max_length=20)
    color = models.CharField(max_length=15)
    rules_text = models.CharField(max_length=400, blank=True)
    flavor_text = models.CharField(max_length=400, blank=True)
    stats = models.CharField(max_length=10, blank=True)
    set = models.CharField(max_length=200, db_index=True)
    def __str__(self):
            return self.card_name

class CardTyperel(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    CARD_TYPE_CHOICES = {
        "CREATURE": "Creature",
        "SORCERY": "Sorcery",
        "INSTANT": "Instant",
        "ENCHANTMENT": "Enchantment",
        "ARTIFACT": "Artifact",
        "PLANESWALKER": "Planeswalker",
        "BATTLE": "Battle",
        "LAND": "Land",
    }
    card_type = models.CharField(max_length=12, choices=CARD_TYPE_CHOICES, db_index = True)
    def __str__(self):
                return self.card_type

class Supertyperel(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    SUPERTYPE_CHOICES = {
        "BASIC": "Basic",
        "LEGENDARY": "Legendary",
        "SNOW": "Snow",
        "WORLD": "World",
    }
    super_type = models.CharField(max_length=12, choices=SUPERTYPE_CHOICES, default="LEGENDARY", db_index = True)
    def __str__(self):
                return self.super_type

class Subtyperel(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    sub_type = models.CharField(max_length=30)
    def __str__(self):
                return self.sub_type