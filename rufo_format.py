import sublime_plugin
import sublime
import subprocess
from .diff_match_patch import diff_match_patch
import json

class RufoPluginListener(sublime_plugin.EventListener):
  def on_pre_save(self, view):
    settings = sublime.load_settings('sublime-rufo.sublime-settings')
    if settings.get('auto_format') == None or settings.get('auto_format') == True:
      view.run_command('rufo_format')

class RufoFormatCommand(sublime_plugin.TextCommand):
  def is_enabled(self):
    caret = self.view.sel()[0].a
    syntax_name = self.view.scope_name(caret)
    return any(name in syntax_name for name in ["source.ruby", "text.html.ruby"])

  def has_redo(self):
    cmd, args, repeat = self.view.command_history(1)
    return cmd != ''

  def run(self, edit):
    vsize = self.view.size()
    region = sublime.Region(0, vsize)
    src = self.view.substr(region)
    window = self.view.window()
    filename = self.view.file_name()

    settings = sublime.load_settings('sublime-rufo.sublime-settings')
    rufo_cmd = settings.get("rufo_cmd") or "rufo"

    command = [rufo_cmd]
    if filename != None:
      command = [rufo_cmd, "--filename", filename]

    with subprocess.Popen(command, stdin = subprocess.PIPE, stdout = subprocess.PIPE) as proc:
      proc.stdin.write(bytes(src, 'UTF-8'))
      proc.stdin.close()
      output = proc.stdout.read().decode('UTF-8')
      exit = proc.wait()

    pos = 0
    if exit == 3:
      if not self.has_redo():
        for op, text in diff_match_patch().diff_main(src, output):
          if op == diff_match_patch.DIFF_DELETE:
            self.view.erase(edit, sublime.Region(pos, pos + len(text)))
          if op == diff_match_patch.DIFF_INSERT:
            self.view.insert(edit, pos, text)
            pos += len(text)
          if op == diff_match_patch.DIFF_EQUAL:
            pos += len(text)
