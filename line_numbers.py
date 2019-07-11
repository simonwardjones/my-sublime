import sublime
import sublime_plugin


class AddLineNumbersCommand(sublime_plugin.TextCommand):
    def run(self, edit, suffix=". "):
        selections = self.view.sel()
        for selection in selections:
            lines = self.view.split_by_newlines(selection)
            for i, line in enumerate(lines):
                line_number = str(i+1)+suffix
                offset = len(line_number) * i
                self.view.insert(edit, line.begin() + offset, line_number)
