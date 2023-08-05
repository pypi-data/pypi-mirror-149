from dataclasses import dataclass
from enum import Enum
from typing import Union, List
import sys
import argparse
import os
import re
from pathlib import Path

quiet = False

class IncludeLine:
    def __init__(self, line: str, filename=None):
        self.line = line
        self.line_stripped = line.strip()
        self.filename = filename
        pass

    def compare(self, other):
        if self.filename != other.filename:
            raise RuntimeError("unexpected error")

        # The precedence between the #includes is the following:
        # 1. header with the same name as this source file
        # 2. headers between square brackets (<>), alphabetically
        # 3. headers between quotes (""), alphabetically

        l1_content = self.line_stripped.split()[1]
        l2_content = other.line_stripped.split()[1]

        l1_sign = l1_content[0]
        l2_sign = l2_content[0]

        l1_name = l1_content[1:-1].split("/")[-1].split(".")[0]
        l2_name = l2_content[1:-1].split("/")[-1].split(".")[0]

        if l1_name == self.filename:
            return -1
        if l2_name == self.filename:
            return 1
        if l1_sign == "<" and l2_sign == "\"":
            return -1
        if l2_sign == "<" and l1_sign == "\"":
            return 1
        if l1_content < l2_content:
            return -1
        if l2_content < l1_content:
            return 1
        return 0

    def __str__(self):
        return self.line

    def __lt__(self, other):
        return self.compare(other) < 0

    def __gt__(self, other):
        return self.compare(other) > 0

    def __eq__(self, other):
        return self.compare(other) == 0

    def __le__(self, other):
        return self.compare(other) <= 0

    def __ge__(self, other):
        return self.compare(other) >= 0

    def __ne__(self, other):
        return self.compare(other) != 0

def eprint(*args, **kwargs):
    print("ERROR:", *args, **kwargs, file=sys.stderr)

def abort(*args, **kwargs):
    eprint(*args, **kwargs)
    exit(1)

def is_include_line(line):
    return line.strip().startswith("#include")

def cpp_include_lint_file(input_file: Path,
                          output_file: Path):
    class EntryType(Enum):
        LINE = 1
        INCLUDE_BATCH = 2

    @dataclass
    class Entry:
        type: EntryType
        content: Union[str, List[IncludeLine]]

        def is_line(self):
            return self.type == EntryType.LINE

        def is_include_batch(self):
            return self.type == EntryType.INCLUDE_BATCH

    entries: List[Entry] = []

    # read and parse
    try:
        with input_file.open() as f:
            for l in f:
                if is_include_line(l):
                    if not entries or not entries[-1].is_include_batch():
                        # begin of a new #include batch
                        entries.append(Entry(type=EntryType.INCLUDE_BATCH, content=[]))
                    # append the line to the last #include batch
                    entries[-1].content.append(IncludeLine(l, input_file.stem))
                else:
                    entries.append(Entry(type=EntryType.LINE, content=l))
    except Exception as ex:
        print(f"WARN: skipping '{input_file}': {ex}")
        return

    # sort
    for entry in entries:
        if entry.is_include_batch():
            entry.content = sorted(entry.content)

    # write
    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with output_file.open("w") as f:
            for entry in entries:
                if entry.is_include_batch():
                    for l in entry.content:
                        f.write(str(l))
                else:
                    f.write(str(entry.content))
    except Exception as ex:
        print(f"WARN: skipping '{input_file}': {ex}")
        return



def cpp_include_lint(input_path,
                     output_path,
                     recursive=False,
                     dry_run=False,
                     files_filter=None):

    input_path = Path(input_path)
    output_path = Path(output_path) if output_path else input_path

    if not input_path.exists():
        abort("input path does not exists")

    if input_path.is_file() and recursive:
        abort("input path must be a directory")

    if input_path.is_dir() and not recursive:
        abort("input path must be a file; use -R if you want to lint the directory recursively")

    if output_path.is_file() and recursive:
        abort("output path must be a directory")

    if output_path.is_dir() and not recursive:
        abort("output path must be a file")


    files_filter_re = None
    if files_filter:
        try:
            files_filter_re = re.compile(files_filter)
        except Exception as ex:
            abort(f"invalid regular expression: {ex}")

    files_to_lint = []

    # figure out files to lint
    if recursive:
        for root, dirs, files in os.walk(input_path, topdown=True):
            for name in files:
                trailing = str((Path(root) / name).relative_to(input_path))
                if not files_filter_re or files_filter_re.match(trailing):
                    files_to_lint.append((
                        (input_path / trailing),
                        (output_path / trailing)
                    ))
    else:
        files_to_lint.append((input_path, output_path))


    # lint files
    for (in_, out_) in files_to_lint:
        if not quiet:
            if in_ != out_:
                print(f"Linting '{in_}' to '{out_}'")
            else:
                print(f"Linting '{in_}'")
        if not dry_run:
            cpp_include_lint_file(in_, out_)


def main():
    global quiet

    parser = argparse.ArgumentParser(
        description="Sort #include directives of C/C++ files."
    )

    parser.add_argument("-r", "-R", "--recursive", dest="recursive",
                        action="store_const", const=True, default=False,
                        help="lint all the files in the input folder recursively")
    parser.add_argument("-d", "--dry-run", dest="dry_run",
                        action="store_const", const=True, default=False,
                        help="just print the files that would have been linted")
    parser.add_argument("-f", "--filter", dest="filter",
                        default=".*\.(h|hpp|c|cpp|tpp)", metavar="REGEX",
                        help="filter files to lint using the given regular expression. "
                             "The default one is: \".*\.(h|hpp|c|cpp|tpp)\"")
    parser.add_argument("-q", "--quiet", dest="quiet",
                        action="store_const", const=True, default=False,
                        help="suppress information messages")

    parser.add_argument("input", help="input path", )
    parser.add_argument("output", help="output path", nargs="?")

    parsed = vars(parser.parse_args(sys.argv[1:]))
    recursive = parsed.get("recursive")
    dry_run = parsed.get("dry_run")
    files_filter = parsed.get("filter")

    quiet = parsed.get("quiet")
    input_file = parsed.get("input")
    output_file = parsed.get("output")

    cpp_include_lint(input_file, output_file,
                     recursive=recursive,
                     dry_run=dry_run,
                     files_filter=files_filter)


if __name__ == "__main__":
    main()
