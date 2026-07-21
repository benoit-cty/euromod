from __future__ import annotations

from unittest.mock import MagicMock, patch

from nomotheca_mcp import server


def test_full_text_tool_does_not_load_encoder() -> None:
    connection = MagicMock()
    context = MagicMock()
    context.__enter__.return_value = connection

    with (
        patch.object(server, "_connect", return_value=context),
        patch.object(server, "search", return_value=[]),
        patch.object(server.encoder, "encode_literal") as encode,
    ):
        result = server.search_legislation("income tax", mode="full_text")

    encode.assert_not_called()
    assert result["result_count"] == 0
    assert result["model_id"] is None


def test_vector_tool_uses_bge_m3_model_id() -> None:
    connection = MagicMock()
    context = MagicMock()
    context.__enter__.return_value = connection

    with (
        patch.object(server, "_connect", return_value=context),
        patch.object(server, "search", return_value=[]) as search,
        patch.object(server.encoder, "encode_literal", return_value="[0]") as encode,
    ):
        result = server.search_legislation("income tax", mode="vector")

    encode.assert_called_once_with("income tax")
    assert search.call_args.kwargs["model_id"] == 1
    assert result["model_id"] == 1
