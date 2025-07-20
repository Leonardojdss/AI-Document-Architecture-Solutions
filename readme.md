# AZURE AI - Arquitetura de Solução de IA - Documentos - 01 de 3 

### Problema Identificado – Email único Leonardo Advocacia e Associados

Na estrutura atual da Leonardo Advocacia e Associados, existe apenas um único e-mail institucional que recebe todos os documentos essenciais da operação jurídica. Esse e-mail é o canal por onde chegam:
* Contratos enviados por clientes ou parceiros;
* Documentos e peças relacionadas a processos judiciais em andamento.

Contudo, duas áreas distintas da organização, setor de contratos e setor documentos processuais precisam acessar esse mesmo e-mail constantemente, o que gera os seguintes problemas:
1. Conflito de acesso: ao abrir o e-mail em um dispositivo, o outro é automaticamente desconectado, interrompendo o trabalho.
2. Retrabalho e lentidão: como não há segmentação automática dos documentos, os colaboradores precisam identificar manualmente o tipo e destino de cada arquivo.
3. Risco de perda ou atraso de informação: com muitos e-mails acumulados e nenhum sistema automatizado, documentos podem ser ignorados, classificados incorretamente ou processados fora do prazo.

A empresa não pode criar um segundo e-mail institucional, por restrições técnicas ou operacionais, tornando necessário trabalhar com esse único canal.

# Solução com Azure AI + LangGraph + MCP + PostgreSQL + Blob Storage

![alt text](image-1.png)

## Descrição da Solução

A solução proposta utiliza uma arquitetura integrada baseada em Azure AI, LangGraph, MCP (Model Context Protocol), PostgreSQL e Blob Storage para automatizar o processamento e a classificação de documentos jurídicos recebidos por e-mail.

**Fluxo da solução:**

1. **Recepção e Classificação**: Todos os documentos chegam por um único canal de e-mail institucional. O serviço Azure Document Intelligence faz a classificação automática dos arquivos em dois grupos principais: contratos e documentos processuais.
2. **Armazenamento Seguro**: Os documentos classificados são armazenados no Azure Blob Storage, garantindo segurança, escalabilidade e fácil acesso.
3. **Agentes Inteligentes (LangGraph)**: Dois agentes principais (Agente Gerente de Contratos e Agente Gerente de Processos) coordenam o fluxo de trabalho. Eles interagem com agentes especializados para análise e consulta de contratos e documentos processuais, utilizando LangGraph para orquestração e automação das tarefas.
4. **Banco de Dados MCP + PostgreSQL**: As análises realizadas pelos agentes são salvas em um banco de dados MCP, que utiliza PostgreSQL para garantir integridade, consulta eficiente e histórico das operações. O sistema permite consultar análises de contratos e documentos a qualquer momento.
5. **Interface de Usuário**: Usuários podem realizar perguntas e consultas diretamente aos agentes, obtendo respostas rápidas sobre contratos e documentos processuais, sem depender do acesso manual ao e-mail.

Essa arquitetura elimina conflitos de acesso, automatiza a segmentação dos documentos, reduz retrabalho e minimiza o risco de perda ou atraso de informações, tornando o fluxo jurídico mais eficiente e seguro.

# MS-DOCUMENT-INTELLIGENCE

Ligar 

```bash
cd ms_document_intelligence
export PYTHONPATH=/Users/leonardojdss/Desktop/projetos/AI-Document-Architecture-Solutions
uvicorn ms_document_intelligence.src.main:app --host 0.0.0.0 --port 8000
```

# MS-LANGGRAPH-INTELLIGENCE

Ligar 

```bash
cd ms_document_intelligence
export PYTHONPATH=/Users/leonardojdss/Desktop/projetos/AI-Document-Architecture-Solutions
uvicorn ms_langgraph_agents.main:app --host 0.0.0.0 --port 8001
```

# MS-MCP-DATABASE

deve criar essas tabelas 

CREATE TABLE documents (
    id SERIAL NOT NULL PRIMARY KEY,
    date DATE NOT NULL,
	document_name TEXT NOT NULL,
    resume_ai TEXT NOT NULL
);

CREATE TABLE contracts (
    id SERIAL NOT NULL PRIMARY KEY,
    date DATE NOT NULL,
	document_name TEXT NOT NULL,
    resume_ai TEXT NOT NULL
);

```bash
cd ms_document_intelligence
export PYTHONPATH=/Users/leonardojdss/Desktop/projetos/AI-Document-Architecture-Solutions
uvicorn ms_mcp_database.server:mcp_app --host 0.0.0.0 --port 8002
```