from django.db import models
from django.conf import settings

# Create your models here.



class ActivityList(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def status(self):
        items = self.items.all()
        progress = {item.status for item in items}
        if progress:
            if 'PE' not in progress:
                return 'Finished'
            if 'FI' not in progress:
                return 'Not Started'
            return 'In Progress'
        return 'Empty'

    @property
    def item_count(self):
        return self.items.count()
                

class ActivityItem(models.Model):

    class Progress(models.TextChoices):
        FINISHED = 'FI', 'Finished'
        PENDING = 'PE', 'Pending'

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    list_id = models.ForeignKey(ActivityList, on_delete=models.CASCADE, related_name='items')
    status = models.CharField(
        max_length=2,
        choices=Progress.choices,
        default=Progress.PENDING
    )

    def __str__(self):
        return self.name
