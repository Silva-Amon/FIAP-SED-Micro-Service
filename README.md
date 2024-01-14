# Create User Micro Service

## Introdução

Esse micro serviço tem como objetivo simular a criação de um usuário.

Fizemos integração com um banco de dados sqllite, e estamos usando container docker para a execução da aplicação.

## Requisitos de sistema

* [Python 3.10](https://www.python.org/)

## Execução da aplicação utilizando Docker

Para executar a aplicação utilizando o docker, realize o build do dockerfile:

```shell
docker build -t fiap/micro-service . 
```

Após o build, execute o seguinte comando para subir o container:

```shell
docker run -d -p 8000:8000 fiap/micro-service
```

E acessar a URL: http://127.0.0.1:8000/docs ou http://127.0.0.1:8000/redoc

## Execução da aplicação localmente

### Instalando dependências
> Recomenda-se que você tenha um ambiente python virtual, para não instalar de forma global as dependências no sistema. <br />
> [Saiba mais sobre a instalação do virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) <br />
> [Saiba mais sobre como inicializar e utilizar o virtualenv](https://virtualenv.pypa.io/en/latest/user_guide.html)
```shell
pip install -r requirements.txt
```

### Rodando a aplicação

Basta executar o seguinte comando:

```shell
uvicorn app.main:app --reload
```

## Documentação

As documentações da API podem ser acessadas em:
* [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Ambas possuem exemplos de parametros e payloads. Também é possível executar os endpoints diretamente delas.

## Testes

Para executar os testes, basta executar o seguinte comando (após já ter instalado as dependências):

```shell
pytest
```
