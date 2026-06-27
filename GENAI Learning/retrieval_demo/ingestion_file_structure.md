hybrid-search/
│
├── app/
│
├── core/
│   ├── config.py
│   ├── logger.py
│   └── container.py
│
├── ingestion/
│   ├── loaders/
│   ├── chunkers/
│   ├── embedders/
│   │   ├── dense_embedder.py
│   │   ├── sparse_embedder.py
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── ingestion_service.py
│   │   └── __init__.py
│   │
│   └── __init__.py
│
├── repositories/
|    │
|    ├── interfaces/
|    │   ├── collection_repository.py
|    │   ├── point_repository.py
|    |   |
|    │   └── search_repository.py
|    │
|    ├── qdrant/
|    │   ├── qdrant_repository.py
|    │   ├── collection_repository.py
|    │   ├── point_repository.py
|    │   └── __init__.py
|    │
|    └── __init__.py
│
├── schemas/
│   ├── chunk.py
│   ├── point.py
│   ├── vectors.py
│   └── __init__.py
│
├── scripts/
│   └── ingest.py
│
├── tests/
│
├── .env
├── requirements.txt
└── README.md