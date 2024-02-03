import os
import argparse
from typing import List, Tuple, Dict

def parse_series_arg(series_arg: List[str]) -> Tuple[str, str, List[int]]:
    level, name_pattern, number_range = series_arg
    start, end = map(int, number_range.split('-'))
    return level, name_pattern, list(range(start, end + 1))

def create_directories(name_pattern: str, numbers: List[int], sub_dirs: Dict[str, List[str]]):
    for number in numbers:
        dir_name = name_pattern.replace("#", str(number))
        os.makedirs(dir_name, exist_ok=True)  # Create main directory

        # Create subdirectories for L2
        for sub_dir in sub_dirs.get("L2", []):
            os.makedirs(os.path.join(dir_name, sub_dir), exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description='Create a flexible directory tree.')
    parser.add_argument('--series', nargs=3, help='Level, name pattern, and number range for main directories')
    parser.add_argument('--create', action='append', nargs=2, help='Level and name for sub-directories', default=[])

    args = parser.parse_args()

    # Parse series argument
    level, name_pattern, numbers = parse_series_arg(args.series)

    # Collect subdirectories for each level
    sub_dirs = {}
    for lvl, name in args.create:
        sub_dirs.setdefault(lvl, []).append(name)

    # Create directories
    create_directories(name_pattern, numbers, sub_dirs)

if __name__ == "__main__":
    main()
