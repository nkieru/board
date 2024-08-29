from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field


class Notice(models.Model):
    tanks = 'TK'
    healers = 'HL'
    dd = 'DD'
    merchants = 'MR'
    guildmasters = 'GM'
    questgivers = 'QG'
    blacksmiths = 'BS'
    tanners = 'TN'
    potion_makers = 'PM'
    spellcasters = 'SC'

    CAT = [
        (tanks, 'Танки'),
        (healers, 'Хилы'),
        (dd, 'ДД'),
        (merchants, 'Торговцы'),
        (guildmasters, 'Гилдмастеры'),
        (questgivers, 'Квестгиверы '),
        (blacksmiths, 'Кузнецы'),
        (tanners, 'Кожевники'),
        (potion_makers, 'Зельевары'),
        (spellcasters, 'Мастера заклинаний')
    ]

    author_nc = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=15, choices=CAT)
    title = models.CharField(max_length=100)
    content = CKEditor5Field('Content', config_name='extends', blank=True)
    date_nc = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/notices/{self.id}'


class Feedback(models.Model):
    author_fb = models.ForeignKey(User, on_delete=models.CASCADE)
    notice_fb = models.ForeignKey(Notice, on_delete=models.CASCADE)
    text = models.TextField()
    date_fb = models.DateTimeField(auto_now_add=True)
    accept = models.BooleanField(default=False)

