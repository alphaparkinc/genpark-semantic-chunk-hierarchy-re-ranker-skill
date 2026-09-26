import json, sys
from client import SemanticChunkHierarchyReRankerClient

def handle_mcp_request(payload):
    method = payload.get("method")
    req_id = payload.get("id", 1)
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "semantic-chunk-hierarchy-re-ranker", "version": "1.0.0"}}}
    elif method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [{"name": "rerank_hierarchical_chunks", "description": "Re-ranks candidate document chunks using hybrid semantic scoring and packs optimal token context."}]}}
    elif method == "tools/call":
        client = SemanticChunkHierarchyReRankerClient()
        res = client.rerank_hierarchical_chunks()
        return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
    return {"jsonrpc": "2.0", "id": req_id, "result": {"status": "ACTIVE"}}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(handle_mcp_request({"method": "tools/list"})))
    else:
        client = SemanticChunkHierarchyReRankerClient()
        print(json.dumps(client.rerank_hierarchical_chunks(), indent=2))
