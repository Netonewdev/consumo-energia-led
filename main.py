"""Sistema de Controle de Consumo de Iluminação - menu no terminal."""
import sqlite3

import banco
import relatorio
from regras import custo_reais, meses_para_retorno

DIAS_POR_MES = 22   # dias úteis em um mês
TARIFA_KWH = 0.90   # R$ por kWh (valor de exemplo: ajuste conforme a conta de luz)


# ---------- Funções auxiliares de entrada e formatação ----------

def ler_inteiro(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Digite um número inteiro.")


def ler_decimal(mensagem):
    while True:
        try:
            return float(input(mensagem).replace(",", "."))
        except ValueError:
            print("Digite um número (ex.: 8 ou 7,5).")


def reais(valor):
    """Formata no padrão brasileiro: 1234.5 -> 'R$ 1.234,50'."""
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


# ---------- Opções do menu ----------

def mostrar_ambientes(conexao):
    ambientes = banco.listar_ambientes(conexao)
    if not ambientes:
        print("Nenhum ambiente cadastrado.")
        return
    print(f"\n{'ID':>3}  {'Ambiente':<28} {'Horas/dia':>9} {'Lâmpadas':>9}")
    for a in ambientes:
        print(f"{a['id']:>3}  {a['nome']:<28} {a['horas_por_dia']:>9.1f} {a['total_lampadas']:>9}")


def cadastrar_ambiente(conexao):
    nome = input("Nome do ambiente: ")
    horas = ler_decimal("Horas ligadas por dia: ")
    try:
        novo_id = banco.cadastrar_ambiente(conexao, nome, horas)
        print(f"Ambiente cadastrado com ID {novo_id}.")
    except ValueError as erro:
        print(f"Erro: {erro}")
    except sqlite3.IntegrityError:
        print("Erro: já existe um ambiente com esse nome.")


def adicionar_lampadas(conexao):
    mostrar_ambientes(conexao)
    ambiente_id = ler_inteiro("\nID do ambiente: ")

    print(f"\n{'ID':>3}  {'Lâmpada':<28} {'Potência':>8} {'Preço':>10}")
    for t in banco.listar_tipos_lampada(conexao):
        print(f"{t['id']:>3}  {t['nome']:<28} {t['potencia_watts']:>6.0f} W {reais(t['preco']):>10}")
    lampada_id = ler_inteiro("\nID do tipo de lâmpada: ")
    quantidade = ler_inteiro("Quantidade: ")

    try:
        banco.adicionar_lampadas(conexao, ambiente_id, lampada_id, quantidade)
        print("Lâmpadas adicionadas.")
    except ValueError as erro:
        print(f"Erro: {erro}")
    except sqlite3.IntegrityError:
        print("Erro: ambiente ou tipo de lâmpada não encontrado.")


def mostrar_consumo(conexao):
    linhas = relatorio.consumo_por_ambiente(conexao, DIAS_POR_MES)
    if not linhas:
        print("Nenhuma lâmpada cadastrada ainda.")
        return

    print(f"\nConsumo mensal ({DIAS_POR_MES} dias, tarifa {reais(TARIFA_KWH)}/kWh)\n")
    print(f"{'Ambiente':<28} {'kWh/mês':>9} {'Custo/mês':>13}")
    total_kwh = 0
    for linha in linhas:
        total_kwh += linha["kwh_mes"]
        custo = custo_reais(linha["kwh_mes"], TARIFA_KWH)
        print(f"{linha['ambiente']:<28} {linha['kwh_mes']:>9.1f} {reais(custo):>13}")
    print("-" * 52)
    print(f"{'TOTAL':<28} {total_kwh:>9.1f} {reais(custo_reais(total_kwh, TARIFA_KWH)):>13}")


def mostrar_simulacao(conexao):
    linhas = relatorio.simulacao_troca_led(conexao, DIAS_POR_MES)
    if not linhas:
        print("Todas as lâmpadas já são LED. Nada para trocar!")
        return

    print("\nSimulação: trocar as lâmpadas atuais por LED\n")
    print(f"{'Ambiente':<28} {'Trocas':>6} {'Economia/mês':>13} {'Investimento':>13} {'Retorno':>9}")
    total_economia = total_investimento = 0
    for linha in linhas:
        economia = custo_reais(linha["economia_kwh_mes"], TARIFA_KWH)
        total_economia += economia
        total_investimento += linha["investimento"]
        meses = meses_para_retorno(linha["investimento"], economia)
        retorno = f"{meses:.1f} m" if meses else "-"
        print(f"{linha['ambiente']:<28} {linha['lampadas_trocadas']:>6} "
              f"{reais(economia):>13} {reais(linha['investimento']):>13} {retorno:>9}")
    print("-" * 73)
    meses_total = meses_para_retorno(total_investimento, total_economia)
    print(f"{'TOTAL':<28} {'':>6} {reais(total_economia):>13} {reais(total_investimento):>13} "
          f"{meses_total:>7.1f} m")
    print(f"\nEconomia estimada em 1 ano: {reais(total_economia * 12)}")


def recriar_banco(conexao):
    if input("Isso apaga tudo e volta aos dados de exemplo. Confirmar? (s/n) ").lower() == "s":
        banco.criar_tabelas(conexao)
        print("Banco recriado.")


# ---------- Programa principal ----------

OPCOES = {
    "1": ("Listar ambientes", mostrar_ambientes),
    "2": ("Cadastrar ambiente", cadastrar_ambiente),
    "3": ("Adicionar lâmpadas a um ambiente", adicionar_lampadas),
    "4": ("Relatório de consumo", mostrar_consumo),
    "5": ("Simular troca para LED", mostrar_simulacao),
    "6": ("Recriar banco com dados de exemplo", recriar_banco),
}


def main():
    banco_novo = not banco.CAMINHO_BANCO.exists()
    conexao = banco.conectar()
    if banco_novo:
        banco.criar_tabelas(conexao)
        print("Banco criado com dados de exemplo.")

    while True:
        print("\n=== Controle de Consumo de Iluminação ===")
        for tecla, (texto, _) in OPCOES.items():
            print(f"{tecla} - {texto}")
        print("0 - Sair")

        escolha = input("Opção: ").strip()
        if escolha == "0":
            break
        if escolha in OPCOES:
            OPCOES[escolha][1](conexao)
        else:
            print("Opção inválida.")

    conexao.close()


if __name__ == "__main__":
    main()
