# Controle de Consumo de Iluminação

Sistema em **Python + SQL (SQLite)** que registra a iluminação dos ambientes de um prédio (escola, escritório) e calcula:

- quanto cada ambiente consome de energia por mês (kWh e R$);
- quanto seria economizado trocando as lâmpadas fluorescentes e incandescentes por **LED**;
- em quantos meses o investimento na troca se paga.


## Tecnologias

- **Python 3** (biblioteca padrão, sem dependências externas)
- **SQLite** como banco de dados
- **SQL**: `JOIN`, `LEFT JOIN`, `GROUP BY`, funções de agregação, `CTE (WITH)`, chaves estrangeiras e `CHECK`
- **unittest** para testes automatizados

## Como rodar

```bash
git clone https://github.com/Netonewdev/consumo-energia-led.git
cd consumo-energia-led
python main.py
```

Na primeira execução o banco `energia.db` é criado automaticamente com dados de exemplo.

Para rodar os testes:

```bash
python -m unittest -v
```

## Funcionalidades (menu)

1. Listar ambientes
2. Cadastrar ambiente
3. Adicionar lâmpadas a um ambiente
4. Relatório de consumo mensal
5. Simulação de troca para LED (economia e retorno do investimento)
6. Recriar o banco com os dados de exemplo

## Modelo de dados

```
ambientes                 instalacoes                  tipos_lampada
-----------               ---------------              ------------------
id (PK)        1 ----- N  id (PK)             N ---- 1 id (PK)
nome                      ambiente_id (FK)             nome
horas_por_dia             lampada_id (FK)              tecnologia
                          quantidade                   potencia_watts
                                                       preco
                                                       led_equivalente_id (FK -> tipos_lampada)
```

- Um **ambiente** tem várias **instalações** (tipos de lâmpada + quantidade).
- Cada lâmpada não-LED aponta para a **LED equivalente** que pode substituí-la (relacionamento da tabela com ela mesma).

## Estrutura do projeto

```
consumo-energia-led/
├── main.py            # menu no terminal
├── banco.py           # conexão e operações de cadastro/listagem
├── relatorio.py       # consultas de relatório e simulação
├── regras.py          # cálculos e validações (regras de negócio)
├── sql/
│   ├── schema.sql     # criação das tabelas
│   ├── dados.sql      # dados de exemplo
│   └── consultas.sql  # consultas de estudo comentadas
└── tests/
    └── test_sistema.py
```

## Exemplo de resultado

Com os dados de exemplo (22 dias úteis, tarifa de R$ 0,90/kWh):

```
Simulação: trocar as lâmpadas atuais por LED

Ambiente                     Trocas  Economia/mês  Investimento   Retorno
Corredor principal               10     R$ 141,37     R$ 120,00     0.8 m
Biblioteca                       14      R$ 67,48     R$ 298,00     4.4 m
Laboratório de Informática       12      R$ 62,73     R$ 300,00     4.8 m
Sala 101                          8      R$ 34,85     R$ 200,00     5.7 m
Sala 102                          6      R$ 26,14     R$ 150,00     5.7 m
Secretaria                        4      R$ 11,40      R$ 48,00     4.2 m
-------------------------------------------------------------------------
TOTAL                                   R$ 343,97   R$ 1.116,00     3.2 m

Economia estimada em 1 ano: R$ 4.127,59
```

Gasto atual com iluminação: **R$ 541,41/mês**. Com LED, a economia é de cerca de **63%**, e a troca se paga em pouco mais de **3 meses**.

## Boas práticas aplicadas

- **Consultas parametrizadas** (`?`) em vez de concatenar texto no SQL, evitando SQL Injection.
- **Validação** dos dados no Python e também no banco (`CHECK`, `NOT NULL`, `UNIQUE`, chaves estrangeiras).
- **Tratamento de erros** com mensagens claras para o usuário.
- **Testes automatizados** com banco em memória, incluindo um teste que confere se o cálculo feito em SQL bate com o cálculo feito em Python.

## Próximos passos

- Exportar os relatórios para CSV
- Gráfico de consumo por ambiente com `matplotlib`
- Interface web com Flask

## Autor

Francisco — estudante de TI em Manaus/AM
[GitHub](https://github.com/Netonewdev)
