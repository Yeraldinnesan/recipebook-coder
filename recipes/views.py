from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .forms import RecipeForm
from .models import Recipe
from django.db.models import Q
from django.urls import reverse

# Create your views here.


def home(request):
    recipes = Recipe.objects.all()

    return render(request, 'index.html', {'recipes': recipes})


# def recipe_detail(request, recipe_id):
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
#     recipe = get_object_or_404(Recipe, pk=recipe_id)
    comments = recipe.comments.all().order_by('-created_at')
    return render(request, 'recipedetail.html', {'recipe': recipe, 'comments': comments})
#     return render(request, 'recipedetail.html', {'recipe': recipe, 'comments': comments})


def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.category = form.cleaned_data['category']
            recipe.save()
            return redirect(reverse('recipedetail', args=[recipe.id]))
    else:
        form = RecipeForm()
    return render(request, 'createrecipe.html', {'form': form})


def search_recipe(request):
    queryset = Recipe.objects.all()
    query = request.GET.get('keywords')

    if query:
        queryset = queryset.filter(
            # Q object to construct an OR query
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__icontains=query) |
            Q(instructions__icontains=query)
        ).distinct()

    return render(request, 'searchresult.html', {'recipes': queryset})
