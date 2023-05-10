from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import timezone
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import *
from django.urls import reverse
from django.views import generic
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.template.context_processors import csrf
from django.views.decorators.csrf import requires_csrf_token
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core import serializers
from django.db.models import Count



class HomePage(generic.ListView):

    template_name = 'calculator/homepage.html'
    context_object_name = 'recipe_list'


    def get_queryset(self):
    # recipe_list = recipe.objects.order_by('recipe_name')[:5]
    # output = ','.join([r.recipe_name for r in recipe_list])
        return Recipe.objects.order_by('recipe_name')[:5]

    def post(self, request):
        return HttpResponseRedirect(reverse("calculator:homepage"))
    
    @csrf_exempt
    def addItem(request):
        new_recipe = Recipe(recipe_name=request.POST.get('name'), servings=1, descripton=request.POST.get("desc"))
        new_recipe.save()

        data = {
            "id" : new_recipe.id,
            "url" : reverse("calculator:ing_list", kwargs={"pk" : new_recipe.id}),
            "del_url" : reverse("calculator:recipe_delete", kwargs={"id" : new_recipe.id}),
            "csrf" : get_token(request),
            "desc" : new_recipe.descripton,
            "time" : new_recipe.parse_time(),
        }

        return JsonResponse(data)

    @csrf_exempt
    @staticmethod
    def delete(request, id):
        recipe = get_object_or_404(Recipe, id=id)
        recipe.delete()

        return JsonResponse("Deleted",safe=False)

    @csrf_exempt
    @staticmethod
    def search(request):
        recipes = Recipe.objects.filter(recipe_name__contains=request.POST.get("name"))
        response = []
        for recipe in recipes:
            response.append({"label": recipe.recipe_name, 
            "value": recipe.id, "desc": recipe.descripton, 
            "date": recipe.parse_time(), 
            "del_url":reverse("calculator:recipe_delete", kwargs={"id" : recipe.id}),
            "url": reverse("calculator:ing_list", kwargs={"pk" : recipe.id})})
        return JsonResponse(response, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class RecipeFilterPage(generic.ListView):
    template_name = "calculator/recipe_filter.html"
    context_object_name = "recipe_list"

    def get_queryset(self):
        return Recipe.objects.order_by("-time_created")[:10]

    def filter(self, filter):
        pass
    
    def post(self, request):
        Date = ""
        Price = ""
        Name = ""

        if request.POST["Date"]=="Newest":
            Date = "time_created"
        if request.POST["Date"]=="Oldest":
            Date = "-time_created"
        
        if request.POST["Price"] == "Descending":
            Price = "-price"
        if request.POST["Price"] == "Ascending":
            Price = "price"

        if request.POST["Name"] == "Descending":
            Name = "-name"
        if request.POST["Name"] == "Ascending":
            Name = "name"

        filter = []

        for key, value in request.POST.items():
            col = ""
            if key=="Date":
                col = "time_created"
                if value == "Oldest":
                    col = "-" + col

            elif key=="Name":
                col = "recipe_name"
                if value == "Descending":
                    col = "-" + col

            if col != "":
                filter.append(col)


        
        
        recipes = Recipe.objects.order_by(*filter)
        if request.POST["minIng"] != "null":
            min = int(request.POST["minIng"])
            recipes = recipes.annotate(numIpytng=Count("recipeing"))
            recipes=recipes.filter(numIng__gte=min)
        


        SerializedObj = list(recipes.values())

        if request.POST["Price"] != "null":
            def key_func(x):
                price = Recipe.objects.get(pk=x["id"]).calulcate_price()[0]
                if request.POST["Price"] == "Ascending":
                    return price
                else:
                    return -price

            SerializedObj = sorted(SerializedObj, key=key_func)

        print(SerializedObj)
        for rec_id in SerializedObj:
            rec_id["url"] = reverse("calculator:ing_list", kwargs={"pk" : rec_id["id"]})


        return JsonResponse(SerializedObj,safe=False)
        
        
@method_decorator(csrf_exempt, name='dispatch')
class RecipeDetailPage(generic.DetailView):

    model = Recipe

    def post(self,request,*args,**kwargs):
        Bases = BaseIng
        if "servings" in request.POST:
            object = self.get_object()
            object.servings = int(request.POST.get('servings'))
            object.save()


            data = {
             "servings" : object.servings,
             "perSprice" : object.calulcate_price(),
            }

            return JsonResponse(data)

        else:
            newRecipeIng = RecipeIng(item_mass = float(request.POST.get('quan')), recipe=self.get_object(), base_ing=Bases.objects.get(id=request.POST.get('ing')))
            newRecipeIng.save()
            print(newRecipeIng.base_ing.price_per_unit,newRecipeIng.item_mass)
            print(newRecipeIng.calulcate_price())
            data = {
            "mass" : newRecipeIng.item_mass,
            "name" : newRecipeIng.base_ing.ing_name,
            "price" : newRecipeIng.base_ing.price_per_unit,
            "del_url" : reverse("calculator:ring_delete", kwargs={'id':newRecipeIng.id}),
            "csrf" : get_token(request),
            "obj_id" : newRecipeIng.id,
            "total_price" : newRecipeIng.calulcate_price()

            }

            return JsonResponse(data)

    @staticmethod
    def autocomplete(request):
        query = request.get("term", " ")
        Options = BaseIng.objects.filter(ing_name__icontains=query)
        Options = [option.name for option in Options]

        return JsonResponse(Options)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['ing_list'] = self.get_object().recipeing_set.all()
        context['base_ing'] = BaseIng.objects.all()
        context['servings'] = self.get_object().servings
        context['prices'] = self.get_object().calulcate_price()

        return context

    @csrf_exempt
    @staticmethod
    def delete_ing(request, id):
        Ing = get_object_or_404(RecipeIng, id=id)
        Ing.delete()

        return JsonResponse("deleted", safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class BaseIngPage(generic.ListView):

    model = BaseIng

    def post(self,request,*args,**kwargs):
        if request.POST.get('ing_name') and request.POST.get('price_per_unit'):
            new_base = BaseIng(ing_name = request.POST.get('ing_name'), price_per_unit = request.POST.get('price_per_unit'), measurement_type=request.POST.get('m_u'))
            new_base.save()

            return HttpResponseRedirect(reverse("calculator:base_list"))
       
        else:

            Ing = get_object_or_404(BaseIng, id=request.POST.get('id'))
            Ing.delete()
            return JsonResponse("deleted", safe=False)
        
