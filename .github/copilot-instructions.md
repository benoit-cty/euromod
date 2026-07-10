# Repository instructions

The local legislation MCP server is implemented with the stable Python MCP SDK
v1.x and FastMCP. When changing `mcp-server/`, follow:

- Python SDK: https://github.com/modelcontextprotocol/python-sdk/tree/v1.x
- Server guide: https://github.com/modelcontextprotocol/python-sdk/blob/v1.x/docs/server.md
- Testing guide: https://github.com/modelcontextprotocol/python-sdk/blob/v1.x/docs/testing.md
- Protocol documentation: https://modelcontextprotocol.io/docs

Keep database tools read-only and task-specific. Do not expose arbitrary SQL.
Preserve point-in-time, jurisdiction, and language filters and return citable
`chunks.id` values with provenance and ranking evidence.
