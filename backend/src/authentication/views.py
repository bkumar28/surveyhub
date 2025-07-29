from django.shortcuts import render
from django.views import View


class RootView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "dashboard.html")
        return render(request, "auth/login.html")
