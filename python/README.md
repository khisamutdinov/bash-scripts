# Python CLI Tools

A collection of Python-based CLI tools for the bash-scripts repository.

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for Python package management.

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Available Tools

### greet

A simple greeting tool that says hello to someone.

**Usage:**
```bash
# For development (recommended)
uv run scripts/greet.py alex
# Output: Hello Alex!

# Show help
uv run scripts/greet.py --help
```

**Direct execution:**
```bash
python3 scripts/greet.py alex
```

**Using uvx (after project installation):**
```bash
uvx --from . greet alex
```

## Adding New Scripts

To add a new CLI tool:

1. Create a new Python file in the `scripts/` directory (e.g., `scripts/my-tool.py`)
2. Implement your tool using the same pattern:
   ```python
   #!/usr/bin/env python3
   import argparse

   def main():
       parser = argparse.ArgumentParser(description="Your tool description")
       parser.add_argument("arg", help="Argument description")
       args = parser.parse_args()

       # Your logic here
       print(f"Result: {args.arg}")

   if __name__ == "__main__":
       main()
   ```
3. Add an entry point to `pyproject.toml`:
   ```toml
   [project.scripts]
   my-tool = "scripts.my_tool:main"
   ```
4. Add any dependencies to the `dependencies` array in `pyproject.toml`

## Dependencies

This project uses Python's built-in libraries by default. Dependencies can be added to `pyproject.toml` as needed.

## Development

Run scripts directly during development:
```bash
uv run scripts/<script-name>.py [args]
```

The `uv run` command automatically manages the virtual environment for you.
