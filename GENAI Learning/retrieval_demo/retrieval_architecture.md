                    User
                     │
                     ▼
          "OAuth2 authentication"
                     │
                     ▼
            Retrieval Service
                     │
     ┌───────────────┴───────────────┐
     ▼                               ▼
Dense Query Embedder          Sparse Query Embedder
     │                               │
     └───────────────┬───────────────┘
                     ▼
              Search Repository
                     │
                     ▼
               Qdrant Client
                     │
                     ▼
                  Qdrant
                     │
             Raw Search Results
                     │
                     ▼
            Search Repository
         (Maps to Domain Models)
                     │
                     ▼
            Retrieval Service
        (Fusion / Filtering / RRF)
                     │
                     ▼
        List[RetrievedChunk]