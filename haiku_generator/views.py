from django.shortcuts import render

# Create your views here.
# haiku_generator/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Haiku
from .forms import HaikuForm  # You'll create this form to handle haiku editing

@login_required
def generate_haiku(request):
    # Your logic to generate a haiku and save it
    haiku = Haiku.objects.create(text="Generated haiku", image="path/to/generated/image.jpg")
    return redirect('edit_haiku', pk=haiku.pk)

@login_required
def edit_haiku(request, pk):
    haiku = Haiku.objects.get(pk=pk)
    if request.method == 'POST':
        form = HaikuForm(request.POST, request.FILES, instance=haiku)
        if form.is_valid():
            form.save()
            return redirect('edit_haiku', pk=haiku.pk)
    else:
        form = HaikuForm(instance=haiku)
    return render(request, 'haiku_generator/edit_haiku.html', {'form': form})

@login_required
def publish_haiku(request, pk):
    # Your logic to publish a haiku
    haiku = Haiku.objects.get(pk=pk)
    haiku.published = True
    haiku.save()
    # Add your Instagram API publishing logic here
    return redirect('edit_haiku', pk=haiku.pk)

def home(request):
    return render(request, 'haiku_generator/home.html')
