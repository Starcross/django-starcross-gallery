from django.core.files.storage import FileSystemStorage
import re


class DiacriticFileStorage(FileSystemStorage):
    """ Allow storage of files preserving accent characters in their name """

    def get_valid_name(self, name):
        """
        Return a filename, based on the provided filename, that's suitable for
        use in the target storage system. Based on django.utils.text.get_valid_name
        """
        name = str(name).strip().replace(' ', '_')
        return re.sub(r'(?u)[^A-Za-zÀ-ÖØ-öø-ÿ._-]', '', name)
