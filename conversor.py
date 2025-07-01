import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading

class ConversorMonedas:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("💱 Conversor de Monedas")
        self.ventana.geometry("400x300")

        self.monedas = ["USD", "EUR", "MXN", "JPY", "GBP"]

        # Widgets
        tk.Label(ventana, text="Cantidad:").pack(pady=5)
        self.entry_monto = tk.Entry(ventana)
        self.entry_monto.pack()

        tk.Label(ventana, text="De:").pack()
        self.combo_de = ttk.Combobox(ventana, values=self.monedas)
        self.combo_de.pack()
        self.combo_de.set("USD")

        tk.Label(ventana, text="A:").pack()
        self.combo_a = ttk.Combobox(ventana, values=self.monedas)
        self.combo_a.pack()
        self.combo_a.set("MXN")

        tk.Button(ventana, text="Convertir", command=self.iniciar_conversion).pack(pady=10)
        self.label_resultado = tk.Label(ventana, text="", font=("Arial", 14))
        self.label_resultado.pack()

    def iniciar_conversion(self):
        threading.Thread(target=self.convertir).start()

    def convertir(self):
        try:
            self.label_resultado.config(text="Convirtiendo...")
            cantidad = float(self.entry_monto.get())
            moneda_origen = self.combo_de.get()
            moneda_destino = self.combo_a.get()

            url = f"https://open.er-api.com/v6/latest/{moneda_origen}"
            respuesta = requests.get(url, timeout=5)
            data = respuesta.json()

            if data["result"] == "success" and moneda_destino in data["rates"]:
                tasa = data["rates"][moneda_destino]
                resultado = cantidad * tasa
                texto = f"{cantidad:.2f} {moneda_origen} = {resultado:.2f} {moneda_destino}"
            else:
                texto = "❌ No se pudo obtener el tipo de cambio."

            self.label_resultado.config(text=texto)

        except requests.exceptions.Timeout:
            self.label_resultado.config(text="⏱ Timeout: conexión muy lenta")
            messagebox.showerror("Timeout", "La API tardó demasiado en responder.")
        except Exception as e:
            self.label_resultado.config(text="⚠️ Error inesperado")
            messagebox.showerror("Error", str(e))

# Ejecutar
if __name__ == "__main__":
    root = tk.Tk()
    app = ConversorMonedas(root)
    root.mainloop()
