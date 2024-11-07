import tkinter as tk
from tkinter import ttk

class Sinal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Sinal')

        # Configurações do sinal
        self.sinal_type = tk.StringVar()
        self.sinal_type.set('buy')

        self.lote_size = tk.StringVar()
        self.lote_size.set('0.1')

        # Tipo de sinal
        self.tipo_sinal_label = ttk.Label(self.root, text='Tipo de sinal:')
        self.tipo_sinal_label.grid(row=0, column=0)
        self.tipo_sinal = ttk.OptionMenu(self.root, self.sinal_type, 'buy', 'sell')
        self.tipo_sinal.grid(row=0, column=1)

        # Lote size
        self.lote_size_label = ttk.Label(self.root, text='Lote size:')
        self.lote_size_label.grid(row=1, column=0)
        self.lote_size = ttk.OptionMenu(self.root, self.lote_size, '0.1', '0.5', '1.0')
        self.lote_size.grid(row=1, column=1)

        # Botão para enviar o sinal
        self.enviar_sinal_button = ttk.Button(self.root, text='Enviar sinal', command=self.enviar_sinal)
        self.enviar_sinal_button.grid(row=2, column=0, columnspan=2)

    def enviar_sinal(self):
        # Enviar o sinal para o EA
        # Você precisa substituir os valores por seus próprios
        sinal_eara = SinalEA()
        sinal_eara.corretora = CORRETORA_FXPRO
        sinal_eara.api_key = CORRETORA_FXPRO_API_KEY
        sinal_eara.api_secret = CORRETORA_FXPRO_SECRET
        sinal_eara.Mt4_symbol = 'XAUUSD'

        sinal_eara.sinal_type = self.sinal_type.get()
        sinal_eara.lote_size = self.lote_size.get()

        if sinal_eara.sinal_type == 'buy':
            sinal_eara.Mt4_symbol = 'XAUUSD'
            sinal_eara.corretora.fetch_price(sinal_eara.Mt4_symbol)
        else:
            sinal_eara.Mt4_symbol = 'XAUUSD'
            sinal_eara.corretora.fetch_price(sinal_eara.Mt4_symbol)

        sinal_eara.enviar_sinal()

    def run(self):
        self.root.mainloop()

sinal = Sinal()
sinal.run()