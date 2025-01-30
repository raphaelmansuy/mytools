#!/usr/bin/env -S uv run

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "litellm>=1.59.8",
#     "loguru",
#     "pydantic>=2.0.0",
#     "python-dotenv",
#     "rich",
#     "typing",
#     "argparse",
# ]
# ///

import os
import argparse
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markup import escape
from typing import Dict, List, Optional

def normalize_search_text(text: str) -> str:
    """Normalize text for fuzzy matching by removing special characters and lowercase."""
    return ''.join([c.lower() for c in text if c.isalnum() or c.isspace()]).strip()

def list_models(models_data: Dict[str, List[Dict[str, str]]], 
               console: Console, 
               search_filter: Optional[str] = None) -> None:
    """Display models with enhanced fuzzy search functionality."""
    all_models = models_data.get("data", [])
    filtered_models = all_models

    if search_filter:
        # Convert search filter to lowercase for case-insensitive substring match
        normalized_filter = search_filter.lower()
        
        # Filter models based on substring match in ID, name, provider, or description
        filtered_models = [
            model for model in all_models 
            if (
                normalized_filter in model.get('id', '').lower() or
                normalized_filter in model.get('name', '').lower() or
                normalized_filter in model.get('provider', {}).get('id', '').lower() or
                normalized_filter in model.get('description', '').lower()
            )
        ]

    # Build table with original styling
    table = Table(
        show_header=True,
        header_style="bold magenta",
        expand=True,
        box=None,
        show_edge=False
    )
    table.add_column("Model ID", style="cyan", no_wrap=True)
    table.add_column("Context Window", justify="right")
    table.add_column("Provider", style="green")
    table.add_column("Input Pricing", justify="right")
    table.add_column("Output Pricing", justify="right")
    table.add_column("Description", style="yellow", width=40)

    for model in filtered_models:
        pricing = model.get("pricing", {})
        input_cost = pricing.get("prompt", "N/A")
        output_cost = pricing.get("completion", "N/A")

        table.add_row(
            escape(model.get("id", "N/A")),
            f"{model.get('context_length', 'N/A'):,} tokens",
            escape(model.get("provider", {}).get("id", "N/A")),
            f"${input_cost}/1M" if isinstance(input_cost, float) else "N/A",
            f"${output_cost}/1M" if isinstance(output_cost, float) else "N/A",
            escape(model.get("description", "No description available"))
        )

    # Build subtitle with filtering info
    subtitle_parts = [
        f"Showing {len(filtered_models)} of {len(all_models)} models",
        f"(filter: '{escape(search_filter)}')" if search_filter else ""
    ]

    console.print(
        Panel.fit(
            table,
            title="[bold]OpenRouter AI Model Explorer[/bold]",
            border_style="blue",
            subtitle=" ".join(subtitle_parts),
            padding=(1, 2)
        )
    )

def show_model_details(model_data: Dict[str, str], console: Console) -> None:
    """Display detailed model information with original formatting."""
    details = [
        f"[bold]Name:[/bold] {escape(model_data.get('name', 'N/A'))}",
        f"[bold]Description:[/bold] {escape(model_data.get('description', 'No description'))}",
        f"[bold]Context Window:[/bold] {model_data.get('context_length', 'N/A'):,} tokens",
        f"[bold]Provider:[/bold] {escape(model_data.get('provider', {}).get('id', 'N/A'))}",
        f"[bold]Pricing:[/bold] Input: ${model_data.get('pricing', {}).get('prompt', 'N/A')}/1M | "
        f"Output: ${model_data.get('pricing', {}).get('completion', 'N/A')}/1M",
        f"[bold]Tags:[/bold] {escape(', '.join(model_data.get('tags', [])))}",
        f"[bold]Features:[/bold] {escape(', '.join(model_data.get('features', [])))}",
        f"[bold]Model ID:[/bold] {escape(model_data.get('id', 'N/A'))}"
    ]

    console.print(
        Panel.fit(
            "\n".join(details),
            title=f"[bold]Model Details[/bold]",
            border_style="green",
            padding=(1, 4)
        )
    )

def main() -> None:
    """Main CLI execution flow with error handling."""
    parser = argparse.ArgumentParser(
        description="OpenRouter Model Explorer",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # List command with improved filter help
    list_parser = subparsers.add_parser('list', help='List models with optional fuzzy search')
    list_parser.add_argument(
        '-f', '--filter',
        type=str,
        help="Fuzzy search across ID, name, provider, and description (supports partial matches)"
    )

    # Info command preserved
    info_parser = subparsers.add_parser('info', help='Show detailed model information')
    info_parser.add_argument(
        'model_id',
        type=str,
        help='Exact model ID to inspect (case-sensitive)'
    )

    args = parser.parse_args()

    # API request configuration
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "HTTP-Referer": "https://github.com/yourusername/openrouter-tool",
        "X-Title": "OpenRouter Model Explorer"
    }
    
    try:
        response = requests.get("https://openrouter.ai/api/v1/models", headers=headers)
        response.raise_for_status()
        models_data = response.json()
    except requests.RequestException as e:
        Console().print(f"[bold red]Error:[/bold red] Failed to fetch models: {str(e)}")
        return

    console = Console()

    if args.command == 'list':
        list_models(models_data, console, args.filter)
    elif args.command == 'info':
        model = next(
            (m for m in models_data.get('data', []) if m['id'] == args.model_id),
            None
        )
        if model:
            show_model_details(model, console)
        else:
            console.print(
                f"[bold red]Error:[/bold red] Model '{escape(args.model_id)}' not found. "
                "Use 'list' command to see available models."
            )

if __name__ == "__main__":
    main()