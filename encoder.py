import sublime
import sublime_plugin
import urllib.parse


class Encoder(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            text_content = self.view.substr(region)
            split_url = urllib.parse.urlsplit(text_content)
            quoted_path = urllib.parse.quote(split_url.path)
            quoted_query = urllib.parse.quote(split_url.query)
            encoded_text_content = urllib.parse.urlunsplit((
                split_url.scheme,
                split_url.netloc,
                quoted_path,
                quoted_query,
                split_url.fragment))
            self.view.replace(edit, region, encoded_text_content)
