import tkinter
import win32api
import win32con
import threading
import pywintypes



class foreground:
    '''
    # Message Foreground

    This library allows you to create a message that is
    displayed in the foreground and above all other elements.
    ---------------------------------------------------------


    Settings:
    ---------

    - `text` → Le texte à afficher.
    - `font` → La police de caractère à utiliser.
    - `fg` → La couleur de texte à utiliser.
    - `bg` → La couleur de fond à utiliser.
    - `geometry` → La position du message.

    To write in white you have to make white -1 or #fffffe


    Example:
    --------
    This code creates a message that displays "Hello World" in white color on a transparent background.

    >>> from message import foreground
    >>> f = foreground('Hello World', font=('Consolas', '15'), fg='#fffffe', bg='white')
    >>> f.display()
    '''


    def __init__(self, text, fg, bg='white', font=('Consolas','15'), geometry=None):
        self.stop = False
        self.text = text
        self.font = font
        self.fg = fg
        self.bg = bg
        self.geometry = geometry
    

    def __run__(self):
        def exit():
            while not self.stop: pass
            label.quit()

        def set_text():
            label.config(text=self.text)
            label.update()
        def set_font():
            label.config(font=self.font)
            label.update()
        def set_fg():
            label.config(fg=self.fg)
            label.update()
        def set_bg():
            label.config(bg=self.bg)
            label.update()

        def set():
            while not self.stop:
                temp = [self.text, self.font, self.fg, self.bg]
                while temp == [self.text, self.font, self.fg, self.bg]: pass
                set_text(); set_font(); set_fg(); set_bg()

        label = tkinter.Label(text=self.text, font=self.font, fg=self.fg, bg=self.bg)
        label.master.overrideredirect(True)
        label.master.resizable(False, False)

        if self.geometry is None or self.geometry == 'center':
            windowWidth = label.winfo_reqwidth()
            windowHeight = label.winfo_reqheight()
            positionRight = int(label.winfo_screenwidth()/2 - windowWidth/2)
            positionDown = int(label.winfo_screenheight()/2 - windowHeight/2)
            label.master.geometry(f"+{positionRight}+{positionDown}")
        else:
            label.master.geometry(self.geometry)

        label.master.lift()
        label.master.wm_attributes("-topmost", True)
        label.master.wm_attributes("-disabled", True)
        label.master.wm_attributes("-transparentcolor", "white")
        hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
        exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
        win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)
        label.pack()

        threading.Thread(target=exit).start()
        threading.Thread(target=set).start()

        label.mainloop()


    def display(self):
        threading.Thread(target=self.__run__).start()


    def update(self, text=None, font=None, fg=None, bg=None):
        if text is not None: self.text = text
        if font is not None: self.font = font
        if fg is not None: self.fg = fg
        if bg is not None: self.bg = bg
        if text is None or font is None or fg is None or bg is None:
            raise ValueError('text, font, fg, bg must be set')


    def exit(self):
        self.stop = True