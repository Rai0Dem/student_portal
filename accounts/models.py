from django.db import models
from django.contrib.auth.models import User

User.add_to_class('friends', models.ManyToManyField("self", symmetrical=True, blank=True))