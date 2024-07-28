from django.db import models
# Create your models here.
import random
# Create your models here.
class CustomUrl(models.Model):
    shortUrl = models.CharField(max_length = 255, blank = True, null = True)
    longUrl = models.CharField(max_length = 255, blank = True, null = True)

    def __str__(self):
        return self.shortUrl

    def get_shortened_url(self):
        if not self.shortUrl:
            shortened_url = "".join([random.choice("abcdefghijklmnopqrstuvwxyz1234567890") for i in range(7)])
            self.shortUrl = shortened_url
            self.save()
        return self.shortUrl

    def get_expanded_url(self, url):
        if url == self.shortUrl:
            return self.longUrl
        else:
            return ''