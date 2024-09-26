from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Cliente, Carro
import re
from django.core import serializers
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
import json
from django.views.decorators.csrf import csrf_exempt


def clientes(request):
    if request.method == "GET":
        clientes_list = Cliente.objects.all()
        return render(request, 'clientes.html', {'clientes': clientes_list})
    elif request.method == "POST":
        nome = request.POST.get('Primeiro nome')
        sobrenome = request.POST.get('Sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        carros = request.POST.getlist('carro')
        placas = request.POST.getlist('placa')
        anos = request.POST.getlist('ano')
        print(nome)
        cliente = Cliente.objects.filter(cpf=cpf)
        print(email)
        
        if cliente.exists(): 
            return HttpResponse('Cliente ja existe')
        
        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'cpf': cpf, 'carros': zip(carros, placas, anos)})

        
        cliente = Cliente(
            nome = nome,
            sobrenome = sobrenome,
            email = email,
            cpf = cpf
        )
        cliente.save()
        
        
        for carro, placa, ano in zip(carros, placas, anos):
            car = Carro(carro=carro, placa=placa, ano=ano, cliente=cliente)
            car.save()
        return render(request, 'clientes.html')
def att_cliente(request):
    id_cliente = request.POST.get('id_cliente')
    cliente = Cliente.objects.filter(id=id_cliente)
    carros = Carro.objects.filter(cliente=cliente[0])
    print(carros)
    cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']
    cliente_id = json.loads(serializers.serialize('json', cliente))[0]['pk']
    cliente_id = json.loads(serializers.serialize('json', cliente))[0]['pk']    
    carros_json =  json.loads(serializers.serialize('json', carros))
    carros_json = [{'fields': carro['fields'], 'id': carro['pk']} for carro in carros_json] 
    data = {'cliente': cliente_json, 'carros': carros_json, 'clientes_id': cliente_id} 
    print(carros_json)
    return  JsonResponse(data)

@csrf_exempt    
def update_carro(request, id):
    nome_carro = request.POST.get('carro')
    placa = request.POST.get('placa') 
    ano = request.POST.get('ano')
    
    carro = Carro.objects.get(id=id)

    list_carros = Carro.objects.filter(placa=placa).exclude(id=id)
    
    if list_carros.exists():
        return HttpResponse('Placa já existe')
    carro.carro = nome_carro
    carro.placa = placa
    carro.ano = ano
    carro.save()
    return HttpResponse ('dados alterados com sucesso')
 
def excluir_carro(request, id):
    try:
        carro = Carro.objects.get(id=id)
        carro.delete()
        return redirect(reverse('clientes')+f'?aba=att_cliente&id_cliente={id}') 
    except:
        return redirect(reverse('clientes'))
    
def update_cliente(request, id):
    body = json.loads(request.body)
    nome = body['nome']
    sobrenome = body['sobrenome']
    email = body['email']
    cpf = body['cpf']
    cliente = get_object_or_404(Cliente, id=id)
    try: 
        cliente.nome = nome
        cliente.sobrenome = sobrenome
        cliente.email = email
        cliente.cpf = cpf
        cliente.save()
        return JsonResponse({'status': '200','nome': nome, 'sobrenome': sobrenome, 'email': email, 'cpf': cpf})
    except:
        return JsonResponse({'status': '500'})
    return JsonResponse({'teste': teste})