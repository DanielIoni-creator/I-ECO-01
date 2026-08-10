#!/usr/bin/env python3
"""
AI Sommelier - Raccomandazioni drink personalizzate
"""

import random
import json
from datetime import datetime

class AISommelier:
    def __init__(self):
        self.name = "AI Sommelier"
        self.drinks = {
            'classic': [
                {'name': 'Mojito', 'ingredients': ['Rum', 'Menta', 'Lime', 'Zucchero', 'Soda']},
                {'name': 'Martini', 'ingredients': ['Gin', 'Vermouth', 'Olive']},
                {'name': 'Negroni', 'ingredients': ['Gin', 'Campari', 'Vermouth']}
            ],
            'modern': [
                {'name': 'Espresso Martini', 'ingredients': ['Vodka', 'Caffè', 'Liquore']},
                {'name': 'Aperol Spritz', 'ingredients': ['Aperol', 'Prosecco', 'Soda']},
                {'name': 'Gin Tonic', 'ingredients': ['Gin', 'Tonica', 'Lime']}
            ]
        }
        self.user_preferences = {}
    
    def get_recommendation(self, mood, weather):
        """Raccomanda un drink in base a umore e meteo"""
        print(f"🎯 Analisi: Umore={mood}, Meteo={weather}")
        
        recommendations = []
        
        if weather in ['hot', 'sunny']:
            recommendations.append(self.drinks['modern'][1])  # Aperol Spritz
            recommendations.append(self.drinks['classic'][0])  # Mojito
        
        if mood in ['happy', 'celebrating']:
            recommendations.append(self.drinks['classic'][1])  # Martini
            recommendations.append(self.drinks['modern'][2])  # Gin Tonic
        
        if mood in ['relaxed', 'chill']:
            recommendations.append(self.drinks['classic'][2])  # Negroni
            recommendations.append(self.drinks['modern'][0])  # Espresso Martini
        
        if not recommendations:
            recommendations.append(random.choice(self.drinks['classic']))
        
        return recommendations[:2]
    
    def learn_preference(self, user_id, drink, rating):
        """Apprende le preferenze dell'utente"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = []
        
        self.user_preferences[user_id].append({
            'drink': drink,
            'rating': rating,
            'timestamp': datetime.now().isoformat()
        })
        
        print(f"📊 Preferenza registrata per utente {user_id}: {drink} ({rating}/5)")
        return True
    
    def get_personalized_recommendation(self, user_id):
        """Raccomanda un drink basato sulle preferenze dell'utente"""
        if user_id not in self.user_preferences or not self.user_preferences[user_id]:
            print("ℹ️ Nessuna preferenza registrata, uso raccomandazione generica")
            return self.get_recommendation('neutral', 'normal')
        
        # Analizza preferenze
        favorites = {}
        for pref in self.user_preferences[user_id]:
            if pref['rating'] >= 4:
                drink_name = pref['drink']['name']
                favorites[drink_name] = favorites.get(drink_name, 0) + 1
        
        if not favorites:
            return self.get_recommendation('neutral', 'normal')
        
        # Prendi il drink più apprezzato
        best_drink = max(favorites, key=favorites.get)
        print(f"🎯 Raccomandazione personalizzata per utente {user_id}: {best_drink}")
        
        # Trova il drink completo
        for category in self.drinks.values():
            for drink in category:
                if drink['name'] == best_drink:
                    return [drink]
        
        return self.get_recommendation('neutral', 'normal')
    
    def run(self):
        """Simula il sommelier AI"""
        print(f"🍷 {self.name} avviato!")
        print("🤖 IA pronta per raccomandazioni personalizzate")
        
        # Simula interazioni
        interactions = [
            {'mood': 'happy', 'weather': 'sunny'},
            {'mood': 'relaxed', 'weather': 'normal'},
            {'mood': 'celebrating', 'weather': 'hot'}
        ]
        
        for i, interaction in enumerate(interactions, 1):
            print(f"\n📌 Interazione {i}")
            recommendations = self.get_recommendation(
                interaction['mood'],
                interaction['weather']
            )
            print(f"🍹 Raccomandazioni: {', '.join([d['name'] for d in recommendations])}")
            
            # Simula feedback
            user_id = f"USER{i}"
            for drink in recommendations:
                rating = random.randint(3, 5)
                self.learn_preference(user_id, drink, rating)
        
        print("\n📊 RIEPILOGO PREFERENZE:")
        for user, prefs in self.user_preferences.items():
            print(f"   Utente {user}: {len(prefs)} preferenze registrate")

if __name__ == "__main__":
    sommelier = AISommelier()
    sommelier.run()
