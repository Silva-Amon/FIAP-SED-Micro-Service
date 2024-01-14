# Create User Micro Service

## Introdução
Esse micro serviço tem como objetivo simular a criação de um usuário.

Fizemos integração com um banco de dados mySQL, e estamos usando container docker para a execução da aplicação.

## Requisitos de sistema
* [Python 3.9](https://www.python.org/)

## Instalando dependências
> Recomenda-se que você tenha um ambiênte python virtual, para não instalar de forma global as dependências no sistema. <br />
> [Saiba mais sobre a instalação do virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) <br />
> [Saiba mais sobre como inicializar e utilizar o virtualenv](https://virtualenv.pypa.io/en/latest/user_guide.html)
```shell
pip install -r requirements.txt
```

## Rodando a aplicação
Basta executar o seguinte comando:
```shell
uvicorn main:app --reload
```
or
```shell
docker-compose up --build -d
```

## Documentação
As documentações da API podem ser acessadas em:
* [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Ambas possuem exemplos de parametros e payloads. Também é possível executar os endpoints diretamente delas.
