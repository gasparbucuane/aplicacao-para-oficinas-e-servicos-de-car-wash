from django.forms import ModelForm
from .models import Servico, CategoriaManutencao

class FormServico(ModelForm):
    class Meta:
        model = Servico
        exclude = ['finalizado', 'protocolo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields[field].widget.attrs.update({'placeholder': field})
            

        choices = list()
        for i, j in self.fields['categoria_manutencao'].choices:
            categorias = CategoriaManutencao.objects.filter(titulo=j)
            categoria = categorias.first()  # ou outra lógica para escolher a categoria correta
            choices.append((i.value, categoria.get_titulo_display()))
            self.fields['categoria_manutencao'].choices = choices
