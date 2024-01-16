from keras.models import load_model
from tkinter import *
import tkinter as tk
import subprocess
from PIL import Image
import numpy as np

model = load_model('mnist4.h5')

def predict_digit(img):
    # изменение рзмера изобржений на 28x28
    img = img.resize((28,28))
    # конвертируем rgb в grayscale
    img = img.convert('L')
    img.save("/Users/iisuos/Digit Recognize/screenshot2.png")
    img = np.array(img)
    # изменение размерности для поддержки модели ввода и нормализации
    img = img.reshape(1,28,28,1)
    img = img/255.0
    # предстказание цифры
    res = model.predict([img])
    res = res[0]
    return np.argmax(res), max(res)
    
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.x = self.y = 0
        
        # Создание элементов
        self.canvas = tk.Canvas(self, width=300, height=300, bg = "black", cursor="cross")
        self.label = tk.Label(self, text="Думаю..", font=("Helvetica", 48))
        self.classify_btn = tk.Button(self, text = "Распознать", command =         self.classify_handwriting) 
        self.button_clear = tk.Button(self, text = "Очистить", command = self.clear_all)
        
        # Сетка окна
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1,pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)
        
        # self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)
        
    def clear_all(self):
        self.canvas.delete("all")
    def capture_screenshot(x, y, width, height):
        # Формируем команду для снятия скриншота указанной области
        command = ["screencapture", "-R{},{},{},{}".format(x, y, width, height), "-tpng", "/Users/iisuos/Digit Recognize/screenshot.png"]
        
        # Запускаем команду с помощью subprocess
        subprocess.run(command, check=True)
        
        # Открываем скриншот с помощью PIL
        
        screenshot = Image.open("/Users/iisuos/Digit Recognize/screenshot.png")
        cropped_image = screenshot.crop((50, 50, 50, 50))
        cropped_image.save("/Users/iisuos/Digit Recognize/screenshot.png")
        return screenshot   
     
    def classify_handwriting(self):
        x, y, width, height = self.canvas.winfo_rootx(), self.canvas.winfo_rooty(), self.canvas.winfo_width(), self.canvas.winfo_height()
        # rect = (x, y, x + width, y + height)  # получение координат холста
        # screenshot = pyautogui.screenshot(region=rect)
        # im = Image.fromarray(screenshot)
        command = ["screencapture", "-R{},{},{},{}".format(x, y, width, height), "-tpng", "/Users/iisuos/Digit Recognize/screenshot.png"]
        
        # Запускаем команду с помощью subprocess
        subprocess.run(command, check=True)
        
        # Открываем скриншот с помощью PIL
        # im = Image.open("/Users/iisuos/Digit Recognize/Снимок экрана 2023-11-24 в 12.27.52.png")
       
        im = Image.open("/Users/iisuos/Digit Recognize/screenshot.png")
        
        # im = Image.open("/Users/iisuos/Digit Recognize/Снимок экрана 2023-11-24 в 08.28.24.png")
        digit, acc = predict_digit(im)
        self.label.configure(text= str(digit)+', '+ str(int(acc*100))+'%')
        
    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=8
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='white', outline='')


app = App()
mainloop()
