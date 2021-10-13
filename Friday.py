import speech_recognition as sr
from time import sleep
from gtts import gTTS
import playsound, os, _sqlite3
import skillsFriday as skills


def takeVoiceInput(consoleShow):
	while True:
		r = sr.Recognizer()
		with sr.Microphone() as source:
			r.adjust_for_ambient_noise(source)
			print(consoleShow)
			audio = r.listen(source)
			try:
				voiceInput = r.recognize_google(audio)
				return voiceInput.lower()
			except Exception:
				pass

def wakeWordActivation(wakeword):
	while True:
		voiceInput = takeVoiceInput('Start Speaking...')
		if voiceInput.find(wakeword) >= 0:
			index = voiceInput.find(wakeword)+7
			tempVar = voiceInput[index::]
			return tempVar.lower()

def speak(text):
	tts = gTTS(text=text, lang='en')
	filename = 'voice.mp3'
	tts.save(filename)
	playsound.playsound(filename)
	os.remove(filename)

def main():
	audio = wakeWordActivation('friday')
	print(audio)
	with _sqlite3.connect("Response.db") as database:
		cursor = database.cursor()

	findUser = ("SELECT * FROM responses WHERE Question = ?")
	cursor.execute(findUser,[(audio)])

	
	if audio.find('play') >= 0:
		index = audio.find('play')+5
		tempVar = audio[index::]
		skills.playSongs(tempVar)
		speak('Playing '+tempVar)

	elif audio.find('open') >= 0:
		index = audio.find('open')+5
		tempVar = audio[index::]
		skills.openWebsite(tempVar)
		speak("Opening "+tempVar)

	elif audio.find('time') >= 0:
		hours, mins, half = skills.getTime()
		speak('The time is ' +hours+ ' ' +mins+ ' ' +half)

	elif audio.find('date') >= 0:
		day, date, month, year = skills.getDate()	
		speak('Today is '+day+', the '+date+' of '+month+' '+year)

	elif audio.find('weather') >= 0:
		currentTemp = skills.getWeather()
		speak('The current temperature at your location is ' +str(currentTemp)+ ' fahrenheit')

	elif audio.find('news') >= 0:
		result = skills.getNews()
		speak('Here is your daily briefings')
		for i in result:
			speak(i)
		speak('Thats it for todays briefings')

	elif audio.find('stock') >= 0:
		speak('Can you please tell me the code name for your company')
		stockName = takeVoiceInput('Company\'s NASDAQ code...')
		stockPrice = skills.getStockPrices(stockName)
		speak('The curren stock value for ' +stockName+ " is " +str(stockPrice))

	elif (audio.find('what') >= 0 or audio.find('who') >= 0 or audio.find('tell me about') >= 0):
		if audio.find('what') >= 0:
			index = audio.find('what')+5
			tempVar = audio[index::]
			result = skills.getResults(tempVar)
			speak(result)
		elif audio.find('who') >= 0:
			index = audio.find('who')+4
			tempVar = audio[index::]
			result = skills.getResults(tempVar)
			speak(result)
		else:
			index = audio.find('tell me about')+14
			tempVar = audio[index::]
			result = skills.getResults(tempVar)
			speak(result)		

	elif cursor.fetchall():
		getUser = ("SELECT * FROM responses WHERE Question = ?")
		cursor.execute(getUser, [(audio)])
		results = cursor.fetchall()
		for i in results:
			speak(i[2])
	else:
		speak("Sorry, I do not know that one")
		speak("Can you help me improve my database")
		choice = takeVoiceInput('Yes or No...')

		if choice == 'yes' or choice == 'sure' or choice == 'ok':
			speak("Tell me what to say when you ask me" +audio)
			solution = takeVoiceInput('Say your response')

			insertAns = '''INSERT INTO responses(Question, Response) VALUES(?,?)'''
			cursor.execute(insertAns, [(audio),(solution)])
			database.commit()
		elif choice == 'no':
			speak("Thanks for your participation")
		else:
			speak("Please say either yes or no")

if __name__ == "__main__":
	while True:
		try:
			main()
		except KeyboardInterrupt:
			print("Program closeed using [ctrl-c]")
			exit()