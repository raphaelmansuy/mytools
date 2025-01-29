#!/usr/bin/env -S uv run

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "litellm>=1.59.8",
#     "loguru",
#     "pydantic>=2.0.0",
#     "python-dotenv",
#     "rich",  # Added rich for enhanced terminal support
#     "typing",  # For type hints
# ]
# ///

import subprocess
import pathlib
import sys
from typing import Optional, List, Union
from rich import print
from rich.console import Console
from rich.panel import Panel

console = Console()

def markdown_to_docx(
    input_md: Union[str, pathlib.Path],
    output_docx: Union[str, pathlib.Path],
    reference_doc: Optional[Union[str, pathlib.Path]] = None,
    resource_dir: Optional[Union[str, pathlib.Path]] = None
) -> None:
    """
    Convert Markdown to DOCX with Pandoc using advanced formatting options
    
    Args:
        input_md: Path to input Markdown file
        output_docx: Path for output DOCX file
        reference_doc: Path to reference template DOCX (optional)
        resource_dir: Resource path for images/assets (optional)
    """
    input_md = str(input_md)
    output_docx = str(output_docx)
    
    cmd = [
        "pandoc",
        "-s",  # Standalone document
        "--mathml",  # Preserve math equations
        "--columns=80",  # Control text width
        "--toc",  # Add table of contents
        "--metadata", "title=Document",  # Set metadata
        "-f", "markdown+emoji+smart",  # Enable extended Markdown features
        input_md,
        "-o", output_docx
    ]
    
    if reference_doc:
        cmd.extend(["--reference-doc", str(reference_doc)])
    
    if resource_dir:
        cmd.extend(["--resource-path", str(resource_dir)])
    
    try:
        with console.status("Converting Markdown to DOCX...", spinner='dots'):
            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        
        console.print(
            Panel(
                f"Successfully created DOCX file: [green]{output_docx}",
                title="Success",
                style="green"
            )
        )
        
    except subprocess.CalledProcessError as e:
        console.print(
            Panel(
                f"Conversion failed: {e.stderr}",
                title="Error",
                style="red"
            )
        )
        sys.exit(1)
    except FileNotFoundError:
        console.print(
            Panel(
                "Pandoc not found. Please install Pandoc from https://pandoc.org/installing.html",
                title="Error",
                style="red"
            )
        )
        sys.exit(1)

def main():
    if len(sys.argv) == 1:
        console.print(
            Panel(
                "Convert Markdown to DOCX\n"
                "Usage: python convert.py input.md output.docx [options]",
                title="Usage"
            )
        )
        return
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Convert Markdown to DOCX with Pandoc"
    )
    
    parser.add_argument(
        "input_md",
        type=pathlib.Path,
        help="Path to input Markdown file"
    )
    
    parser.add_argument(
        "output_docx",
        type=pathlib.Path,
        help="Path for output DOCX file"
    )
    
    parser.add_argument(
        "--reference-doc",
        type=pathlib.Path,
        help="Path to reference template DOCX"
    )
    
    parser.add_argument(
        "--resource-dir",
        type=pathlib.Path,
        help="Directory containing images/assets"
    )
    
    args = parser.parse_args()
    
    markdown_to_docx(
        input_md=args.input_md,
        output_docx=args.output_docx,
        reference_doc=args.reference_doc,
        resource_dir=args.resource_dir
    )

if __name__ == "__main__":
    main()