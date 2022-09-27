from django.apps import apps
from django.contrib.auth import get_user_model
from recipe.models import *

User = get_user_model()
Follow = apps.get_model('users', 'Follow')
