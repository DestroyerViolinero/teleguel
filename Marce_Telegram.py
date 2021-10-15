import time, datetime
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
now = datetime.datetime.now()


def acciones(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	if content_type == 'text':
		Texto(msg)
	elif content_type == 'voice':
		message="Aun no comprendo audio pero mi padre trabaja en ello"
		telegram_bot.sendMessage (chat_id, message)
		print(content_type, chat_type, chat_id)
	elif content_type == 'photo':
		message="No es una entrada valida"
		telegram_bot.sendMessage (chat_id, message)
		print(content_type, chat_type, chat_id)
		print(msg['caption'])
	else:
		print(content_type, chat_type, chat_id)
def Texto(msg):
	chat_id = msg['chat']['id']
	comando = msg['text']
	print ('Recibi: %s' % comando)
	identidad = msg['chat']['first_name']
	if 'last_name' in msg['chat']:
		identidad = identidad+" "+msg['chat']['last_name']
	identidad = identidad+" "+str(chat_id)
	print ("De: "+identidad)
	d=str(identidad)
	archivo=open("Registro.txt","r")
	Registro=archivo.read()
	archivo.close()
	if 'Marce2021' in comando:
		archivo=open("Registro.txt","r")
		data=archivo.read()
		archivo.close()
		archivo=open("Registro.txt","w")
		archivo.write(str(data)+"\n"+str(identidad))
		archivo.close()
		archivo=open("Registro.txt","r")
		Registro=archivo.read().split("\n")
		archivo.close()
		message="¡ya estas registrado!"
		telegram_bot.sendMessage (chat_id, message)
	elif d in Registro:
		if 'reply_to_message' in msg:
			if 'Canaleta='in msg['reply_to_message']['text']:
				markup = ForceReply(selective=False)
				texto=msg['reply_to_message']['text'].replace('=', ' ')
				telegram_bot.sendMessage(chat_id, texto+' '+msg['text']+' Responsable:', reply_markup=markup)
			if 'Responsable:'in msg['reply_to_message']['text']:
				texto = msg['reply_to_message']['text'].replace(':', ' ')
				texto = texto+' '+msg['text']
				keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Guardar', callback_data=texto+' guardar?'),InlineKeyboardButton(text='Cancelar', callback_data=' ')]])
				telegram_bot.sendMessage(chat_id, texto+' guardar?', reply_markup=keyboard)

		else:
			keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Canaleta', callback_data='falloCanaleta ')],[InlineKeyboardButton(text='General', callback_data='falloGeneral ')]])
			telegram_bot.sendMessage(chat_id, 'Que tipo de reporte desea hacer Canaleta o General?', reply_markup=keyboard)
			
    
	else:
		message="Hola soy Marce, Un bot creado para brindar todo tipo de informacion acerca de nuestra planta usted no esta registrado, comuniquese con el area de soporte para que le indiquen como hacer su registro "
		telegram_bot.sendMessage (chat_id, message)

def on_callback_query(msg):
	query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
	telegram_bot.answerCallbackQuery(query_id, text='Procesando')
	keyboard = []
	if query_data =="falloCanaleta ":
		keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Fallo Programa', callback_data='Fallo Programa Canaleta: '),InlineKeyboardButton(text='Pantalla no corresponde', callback_data='Pantalla no corresponde Canaleta: ')],[InlineKeyboardButton(text='Fallo Electrico', callback_data='Fallo Electrico Canaleta: '),InlineKeyboardButton(text='Asignacion no corresponde', callback_data='Asignacion no corresponde Canaleta: ')],[InlineKeyboardButton(text='Fallo de Red', callback_data='Fallo de Red Canaleta: '),InlineKeyboardButton(text='Mala Operacion', callback_data='Mala Operacion Canaleta: ')],[InlineKeyboardButton(text='Todo OK', callback_data='Todo OK Canaleta: ')]])
		telegram_bot.sendMessage(chat_id, 'TIPO DE FALLO ?', reply_markup=keyboard)
	
	elif query_data =="falloGeneral ":
		telegram_bot.sendMessage(chat_id, 'Usted es una loca')
		
	elif 'Canaleta:' in query_data : 	
		markup = ForceReply(selective=False)
		query_data = query_data.replace(':','= ')
		telegram_bot.sendMessage(chat_id, query_data, reply_markup=markup)
	
	elif ' guardar?' in query_data :#//aqui gaurda el texto
		query_data = query_data.replace(' guardar?','')
		telegram_bot.sendMessage(chat_id, 'Su reprte ha sido guardado')
		query_data = ''

	

telegram_bot = telepot.Bot('1702388557:AAH-K3gtzvMOI3cqV_8SKzhSqzM7BFr4VV0')
telegram_bot.setWebhook ()
telegram_bot.sendMessage ( 1075028126, "Marce-Telegram")
print ("Marce-Telegram")
archivo=open("Registro.txt","r")
Registro=archivo.read().split("\n")
archivo.close()
for i in Registro:
	i= i.split(" ")
	j= i[-1]
	if j!="":
		telegram_bot.sendMessage (j, "Marce-Telegram")
MessageLoop(telegram_bot, {'chat': acciones,'callback_query': on_callback_query }).run_as_thread()


while 1:	
	time.sleep(10)
	
