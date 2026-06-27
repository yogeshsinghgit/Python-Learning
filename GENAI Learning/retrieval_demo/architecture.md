                  scripts/
                      │
                      ▼
            Ingestion Service
          /         |          \
         ▼          ▼           ▼
   Chunker   Dense Embedder   Sparse Embedder
          \         |          /
           \        |         /
                 ▼
         Qdrant Repository
                 │
                 ▼
             Qdrant