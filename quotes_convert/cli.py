"""Command-line interface for quotes-convert.

This module provides CLI functionality for converting quotes in files and streams.
Requires the 'cli' extra: pip install quotes-convert[cli]
"""
import sys
from pathlib import Path
from typing import Optional, List, TextIO

from quotes_convert import (
    single_quotes,
    double_quotes,
    single_quotes_stream,
    double_quotes_stream,
)

CHUNK_SIZE = 8192


def _process_stream(
    input_stream: TextIO,
    output_stream: TextIO,
    to_single: bool
) -> None:
    """Process input stream and write to output stream.

    Args:
        input_stream: Input text stream to read from.
        output_stream: Output text stream to write to.
        to_single: If True, convert to single quotes; otherwise double quotes.
    """
    converter = single_quotes_stream if to_single else double_quotes_stream

    def read_chunks():
        """Read input in chunks."""
        while True:
            chunk = input_stream.read(CHUNK_SIZE)
            if not chunk:
                break
            yield chunk

    for output_chunk in converter(read_chunks()):
        output_stream.write(output_chunk)


def cli_main():
    """CLI entry point with graceful dependency check."""
    try:
        import typer
    except ImportError:
        print(
            "Error: CLI dependencies not installed.\n"
            "Install with: pip install quotes-convert[cli]",
            file=sys.stderr,
        )
        sys.exit(1)

    _run_cli(typer)


def _run_cli(typer):
    """Run the CLI application."""
    from typing_extensions import Annotated
    from importlib.metadata import version as get_version

    app = typer.Typer(
        name="quotes-convert",
        help="Convert matching double-quotes to single-quotes or vice versa in strings and streams.",
        add_completion=False,
    )

    def version_callback(value: bool):
        """Print version and exit."""
        if value:
            try:
                ver = get_version("quotes-convert")
            except Exception:
                ver = "unknown"
            print(f"quotes-convert {ver}")
            raise typer.Exit()

    @app.command()
    def main(
        files: Annotated[
            Optional[List[Path]],
            typer.Argument(
                help="Files to convert. If not provided, reads from stdin.",
                exists=True,
                dir_okay=False,
                readable=True,
            ),
        ] = None,
        single: Annotated[
            bool,
            typer.Option(
                "--single",
                "-s",
                help="Convert to single quotes.",
            ),
        ] = False,
        double: Annotated[
            bool,
            typer.Option(
                "--double",
                "-d",
                help="Convert to double quotes.",
            ),
        ] = False,
        in_place: Annotated[
            bool,
            typer.Option(
                "--in-place",
                "-i",
                help="Edit files in place. Only valid when processing files.",
            ),
        ] = False,
        output: Annotated[
            Optional[Path],
            typer.Option(
                "--output",
                "-o",
                help="Output file. Only valid when processing a single file or stdin.",
            ),
        ] = None,
        version: Annotated[
            bool,
            typer.Option(
                "--version",
                "-V",
                callback=version_callback,
                is_eager=True,
                help="Show version and exit.",
            ),
        ] = False,
    ) -> None:
        """Convert matching quotes in files or stdin."""

        if single and double:
            raise typer.BadParameter("Cannot specify both --single and --double")

        if not single and not double:
            raise typer.BadParameter("Must specify either --single or --double")

        # Determine conversion direction (explicitly check both flags for clarity)
        to_single = True if single else False  # single=True for --single, False when double=True

        if in_place and output:
            raise typer.BadParameter("Cannot specify both --in-place and --output")

        if in_place and not files:
            raise typer.BadParameter("--in-place requires file arguments")

        if output and files and len(files) > 1:
            raise typer.BadParameter("--output can only be used with a single input file")

        if not files:
            if output:
                with open(output, "w", encoding="utf-8") as out_file:
                    _process_stream(sys.stdin, out_file, to_single)
            else:
                _process_stream(sys.stdin, sys.stdout, to_single)
            return

        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8") as in_file:
                    if in_place:
                        content = in_file.read()
                        converted = single_quotes(content) if to_single else double_quotes(content)

                        with open(file_path, "w", encoding="utf-8") as out_file:
                            out_file.write(converted)
                    elif output:
                        with open(output, "w", encoding="utf-8") as out_file:
                            _process_stream(in_file, out_file, to_single)
                    else:
                        _process_stream(in_file, sys.stdout, to_single)

            except FileNotFoundError:
                typer.echo(f"Error: File not found: {file_path}", err=True)
                raise typer.Exit(code=1)
            except PermissionError:
                typer.echo(f"Error: Permission denied: {file_path}", err=True)
                raise typer.Exit(code=1)
            except UnicodeDecodeError:
                typer.echo(f"Error: Cannot decode file (not UTF-8): {file_path}", err=True)
                raise typer.Exit(code=1)
            except IOError as e:
                typer.echo(f"Error processing {file_path}: {e}", err=True)
                raise typer.Exit(code=1)

    app()


if __name__ == "__main__":
    cli_main()
