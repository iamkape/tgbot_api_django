from datetime import datetime
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models, serializers
from docxtpl import DocxTemplate


@api_view(['GET'])
def data_admin(request, id_lot):
    '''Отправляет все данные из модели Админа'''
    all_info = models.AdminProfile.objects.all()
    serializer = serializers.AdminProfileSerializer(all_info, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def data_lot(request, id_lot):
    '''Отправляет все данные из модели Лота'''
    all_info = models.Lot.objects.filter(id=id_lot)
    serializer = serializers.LotSerializer(all_info, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def save_price(request, id_lot):
    '''Сохраняет данные в БД'''
    request_data = dict(request.GET)
    lot = models.Lot.objects.get(id=id_lot)
    admin = models.AdminProfile.objects.get(lot=id_lot)
    admin.current_price = float(request_data['new_price'][0])
    admin.user_name_bid = request_data['user_name_bid'][0]
    lot.start_price = float(request_data['new_price'][0])
    admin.save()
    lot.save()
    return Response('ok')

@api_view(['POST'])
def upload_doc(request, id_lot):
    '''Создаёт документы на основе шаблона'''
    request_data = dict(request.GET) #{'type': ['hist'], 'user_name': ['unotuno']}
    lot = models.Lot.objects.get(id=id_lot)
    type = request_data['type']
    type_doc = ''.join(type)
    name = request_data['user_name']
    user_name = ''.join(name)
    doc = DocxTemplate(f'auctionsite/document/template/{type_doc}.docx')
    data_doc = {}
    for field_name in lot._meta.get_fields():
        if field_name.name != 'id' and not field_name.many_to_many and not field_name.one_to_many:
            data_doc[field_name.name] = getattr(lot, field_name.name)
        data_doc['user_name'] = user_name
    doc.render(data_doc)
    file_name = f'{lot.name_lot}_{user_name}_{type_doc}.docx'
    path_to_doc = f'auctionsite/document/{lot.name_lot}_{user_name}_{type_doc}.docx'
    doc.save(path_to_doc)
    return JsonResponse({'path_to_doc': path_to_doc, 'file_name': file_name})

@api_view(['POST'])
def unactive_lot(request):
    '''Удаляет и в модели юзера отнимает 5% от текущей стоимости лота'''
    request_data = dict(request.GET)
    id_lot = request_data['name_lot']
    name = ''.join(id_lot)
    lot = models.Lot.objects.get(name_lot=name)
    admin = models.AdminProfile.objects.get(lot=lot.id)
    user = models.UserProfile.objects.get(user=lot.creator)
    penalty = float(user.balance) - ((float(admin.current_price) * 0.05))
    user.balance = penalty
    admin.current_price = 0.00
    admin.active_lot = 'False'
    admin.user_name_bid = ''
    admin.save()
    user.save()
    return JsonResponse({'pen':user.balance})