from django.db.models import TextChoices

class ChoicesCategoriaManutencao(TextChoices):
    TROCAR_VALVULA_MOTOR = "TVM", "Trocar Valvula do motor"
    TROCAR_OLEO = "TO", "Troca de oleo"
    BALANCEAMENTO = "B", "Balanceamneto"