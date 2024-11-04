from flask import Flask, request
import telegram
import MetaTrader5 as mt5

app = Flask(__name__)

# Configurações do MetaTrader
mt5.initialize()
account = 87798184  # Substitua pelo seu número de conta
password = "V*Yw2lEb"  # Substitua pela sua senha
server = "MetaQuotes-Demo"  # Substitua pelo seu servidor
mt5.login(account, password, server)

# Configurações do Telegram
bot_token = "7689407708:AAFE3orCUoMQUtJ_jKP7hr46oaviz3UXiCI"
bot = telegram.Bot(token=bot_token)

@app.route('/endpoint', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(), bot)
    
    if update.message:
        chat_id = update.message.chat.id
        command = update.message.text.lower()

        if 'buy' in command:
            place_order('buy')
            bot.send_message(chat_id=chat_id, text="Ordem de compra executada")
        elif 'sell' in command:
            place_order('sell')
            bot.send_message(chat_id=chat_id, text="Ordem de venda executada")
    
    return 'ok'

def place_order(order_type):
    symbol = "YOUR_SYMBOL"  # Substitua pelo símbolo desejado
    lot = 0.1  # Volume de cada ordem

    if order_type == 'buy':
        order = mt5.OrderSendRequest(
            action=mt5.TRADE_ACTION_DEAL,
            symbol=symbol,
            volume=lot,
            type=mt5.ORDER_TYPE_BUY,
            price=mt5.symbol_info_tick(symbol).ask,
            slippage=10,
            magic=234000,
            comment="Telegram Trade",
            type_filling=mt5.ORDER_FILLING_RETURN,
        )
    elif order_type == 'sell':
        order = mt5.OrderSendRequest(
            action=mt5.TRADE_ACTION_DEAL,
            symbol=symbol,
            volume=lot,
            type=mt5.ORDER_TYPE_SELL,
            price=mt5.symbol_info_tick(symbol).bid,
            slippage=10,
            magic=234000,
            comment="Telegram Trade",
            type_filling=mt5.ORDER_FILLING_RETURN,
        )

    result = mt5.order_send(order)
    print(result)

if __name__ == '__main__':
    app.run(port=8443)
