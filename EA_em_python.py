import ccxt
import ccxt.base
import ccxt.exchange as exchange
import ccxt.base.utils as utils
import ccxt.exchange.utils as exchange_utils
import ccxt.base.exceptions as base_exceptions
import ccxt.exchange.exceptions as exchange_exceptions
import ccxt.base.utils.json as json_utils
import ccxt.exchange.utils.json as json_exchange_utils
import ccxt.base.utils.crypto as crypto_utils
import ccxt.exchange.utils.crypto as crypto_exchange_utils
import ccxt.base.utils.string as string_utils
import ccxt.exchange.utils.string as string_exchange_utils
import ccxt.base.utils.datetime as datetime_utils
import ccxt.exchange.utils.datetime as datetime_exchange_utils
import ccxt.base.utils.number as number_utils
import ccxt.exchange.utils.number as number_exchange_utils
import ccxt.base.utils.array as array_utils
import ccxt.exchange.utils.array as array_exchange_utils
import ccxt.base.utils.object as object_utils
import ccxt.exchange.utils.object as object_exchange_utils
import ccxt.base.utils.function as function_utils
import ccxt.exchange.utils.function as function_exchange_utils
import ccxt.base.utils.collection as collection_utils
import ccxt.exchange.utils.collection as collection_exchange_utils
import ccxt.base.utils.map as map_utils
import ccxt.exchange.utils.map as map_exchange_utils
import ccxt.base.utils.set as set_utils
import ccxt.exchange.utils.set as set_exchange_utils
import ccxt.base.utils.list as list_utils
import ccxt.exchange.utils.list as list_exchange_utils
import ccxt.base.utils.tuple as tuple_utils
import ccxt.exchange.utils.tuple as tuple_exchange_utils
import ccxt.base.utils.dict as dict_utils
import ccxt.exchange.utils.dict as dict_exchange_utils
import ccxt.base.utils.parse as parse_utils
import ccxt.exchange.utils.parse as parse_exchange_utils
import ccxt.base.utils.stringify as stringify_utils
import ccxt.exchange.utils.stringify as stringify_exchange_utils
import ccxt.base.utils.jsonify as jsonify_utils
import ccxt.exchange.utils.jsonify as jsonify_exchange_utils

import requests
import os
import json
import datetime
import threading
import time

# Configurações da corretora
CORRETORA_FXPRO = 'FXPRO'
CORRETORA_XM = 'XM'
CORRETORA_FXPRO_API_KEY = 'SEU_API_KEY_FXPRO'
CORRETORA_FXPRO_SECRET = 'SEU_SECRET_FXPRO'
CORRETORA_XM_API_KEY = 'SEU_API_KEY_XM'
CORRETORA_XM_SECRET = 'SEU_SECRET_XM'

# Configurações do sinal
SINAL_TYPE = 'buy'
LOTE_SIZE = 0.1
TP1 = 2778.0
TP2 = 2779.5
TP3 = 2784.0
SL = 2770.0

# Configurações do Telegram
TELEGRAM_API_KEY = '7689407708:AAFE3orCUoMQUtJ_jKP7hr46oaviz3UXiCI'
TELEGRAM_CHAT_ID = '-1002251202547'

# Configurações do MT4
MT4_SYMBOL = 'XAUUSD'

class SinalEA:
    def __init__(self):
        self.corretora = None
        self.api_key = None
        self.api_secret = None
        self Mt4_symbol = None

    def conectar_corretora(self, corretora):
        if corretora == CORRETORA_FXPRO:
            self.corretora = ccxt.fxtx()
            self.api_key = CORRETORA_FXPRO_API_KEY
            self.api_secret = CORRETORA_FXPRO_SECRET
        elif corretora == CORRETORA_XM:
            self.corretora = ccxt.xm()
            self.api_key = CORRETORA_XM_API_KEY
            self.api_secret = CORRETORA_XM_SECRET
        else:
            raise ValueError('Corretora não suportada')

    def verificar_sinal(self):
        # Verificar se o preço está dentro do rango de TP1, TP2 e TP3
        preço = self.corretora.fetch_price(self.Mt4_symbol)
        if preço >= TP1 and preço <= TP2:
            # Verificar se o preço está fora do rango de SL
            if preço < SL:
                return True
        return False

    def enviar_sinal(self):
        # Enviar o sinal para o Telegram
        url = f'https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage'
        headers = {'Content-Type': 'application/json'}
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': f'SIGNAL ALERT\n\nBUY {self.Mt4_symbol} {TP1}\nTP2: {TP2}\nTP3: {TP3}\nSL: {SL}'
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print('Sinal enviado com sucesso')
        else:
            print('Erro ao enviar sinal')

    def rodar(self):
        # Rodar o EA em segundo plano
        while True:
            if self.verificar_sinal():
                self.enviar_sinal()
            time.sleep(60)

# Criar uma instância do SinalEA
sinal_eara = SinalEA()

# Conectar a corretora
sinal_eara.conectar_corretora(CORRETORA_FXPRO)

# Verificar se o preço está dentro do rango de TP1, TP2 e TP3
if sinal_eara.verificar_sinal():
    # Enviar o sinal para o Telegram
    sinal_eara.enviar_sinal()

# Rodar o EA
sinal_eara.rodar()