from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from .models import Profile


class ProfileView(TemplateView):
    template_name = 'users/profile_details.html'

    def get_context_data(self, **kwargs):
        context_data = super(ProfileView, self).get_context_data(**kwargs)
        user = self.request.user
        try:
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            profile = Profile.create(user=user)

        context_data['profile'] = profile
        return context_data


class ProfileEditView(UpdateView):
    model = Profile
    template_name = 'users/profile_edit.html'