from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import pandas as pd
from fastapi import FastAPI
import requests
# configuracao do conexao com banco de dados
host = "127.0.0.1"
port = 3306
user = "root"
password = "030407"
banco_dados = "db_escola"
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{banco_dados}")
# instaciar
app = FastAPI()

# schema
class Aluno(BaseModel):
    matricula: str
    nome_aluno: str
    email: Optional[str]
    endereco_id: Optional[int] = None

class MsgPost(BaseModel):
    mensagem: str


@app.get("/alunos/", response_model=List[Aluno])
def listar_alunos():
    query = "select * from tb_alunos"
    df_alunos = pd.read_sql(query, con=engine)
    return df_alunos.to_dict(orient="records")

@app.post("/cadastrar-aluno/", response_model=MsgPost)
def cadastrar_alunos(aluno:dict):
    df = pd.DataFrame([aluno])
    df.to_sql("tb_alunos", engine, if_exists="append", index=False)
    return {"mensagem": "Alunos Cadastrado com sucesso."}

@app.put("/atualizar-alunos/{id}")
def atualizar_alunos(id:int, alunos:dict):
    with engine.begin() as conn:
        conn.execute(
            text(
            """
                update tb_alunos
                set matricula = :matricula,
                nome_aluno = :nome_aluno,
                email = :email,
                endereco_id = :endereco_id
                where id = :id
            """
        ), {"id":id, **alunos}
    )
    return {"mensagem": "Alunos Atualizado com sucesso."}

@app.delete("/deletar-alunos/{id}")
def deletar_alunos(id:int):
    with engine.begin() as conn:
        conn.execute(
            text(
            """
                delete from tb_alunos
                where id = :id
            """
        ), {"id":id}
    )
    return {"mensagem": "Aluno Deletado com sucesso."}



# Corrigindo nome da classe para Endereco
class Endereco(BaseModel):
    cep: str
    endereco: str
    bairro: str
    estado: str



@app.post("/cadastrar-endereco/", response_model=MsgPost)
def cadastrar_endereco(dados_cep: dict):
    cep_input = dados_cep.get("cep")
    
    
    response = requests.get(f"https://viacep.com.br/ws/{cep_input}/json/")
    info_cep = response.json()
    
    if "erro" in info_cep:
        return {"mensagem": "CEP não encontrado."}


    novo_reg = {
        "cep": info_cep.get("cep"),
        "endereco": info_cep.get("logradouro"), 
        "bairro": info_cep.get("bairro"),
        "cidade": info_cep.get("localidade"),
        "estado": info_cep.get("uf"),
        "regiao": info_cep.get("regiao" )
    }
    df = pd.DataFrame([novo_reg])
    df.to_sql("tb_enderecos", engine, if_exists="append", index=False)
    return {"mensagem": "Endereço cadastrado com sucesso!"}

@app.get("/endereco/", response_model=List[Endereco])
def listar_endereco():
    query = "select * from tb_enderecos"
    df_endereco = pd.read_sql(query, con=engine)
    return df_endereco.to_dict(orient="records")

@app.put("/atualizar-endereco/{id}")
def atualizar_endereco(id:int, endereco:dict):
    with engine.begin() as conn:
        conn.execute(
            text(
            """
                update tb_enderecos
                set cep = :cep,
                endereco = :endereco,
                bairro = :bairro
                where id = :id
            """
        ), {"id":id, **endereco}
    )
    return {"mensagem": "endereco Atualizado com sucesso."}

@app.delete("/deletar-endereco/{id}")
def endereco(id:int):
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                delete from tb_enderecos
                where id = :id
                """
            ), {"id":id}
        )
    return {"mensagem": "endereco Deletado com sucesso."}



