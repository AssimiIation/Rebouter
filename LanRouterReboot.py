from tkinter import *
from threading import *
import xmlrpc.client

class MessageBox:
    def __init__(self, container):
        self.widget = Text(container, font="Raleway", height=20, width=50, state=DISABLED, wrap='word', borderwidth=2)

    def display_message(self, text):
        self.widget.config(state=NORMAL)
        message = text + "\n"
        self.widget.insert(END, message)
        self.widget.config(state=DISABLED)

def reboot_router():
    reboot_button.config(state='disabled')
    try:
        msg_window.display_message("Rebooting...")
        result = client.reboot_router(10)
        if result == "OK":
            msg_window.display_message("Router rebooted successfully!")
        else:
            msg_window.display_message("Error rebooting router. Please try again")
        reboot_button.config(state='normal')
    except xmlrpc.client.Fault as error:
        msg_window.display_message(f"Call to server failed with xml-rpc fault: {error}")
    except ConnectionError as error:
        msg_window.display_message(f"Connection error (Is the server running?): {error}")
    reboot_button.config(state='normal')

def thread_reboot():
    #Create a thread
    t1 = Thread(target=reboot_router)
    t1.start()

server_ip = "192.168.1.163"
server_port = '6870'

root = Tk()
root.title("LAN Router Reboot")
root.resizable(False, False)
root.geometry("520x460")

msg_window = MessageBox(root)
msg_window.widget.pack(pady=10)

button_frame = Frame(root)
button_frame.pack()

reboot_button = Button(button_frame, text="Reboot Router", font="Raleway", command=thread_reboot)
reboot_button.grid(column=0, row=0)

exit_button = Button(button_frame, text="Exit", font="Raleway", command=root.quit)
exit_button.grid(column=1, row=0)

client = xmlrpc.client.ServerProxy(f'http://{server_ip}:{server_port}')

root.mainloop()