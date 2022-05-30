"""A single-scene editor plugin for novelyst.

Compatibility: novelyst v0.16.0 API 
Requires Python 3.6+
Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_editor
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

APPLICATION = 'Scene Editor'
PLUGIN = f'{APPLICATION} plugin v@release'


class Plugin:
    """novelyst single-scene editor plugin class.
    
    Public methods:
        on_quit() -- apply changes before closing the editor windows.       
    """

    def __init__(self, ui):
        """Place a ScrolledText widget in novelyst's middle window.
        
        Positional arguments:
            ui -- reference to the NovelystTk instance of the application.
        """
        self._ui = ui

        # Place an editor window in the middle frame.
        self._editWindow = tk.Frame(self._ui.middleFrame)
        self._editWindow.pack(expand=True, fill='both')
        # Add a text editor with scrollbar to the editor window.
        self._sceneEditor = TextBox(self._editWindow, wrap='word', undo=True, autoseparators=True, maxundo=-1, height=25, width=60, padx=5, pady=5)
        self._sceneEditor.pack(expand=True, fill=tk.BOTH)

    def _apply_changes(self, event=None):
        """Write the editor content to the project, if possible."""
        sceneText = self._sceneEditor.get_text()
        if sceneText or self._scene.sceneContent:
            if self._scene.sceneContent != sceneText:
                if self._ui.isLocked:
                    messagebox.showinfo(PLUGIN, 'Cannot apply scene changes, because the project is locked.')
                    return

                self._scene.sceneContent = sceneText
                self._ui.isModified = True

    def on_quit(self, event=None):
        """Exit the editor. Apply changes, if possible."""
        sceneText = self._sceneEditor.get_text()
        if sceneText or self._scene.sceneContent:
            if self._scene.sceneContent != sceneText:
                if self._ui.ask_yes_no('Apply scene changes?'):
                    if self._ui.isLocked:
                        if self._ui.ask_yes_no('Cannot apply scene changes, because the project is locked.\nUnlock and apply changes?'):
                            self._ui.unlock()
                            self._scene.sceneContent = sceneText
                            self._ui.isModified = True
                    else:
                        self._scene.sceneContent = sceneText
                        self._ui.isModified = True
        self._editWindow.destroy()


class TextBox(scrolledtext.ScrolledText):
    """If a more sophisticated text box is needed, create it here."""

    def get_text(self):
        text = self.get('1.0', tk.END).strip(' \n')
        # convert text to yWriter markup, if applicable.
        return text

    def set_text(self, text):
        # convert text from yWriter markup, if applicable.
        self.insert(tk.END, text)
