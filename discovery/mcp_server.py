"""Optional MCP stdio adapter: pip install 'mcp[cli]'."""
from mcp.server.fastmcp import FastMCP
from skills_discovery import ROOT, read_index, search

app = FastMCP("skills-superset-discovery")


@app.tool()
def search_skills(query: str, top_k: int = 5) -> dict:
    """Return skill paths and metadata, without loading full SKILL.md bodies."""
    rows = read_index(ROOT / "skills-index.jsonl")
    if not rows:
        return {"error": "Run python discovery/skills_discovery.py index first"}
    return {"query": query, "results": search(query, rows, min(max(top_k, 1), 10))}


@app.tool()
def read_skill(path: str) -> str:
    """Read a selected indexed SKILL.md; never arbitrary paths."""
    if path not in {x["path"] for x in read_index(ROOT / "skills-index.jsonl")}:
        raise ValueError("Path is not in the skill index")
    source = ROOT / path
    source.resolve().relative_to((ROOT / "skills").resolve())
    if source.name != "SKILL.md" or source.is_symlink():
        raise ValueError("Not a regular indexed SKILL.md")
    return source.read_text(encoding="utf-8")


if __name__ == "__main__":
    app.run(transport="stdio")
