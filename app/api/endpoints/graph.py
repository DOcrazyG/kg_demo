from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile

from app.core.builder import GraphBuilder
from app.core.extractor import extract_medical_knowledge_graph

router = APIRouter()


@router.post("/build_graph")
async def build_graph(file: UploadFile = File(...)):
    """
    Upload a text file (CSV or TXT) and build knowledge graph from each line.

    Each line of the file will be processed to extract medical entities and relations,
    then stored in Neo4j graph database.

    Args:
        file: Uploaded file (supported formats: .txt, .csv)
    """
    from app.main import app

    # Validate file type
    allowed_extensions = [".txt", ".csv"]
    filename = file.filename.lower()
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}",
        )

    # Read file content
    try:
        content = await file.read()
        lines = content.decode("utf-8").splitlines()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")

    if not lines:
        raise HTTPException(status_code=400, detail="File is empty")

    # Process each line
    total_lines = len(lines)
    processed_lines = 0
    created_nodes = 0
    created_relations = 0
    failed_lines = []

    for idx, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue

        try:
            # Extract knowledge graph from text
            result = extract_medical_knowledge_graph(line)
            graph = result.graph

            # Build graph in Neo4j
            builder = GraphBuilder(graph, app.state.neo4j_client)
            await builder.build()

            created_nodes += len(graph.nodes)
            created_relations += len(graph.edges)
            processed_lines += 1

        except Exception as e:
            failed_lines.append({"line": idx, "text": line[:100], "error": str(e)})

    return {
        "status": "completed",
        "total_lines": total_lines,
        "processed_lines": processed_lines,
        "created_nodes": created_nodes,
        "created_relations": created_relations,
        "failed_lines": failed_lines,
    }

