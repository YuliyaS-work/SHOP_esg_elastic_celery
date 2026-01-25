from django.urls import path

from .views import *

urlpatterns = [
    path('', get_main_page, name='main'),
    path('catalog/', get_catalog, name='catalog'),
    path('contacts/', get_contact, name='contacts'),
    path('payments/', get_payments, name='payments'),
    path('partners/', get_partners, name='partners'),
    path('privacy/', get_privacy, name='privacy'),

    path('basket/', get_basket, name='basket'),
    path('search/', search_view, name='search'),
    # path('404/', get_404, name='404'),

    path('basket/api/order/', OrderAPICreate.as_view(), name='order_api_create'),
    path('api/feedback/', FeedbackAPICreate.as_view(), name='feedback'),

    path('<slug:rubric_name_translit>/<slug:subrubric_title_translit>/<slug:product_title_translit>/', get_product, name='product'),
    path('<slug:rubric_name_translit>/<slug:subrubric_title_translit>/', get_products, name='products'),
    path('<slug:rubric_name_translit>/', get_subrubrics, name='subrubrics'),
]
