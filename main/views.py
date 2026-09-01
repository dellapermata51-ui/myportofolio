from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'name': 'Della Permata Prasilda',
        'class': 'PBP A', # Bisa kamu sesuaikan
        'npm': '2506656614', # Bebas diisi atau disesuaikan
        'description': 'Selamat datang di website portofolio pribadiku!',
    }
    return render(request, "main.html", context)