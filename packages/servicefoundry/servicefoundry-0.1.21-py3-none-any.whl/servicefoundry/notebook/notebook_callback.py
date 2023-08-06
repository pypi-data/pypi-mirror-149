from ipywidgets import Output


class NotebookOutputCallBack:
    output: Output

    def __init__(self, output):
        self.output = output

    def print_header(self, line):
        self.output.append_stdout(f"{line} ----------------------------------------\n")

    def print_line(self, line):
        self.output.append_stdout(f"{line}\n")

    def print_lines_in_panel(self, lines, header):
        self.print_header(header)
        for line in lines:
            self.print_line(line)
