-- =============================================================
-- Dados de exemplo (fictícios) para testar o sistema
-- =============================================================

-- Lâmpadas LED primeiro, porque as outras apontam para elas
INSERT INTO tipos_lampada (id, nome, tecnologia, potencia_watts, preco, led_equivalente_id) VALUES
    (1, 'LED tubular 18W',           'LED',           18, 25.00, NULL),
    (2, 'LED bulbo 9W',              'LED',            9, 12.00, NULL),
    (3, 'Fluorescente tubular 40W',  'Fluorescente',  40, 15.00, 1),
    (4, 'Incandescente 60W',         'Incandescente', 60,  5.00, 2),
    (5, 'Fluorescente compacta 25W', 'Fluorescente',  25, 12.00, 2);

INSERT INTO ambientes (id, nome, horas_por_dia) VALUES
    (1, 'Sala 101',                   10),
    (2, 'Sala 102',                   10),
    (3, 'Laboratório de Informática', 12),
    (4, 'Biblioteca',                 12),
    (5, 'Corredor principal',         14),
    (6, 'Secretaria',                  9);

INSERT INTO instalacoes (ambiente_id, lampada_id, quantidade) VALUES
    (1, 3,  8),   -- Sala 101: 8 fluorescentes tubulares
    (2, 3,  6),   -- Sala 102: 6 fluorescentes tubulares...
    (2, 1,  2),   --           ...e 2 que já foram trocadas por LED
    (3, 3, 12),   -- Laboratório: 12 fluorescentes tubulares
    (4, 3, 10),   -- Biblioteca: 10 fluorescentes tubulares...
    (4, 5,  4),   --             ...e 4 compactas
    (5, 4, 10),   -- Corredor: 10 incandescentes
    (6, 5,  4),   -- Secretaria: 4 compactas...
    (6, 1,  2);   --             ...e 2 LED tubulares
