## Project Overview

This is a **Python CLI tools collection** using `uv` (modern Python package manager) as the build and runtime system. Each script in the `scripts/` directory is a standalone CLI tool that can be extended over time.

**Key characteristics:**
- Modern Python 3.9+ with `uv` package management
- Standalone scripts architecture (not a monolithic package)
- Entry points configured in `pyproject.toml` for easy CLI execution
- Uses Python's built-in `argparse` library for CLI argument parsing
- No external dependencies by default (keeps setup minimal)

## Common Development Commands

```bash
# Run a script during development
cd /Users/alexey/dev/bash-scripts/python
uv run scripts/greet.py alex
uv run scripts/greet.py --help

# Direct Python execution (alternative)
python3 scripts/greet.py alex

# Using uvx (after project installation)
uvx --from . greet alex
```

## Project Structure

```
python/
├── pyproject.toml          # Project config, dependencies, entry points
├── .gitignore              # Python ignore patterns
├── README.md               # User-facing documentation
├── .venv/                  # Virtual environment (auto-created)
├── uv.lock                 # Dependency lock file
└── scripts/
    ├── __init__.py         # Makes scripts/ a Python package
    └── greet.py            # Example CLI tool
```

## Architecture & Key Patterns

### Script Pattern

Every CLI tool follows this structure:

```python
#!/usr/bin/env python3
"""Module docstring describing the tool"""
import argparse

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        prog="tool-name",
        description="What this tool does",
    )
    parser.add_argument("positional_arg", help="Description")
    parser.add_argument("-o", "--optional", help="Optional flag")

    args = parser.parse_args()

    # Tool logic here
    print(f"Result: {args.positional_arg}")

if __name__ == "__main__":
    main()
```

**Key points:**
- Uses `argparse` (Python built-in, no dependencies)
- Single `main()` function as entry point
- `__main__` guard for direct execution
- Arguments parsed before any logic runs

### Entry Points Configuration

Tools are registered in `pyproject.toml`:

```toml
[project.scripts]
greet = "scripts.greet:main"
new-tool = "scripts.new_tool:main"
```

This makes commands directly callable via `uv run` or `uvx` without needing a wrapper script.

### The scripts/ Package

The `scripts/` directory is a Python package (has `__init__.py`). This allows:
- Entry points to reference scripts as modules (`scripts.greet:main`)
- Future organization with submodules if needed
- Clean separation of tools from configuration

## Adding a New CLI Tool

1. **Create the script** file in `scripts/new-tool.py`:
   ```python
   #!/usr/bin/env python3
   """One-line description of your tool"""
   import argparse

   def main():
       parser = argparse.ArgumentParser(
           prog="new-tool",
           description="What this tool does",
       )
       parser.add_argument("name", help="Argument description")
       args = parser.parse_args()

       # Your logic
       print(f"Output: {args.name}")

   if __name__ == "__main__":
       main()
   ```

2. **Register in `pyproject.toml`** under `[project.scripts]`:
   ```toml
   new-tool = "scripts.new_tool:main"
   ```

3. **Test it**:
   ```bash
   uv run scripts/new-tool.py --help
   uv run scripts/new-tool.py your-input
   ```

4. **Document it** in `README.md` usage section

## Adding Dependencies

If a new tool needs external libraries:

1. Add to `pyproject.toml` `dependencies` array:
   ```toml
   [project]
   dependencies = [
       "requests>=2.28.0",
       "click>=8.0.0",
   ]
   ```

2. Run `uv sync` to update `uv.lock`

3. Scripts can now import and use these packages

## Important Files

- **`pyproject.toml`** - Project metadata, Python version requirement (3.9+), dependencies, and script entry points. **Modify when adding new tools or dependencies.**
- **`scripts/__init__.py`** - Empty file making `scripts/` a package. Required for entry points to work.
- **`README.md`** - User documentation with setup, usage examples, and instructions for adding new tools.
- **`uv.lock`** - Auto-generated lock file for reproducible builds. Commit to git.
- **`.gitignore`** - Standard Python ignores. Update if adding new patterns needed.

## Testing & Validation

```bash
# Test a script works
uv run scripts/greet.py alex

# Test help text
uv run scripts/greet.py --help

# Test argument validation
uv run scripts/greet.py  # Should fail (missing required argument)
```

## Git Workflow

This Python subproject is in the `python` branch of a larger monorepo. When making changes:
- Keep commits scoped to the `python/` directory
- Update `README.md` when adding new tools
- Commit `uv.lock` when dependencies change
- Keep `.venv/` and `__pycache__/` out of commits (already in `.gitignore`)

## When to Use argparse vs. Click vs. Typer

**Current choice: argparse** (built-in Python standard library)

- ✅ No dependencies (keeps project lightweight)
- ✅ Built into Python 3.9+
- ✅ Good for simple CLI tools with straightforward argument parsing
- ❌ More verbose than modern alternatives

If a tool needs complex subcommands or advanced CLI features, consider:
- **Click** - Popular, decorator-based, very Pythonic
- **Typer** - Modern, uses type hints, very intuitive

Just add to dependencies in `pyproject.toml` if switching.

## Virtual Environment Notes

`uv` automatically manages virtual environments. When you run `uv run scripts/greet.py`, it:
1. Creates `.venv/` if it doesn't exist
2. Ensures dependencies are installed
3. Executes the script in that environment

You don't need to manually activate virtual environments.

## Troubleshooting

**"uv: command not found"**
- Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`

**"ModuleNotFoundError" when importing**
- Check dependency is in `pyproject.toml` `dependencies` array
- Run `uv sync` to update lock file
- Ensure script is in `scripts/` directory

**Script works locally but not with entry point**
- Verify entry point in `pyproject.toml` matches: `scripts.filename:main`
- Check `scripts/__init__.py` exists
- Script name in `pyproject.toml` should use hyphens, file name uses underscores: `new-tool = "scripts.new_tool:main"`
