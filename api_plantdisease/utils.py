import six
import shortuuid
from django.db import models
from django.http import JsonResponse
from django.utils.text import slugify


class Manager(models.Manager):
    def is_not_deleted(self):
        return self.filter(is_deleted=False)

    def active(self):
        return self.filter(is_deleted=False, status=True)
    
class BaseModel(models.Model):
    """
    This is the base model for all the models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    sorting_order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    objects = Manager()

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def catch_exception(self, slug_item, *args, **kwargs):
        self.slug = slugify(slug_item) + "-" + str(six.text_type(shortuuid.uuid()))
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):

        if hasattr(self, "slug"):
            if hasattr(self, "name"):
                if self.name:
                    try:
                        self.slug = slugify(self.name)
                        super().save(*args, **kwargs)
                    except Exception:
                        self.catch_exception(self, self.name, *args, **kwargs)

            elif hasattr(self, "title"):
                if self.title:
                    try:
                        self.slug = slugify(self.title)
                        super().save(*args, **kwargs)
                    except Exception:
                        self.catch_exception(self, self.title, *args, **kwargs)

        super().save(*args, **kwargs)