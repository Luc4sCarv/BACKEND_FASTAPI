import sqlite3

# Conecta ao arquivo (ou cria se não existir)
conexao = sqlite3.connect('Banco_dados.db')
cursor = conexao.cursor()

# Executa a criação da tabela
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER
)
''')

# Salva as alterações e fecha a conexão
conexao.commit()
conexao.close()

print("Tabela criada com sucesso direto no arquivo!")