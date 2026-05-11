from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI()

class LoginRequest(BaseModel):
    email: str
    password: str

class Jogo(BaseModel):
    nome: str
    tipo: str
    nota: int
    review: str

jogos = [
    {"id": 1, "nome": "The Legend of Zelda", "tipo": "Aventura", "nota": 10, "review": "Um clássico absoluto."},
    {"id": 2, "nome": "FIFA 23", "tipo": "Esporte", "nota": 7, "review": "Bom para jogar com amigos."}
]
next_id = 3

@app.post("/login")
def login(request: LoginRequest):
    if request.email == "usuario@esoft.com" and request.password == "Abc123":
        return {"token": str(uuid.uuid4())}
    raise HTTPException(status_code=401, detail="Inválido")

@app.get("/jogos")
def get_jogos():
    return jogos

@app.get("/jogos/{id}")
def get_jogo(id: int):
    jogo = next((j for j in jogos if j["id"] == id), None)
    if not jogo:
        raise HTTPException(status_code=404, detail="Não encontrado")
    return jogo

@app.post("/jogos", status_code=201)
def criar_jogo(jogo: Jogo):
    global next_id
    novo = {"id": next_id, **jogo.dict()}
    jogos.append(novo)
    next_id += 1
    return novo

@app.put("/jogos/{id}")
def atualizar_jogo(id: int, jogo: Jogo):
    item = next((j for j in jogos if j["id"] == id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Não encontrado")
    item.update(jogo.dict())
    return item

@app.delete("/jogos/{id}", status_code=204)
def deletar_jogo(id: int):
    global jogos
    if not any(j["id"] == id for j in jogos):
        raise HTTPException(status_code=404, detail="Não encontrado")
    jogos[:] = [j for j in jogos if j["id"] != id]
