import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from .forms import ProductForm

def get_product_data(product):
    return {
        'id': product.id, 
        'name': product.name, 
        'description': product.description,
        'price': product.price,
        'category': product.category,
        'quantity': product.quantity,
        'created_at': product.created_at,
        'updated_at': product.updated_at,
    }

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        product_data = [get_product_data(product) for product in products]

        return JsonResponse({
            'success': True,
            'data': product_data,
        }, safe=False)

@csrf_exempt
def product_detail(request, pk):
    if request.method == 'GET':
        product = Product.objects.get(pk=pk)
        product_data = get_product_data(product)

        return JsonResponse({
            'success': True,
            'data': product_data,
        })

@csrf_exempt
def product_new(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = ProductForm(data)
            if form.is_valid():
                product = form.save()
                product_data = get_product_data(product)

                return JsonResponse({
                        'success': True,
                        'data': product_data,
                })
            else:
                return JsonResponse({
                    'success': True,
                    'data': 'Invalid data',
                }, status=400)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'data': 'Invalid JSON data',
            }, status=400)

@csrf_exempt
def product_edit(request, pk):
    if request.method == 'PUT':
        product = Product.objects.get(pk=pk)
        try:
            data = json.loads(request.body)
            form = ProductForm(data, instance=product)
            if form.is_valid():
                product = form.save()
                product_data = get_product_data(product)

                return JsonResponse({
                        'success': True,
                        'data': product_data,
                })
            else:
                return JsonResponse({
                    'success': False,
                    'data': 'Invalid data',
                }, status=400)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'data': 'Invalid JSON data',
            }, status=400)

@csrf_exempt
def product_delete(request, pk):
    if request.method == 'DELETE':
        product = Product.objects.get(pk=pk)
        product.delete()

        return JsonResponse({
            'status': True,
            'data': 'Product successfully deleted',
        })
