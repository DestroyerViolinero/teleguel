"""
	Este script procesa los mensajes del Bot Bitacora de Telegram
	para llevar registro sobre fallas presentadas en el sistema MARCE
"""
import time
import datetime
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
import Generar_Reporte as GRep

def actions(msg):
	"""
		Ejecuta diferentes metodos segun el tipo de contenido del mensaje
	"""
	try:
		content_type, chat_type, chat_id = telepot.glance(msg)

		if content_type == 'text':
			processText(msg)

		else:
			telegram_bot.sendMessage (chat_id, "Solo me gusta leer, envia mensajes en texto.")

	except Exception as e:
		print("Error actions, ", e)

def getIdentity(msg):
	"""
		Retorna la identida del usuario, mensaje, fecha del mensaje, y chat_id
	"""
	try:
		chat 			= msg['chat']
		date 			= msg['date']
		chat_id 		= chat['id']
		comando 		= msg["text"]
		firstName 		= chat['first_name']

		if 'last_name' in chat:
			fullName 	= f'{firstName} {chat["last_name"]}'
		else:
			fullName	= firstName
		
		identity 		= f'{fullName} {str(chat_id)}'

		return identity, comando, chat_id, date
	except Exception as e:
		print("Imposible identificar", e)
		return "Indefinido"

def processText(msg):
	try:
		"""
			Valida existencia del usuario en el registro, si el usuario existe, 
			procede a decidir sobre los comandos enviados por el usuario existente
		"""
		identity, comando, chat_id, date = getIdentity(msg)

		file			=	open("Registro.txt","r")
		Registro		=	file.read()
		file.close()

		if 'Marce2021' in comando:
			# Crear Registro
			MESSAGE		=	"¡Ya estas registrado!"
			
			with open("Registro.txt","a+") as file:
				file.write(f'\n{str(identity)}')
				file.close()

			telegram_bot.sendMessage (chat_id, MESSAGE)
		
		elif identity in Registro:
			# Procesar comandos para usuario existente
			
			if 'reply_to_message' in msg:
				
				# Continuar el proceso de reporte cuando el usuario esta respondiendo un mensaje
				
				replyTo = msg['reply_to_message']['text']
				if 'Digite Otro reporte:' in replyTo:
					markup 	=	ForceReply(selective=False)
					MESSAGE = f'{comando} Canaleta='
					telegram_bot.sendMessage(chat_id, MESSAGE, reply_markup=markup)

				elif 'Canaleta=' in replyTo:
					markup 	=	ForceReply(selective=False)
					text	=	replyTo.replace('=', '')
					MESSAGE = f'{text} {comando} Responsable:'
					telegram_bot.sendMessage(chat_id, MESSAGE, reply_markup=markup)

				elif 'Responsable:'in replyTo:
					text = replyTo.replace(':', '')
					text = f'{text} {comando} guardar?'
				
					keyboard = InlineKeyboardMarkup(
						inline_keyboard=[
									[
										InlineKeyboardButton(text='Guardar', callback_data="guardar?"),
										InlineKeyboardButton(text='Cancelar', callback_data=' ')
									]
									])

					telegram_bot.sendMessage(chat_id, text, reply_markup=keyboard)
					print(text)

			elif 'Generar Reporte' in comando:
				comando = comando.replace('Generar Reporte ','')
				comando = comando.split(' ')
				start, end 	= GRep.requestRange(comando[0], comando[1])
				data 		= GRep.getFilteredData(start, end)
				nameReport  = f'Reporte_{str(datetime.datetime.now())[0:11]}.xlsx'
				GRep.createNewReport(nameReport)
				GRep.copyData(nameReport, data)
				with open(nameReport, 'rb') as file:
					telegram_bot.sendDocument(chat_id=chat_id, document=file)
			else:
				# Si el mensaje no esta respondiendo a mensajes especificos, se procede a preguntar por el tipo de fallo
				startProcess(chat_id)
				
		else:
			# Usuario no esta registrado
			message=(f'Hola soy Marce, '
				'Un bot creado para brindar todo tipo de informacion acerca de nuestra planta, '
				'usted no esta registrado, comuniquese con el area de soporte para que le indiquen como hacer su registro')

			telegram_bot.sendMessage (chat_id, message)
	except Exception as e:
		print('Error en processText,', e)

def startProcess(chat_id):
	"""
		Despliega Menu principal al usuario
	"""
	keyboard = InlineKeyboardMarkup(
	inline_keyboard=[
		[InlineKeyboardButton(text='Canaleta', callback_data='falloCanaleta ')]
		,[InlineKeyboardButton(text='Tarea', callback_data='Tarea ')]
		])
	telegram_bot.sendMessage(chat_id, 'Que tipo de reporte desea hacer Canaleta o General?', reply_markup=keyboard)

def on_callback_query(msg):
	"""
		Procesa los Callback disparados por los botones
	"""
	try:
		query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
		telegram_bot.answerCallbackQuery(query_id, text='Procesando')
		keyboard = []

		if query_data =="falloCanaleta ":
			
			keyboard = InlineKeyboardMarkup(
				inline_keyboard=[
					[
						InlineKeyboardButton(text='Fallo Aplicativo', callback_data='Fallo Aplicativo Canaleta: '),
						InlineKeyboardButton(text='Pantalla no corresponde', callback_data='Pantalla no corresponde Canaleta: ')
					],
					[
						InlineKeyboardButton(text='Fallo Electrico', callback_data='Fallo Electrico Canaleta: '),
						InlineKeyboardButton(text='Asignacion no corresponde', callback_data='Asignacion no corresponde Canaleta: ')
					],
					[
						InlineKeyboardButton(text='Fallo de Red', callback_data='Fallo de Red Canaleta: '),
						InlineKeyboardButton(text='Manipulacion Inadecuada', callback_data='Manipulacion Inadecuada Canaleta: ')
					],
					[
						InlineKeyboardButton(text='Fallo de Mouse', callback_data='Fallo de Mouse Canaleta: '),
						InlineKeyboardButton(text='Otro...', callback_data='Otro: ')
					],
					[
						InlineKeyboardButton(text='Todo OK', callback_data='Todo OK Canaleta: ')
					]])

			telegram_bot.sendMessage(chat_id, 'Seleccione tipo de fallo:', reply_markup=keyboard)
		
		elif query_data =="Tarea ":

			telegram_bot.sendMessage(chat_id, 'Digite la tarea que desea realizar')
		
		elif 'Otro' in query_data:
			markup 		= ForceReply(selective=False)
			telegram_bot.sendMessage(chat_id, 'Digite Otro reporte: ', reply_markup=markup)

		elif 'Canaleta:' in query_data : 
			markup 		= ForceReply(selective=False)
			query_data 	= query_data.replace(':','= ')
			telegram_bot.sendMessage(chat_id, query_data, reply_markup=markup)

		elif 'guardar?' in query_data :
			query_data = msg['message']['text']
			query_data 	= query_data.replace(' guardar?','')
			done, message		= saveReport(query_data,msg['message'])
			telegram_bot.sendMessage(chat_id, message)
			query_data	= ''
			startProcess(chat_id)
	except Exception as e:
		print("Error on_callback_query, ", e)

def saveReport(data,msg):
	"""
		Guarda nuevo registro en reports.csv
	"""
	try:
		done 					= False
		Fecha					= str(datetime.datetime.now())
		report, data 			= data.split(" Canaleta ")
		location, responsable 	= data.split(" Responsable ")
		data					= getIdentity(msg)
		report_to_save			= f'\n{location},{report},{responsable},{data[0]},{data[3]}'
		message_to_user			= f'Reporte Guardado correctamente\nCanaleta: {location}\nReporte: {report}\nResponsable: {responsable}\nReportado por: {data[0]}\n'
		
		

		with open("reports.csv","a+") as reports:
			reports.write(report_to_save)
			done = True

	except Exception as e:
		print(e)
		message_to_user 		= 'No se ha podido guardar el reporte'
		

	finally:
		return done, message_to_user

def startMessage():
	"""
		Envia mensaje a todos los usuarios registrados cuando se inicializa por primera vez el codigo
	"""
	try:
		MESSAGE 				= "Bitacora disponible"

		with open("Registro.txt","r") as USERS_FILE:
			USERS				=	USERS_FILE.read().split("\n")
			USERS_FILE.close()

		for row in USERS:
			idUser		= row.split(" ")[-1]
			if idUser != "":
				telegram_bot.sendMessage (idUser, MESSAGE)
	except Exception as e:
		print('Error startMessage, ', e)

if __name__ == "__main__":
	try:
		OWNER_BOT_ID 	= 1075028126
		MESSAGE 		= "Bitacora-Inicializada"
		telegram_bot 	= telepot.Bot('1702388557:AAH-K3gtzvMOI3cqV_8SKzhSqzM7BFr4VV0')
		telegram_bot.setWebhook ()
		telegram_bot.sendMessage ( OWNER_BOT_ID, MESSAGE )
		startMessage()
		print ("Marce-Telegram")
		MessageLoop(telegram_bot, {'chat': actions,'callback_query': on_callback_query }).run_as_thread()
		while 1:
			# Mantiene el programa en ejecucion
			time.sleep(10)
	except KeyboardInterrupt:
		print("Interrupcion por Teclado")

	except Exception as e:
		print("Error en principal: ", e)
