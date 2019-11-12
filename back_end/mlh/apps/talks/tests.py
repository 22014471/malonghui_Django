from django.test import TestCase

# Create your tests here.
from talks.models import Talks

a = Talks.objects.get(id=1)
for i in range(1, 100):
    a.id = None
    a.content = "传智播客python第%s开始吐槽了" % i
    a.save()

