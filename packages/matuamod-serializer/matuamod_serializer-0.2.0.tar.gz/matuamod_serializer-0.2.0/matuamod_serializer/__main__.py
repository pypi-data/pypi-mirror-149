import sys
from .converters.converters import Converter


def main():
    converter = Converter()
    args = converter.parse_args()
    converter.get_args(args)


if __name__ == "__main__":
    main()