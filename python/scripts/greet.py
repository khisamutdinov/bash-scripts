#!/usr/bin/env python3
"""
Simple greet CLI tool - demonstrates basic argparse usage
"""
import argparse


def main():
    """Main entry point for the greet CLI"""
    parser = argparse.ArgumentParser(
        prog="greet",
        description="Greet someone with a friendly message",
    )
    parser.add_argument(
        "name",
        help="The name of the person to greet",
    )

    args = parser.parse_args()

    # Capitalize the name and print greeting
    greeting = f"Hello {args.name.capitalize()}!"
    print(greeting)


if __name__ == "__main__":
    main()
