import urwid

def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

class QuestionBox(urwid.Filler):
    def keypress(self, size, key):
        if key != 'enter':
            return super(QuestionBox, self).keypress(size, key)
        self.original_widget = urwid.Text(
            "Nice to meet you, \n{0}\nPress Q to exit.".format(
                edit.edit_text
            )
        )

edit = urwid.Edit("What is your name?\n")
fill = QuestionBox(edit)
loop = urwid.MainLoop(fill, unhandled_input=exit_on_q)
loop.run()
