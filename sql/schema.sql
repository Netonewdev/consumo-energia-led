-- =============================================================
-- Estrutura do banco: Sistema de Controle de Consumo de Iluminação
-- Banco: SQLite
-- =============================================================

PRAGMA foreign_keys = ON;

-- Apaga as tabelas se já existirem (permite recriar o banco do zero).
-- A ordem importa: primeiro quem depende das outras.
DROP TABLE IF EXISTS instalacoes;
DROP TABLE IF EXISTS tipos_lampada;
DROP TABLE IF EXISTS ambientes;

-- Locais que possuem iluminação (salas, corredores, laboratórios...)
CREATE TABLE ambientes (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    nome          TEXT    NOT NULL UNIQUE,
    horas_por_dia REAL    NOT NULL CHECK (horas_por_dia > 0 AND horas_por_dia <= 24)
);

-- Catálogo de lâmpadas. Lâmpadas não-LED apontam para a LED que as substitui.
CREATE TABLE tipos_lampada (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    nome               TEXT    NOT NULL UNIQUE,
    tecnologia         TEXT    NOT NULL CHECK (tecnologia IN ('LED', 'Fluorescente', 'Incandescente')),
    potencia_watts     REAL    NOT NULL CHECK (potencia_watts > 0),
    preco              REAL    NOT NULL CHECK (preco >= 0),
    led_equivalente_id INTEGER REFERENCES tipos_lampada(id)
);

-- Quantas lâmpadas de cada tipo existem em cada ambiente
CREATE TABLE instalacoes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ambiente_id INTEGER NOT NULL REFERENCES ambientes(id) ON DELETE CASCADE,
    lampada_id  INTEGER NOT NULL REFERENCES tipos_lampada(id),
    quantidade  INTEGER NOT NULL CHECK (quantidade > 0)
);
