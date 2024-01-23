from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item
from .forms import ItemForm

@csrf_exempt
def item_list(request):
    if request.method == 'GET':
        items = Item.objects.all()
        data = [{'id': item.id, 'name': item.name, 'description': item.description} for item in items]
        return JsonResponse({'items': data}, safe=False)

@csrf_exempt
def item_detail(request, pk):
    if request.method == 'GET':
        item = Item.objects.get(pk=pk)
        data = {'id': item.id, 'name': item.name, 'description': item.description}
        return JsonResponse(data)

@csrf_exempt
def item_new(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = ItemForm(data)
            if form.is_valid():
                item = form.save()
                return JsonResponse({'id': item.id, 'name': item.name, 'description': item.description})
            else:
                return JsonResponse({'error': 'Invalid data'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

@csrf_exempt
def item_edit(request, pk):
    if request.method == 'PUT':
        item = Item.objects.get(pk=pk)
        try:
            data = json.loads(request.body)
            form = ItemForm(data, instance=item)
            if form.is_valid():
                item = form.save()
                return JsonResponse({'id': item.id, 'name': item.name, 'description': item.description})
            else:
                return JsonResponse({'error': 'Invalid data'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)


@csrf_exempt
def item_delete(request, pk):
    if request.method == 'DELETE':
        item = Item.objects.get(pk=pk)
        item.delete()
        return JsonResponse({'message': 'Item deleted successfully'})
