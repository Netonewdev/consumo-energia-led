"""Consultas de relatório: consumo atual e simulação de troca para LED."""


def consumo_por_ambiente(conexao, dias_por_mes):
    return conexao.execute("""
        SELECT a.nome AS ambiente,
               SUM(t.potencia_watts * i.quantidade * a.horas_por_dia * ? / 1000.0) AS kwh_mes
        FROM instalacoes i
        JOIN ambientes a     ON a.id = i.ambiente_id
        JOIN tipos_lampada t ON t.id = i.lampada_id
        GROUP BY a.id
        ORDER BY kwh_mes DESC
    """, (dias_por_mes,)).fetchall()


def simulacao_troca_led(conexao, dias_por_mes):
    """Para cada ambiente, quanto se economiza trocando as lâmpadas não-LED pela LED equivalente.

    A tabela tipos_lampada aparece duas vezes no JOIN: uma como a lâmpada
    atual e outra como a LED que a substitui (led_equivalente_id).
    """
    return conexao.execute("""
        WITH trocas AS (
            SELECT a.id                 AS ambiente_id,
                   a.nome               AS ambiente,
                   i.quantidade,
                   a.horas_por_dia,
                   atual.potencia_watts AS potencia_atual,
                   led.potencia_watts   AS potencia_led,
                   led.preco            AS preco_led
            FROM instalacoes i
            JOIN ambientes a         ON a.id = i.ambiente_id
            JOIN tipos_lampada atual ON atual.id = i.lampada_id
            JOIN tipos_lampada led   ON led.id = atual.led_equivalente_id
        )
        SELECT ambiente,
               SUM(quantidade) AS lampadas_trocadas,
               SUM((potencia_atual - potencia_led) * quantidade * horas_por_dia * ? / 1000.0)
                   AS economia_kwh_mes,
               SUM(preco_led * quantidade) AS investimento
        FROM trocas
        GROUP BY ambiente_id
        ORDER BY economia_kwh_mes DESC
    """, (dias_por_mes,)).fetchall()
