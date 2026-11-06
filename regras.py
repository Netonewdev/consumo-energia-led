"""Regras de negócio: cálculos de consumo e validação dos dados de entrada."""


def consumo_kwh(potencia_watts, quantidade, horas_por_dia, dias):
    """Energia consumida em kWh: watts x quantidade x horas x dias / 1000."""
    return potencia_watts * quantidade * horas_por_dia * dias / 1000


def custo_reais(kwh, tarifa_kwh):
    """Custo em reais de uma quantidade de energia."""
    return kwh * tarifa_kwh


def meses_para_retorno(investimento, economia_mensal_reais):
    """Em quantos meses a troca se paga. Retorna None se não houver economia."""
    if economia_mensal_reais <= 0:
        return None
    return investimento / economia_mensal_reais


def validar_nome(nome):
    if not nome or not nome.strip():
        raise ValueError("O nome não pode ficar vazio.")


def validar_horas(horas_por_dia):
    if not 0 < horas_por_dia <= 24:
        raise ValueError("As horas por dia devem estar entre 0 e 24.")


def validar_quantidade(quantidade):
    if not isinstance(quantidade, int) or quantidade <= 0:
        raise ValueError("A quantidade deve ser um número inteiro maior que zero.")
