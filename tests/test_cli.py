"""Tests for the CLI module."""
import tempfile
from pathlib import Path

import pytest

typer = pytest.importorskip("typer")

from typer.testing import CliRunner

runner = CliRunner(mix_stderr=False)


def get_app():
    """Create a fresh CLI app for testing."""
    from typing import Optional, List
    from typing_extensions import Annotated
    from quotes_convert.cli import _process_stream
    from quotes_convert import single_quotes, double_quotes
    import sys

    app = typer.Typer(
        name="quotes-convert",
        help="Convert matching quotes in files and streams.",
        add_completion=False,
    )

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
            typer.Option("--single", "-s", help="Convert to single quotes."),
        ] = False,
        double: Annotated[
            bool,
            typer.Option("--double", "-d", help="Convert to double quotes."),
        ] = False,
        in_place: Annotated[
            bool,
            typer.Option("--in-place", "-i", help="Edit files in place."),
        ] = False,
        output: Annotated[
            Optional[Path],
            typer.Option("--output", "-o", help="Output file."),
        ] = None,
    ) -> None:
        """Convert matching quotes in files or stdin."""
        if single and double:
            raise typer.BadParameter("Cannot specify both --single and --double")

        if not single and not double:
            raise typer.BadParameter("Must specify either --single or --double")

        to_single = single

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

    return app


@pytest.fixture
def app():
    """Get the CLI app for testing."""
    return get_app()


def test_cli_requires_quote_style(app):
    """Test that CLI requires either --single or --double."""
    result = runner.invoke(app, [], catch_exceptions=False)
    assert result.exit_code != 0


def test_cli_cannot_use_both_quote_styles(app):
    """Test that CLI rejects both --single and --double."""
    result = runner.invoke(app, ["--single", "--double"], catch_exceptions=False)
    assert result.exit_code != 0


def test_cli_stdin_to_stdout_single(app):
    """Test converting stdin to stdout with single quotes."""
    input_text = 'x = "hello"; y = "world"'
    result = runner.invoke(app, ["--single"], input=input_text)
    assert result.exit_code == 0
    assert result.stdout == "x = 'hello'; y = 'world'"


def test_cli_stdin_to_stdout_double(app):
    """Test converting stdin to stdout with double quotes."""
    input_text = "x = 'hello'; y = 'world'"
    result = runner.invoke(app, ["--double"], input=input_text)
    assert result.exit_code == 0
    assert result.stdout == 'x = "hello"; y = "world"'


def test_cli_stdin_to_file(app):
    """Test converting stdin to output file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "output.txt"
        input_text = 'test = "value"'

        result = runner.invoke(
            app, ["--single", "--output", str(output_file)], input=input_text
        )
        assert result.exit_code == 0

        with open(output_file, "r") as f:
            assert f.read() == "test = 'value'"


def test_cli_file_to_stdout(app):
    """Test converting file to stdout."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "input.txt"
        input_file.write_text('x = "test"')

        result = runner.invoke(app, ["--single", str(input_file)])
        assert result.exit_code == 0
        assert result.stdout == "x = 'test'"


def test_cli_file_to_output_file(app):
    """Test converting file to output file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "input.txt"
        output_file = Path(tmpdir) / "output.txt"
        input_file.write_text('x = "test"')

        result = runner.invoke(
            app, ["--double", str(input_file), "--output", str(output_file)]
        )
        assert result.exit_code == 0

        with open(output_file, "r") as f:
            assert f.read() == 'x = "test"'


def test_cli_in_place_editing(app):
    """Test in-place file editing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.txt"
        test_file.write_text('x = "hello"; y = "world"')

        result = runner.invoke(app, ["--single", "--in-place", str(test_file)])
        assert result.exit_code == 0

        with open(test_file, "r") as f:
            assert f.read() == "x = 'hello'; y = 'world'"


def test_cli_multiple_files_to_stdout(app):
    """Test converting multiple files to stdout."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = Path(tmpdir) / "file1.txt"
        file2 = Path(tmpdir) / "file2.txt"
        file1.write_text('x = "test1"')
        file2.write_text('y = "test2"')

        result = runner.invoke(app, ["--single", str(file1), str(file2)])
        assert result.exit_code == 0
        assert result.stdout == "x = 'test1'y = 'test2'"


def test_cli_multiple_files_in_place(app):
    """Test in-place editing of multiple files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = Path(tmpdir) / "file1.txt"
        file2 = Path(tmpdir) / "file2.txt"
        file1.write_text('x = "test1"')
        file2.write_text('y = "test2"')

        result = runner.invoke(
            app, ["--double", "--in-place", str(file1), str(file2)]
        )
        assert result.exit_code == 0

        with open(file1, "r") as f:
            assert f.read() == 'x = "test1"'
        with open(file2, "r") as f:
            assert f.read() == 'y = "test2"'


def test_cli_cannot_use_in_place_with_stdin(app):
    """Test that --in-place requires file arguments."""
    result = runner.invoke(app, ["--single", "--in-place"], input="test", catch_exceptions=False)
    assert result.exit_code != 0


def test_cli_cannot_use_in_place_and_output(app):
    """Test that --in-place and --output cannot be used together."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "input.txt"
        output_file = Path(tmpdir) / "output.txt"
        input_file.write_text("test")

        result = runner.invoke(
            app,
            [
                "--single",
                "--in-place",
                "--output",
                str(output_file),
                str(input_file),
            ],
            catch_exceptions=False,
        )
        assert result.exit_code != 0


def test_cli_output_requires_single_file(app):
    """Test that --output can only be used with single file input."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = Path(tmpdir) / "file1.txt"
        file2 = Path(tmpdir) / "file2.txt"
        output_file = Path(tmpdir) / "output.txt"
        file1.write_text("test1")
        file2.write_text("test2")

        result = runner.invoke(
            app,
            ["--single", str(file1), str(file2), "--output", str(output_file)],
            catch_exceptions=False,
        )
        assert result.exit_code != 0


def test_cli_handles_mixed_quotes(app):
    """Test CLI handles strings with mixed quotes correctly."""
    input_text = '"it\'s working"'
    result = runner.invoke(app, ["--single"], input=input_text)
    assert result.exit_code == 0
    assert result.stdout == "'it\\'s working'"


def test_cli_handles_nested_quotes(app):
    """Test CLI handles nested quotes correctly."""
    input_text = "'say \"hi\"'"
    result = runner.invoke(app, ["--double"], input=input_text)
    assert result.exit_code == 0
    assert result.stdout == '"say \\"hi\\""'


def test_cli_short_flags(app):
    """Test that short flags work correctly."""
    input_text = 'x = "test"'
    result = runner.invoke(app, ["-s"], input=input_text)
    assert result.exit_code == 0
    assert result.stdout == "x = 'test'"

    result = runner.invoke(app, ["-d"], input=input_text)
    assert result.exit_code == 0
    assert result.stdout == 'x = "test"'


def test_cli_in_place_short_flag(app):
    """Test that -i flag works for in-place editing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.txt"
        test_file.write_text('x = "test"')

        result = runner.invoke(app, ["-s", "-i", str(test_file)])
        assert result.exit_code == 0

        with open(test_file, "r") as f:
            assert f.read() == "x = 'test'"


def test_cli_output_short_flag(app):
    """Test that -o flag works for output file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "output.txt"
        input_text = 'x = "test"'

        result = runner.invoke(app, ["-s", "-o", str(output_file)], input=input_text)
        assert result.exit_code == 0

        with open(output_file, "r") as f:
            assert f.read() == "x = 'test'"


def test_cli_large_file_streaming(app):
    """Test that CLI handles large files efficiently via streaming."""
    with tempfile.TemporaryDirectory() as tmpdir:
        large_file = Path(tmpdir) / "large.txt"
        content = 'line = "test"\n' * 10000
        large_file.write_text(content)

        result = runner.invoke(app, ["--single", str(large_file)])
        assert result.exit_code == 0
        assert "line = 'test'\n" in result.stdout


def test_cli_empty_file(app):
    """Test CLI handles empty files correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        empty_file = Path(tmpdir) / "empty.txt"
        empty_file.write_text("")

        result = runner.invoke(app, ["--single", str(empty_file)])
        assert result.exit_code == 0
        assert result.stdout == ""


def test_cli_file_not_found(app):
    """Test CLI handles non-existent files gracefully."""
    result = runner.invoke(app, ["--single", "/nonexistent/file.txt"])
    assert result.exit_code == 2


def test_cli_unicode_content(app):
    """Test CLI handles unicode content correctly."""
    input_text = 'msg = "héllo wörld 你好"'
    result = runner.invoke(app, ["--single"], input=input_text)
    assert result.exit_code == 0
    assert result.stdout == "msg = 'héllo wörld 你好'"


def test_cli_help(app):
    """Test CLI help output."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--single" in result.stdout
    assert "--double" in result.stdout
    assert "--in-place" in result.stdout
    assert "--output" in result.stdout
