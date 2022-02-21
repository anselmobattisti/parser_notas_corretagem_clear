# Notas de Corretagem Clear

O objetivo desse script é ler as notas em pdf de uma determinada pasta e gerar um pandas dataframe contendo os dados de todas as transações bem como alguns ajustes importantes, como por exemplo o desconto das taxas de corretagem.

Por padrão o sistema procura as notas de corretagem que estão na pasta notas.

# Instalação

Sugiro utilizar um ambiente virtual 

```shell
# criar o ambiente virtual
python3 -m venv venv

# acessar o ambiente virtual
source venv/bin/activate

# install the packets
pip install -r requirements.txt
```

# Executar 

```shell
# criar o ambiente virtual
python3 -m venv venv

# acessar o ambiente virtual
source venv/bin/activate

python3 main.py
```

# Executar os testes

```shell
# criar o ambiente virtual
python3 -m venv venv

# acessar o ambiente virtual
source venv/bin/activate

python3 -m unittest tests/test_Nota.py 
```

# Todo

* [ ] - Exportar as transações e as notas em Excel
