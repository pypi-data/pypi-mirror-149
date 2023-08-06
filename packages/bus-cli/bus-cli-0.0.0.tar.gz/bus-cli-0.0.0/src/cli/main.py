import argparse
import logging

logger = logging.getLogger("cli")


def _parser_init() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Some description.")

    return parser


def main() -> int:
    parser = _parser_init()

    args = parser.parse_args()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
