# Resumo:
O aplicativo conta com 3 containers na docker, para garantir diferentes funções ao fazer o webscrapping do site https://quotes.toscrape.com
### Database
Foi utilizado Postgres para guardar os dados raspados do site, com as seguintes tabelas:
* quotes: armazena ID, frase e o autor.
* tags: armazena ID e as tags únicas.
* quotes_tags: armazena ID, ID da frase e ID da tag

Isso garante a multiplicidade muitos para muitos e que as tags serão guardadas somente uma vez no banco, facilitando possíveis consultas futuras.

### UpdateDB.py
É o arquivo responsável por atualizar o banco com os dados do site, tem um serviço de cron na docker para executar esse arquivo em periodicidade definido pelo arquivo scheduler.cron

### Server
A interface do aplicativo é feito através do Flask, as rotas podem ser vistas na controller.py e na interface temos os seguintes botões:

**Atualizar Banco de Dados**: roda o UpdateDB para buscar dados no site e gravar usando a engine do SQL Alchemy

**Download** (CSV/JSON): Busca no banco um Dataframe Pandas e salva no caminho definido pelo OUTPUT_DIR, envia para o usuário o arquivo correspondente com as frases, autores e tags

**Crawl & Download** (CSV/JSON): Essa opção não acessa o banco, executa a raspagem de dados e em tempo de execução salva num dataframe, cria o arquivo e envia para o usuário. Sem alterar em nada o db

Também é possível coletar os dados por API acessando a rota /api/quotes

# Passo a passo para executar o projeto

### Execução local:
1. Rode no diretório que quer ter o projeto pelo CMD o comando "git clone https://github.com/RafaelJMartini/desafio-crawler"
2. Crie o ambiente virtual usando python -m venv ./venv
3. Com o ambiente virtual ativo, rode o comando "pip install -r requirements.txt"
4. No Postgres, crie um banco com o nome "quotes"
5. Crie na raiz do projeto um arquivo seguindo os parâmetros do .env.example passando os dados para conexão do banco criado (Usuário do Postgres, Senha, Host, Porta e nome do Db)
6. Execute no terminal python run.py
7. Acesse usando IP do computador:8080 ou na mesma máquina que está rodando o código acesse http://127.0.0.1:8080
### Execução na Docker:
1. Instale a docker.
2. Rode no diretório que quer ter o projeto pelo CMD o comando "git clone https://github.com/RafaelJMartini/desafio-crawler"
2. Abra o CMD e rode na raiz do projeto o código "docker compose up --build"
3. Acesse com o URL fornecido pelo Docker Desktop ou usando o parametro passado no .env POSTGRES_HOST:8080


# beeMôn:

Na beeMôn criamos muitos sistemas de raspagem de dados e buscamos todos os dias inovação na analise dos dados. Este desafio esta aberto para todos que quiserem abrir um fork e submeter suas ideias de tecnologia.

## Desafio:
Escolher uma dos sites abaixo para fazer o desafio

- [quotes.toscrape](https://quotes.toscrape.com/)
- [imdb.com](https://www.imdb.com/chart/top/?ref_=nv_mv_250)

### Minimo Entregável:

- Buscar dados de forma automatizada(script de linha de comando ou interface clicavel)
- Padronizar os retornos de forma estruturada (json/csv)
- Sistema de logs de para acompanhamento da execução
- Ter um prova da consulta (Screenshot)

### Pontos Extra para:

- Armazenamento dos resultados em um banco relacional ou não relacional
- Fazer um dataframe que possibilite visualizar os resultados via pandas
- Trazer resultados de forma dinamica sem fixar caminhos no `xpath`
- Dockerizar a aplicação
- Conseguir agendar uma execução para um dia e horario.

### Libs sugeridas:

 - Selenium 
 - Scrapy
 - Pandas
 - Requests
 - BeautifulSoup 


### O que iremos avaliar:

- Conhecimento em HTML
- Conhecimento em fluxo de request/response
- Conhecimento em extração de dados
- Conhecimento em base64
- Boas práticas de programação
- Utilização de bibliotecas de terceiros
- Documentação
- Criatividade
- Cobertura de testes
- Tempo de execução do código
- Versionamento do código



