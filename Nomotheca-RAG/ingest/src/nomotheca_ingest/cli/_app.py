"""The Typer applications every command module registers on."""

from __future__ import annotations

from typing import Annotated

import typer

app = typer.Typer(help="Archive-first legislation ingestion commands.")
embeddings_app = typer.Typer(help="Build derived chunk embeddings.")
app.add_typer(embeddings_app, name="embeddings")
translate_app = typer.Typer(help="Machine-translate unit texts with an LLM.")
app.add_typer(translate_app, name="translate")

#: The --database-url option every command shares.
DatabaseUrl = Annotated[str, typer.Option("--database-url", "-d", envvar="EUROMOD_DATABASE_URL")]
