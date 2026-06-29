from collections import defaultdict

from retrieval.models.retrieved_chunk import RetrievedChunk


class RRFService:
    """
    Implements Reciprocal Rank Fusion (RRF).

    References:
        Cormack et al. (2009)
        Reciprocal Rank Fusion outperforms Condorcet and
        individual Rank Learning Methods.
    """

    def __init__(
        self,
        k: int = 60,
    ) -> None:
        self._k = k

    def fuse(
        self,
        dense_results: list[RetrievedChunk],
        sparse_results: list[RetrievedChunk],
        top_k: int,
    ) -> list[RetrievedChunk]:
        """
        Fuse dense and sparse retrieval results using RRF.

        Args:
            dense_results:
                Results returned from dense retrieval.

            sparse_results:
                Results returned from sparse retrieval.

            top_k:
                Number of final documents to return.

        Returns:
            Ranked hybrid retrieval results.
        """

        fused_scores: dict[str, float] = defaultdict(float)

        retrieved_chunks: dict[str, RetrievedChunk] = {}

        #
        # Dense ranking
        #
        for rank, chunk in enumerate(dense_results, start=1):
            fused_scores[chunk.id] += 1 / (self._k + rank)
            retrieved_chunks[chunk.id] = chunk

        #
        # Sparse ranking
        #
        for rank, chunk in enumerate(sparse_results, start=1):
            fused_scores[chunk.id] += 1 / (self._k + rank)
            retrieved_chunks[chunk.id] = chunk

        ranked_chunk_ids = sorted(
            fused_scores,
            key=fused_scores.get,
            reverse=True,
        )

        return [
            retrieved_chunks[chunk_id].model_copy(
                update={"rrf_score": fused_scores[chunk_id]}
            )
            for chunk_id in ranked_chunk_ids[:top_k]
        ]