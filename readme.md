# AZURE AI - Arquitetura de Solução de IA - Documentos - 01 de 3 

### Problema Identificado – Email único Leonardo Advocacia e Associados

Na estrutura atual da Leonardo Advocacia e Associados, existe apenas um e-mail institucional que recebe todos os documentos essenciais da operação jurídica, incluindo:
- Contratos enviados por clientes ou parceiros;
- Documentos e peças relacionadas a processos judiciais.

Duas áreas distintas (setor de contratos e setor de documentos processuais) precisam acessar esse e-mail simultaneamente, gerando:
1. Conflito de acesso: ao abrir o e-mail em um dispositivo, o outro é desconectado.
2. Retrabalho e lentidão: falta de segmentação automática dos documentos.
3. Risco de perda ou atraso de informação: documentos podem ser ignorados ou processados fora do prazo.

A empresa não pode criar um segundo e-mail institucional, tornando necessário trabalhar com esse único canal.

---

## Solução com Azure AI + LangGraph + MCP + PostgreSQL + Blob Storage

![Arquitetura](image-1.png)

### Descrição da Solução

A arquitetura proposta integra Azure AI, LangGraph, MCP (Model Context Protocol), PostgreSQL e Blob Storage para automatizar o processamento e classificação dos documentos jurídicos recebidos por e-mail.

**Fluxo da solução:**
1. **Recepção e Classificação:** O Azure Document Intelligence classifica automaticamente os arquivos em contratos e documentos processuais.
2. **Armazenamento Seguro:** Documentos classificados são armazenados no Azure Blob Storage.
3. **Agentes Inteligentes (LangGraph):** Dois agentes principais (Contratos e Processos) coordenam o fluxo de trabalho, utilizando LangGraph para automação.
4. **Banco de Dados MCP + PostgreSQL:** As análises dos agentes são salvas em um banco MCP com PostgreSQL, permitindo consultas eficientes e histórico das operações.
5. **Interface para aplicações de usuário:** Usuários podem consultar informações diretamente aos agentes, sem depender do acesso manual ao e-mail.

Essa arquitetura elimina conflitos de acesso, automatiza a segmentação, reduz retrabalho e minimiza riscos de perda ou atraso de informações.

### Observação Importante sobre Automação de E-mails

A automação para recuperar os arquivos de contratos e documentos processuais diretamente do e-mail deve ser implementada utilizando o **Power Automate**. No entanto, essa funcionalidade não foi desenvolvida neste projeto, pois não era o foco principal da solução apresentada.
---

## Configuração Inicial dos Serviços Azure e PostgreSQL

Antes de clonar o repositório, siga estes passos para preparar os serviços essenciais:

### 1. Criação da Conta de Armazenamento Azure e Containers via Portal

1. Acesse o [Portal Azure](https://portal.azure.com).
2. No menu lateral, clique em **Armazenamento** e selecione **Contas de armazenamento**.
3. Clique em **Criar** e preencha os campos obrigatórios (nome da conta, grupo de recursos, localização, tipo de redundância).
4. Após criar a conta, acesse-a e vá em **Containers** no menu lateral.
5. Clique em **+ Container** para criar um container chamado `contratos`.
6. Repita o processo para criar o container `documentos-processuais`.

Esses containers serão usados para armazenar os arquivos classificados.
### 2. Treinamento do Modelo de Classificação com Documentos Fictícios

Utilize os documentos fictícios presentes na pasta `arquivos_treinamento_ficticios` para treinar o modelo de classificação:

1. Os arquivos fictícios estão em duas subpastas: `contratos` e `documentos-processuais`.
2. Faça upload desses exemplos para um container de treinamento no Azure Blob Storage.
3. No Portal Azure, acesse o serviço **Azure Document Intelligence**.
4. Abra o **Document Intelligence Studio**.
5. Crie um novo projeto de treinamento e selecione o container de treinamento.
6. Defina dois tipos de documento: `contratos` e `documentos-processuais`.
7. Associe os exemplos de cada subpasta ao respectivo tipo.
8. Inicie o treinamento do modelo diretamente pelo Studio.
9. Após o treinamento, publique o modelo para uso na classificação automática.

Consulte a [documentação oficial do Azure Document Intelligence](https://learn.microsoft.com/azure/ai-services/document-intelligence/) para detalhes sobre o treinamento personalizado.


## Subindo os Serviços com Docker Compose

Todos os serviços podem ser inicializados facilmente via Docker Compose. Certifique-se de ter o Docker instalado.

1. **Clone o repositório:**

```bash
git clone https://github.com/Leonardojdss/AI-Document-Architecture-Solutions.git
cd AI-Document-Architecture-Solutions
```

2. **Crie o arquivo `.env` a partir do modelo `.env.example` e popule com suas credenciais dependentes:**

```bash
cp .env.example .env
```

2. **Utilize o arquivo `docker-compose.yml` já criado na raiz do projeto:**

2.1 **Inicialize os containers:**

```bash
docker compose up --build
```

## Banco de Dados MCP

Crie as tabelas no PostgreSQL:

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    document_name TEXT NOT NULL,
    resume_ai TEXT NOT NULL
);

CREATE TABLE contracts (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    document_name TEXT NOT NULL,
    resume_ai TEXT NOT NULL
);
```

A partir daqui, você pode começar a receber os documentos de contratos e processuais que foram enviados para o email.

---

## Testando as Ferramentas MCP

```bash
npx @modelcontextprotocol/inspector
```
---

## Testando a rota de recepção de documentos

Para testar a API de automação de documentos, utilize o comando abaixo:

*Esta é a rota de entrada para receber documentos e classificá-los automaticamente. Ela aceita arquivos nos formatos `.docx` e `.pdf`.*

```bash
curl -X POST \
    'http://localhost:8000/ms_document_intelligence/automation_documents' \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -F 'file=@<seu_documento>'
```

## Testando a rota de interação com os agentes

Essas rotas permitem consultar os agentes inteligentes responsáveis por contratos e documentos processuais. O objetivo é facilitar o acesso às análises e informações dos documentos processados, sem depender do acesso direto ao e-mail institucional.

### Contratos

Use esta rota para solicitar análises dos arquivos classificados como contratos e identificar os arquivos que chegaram em uma data específica:

```bash
curl -X 'POST' \
    'http://0.0.0.0:8001/ms_langgraph_agents/contracts' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "text": "listar as analises dos arquivos que chegaram dia 21 de julho de 2025"
}'
```

### Documentos Processuais

Use esta rota para consultar os arquivos classificados como documentos processuais e identificar os arquivos que chegaram em uma data específica:

```bash
curl -X 'POST' \
    'http://0.0.0.0:8001/ms_langgraph_agents/documents' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "text": "listar os arquivos que chegaram dia 20 de julho de 2025"
}'
```

## Observações

- Ajuste variáveis de ambiente conforme necessário.
- Consulte a documentação de cada serviço para configurações adicionais.
