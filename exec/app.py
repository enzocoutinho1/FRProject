import tkinter as tk
import threading
import constants as const
import recognitioncv
import esp32serial
from tkinter import messagebox
import os


abspath = os.path.abspath("exec\\imagens")
print(abspath)
files = [f for f in os.listdir() if os.path.isdir(f)]
print(files)
    
if "_internal" in files:
    abspath = os.path.abspath("_internal\\imagens")
    print(abspath)

esp32 = esp32serial.Esp32()

def rgb_to_hex(emotions):
    return '#{:02x}{:02x}{:02x}'.format(emotions['r'], 
                                        emotions['g'], 
                                        emotions['b'],)

MAX_PEOPLE = 1

colorMode = ""
colorModeManual = ""
manualWin = None
manualRGB = None
manualList = None


def seguir():
    global colorMode
    colorMode = "Seguir"
    mode.config(text="Seguir")


def manual():
    global manualWin
    global colorMode
    colorMode = "Manual"
    mode.config(text="Manual")
    Select()

def add():
    global colorMode
    colorMode = "Add"
    mode.config(text="Add")


class WindowRGB(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("RGB")
        self.geometry("300x300")
        self.resizable(False, False)
        self.sliderR = tk.Scale(self, from_=0, to_=255, orient="horizontal")
        self.sliderR.place(x=150, y=37)
        self.labelR = tk.Label(self, text="Vermelho", fg="red")

        self.sliderG = tk.Scale(self, from_=0, to_=255, orient="horizontal")
        self.sliderG.place(x=150, y=107)
        self.labelG = tk.Label(self, text="Verde", fg="green")
 
        self.sliderB = tk.Scale(self, from_=0, to_=255, orient="horizontal")
        self.sliderB.place(x=150, y=177)
        self.labelB = tk.Label(self, text="Azul", fg="blue")
        self.labelR.place(x=50, y=50)
        self.labelB.place(x=50, y=190)
        self.labelG.place(x=50, y=120)
        self.wm_protocol(name="WM_DELETE_WINDOW", func=self.close)

    def getRGBValue(self):
        return [self.sliderR.get(), self.sliderG.get(), self.sliderB.get()]
    
    def close(self):
        self.destroy()
        global colorModeManual
        colorModeManual = ""

class Select(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Select")
        self.geometry("300x300")
        self.resizable(False, False)
        self.buttonRGB = tk.Button(self, text="RGB", command=self.openRGB)
        self.buttonYellow = tk.Button(self, text="Yellow", command=self.openYellow)
        self.list = tk.Button(self, text="List")
        self.list.pack(side=tk.TOP, pady=35)
        self.buttonRGB.pack(side=tk.TOP, pady=35)
        self.buttonYellow.pack(side=tk.TOP, pady=35)


    def openYellow(self):
        self.destroy()
        global manualWin
        manualWin = manualWindow()
        global colorModeManual
        colorModeManual = "yellow"

    def openRGB(self):
        self.destroy()
        global manualRGB
        manualRGB = WindowRGB()
        global colorModeManual
        colorModeManual = "rgb"

class manualWindow(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Modo manual")
        self.geometry("300x300")
        self.resizable(False, False)
        self.yellowSlider = tk.Scale(self, from_=50, to_=255, orient="horizontal", length=180)
        self.yellowSlider.place(x=60, y=100)
        self.wm_protocol(name="WM_DELETE_WINDOW", func=self.close)
        

    def getYellowValue(self):
        return self.yellowSlider.get()

      
    def close(self):
        global colorModeManual
        colorModeManual = ""
        self.destroy()


root = tk.Tk()
root.geometry(const.Janela.TAMANHO)
root.resizable(False, False)
root.configure(bg=const.Janela.BACKGROUND_COLOR)
root.title(const.Janela.TITULO)
icon = tk.PhotoImage(file=os.path.join(abspath, const.Janela.CAMINHO_ICON))
root.iconphoto(True, icon)

view_image = tk.PhotoImage(file=os.path.join(abspath, const.View.CAMINHO))
viewcolor = tk.Canvas( root, width = const.View.TAMANHO[const.X], 
                 height = const.View.TAMANHO[const.Y], 
                 background=const.Janela.BACKGROUND_COLOR, highlightthickness=0)

viewcolor.pack(side=tk.BOTTOM)
viewcolor.create_image(const.View.POSICAO[const.X], const.View.POSICAO[const.Y], 
                       image=view_image, anchor="nw")
color = viewcolor.create_oval(const.Circle.circle[const.X], const.Circle.circle[const.Y], 
                              const.Circle.circle[const.XF], const.Circle.circle[const.YF], 
                              fill=const.Circle.color)

select_image = tk.PhotoImage(file=os.path.join(abspath, const.Select.CAMINHO))
select = tk.Canvas(root, width=const.Select.TAMANHO[const.X], 
                 height=const.Select.TAMANHO[const.Y], 
                 background=const.Select.COLOR, highlightthickness=0)
select.create_image(const.Select.TAMANHO_IMAGEM[const.X], const.Select.TAMANHO_IMAGEM[const.Y], 
                    image=select_image)
select.pack(side=tk.BOTTOM)

follow_image = tk.PhotoImage(file=os.path.join(abspath, const.Follow.CAMINHO))
follow = tk.Button(root, image=follow_image, highlightthickness=0, bd=0, 
                   background=const.Follow.COLOR, command=seguir)
follow.place(x=const.Follow.POSICAO[const.X], y=const.Follow.POSICAO[const.Y])

manual_image = tk.PhotoImage(file=os.path.join(abspath, "manual.png"))
manualButton = tk.Button(root, image=manual_image, highlightthickness=0, bd=0, background="#FFAA39",
                   command=manual)
manualButton.place(x=270, y=196)

add_image = tk.PhotoImage(file=os.path.join(abspath, "add.png"))
addButton = tk.Button(root, image=add_image, highlightthickness=0, bd=0, background="#FFAA39",
                      command=add)
addButton.place(x=270, y=247)

mode = tk.Label(root, text="None", fg="#FFAA39", font=("Roboto", 20), bg="#E6E2D6")
mode.place(x=220, y=50)

def sendColorToESP():
    while True:
        emotions = recognitioncv.getcount_emotions()
        message = equation(emotions=emotions, mode=colorMode)
        esp32.sendmessage(message=message)


def equation(emotions, mode):
    if mode == "Seguir" and MAX_PEOPLE == 1:
        if emotions['angry'] == 1:
            emotions['r'] = 255
            emotions['g'] = 0
            emotions['b'] = 0
        elif emotions['sad'] == 1:
            emotions['r'] = 255
            emotions['g'] = 255
            emotions['b'] = 0
        elif emotions['neutral'] == 1:
            emotions['r'] =  255
            emotions['g'] = 0
            emotions['b'] = 255
        elif emotions['happy'] == 1:
            emotions['r'] = 0
            emotions['g'] = 255
            emotions['b'] = 0
        elif emotions['fatigue'] == 1:
            emotions['r'] = 0
            emotions['g'] = 0
            emotions ['b'] = 255
    elif mode == "Add":
        emotions['r'] = (int)(220 + ((emotions['angry'] + emotions['sad']) * (35/MAX_PEOPLE)))
        emotions['g'] = (int)(220 + ((emotions['neutral'] + emotions['happy']) * (35/MAX_PEOPLE)))
        emotions['b'] = (int)(220 + (emotions['fatigue'] * (35/MAX_PEOPLE)))
    elif mode == "Manual":
        global colorModeManual
        if colorModeManual == "yellow":
            emotions['r'] = 255
            emotions['g'] = 210
            emotions['b'] = manualWin.getYellowValue()
        elif colorModeManual == "rgb":
            try:
                emotions['r'] = manualRGB.getRGBValue()[0]
                emotions['g'] = manualRGB.getRGBValue()[1]
                emotions['b'] = manualRGB.getRGBValue()[2]
            except:
                pass
        elif colorModeManual == "list":
            pass
    global viewcolor
    viewcolor.itemconfig(color, fill=rgb_to_hex(emotions))
    return emotions

def initComm():
    try:
        esp32.open()
        recognitioncv.open()
        getExpressionThread = threading.Thread(target=recognitioncv.getRecog, daemon=True)
        getExpressionThread.start()
        sendColorToESPThread = threading.Thread(target=sendColorToESP, daemon=True)
        sendColorToESPThread.start()
    except esp32serial.serial.SerialException:
        messagebox.showerror("Error", "Iluminação não conectada!")


def stopAll():
    try:
        esp32.close()
        recognitioncv.stop()
    except AttributeError:
        messagebox.showerror("Error", "Não é possível utilizar esse comando no momento!")

buttoncomm = tk.Button(root, text="Init", command=initComm)
buttoncomm.place(x=10, y=10)
buttonstop = tk.Button(root, text="Stop", command=stopAll)
buttonstop.place(x=50, y=10)
root.mainloop()
