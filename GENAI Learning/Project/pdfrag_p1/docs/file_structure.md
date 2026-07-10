pdf-rag/

├── app/
│
├── api/
│   ├── routers/
│   └── dependencies/
│
├── core/
│   ├── config.py
│   ├── logging.py
│   ├── exceptions.py
│   └── constants.py
│
├── ingestion/
│   ├── loaders/
│   ├── chunkers/
│   ├── embedding/
│   └── pipeline.py
│
├── vectorstore/
│   ├── base.py
│   ├── pinecone_client.py
│   └── repository.py
│
├── retrieval/
│   ├── retriever.py
│   ├── context_builder.py
│   └── models.py
│
├── prompt/
│   ├── builder.py
│   └── templates/
│
├── llm/
│   ├── base.py
│   ├── grok_client.py
│   └── response_models.py
│
├── services/
│   ├── ingestion_service.py
│   └── qa_service.py
│
├── schemas/
│
├── models/
│
├── tests/
│
├── pyproject.toml
│
└── README.md