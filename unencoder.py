import sublime
import sublime_plugin
import urllib.parse


class UnEncoder(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            text_content = self.view.substr(region)
            split_url = urllib.parse.urlsplit(text_content)
            unquoted_path = urllib.parse.unquote(split_url.path)
            unquoted_query = urllib.parse.unquote(split_url.query)
            unencoded_text_content = urllib.parse.urlunsplit((
                split_url.scheme,
                split_url.netloc,
                unquoted_path,
                unquoted_query,
                split_url.fragment))
            self.view.replace(edit, region, unencoded_text_content)
