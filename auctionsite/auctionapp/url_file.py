from . import api
from django.urls import path

from .api import data_admin, data_lot, save_price, upload_doc, unactive_lot, take_lots, up_balance

urlpatterns = [
    path('active_lots', take_lots),
    path('bid/<str:id_lot>',data_admin),
    path('lot/<str:id_lot>',data_lot),
    path('save_price/<str:id_lot>',save_price),
    path('document/<str:id_lot>', upload_doc),
    path('delete', unactive_lot),
    path('balance_up', up_balance)
]