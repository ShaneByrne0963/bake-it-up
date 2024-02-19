from django.shortcuts import render
from django.views import View


class Home(View):
    """
    View to bring the user to the home page
    """
    template = 'home/index.html'

    def get(self, request):
        context = {}
        return render(request, self.template, context)
