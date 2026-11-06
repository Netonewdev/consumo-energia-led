-- =============================================================
-- Consultas de estudo (rode no sqlite3: .read sql/consultas.sql)
-- Considera 22 dias úteis por mês e tarifa de R$ 0,90 por kWh.
-- =============================================================

.headers on
.mode column

-- 1) Quantas lâmpadas cada ambiente tem
--    LEFT JOIN garante que ambientes sem lâmpada também apareçam
SELECT a.nome AS ambiente,
       COALESCE(SUM(i.quantidade), 0) AS total_lampadas
FROM ambientes a
LEFT JOIN instalacoes i ON i.ambiente_id = a.id
GROUP BY a.id
ORDER BY total_lampadas DESC;

-- 2) Consumo mensal (kWh) por ambiente
--    kWh = watts x quantidade x horas/dia x dias / 1000
SELECT a.nome AS ambiente,
       ROUND(SUM(t.potencia_watts * i.quantidade * a.horas_por_dia * 22 / 1000.0), 1) AS kwh_mes
FROM instalacoes i
JOIN ambientes a     ON a.id = i.ambiente_id
JOIN tipos_lampada t ON t.id = i.lampada_id
GROUP BY a.id
ORDER BY kwh_mes DESC;

-- 3) Ambiente que mais gasta (com custo em reais)
SELECT a.nome AS ambiente,
       ROUND(SUM(t.potencia_watts * i.quantidade * a.horas_por_dia * 22 / 1000.0) * 0.90, 2) AS custo_mes_reais
FROM instalacoes i
JOIN ambientes a     ON a.id = i.ambiente_id
JOIN tipos_lampada t ON t.id = i.lampada_id
GROUP BY a.id
ORDER BY custo_mes_reais DESC
LIMIT 1;

-- 4) Consumo por tecnologia (LED x Fluorescente x Incandescente)
SELECT t.tecnologia,
       SUM(i.quantidade) AS lampadas,
       ROUND(SUM(t.potencia_watts * i.quantidade * a.horas_por_dia * 22 / 1000.0), 1) AS kwh_mes
FROM instalacoes i
JOIN ambientes a     ON a.id = i.ambiente_id
JOIN tipos_lampada t ON t.id = i.lampada_id
GROUP BY t.tecnologia
ORDER BY kwh_mes DESC;

-- 5) Simulação: trocar tudo que não é LED pela LED equivalente
--    Usa CTE (WITH) e a mesma tabela duas vezes (atual e led)
WITH trocas AS (
    SELECT a.nome            AS ambiente,
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
       ROUND(SUM((potencia_atual - potencia_led) * quantidade * horas_por_dia * 22 / 1000.0), 1) AS economia_kwh_mes,
       ROUND(SUM(preco_led * quantidade), 2) AS investimento_reais
FROM trocas
GROUP BY ambiente
ORDER BY economia_kwh_mes DESC;
