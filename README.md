Aqui está uma versão do README simplificada e sem distrações visuais:

Como Rodar o Projeto
Este projeto utiliza o FastAPI e o gerenciador uv.

1. Instalação
Bash
# Clone o repositório
git clone https://github.com/Luc4sCarv/Prototipo.git
cd Prototipo

# Sincronize o ambiente
uv sync
2. Banco de Dados (MySQL)
Execute o arquivo Create_table.sql no seu MySQL Workbench para criar o banco db_escola.

Ajuste de Senha: No arquivo main.py, altere a variável password para a senha do seu banco local:

Python
password = "SUA_SENHA_AQUI"
3. Execução
Bash
uv run uvicorn main:app --reload
A API rodará em: http://127.0.0.1:8000

4. Endpoints Principais (Postman)
GET /alunos/: Lista todos os alunos.

POST /cadastrar-endereco/: Envie o JSON {"cep": "00000000"} para buscar via ViaCEP e salvar no banco automaticamente.
