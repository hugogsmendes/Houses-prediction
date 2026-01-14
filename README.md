# Houses-prediction

API em **FastAPI** + **SQLAlchemy/Alembic** e um pipeline de **Machine Learning (Regressão)** para **inferir o preço de uma casa**.

O objetivo do projeto é treinar um modelo de regressão para prever o preço a partir de features do dataset e, em seguida, disponibilizar a inferência via API. A meta de qualidade do modelo é atingir **coeficiente de determinação ($R^2$) de pelo menos 70%** no conjunto de validação/teste.

## Objetivo

- Treinar um modelo de regressão para prever preço de casas.
- Atingir **$R^2 \ge 0.70$**.
- Expor o modelo por uma API (consumo externo), idealmente com autenticação.

## Stack

- **API**: FastAPI + Uvicorn
- **Auth**: OAuth2 Password Flow (Bearer JWT)
- **Banco**: SQLite (`houses.db`) + SQLAlchemy + Alembic
- **ML**: pandas / numpy / scikit-learn / scipy / joblib

## Estrutura do projeto

- [main.py](main.py): inicialização do FastAPI e inclusão das rotas
- [api/routes/user_routes.py](api/routes/user_routes.py): rotas de usuário (register/login/list/delete)
- [database/session.py](database/session.py): engine e sessão do SQLAlchemy (SQLite)
- [models/users.py](models/users.py): modelo `User`
- [alembic/](alembic/): migrações do banco
- [models_ml/](models_ml/): notebook e dataset do modelo
	- [models_ml/model.ipynb](models_ml/model.ipynb)
	- [models_ml/Housing.csv](models_ml/Housing.csv)

## Como rodar a API

### 1) Criar ambiente e instalar dependências

Usando `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com:

```env
SECRET_KEY=troque_esta_chave_por_uma_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 3) Criar/atualizar banco de dados

O projeto usa SQLite em `sqlite:///houses.db` (ver [database/session.py](database/session.py) e [alembic.ini](alembic.ini)).

Para aplicar as migrações:

```bash
alembic upgrade head
```

### 4) Subir a aplicação

```bash
uvicorn main:app --reload
```

Acesse:

- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Machine Learning (modelo de regressão)

O treinamento/experimentos estão em [models_ml/model.ipynb](models_ml/model.ipynb), usando o dataset [models_ml/Housing.csv](models_ml/Housing.csv).

### Executar o Jupyter com Anaconda/Conda

Este repositório já inclui um ambiente Conda em [models_ml/environment.yml](models_ml/environment.yml). A forma mais simples de rodar o notebook é criar o ambiente e iniciar o Jupyter a partir dele.

1) Instale Anaconda ou Miniconda

- Anaconda (recomendado se você quer tudo pronto) ou Miniconda (mais leve).

2) Criar o ambiente Conda (a partir do `environment.yml`)

```bash
conda env create -f models_ml/environment.yml
```

Se o ambiente já existir e você quiser atualizar pacotes:

```bash
conda env update -f models_ml/environment.yml --prune
```

3) Ativar o ambiente

```bash
conda activate houses-ml
```

4) Subir o Jupyter

Você pode usar Lab ou Notebook:

```bash
jupyter lab
```

ou

```bash
jupyter notebook
```

5) Abrir o notebook do projeto

- Abra [models_ml/model.ipynb](models_ml/model.ipynb) no navegador (ou no VS Code) e selecione o kernel/ambiente `houses-ml`.

Critério de sucesso:

- Alcançar **$R^2 \ge 0.70$** em validação/teste.

Sugestão de fluxo (alto nível):

1. Carregar e explorar o dataset.
2. Separar treino/teste e aplicar pré-processamento (tratamento de nulos, encoding, scaling se necessário).
3. Treinar modelos candidatos (ex.: `LinearRegression`, `RandomForestRegressor`, `GradientBoostingRegressor`).
4. Avaliar com $R^2$ e ajustar hiperparâmetros.
5. Persistir o pipeline/modelo (ex.: `joblib.dump(...)`) para consumo pela API.

## Roadmap (próximos passos)

- Criar um endpoint de inferência (ex.: `POST /api/v1/predict`) que carregue o pipeline treinado e retorne o preço previsto.
- Versionar e armazenar artefatos do modelo (ex.: pasta `models_ml/artifacts/`).
- Adicionar validação de payload (Pydantic) para features do modelo.
- Automatizar treino/avaliação (script) e registrar métricas.