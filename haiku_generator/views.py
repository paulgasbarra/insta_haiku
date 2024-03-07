from haiku_generator.models import Haiku
from django.http import Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
# haiku_generator/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import HaikuForm  # You'll create this form to handle haiku editing
from .utils import generate_haiku_and_image

def generate_haiku(request):
    haiku = generate_haiku_and_image()
    return redirect('view_haiku', haiku_id=haiku.id)

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
    haikus = Haiku.objects.order_by('-created_at')
    return render(request, 'haiku_generator/home.html', {'haikus': haikus})

def haiku(request, haiku_id):
    haiku = get_object_or_404(Haiku, pk=haiku_id)
    if haiku is not None:
        return render(request, 'haiku_generator/haiku.html', {'haiku': haiku})
    else:
        raise Http404("Haiku does not exist")
    
def haiku_list_view(request):
    haikus = Haiku.objects.all()
    return render(request, 'haiku_generator/home.html', {'haikus': haikus})
