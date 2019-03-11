import sublime
import sublime_plugin


class SimonFind(sublime_plugin.TextCommand):
    def run(self, edit, x=None):
        print(x)
        print(list(self.view.sel()))
        self.view.window().run_command(
            'show_panel',
            {
                "panel": "replace",
                "in_selection": True
            })
        # self.view.show_popup('Find in selection 🔍')
        print('POPUP LOADED')
