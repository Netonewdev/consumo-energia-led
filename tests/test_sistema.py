"""Testes automatizados. Rode com: python -m unittest -v"""
import sqlite3
import unittest

import banco
import relatorio
from regras import (consumo_kwh, custo_reais, meses_para_retorno,
                    validar_horas, validar_nome, validar_quantidade)

DIAS = 22


class TestRegras(unittest.TestCase):
    def test_consumo_kwh(self):
        # 10 lâmpadas de 40 W, 10 h por dia, 22 dias = 88 kWh
        self.assertAlmostEqual(consumo_kwh(40, 10, 10, 22), 88.0)

    def test_custo_reais(self):
        self.assertAlmostEqual(custo_reais(100, 0.90), 90.0)

    def test_meses_para_retorno(self):
        self.assertAlmostEqual(meses_para_retorno(300, 100), 3.0)
        self.assertIsNone(meses_para_retorno(300, 0))

    def test_validacoes_rejeitam_valores_invalidos(self):
        with self.assertRaises(ValueError):
            validar_horas(25)
        with self.assertRaises(ValueError):
            validar_horas(0)
        with self.assertRaises(ValueError):
            validar_quantidade(0)
        with self.assertRaises(ValueError):
            validar_nome("   ")


class TestBanco(unittest.TestCase):
    def setUp(self):
        # Banco em memória: cada teste começa do zero e não mexe no energia.db
        self.conexao = banco.conectar(":memory:")
        banco.criar_tabelas(self.conexao)

    def tearDown(self):
        self.conexao.close()

    def test_dados_de_exemplo_carregados(self):
        self.assertEqual(len(banco.listar_ambientes(self.conexao)), 6)

    def test_cadastrar_ambiente(self):
        novo_id = banco.cadastrar_ambiente(self.conexao, "Auditório", 6)
        nomes = [a["nome"] for a in banco.listar_ambientes(self.conexao)]
        self.assertIn("Auditório", nomes)
        self.assertIsNotNone(novo_id)

    def test_nao_aceita_nome_duplicado(self):
        with self.assertRaises(sqlite3.IntegrityError):
            banco.cadastrar_ambiente(self.conexao, "Sala 101", 8)

    def test_nao_aceita_ambiente_inexistente(self):
        with self.assertRaises(sqlite3.IntegrityError):
            banco.adicionar_lampadas(self.conexao, 9999, 1, 5)

    def test_consumo_sql_bate_com_calculo_python(self):
        ambiente_id = banco.cadastrar_ambiente(self.conexao, "Sala Teste", 8)
        banco.adicionar_lampadas(self.conexao, ambiente_id, 1, 5)  # 5 x LED 18 W

        linhas = relatorio.consumo_por_ambiente(self.conexao, DIAS)
        sala = next(l for l in linhas if l["ambiente"] == "Sala Teste")
        self.assertAlmostEqual(sala["kwh_mes"], consumo_kwh(18, 5, 8, DIAS))

    def test_simulacao_ignora_ambiente_que_ja_e_led(self):
        ambiente_id = banco.cadastrar_ambiente(self.conexao, "Sala só LED", 8)
        banco.adicionar_lampadas(self.conexao, ambiente_id, 1, 4)

        linhas = relatorio.simulacao_troca_led(self.conexao, DIAS)
        nomes = [l["ambiente"] for l in linhas]
        self.assertNotIn("Sala só LED", nomes)
        self.assertTrue(all(l["economia_kwh_mes"] > 0 for l in linhas))


if __name__ == "__main__":
    unittest.main()
