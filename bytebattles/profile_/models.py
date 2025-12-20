from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rating = models.IntegerField(default=0)
    max_rating = models.IntegerField(default=0)

    def rank(self, rating=None):
        if rating is None:
            rating = self.rating

        if rating < 500:
            return "Novice"
        elif rating < 800:
            return "Apprentice"
        elif rating < 1100:
            return "Fighter"
        elif rating < 1400:
            return "Knight"
        elif rating < 1700:
            return "Champion"
        elif rating < 2000:
            return "Warlord"
        elif rating < 2300:
            return "Gladiator"
        elif rating < 2600:
            return "Grandmaster"
        else:
            return "Legend"
    
    def color(self, rating=None):
        if rating is None:
            rating = self.rating

        if rating < 500:
            return "#9CA3AF"
        elif rating < 800:
            return "#60A5FA"
        elif rating < 1100:
            return "#10B981"
        elif rating < 1400:
            return "#6366F1"
        elif rating < 1700:
            return "#F59E0B"
        elif rating < 2000:
            return "#F97316"
        elif rating < 2300:
            return "#DC2626"
        elif rating < 2600:
            return "#8B5CF6"
        else:
            return "#111827"
        
    def max_rank(self):
        return self.rank(self.max_rating)
    
    def max_color(self):
        return self.color(self.max_rating)
    
    def __str__(self):
        return self.user.username