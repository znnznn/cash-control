from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404


class UserAffiliationMixin(AccessMixin):
    """ Check user affiliation to view """

    def get_affiliation_user(self):
        """ Check user affiliation to view """

        model = get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        if model.user_id == self.request.user or self.request.user.is_staff:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        affiliation_result = self.get_affiliation_user()
        if not affiliation_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)