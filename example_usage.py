import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from client import SemanticChunkHierarchyReRankerClient

def main():
    client = SemanticChunkHierarchyReRankerClient()
    res = client.rerank_hierarchical_chunks()
    print("=== Semantic Chunk Hierarchy Re-Ranker Output ===")
    print(f"Query: '{res['query']}'")
    print(f"Selected: {res['chunks_selected_count']}/{res['candidate_chunks_evaluated']} chunks ({res['total_context_tokens_used']} tokens, {res['token_budget_utilization']})")
    print("\nSelected Hierarchical Chunks:")
    for sc in res['selected_hierarchical_context']:
        print(f"  * [{sc['chunk_id']} from {sc['parent_doc']}] Score: {sc['hybrid_relevance_score']} | {sc['text']}")

if __name__ == '__main__':
    main()
