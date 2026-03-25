import tkinter as tk
from tkinter import messagebox
import requests

URL = "http://127.0.0.1:8000/area"

def calcular_area():
    base = entry_base.get().strip()
    altura = entry_altura.get().strip()

    try:
        base = float(base)
        altura = float(altura)
    except ValueError:
        messagebox.showerror("Erro", "Digite números válidos.")
        return

    try:
        response = requests.get(URL, params={"base": base, "altura": altura})

        if response.status_code == 200:
            data = response.json()
            label_resultado.config(text=f"Área: {data['area']}")
        else:
            messagebox.showerror("Erro", response.json()["detail"])

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "Servidor não está rodando.")

# Interface
root = tk.Tk()
root.title("Calculadora com API")
root.geometry("300x200")

tk.Label(root, text="Base:").pack(pady=(10, 0))
entry_base = tk.Entry(root)
entry_base.pack()

tk.Label(root, text="Altura:").pack(pady=(10, 0))
entry_altura = tk.Entry(root)
entry_altura.pack()

tk.Button(root, text="Calcular", command=calcular_area).pack(pady=15)

label_resultado = tk.Label(root, text="Área: --")
label_resultado.pack()

root.mainloop()