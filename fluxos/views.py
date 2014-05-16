from django.shortcuts import render, HttpResponseRedirect
from datetime import datetime
from caixas.models import Conta
from pessoas.models import Pessoa

def listarFluxos(request):
    pessoas = Pessoa.objects.all().order_by('nome')
    return render(request, 'fluxos/listarFluxos.html', {'pessoas': pessoas})

def pesquisarFluxos(request):
    if request.method == 'POST':
        pessoaBusca = request.POST.get('pessoaBusca')
        dataBuscaInicio = datetime.strptime(request.POST.get('dataBuscaInicio', ''), '%d/%m/%Y %H:%M:%S')
        dataBuscaFim = datetime.strptime(request.POST.get('dataBuscaFinal', ''), '%d/%m/%Y %H:%M:%S')
        
        nome = Pessoa.objects.filter(id=pessoaBusca)
        pessoas = Pessoa.objects.all().order_by('nome')

        totalreceber = 0
        totalpagar = 0
       
        try:
            sql = "select * from caixas_conta where pessoa_id like %s  and data >= '%s' and  data <= '%s'" % (pessoaBusca, dataBuscaInicio, dataBuscaFim)
            contas = Conta.objects.raw(sql)

            for item in contas:
                if item.tipo == 'E':
                    totalreceber = totalreceber + item.valor
                else:
                    totalpagar = totalpagar + item.valor

                total = totalreceber - totalpagar
        except:
            contas = [Conta(descricao='erro')]

        return render(request, 'fluxos/listarFluxos.html', {'contas': contas, 'nome':nome, 'pessoas': pessoas, 'totalreceber':totalreceber,'totalpagar':totalpagar, 'total':total})


