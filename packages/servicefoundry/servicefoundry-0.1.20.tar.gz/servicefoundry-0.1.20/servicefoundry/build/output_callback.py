import sys


class OutputCallBack:
    def print_header(self, line):
        sys.stdout.write(f"{line}\n")

    def print_line(self, line):
        sys.stdout.write(f"{line}\n")

    def print_lines_in_panel(self, lines, header):
        sys.stdout.write(header)
        for line in lines:
            sys.stdout.write(line)
