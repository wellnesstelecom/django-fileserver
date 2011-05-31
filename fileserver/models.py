# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete

from os.path import basename

from storage import AnonymousStorage


class SecureFile(models.Model):
    name = models.CharField(max_length=255, blank=True, verbose_name=_("name"))  # Original name for the file
    description = models.TextField(null=True, blank=True, verbose_name=_("description"))
    anonymous_file = models.FileField(upload_to='translations',
                                      storage=AnonymousStorage(settings.FILESERVER_ROOT, settings.FILESERVER_URL),
                                      verbose_name=_("anonymized file"))
    users = models.ManyToManyField(User, blank=True, null=True, verbose_name=_("users allowed to access file"))

    # Used to hold a new uploaded file before actually saving it.
    # Needed to work with both new and old file at the same time, as required below.
    _saved_anonymous_file = None

    def __init__(self, *args, **kwargs):
        super(SecureFile, self).__init__(*args, **kwargs)
        self._saved_anonymous_file = self.anonymous_file

    class Meta:
        verbose_name = _('secure file')
        verbose_name_plural = _('secure files')

    def __unicode__(self):
        return unicode(self.name)

    def save(self, *args, **kwargs):
        if self.anonymous_file != self._saved_anonymous_file or not self.id:
            self.name = basename(self.anonymous_file.path)
            if self._saved_anonymous_file.name != '':
                self._saved_anonymous_file.storage.delete(self._saved_anonymous_file.path)
        super(SecureFile, self).save(*args, **kwargs)
        self._saved_anonymous_file = self.anonymous_file


def delete_file(sender, instance, **kwargs):
    try:
        instance.anonymous_file.storage.delete(instance.anonymous_file.path)
    except:
        pass


pre_delete.connect(delete_file, sender=SecureFile)
