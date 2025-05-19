import os
import subprocess
import socket
import random
import ctypes
from tkinter import Tk, Label, Button, messagebox
import webbrowser

def get_adapter_name():
    output = subprocess.check_output("netsh interface show interface", shell=True).decode()
    for line in output.splitlines():
        if "Connected" in line and "Dedicated" in line:
            return line.split()[-1]
    return None

def get_username():
    return os.getlogin()

def generate_random_ip():
    base_ip = "192.168.15."
    while True:
        last_octet = random.randint(100, 200)
        ip = base_ip + str(last_octet)
        if not ip_in_use(ip):
            return ip

def ip_in_use(ip):
    try:
        socket.inet_aton(ip)
        result = os.system(f"ping -n 1 -w 100 {ip} >nul")
        return result == 0
    except socket.error:
        return True

def set_static_ip():
    adapter = get_adapter_name()
    if not adapter:
        messagebox.showerror("Error", "No network adapter found!")
        return

    ip = generate_random_ip()
    subprocess.call(f'netsh interface ip set address name="{adapter}" static {ip} 255.255.255.0 192.168.15.1', shell=True)
    subprocess.call(f'netsh interface ip set dns name="{adapter}" static 10.4.0.14', shell=True)
    subprocess.call(f'netsh interface ip add dns name="{adapter}" 8.8.8.8 index=2', shell=True)
    webbrowser.open("gmail.com")

def set_dynamic_ip():
    adapter = get_adapter_name()
    if not adapter:
        messagebox.showerror("Error", "No network adapter found!")
        return

    output = subprocess.getoutput(f'netsh interface ip show config name="{adapter}"')
    if "DHCP enabled: Yes" in output:
        if messagebox.askyesno("Info", "Your system is already on dynamic. Do you want to switch to static?"):
            set_static_ip()
        return

    subprocess.call(f'netsh interface ip set address name="{adapter}" source=dhcp', shell=True)
    subprocess.call(f'netsh interface ip set dnsservers name="{adapter}" source=dhcp', shell=True)
    messagebox.showinfo("Success", "You are now on dynamic IP.")

def exit_tool():
    root.destroy()

# GUI Setup
root = Tk()
root.title("Tranter IT Network Config Tool by Jesse")
root.geometry("600x400")
root.config(bg="#1c1c1c")

Label(root, text=f"Hi {get_username()}, Welcome to Tranter IT Network Config Tool by Jesse!\nNow you can automatically switch between static and dynamic by yourself!!!", 
      wraplength=550, justify="center", bg="#1c1c1c", fg="white", font=("Segoe UI", 12)).pack(pady=20)

Button(root, text="Switch to Static", command=set_static_ip, bg="#ffcc00", fg="black", font=("Segoe UI", 12), width=25).pack(pady=10)
Button(root, text="Switch to Dynamic", command=set_dynamic_ip, bg="#00cc66", fg="white", font=("Segoe UI", 12), width=25).pack(pady=10)
Button(root, text="Exit", command=exit_tool, bg="red", fg="white", font=("Segoe UI", 12), width=25).pack(pady=10)

root.mainloop()