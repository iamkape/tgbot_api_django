from . import api
from django.urls import path

from .api import data_admin, data_lot, save_price, upload_doc, unactive_lot

urlpatterns = [
    path('bid/<str:id_lot>',data_admin),
    path('lot/<str:id_lot>',data_lot),
    path('save_price/<str:id_lot>',save_price),
    path('document/<str:id_lot>', upload_doc),
    path('delete', unactive_lot)
]