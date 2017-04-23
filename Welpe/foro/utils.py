from __future__ import unicode_literals


from Welpe.site_utils import UtilsForAll

# from accounts.templatetags.accounts_tags import get_name, get_mail


utilsForAll = UtilsForAll()


class ForoUtils:
    def getfromPost(self, request, campo=None):
        """Given a field return its value if exists. Return an empty string otherwise."""
        return utilsForAll.getfromPost(request, campo)

    def getfilefromPost(self, request, campo=None):
        """Given a field return its file value if exists. Return an empty string otherwise."""
        return utilsForAll.getfilefromPost(request, campo)
