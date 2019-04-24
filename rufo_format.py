import os, sublime
import sublime_plugin


class RufoPluginListener(sublime_plugin.EventListener):
  def on_pre_save(self, view):
    view.run_command("rufo_format")

class RufoFormatCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    window = self.view.window()
    filename = self.view.file_name()
    # command = [rufo_cmd, "--filename", filename]
    # caret = self.view.sel()[0].a
    # msg = self.view.scope_name(caret)
    # msg = "'Hello, World!'\n"

    project_data = sublime.Window.project_data()

    # sublime.error_message(msg)
    # os.chdir()
    print(msg)
    # self.console.log(sublime.Window.project_data())