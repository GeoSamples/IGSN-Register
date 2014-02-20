from django.contrib.auth.models import User
from django.db import models
#from tastypie.models import create_api_key

#models.signals.post_save.connect(create_api_key, sender=User)

# Create your models here.
import inspect

class Choice(object):
    """superclass for defining "choices" in Django models.  Refers to this neat little snippet:
    http://tomforb.es/using-python-metaclasses-to-make-awesome-django-model-field-choices?pid=0
    """
    class __metaclass__(type):
        def __init__(self, name, type, other):
            self._data = []
            for name, value in inspect.getmembers(self):
                if not name.startswith("_") and not inspect.isfunction(value):
                    if isinstance(value,tuple) and len(value) > 1:
                        data = value
                    else:
                        data = (value, " ".join([x.capitalize() for x in name.replace("_"," ").split(" ")]),)
                    self._data.append(data)
                    setattr(self, name, data[0])

        def __iter__(self):
            for value, data in self._data:
                yield value, data

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='geopass_profile')
    geopass_usercode = models.CharField(max_length=3, blank=False)
    geopass_username = models.CharField(max_length=64)
    geopass_password = models.CharField(max_length=255)

    def __unicode__(self):
       return u'{geopass_username} - {geopass_usercode}'.format(
           geopass_username=self.geopass_username,  
           geopass_usercode=self.geopass_usercode
       )

