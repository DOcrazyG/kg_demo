"""FastAPI service for Knowledge Graph Demo"""

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.config import get_provider_config
from app.db import Neo4jClient
from app.graph import BaseGraph

config = get_provider_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    app.state.neo4j_client = Neo4jClient(config.neo4j)
    try:
        await app.state.neo4j_client.async_verify_connectivity()
        print("✅ Neo4j connection verified")
    except Exception as e:
        print(f"⚠️ Neo4j connection failed: {e}")
    yield
    await app.state.neo4j_client.async_close()
    print("✅ Application shutdown complete")


app = FastAPI(
    title="Knowledge Graph Demo API",
    description="Medical knowledge graph API with Neo4j integration",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "Knowledge Graph Demo"}


@app.get("/health")
async def health_check():
    """Check service health and database connectivity."""
    try:
        await app.state.neo4j_client.async_verify_connectivity()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=503, detail=f"Database connection failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
