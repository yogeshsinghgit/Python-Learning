chunking-project/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── logger.py
│   │
│   ├── schemas/
│   │   ├── document.py
│   │   └── chunk.py
│   │
│   ├── services/
│   │   ├── document_loader.py
│   │   ├── chunking_service.py
│   │   ├── embedding_service.py
│   │   └── ingestion_service.py
│   │
│   ├── repositories/
│   │   └── qdrant_repository.py
│   │
│   └── main.py
│
├── docs/
│   ├── fastapi_intro.md
│   └── authentication.md
│
├── tests/
│
├── requirements.txt
│
└── .env