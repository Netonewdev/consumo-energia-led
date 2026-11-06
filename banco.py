"""Conexão com o banco SQLite e operações de cadastro e listagem."""
import sqlite3
from pathlib import Path

from regras import validar_horas, validar_nome, validar_quantidade

PASTA_PROJETO = Path(__file__).parent
PASTA_SQL = PASTA_PROJETO / "sql"
CAMINHO_BANCO = PASTA_PROJETO / "energia.db"


def conectar(caminho=CAMINHO_BANCO):
    """Abre a conexão e ativa as chaves estrangeiras (no SQLite vêm desligadas)."""
    conexao = sqlite3.connect(caminho)
    conexao.row_factory = sqlite3.Row  # permite acessar colunas pelo nome: linha["nome"]
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas(conexao, com_dados_exemplo=True):
    """Executa os scripts SQL que criam as tabelas e (opcionalmente) os dados de exemplo."""
    conexao.executescript((PASTA_SQL / "schema.sql").read_text(encoding="utf-8"))
    if com_dados_exemplo:
        conexao.executescript((PASTA_SQL / "dados.sql").read_text(encoding="utf-8"))
    conexao.commit()


def listar_ambientes(conexao):
    return conexao.execute("""
        SELECT a.id, a.nome, a.horas_por_dia,
               COALESCE(SUM(i.quantidade), 0) AS total_lampadas
        FROM ambientes a
        LEFT JOIN instalacoes i ON i.ambiente_id = a.id
        GROUP BY a.id
        ORDER BY a.nome
    """).fetchall()


def listar_tipos_lampada(conexao):
    return conexao.execute("""
        SELECT id, nome, tecnologia, potencia_watts, preco
        FROM tipos_lampada
        ORDER BY tecnologia, potencia_watts
    """).fetchall()


def cadastrar_ambiente(conexao, nome, horas_por_dia):
    """Cadastra um ambiente e devolve o id gerado.

    Os valores vão como parâmetros (?) e não concatenados no texto do SQL,
    o que evita SQL Injection.
    """
    validar_nome(nome)
    validar_horas(horas_por_dia)
    cursor = conexao.execute(
        "INSERT INTO ambientes (nome, horas_por_dia) VALUES (?, ?)",
        (nome.strip(), horas_por_dia),
    )
    conexao.commit()
    return cursor.lastrowid


def adicionar_lampadas(conexao, ambiente_id, lampada_id, quantidade):
    validar_quantidade(quantidade)
    conexao.execute(
        "INSERT INTO instalacoes (ambiente_id, lampada_id, quantidade) VALUES (?, ?, ?)",
        (ambiente_id, lampada_id, quantidade),
    )
    conexao.commit()
