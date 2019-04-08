import tkinter as tk

class ClientGUI:

    def __init__(self, client):
        self.top = tk.Tk()
        self.top.title("AnonChat")
        self.frame = self.create_frame()
        self.messages = self.message_area()
        self.entry_area()
        self.client = client
        self.top.protocol("WM_DELETE_WINDOW", self.client.on_closing)


    def create_frame(self):
        container = tk.Frame(self.top)
        scrollbar = tk.Scrollbar(container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        container.pack()
        return (container, scrollbar)


    def message_area(self):
        message = tk.StringVar()
        message.set("")
        message_box = tk.Listbox(self.frame[0], height=25, width=75, yscrollcommand=self.frame[1].set)
        message_box.configure(fg="red")
        message_box.configure(background="black")
        message_box.pack(side=tk.LEFT, fill=tk.BOTH)
        message_box.pack()
        return (message, message_box)


    def entry_area(self):
        entry_field = tk.Entry(self.top, textvariable=self.messages[0], width=50)
        entry_field.bind("<Return>", self.send_message)
        entry_field.pack()
        send_button = tk.Button(self.top, text="Send", command=self.send_message)
        send_button.pack()


    def mainloop(self):
        self.top.mainloop()


    def insert_message(self, message):
        self.messages[1].insert(tk.END, message)


    def set_message(self, message):
        self.messages[0].set(message)
    
    
    def get_message(self):
        return self.messages[0].get()


    def send_message(self, event):
        self.client.send(event)
    
    


