from django.urls import path
from django.views.generic.base import RedirectView
from django.views.generic.dates import ArchiveIndexView
from . import views
from .models import Article

urlpatterns = [
    path('', views.HomePageView.as_view(), name="article_home"),
    # path('counter/<int:pk>/', views.ArticleCounterRedirectView.as_view(), name='article-counter'),
    path('<int:pk>/', RedirectView.as_view(), name='article-detail'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('lists/', views.ArticleListView.as_view(), name="article-list"),

    path('archive/', ArchiveIndexView.as_view(model=Article, date_field="pub_date"), name="article_archive"),
    path('<int:year>/', views.ArticleYearArchiveView.as_view(), name="article_year_archive"),
    path('<int:year>/<int:month>/', views.ArticleMonthArchiveView.as_view(month_format='%m'), name="month_archive_numeric"),
    path('<int:year>/<str:month>/', views.ArticleMonthArchiveView.as_view(), name="month_archive"),
    path('<int:year>/week/<int:week>/', views.ArticleWeekArchiveView.as_view(), name="week_archive"),
    path('<int:year>/<str:month>/<int:day>/', views.ArticleDayArchiveView.as_view(), name="day_archive"),


]