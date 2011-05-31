# -*- encoding: utf-8 -*-

from django.core.files.storage import FileSystemStorage

from os import close, remove
from os.path import split, join, basename
from tempfile import mkstemp


class AnonymousStorage(FileSystemStorage):
    def get_available_name(self, name):
        """
        Returns a filename that's unique in the repository folder.
        """

        (rel_dir, original_basename) = split(name)
        abs_dir = join(self.location, rel_dir)
        (fd, name) = mkstemp(prefix='ionl_', dir=abs_dir)
        close(fd)
        remove(name)  # Django takes care of possible duplicity here if other instance
                      # happens to select the same name before this instance actually
                      # copies the file.

        return join(rel_dir, basename(name))
