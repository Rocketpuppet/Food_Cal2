from django.urls import path

from . import views

app_name = 'calculator'
urlpatterns = [
    path('',views.HomePage.as_view(), name='homepage'),
    path('add_recipe/', views.HomePage.addItem, name = 'add_recipe'),
    path('<int:pk>/', views.RecipeDetailPage.as_view(),name='ing_list'),
    path('base/', views.BaseIngPage.as_view(), name='base_list'),
    path('base_delete/<int:id>/', views.BaseIngPage.as_view(), name='ing_delete'),
    path('recipeing_delete/<int:id>/', views.RecipeDetailPage.delete_ing, name='ring_delete'),
    path('recipe_delete/<int:id>/', views.HomePage.delete, name = 'recipe_delete'),
    path('search_recipe/', views.HomePage.search, name="recipe_search"),
    path('all_recieps/',views.RecipeFilterPage.as_view(), name="filterPage")
]
