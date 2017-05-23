from django.db import models
from django.shortcuts import get_object_or_404

from vsdk.service_development.models import CallSession


class Result(models.Model):

    name = models.CharField(max_length = 100, blank = True, null = True)
    value = models.CharField(max_length = 100, blank = True, null = True)
    file = models.FileField(upload_to='uploads/', blank=True, null= True)


    session = models.ForeignKey(CallSession, on_delete=models.CASCADE, related_name="session")

    def __str__(self):
        return self.name

def record_exists(session, result_name):
    result, created = Result.objects.get_or_create(None, name=result_name, session_id=session.id)

    return not created


def lookup_or_create_result(session, result_name, value = ''):

    result, created = Result.objects.get_or_create(None, name=result_name, session_id = session.id)

    result.session = session
    result.value = value

    result.save()

    return result
