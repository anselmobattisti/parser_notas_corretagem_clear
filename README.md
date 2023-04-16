# Parser Notas Corretagem Clear

O objetivo desse projeto é criar um parser para os PDFs das notas da Clear.

## Notas em PDF

Antes de executar o script será necessario ter o PDF das notas. Crie uma pasta por mês e salve os PDFs gerados no site 
da Clear. Minha sugestão é que você crie uma pasta chamada "minhas_notas" e dentro dela crie uma pasta por mes, exemplo:

```
01-2021
02-2021
03-2021
.
.
.
12-2021
```

## Arquivos de Configuração

Os arquivos de configuração ficam na pasta "data". 

* **nome_ativos.csv**: Este arquivo contém a relação entre o nome que consta na coluna "Especificação do título" da nota 
com o "ticker" na B3. Por exemplo, no PDF da nota uma transação do ativo ENBR3 aparecerá com o nome "ENERGIAS BR ON NM",
sendo assim, os dados desse arquivo são usados para converter o nome na nota para o código da B3.



## Instalação

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

- [x] Exportar as transações e as notas em Excel
- [x] Exportar as notas em CSV
- [ ] Subscrição de FIIS
- [ ] Bonificação de ações (ITAUSA, Bradesco)