                PDF
                 │
                 ▼
        Document Loader
                 │
                 ▼
          Text Splitter
                 │
                 ▼
        Embedding Generator
                 │
                 ▼
         Pinecone Repository
                 │
       ┌─────────┴──────────┐
       │                    │
Document Ingestion     Query Pipeline
       │                    │
       ▼                    ▼
                  Retriever Service
                          │
                          ▼
                   Prompt Builder
                          │
                          ▼
                     Grok Client
                          │
                          ▼
                      Final Answer