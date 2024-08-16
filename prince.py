import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import cv2
import random
import psutil # for getting current running details like battery status,cpu usage
import pywhatkit as kit
import googletrans
from googletrans import Translator# used in translation
import ctypes # used in translation
import pyjokes
import requests
import time
import pyautogui
import operator
from bs4 import BeautifulSoup
from pywikihow import search_wikihow #used for searching (beautiful soup)
import PyPDF2
import json   # for sending data from server to the user
import nexmo # for sending SMS
import tkinter as tk
from tkinter import messagebox
import urllib.request
import wolframalpha


engine = pyttsx3.init('sapi5')  #The SAPI application programming interface (API) dramatically reduces the code overhead required for an application to use speech recognition and text-to-speech, making speech technology more accessible and robust for a wide range of applications.
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()



def check_login(username, password):
    # You can modify this function to check against your actual user database
    if username == "admin" and password == "password":
        return True
    else:
        return False

def login():
    username = username_entry.get()
    password = password_entry.get()

    if check_login(username, password):
        messagebox.showinfo("Login Successful", "Welcome!")
        root.destroy()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

    # DEFINING WISH ME FUNCTION 
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am jarvis Sir. Please tell me how may I help you")       

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

    # DEFINING CLICK PICTURE CASE IT WILL CLCK THE PICTURE USING CV2 LIBRAAY
def clickpicture():
    # Set directory for saving screenshot
    directory = "Your Screenshot Path"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Get current date and time for naming the file
    now = datetime.datetime.now()
    filename = directory + now.strftime("%Y-%m-%d %H-%M-%S") + ".png"

    # Take screenshot using cv2 library
    img = cv2.VideoCapture(0)
    ret, frame = img.read()
    cv2.imwrite(filename, frame)
    img.release()

    # Speak confirmation message and show file location
    speak("Photo taken!")
    speak(f"The photo has been saved at {filename}")
    # DEFINING SYSTEM INFO CASE
def system_info():
    usage = str(psutil.cpu_percent())+'%'
    speak('CPU usage is at '+usage)
    
    available_ram =  round(psutil.virtual_memory().available / (1024.0 ** 3), 2)
    total_ram = round(psutil.virtual_memory().total / (1024.0 ** 3), 2)
    speak(f'Available RAM is {available_ram} gigabytes out of {total_ram} gigabytes.')
    # DEFINING TRANSLATING CASE ( lANGAUAGE )
def translate_text(text, dest_lang):
    translator = Translator()
    translated = translator.translate(text, dest=dest_lang)
    return translated.text

    # DEFINING LOCK SCREEN CASE
def lockScreen():
    """Lock the screen"""
    ctypes.windll.user32.LockWorkStation()
    speak("Screen locked.")
    # DEFINING CONTROL PANNEL CASE
def openControlPanel():
    os.system("control panel")
    speak("Control Panel opened.")
    #DEFININF TASK MANAGER CASE
    
def openTaskManager():
    os.system("taskmgr")
    speak("Task Manager opened.")
    #DEFINING SEARCH ON GOOGLE 

def searchOnGoogle(query):
    query = query.strip()
    speak(f'Searching for {query} on Google...')
    url = f'https://www.google.com/search?q={query}'
    webbrowser.open(url)
    # DEFINING NEWS FUNCTION

def open_chatgpt():
    url = "https://chat.openai.com/"
    webbrowser.open(url)

def news():
    main_url= "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=YourApiKEY" #please replace your api with your actual api
    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head=[]
    day=["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"] 
    for ar in articles:
        head.append(ar["title"])
    for i in range(len(day)):
        speak(f"today's {day[i]} news is : {head[i]}")
        print(f"today's {day[i]} news is : {head[i]}")
    # DEFINING PDF REDADER FUNCTION FOR READING THE PDF " IMPORT PYPDF2"

def pdf_reader():
    book = open("abc.pdf", "rb")
    pdfReader = PyPDF2.PdfReader(book)
    pages = len(pdfReader.pages)
    speak(f"Total number of pages in this book: {pages}")
    speak("Please enter the page number I have to read.")
    pg = int(input("Please enter the page number: "))
    page = pdfReader.pages[pg]

    text = page.extract_text()
    speak(text)
    # DEFINING CONVERT CURRENCY FUNCTION IT WILL CONVERT THE CURRENCY INTO INTO ANOTHEER CURRENCY


def convert_currency(amount, from_currency, to_currency):
    app_id = 'YourApiID' # replace with your api
    url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}&symbols={from_currency},{to_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)  # Add this line to print the response
        rates = data['rates']
        result = amount * (rates[to_currency] / rates[from_currency])
        print(f"{amount} {from_currency} is {result} {to_currency}")
        return result
    else:
        return None
    # DEFINING WEATHER FUNCTION

def getWeather(city):
    api_key = "Your Api ID " # replace with your api
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] != "404":
        weather = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
        return weather
    else:
        return None


def send_message(api_key, api_secret, sender, recipient, message):
    client = nexmo.Client(key=api_key, secret=api_secret)
    response = client.send_message({
        'from': sender,
        'to': recipient,
        'text': message
    })
    if response['messages'][0]['status'] == '0':
        print('Message sent successfully.')
        speak('Message sent successfully.')
    else:
        print(f'Message failed with error: {response["messages"][0]["error-text"]}')
        speak(f'Message failed with error: {response["messages"][0]["error-text"]}')
        

def get_stock_price(symbol):
    api_key = "Your APIID"
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = json.loads(response.text)
    try:
        price = data['Global Quote']['05. price']
        return float(price)
    except KeyError:
        print("Invalid symbol")
        return None

def speak_webpage(url):
    # Download and parse HTML page
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    # Get text content of web page
    content = ''
    for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']):
        content += tag.get_text() + '\n'

    # Speak content using text-to-speech engine
    engine.say(content)
    engine.runAndWait()

def open_webpage(url):
    try:
        webbrowser.get().open(url)
        speak('Opening webpage in web browser')
    except Exception as e:
        print(e)
        speak('Sorry, unable to open webpage')


 # Replace YOUR_APP_ID with your actual app ID
app_id = 'Your API ID'
client = wolframalpha.Client(app_id)

def get_wolframalpha_response(query):
    
    try:
        res = client.query(query)
        return next(res.results).text
    except:
        return ""

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Login")
    root.geometry("300x150")

    # Create a frame to hold the login widgets
    login_frame = tk.Frame(root)
    login_frame.pack(pady=10)

    # Create labels and entries for the username and password
    username_label = tk.Label(login_frame, text="Username:")
    username_label.grid(row=0, column=0, padx=5, pady=5)

    username_entry = tk.Entry(login_frame)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    password_label = tk.Label(login_frame, text="Password:")
    password_label.grid(row=1, column=0, padx=5, pady=5)

    password_entry = tk.Entry(login_frame, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    # Create a login button to check the credentials
    login_button = tk.Button(login_frame, text="Login", command=login)
    login_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Start the main event loop to display the dashboard
    root.mainloop()

    # If the login is successful, run the rest of the Jarvis program
    if check_login("admin", "password"):

        wishMe()
        while True:
        # if 1:
            query = takeCommand().lower()

            # Logic for executing tasks based on query

    # SEACRCHING WIKIPEDIA       
            if 'wikipedia' in query:
                try:
                    speak('Searching Wikipedia...')
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)
                except wikipedia.exceptions.PageError as e:
                    print(f"{query} not found on Wikipedia")
                    speak(f"{query} not found on Wikipedia")
                except wikipedia.exceptions.DisambiguationError as e:
                    print(f"{query} may refer to multiple things. Please be more specific.")
                    speak(f"{query} may refer to multiple things. Please be more specific.")
                except Exception as e:
                    print(f"Error: {e}")
                    speak("Sorry, there was an error searching on Wikipedia")

    # TALKING WITTH J.A.R.V.I.S
            elif 'hello' in query:
                speak("hello , how can i assist you  ")
                print("hello , how can i assist you  ")

            elif 'how are you' in query:
                speak("i m fine , what about you ")
                print("i m fine , what about you")

    # OPENING YOU TUBE
            elif 'open youtube' in query:
                webbrowser.open("youtube.com")
    # OPENING GOOGLE
            elif 'open google' in query:
                webbrowser.open("google.com")
    # OPENING STACK OVERFLOW
            elif 'open stack overflow' in query:
                webbrowser.open("stackoverflow.com")


    # SHUTDOWN THE SYSTEM 
            elif 'shutdown' in query:
                speak("Are you sure you want to shutdown your computer?")
                confirm = takeCommand().lower()
                if 'yes' in confirm:
                    os.system("shutdown /s /t 1")
                else:
                    speak("Shutdown cancelled")
    # OPENING CMD
            elif 'command prompt' in query or 'command' in query:
                os.system('start cmd') # open command prompt
    # OPEN CAMERA
            elif 'open camera' in query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow("webcam", img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break
                cap.release()
                cv2.destroyAllWindows()
    # THIS CASE SEND THE WHATSAPP MESSAGE USING THE PHONE NUMBER             
            elif 'send whatsapp message' in query:
                kit.sendwhatmsg("Your NUMBER WITH COUNTRY CODE","this is the testing protocoal",22,59) #time in HH,MM
    # IT WILL CLICK THE PICTURES
            elif 'picture' in query:
                clickpicture()
            
    # IT WILL OPEN THE FILES 
            elif 'file' in query:
                file_path = "Your File Path" # We Have To change the path of file if we are using any other laptop
                os.startfile(file_path)
    # IT WILL PROVIDE THE SYSTEM INFORMATION
            elif 'system info' in query:
                system_info()
    # TRANSLATING THE  LANGUAGE INTO ANOTHER LANGUAGE
            elif 'translate' in query:
                speak("What should I translate?")
                text = takeCommand()
                speak("To which language should I translate it?")
                dest_lang = takeCommand()
                translated_text = translate_text(text, dest_lang)
                speak(f"The translated text is {translated_text}")
                print(f"The translated text is {translated_text}")
            # IT WILL LOCK THE PC SCREEN         
            elif 'lock screen' in query:
                lockScreen()  
    # OPENING CONTROL PANEL
            elif 'open control panel' in query:
                openControlPanel()
    # OPEN TASK MANAGER
            elif 'open task manager' in query:
                openTaskManager()
    # SEARCHING ON GOOGLE
            elif 'search' in query:
                searchOnGoogle(query)
    # PLAY MUSIC FROM YOU TUBE 
            elif 'play song on youtube' in query:
                kit.playonyt("see you agiain")
    # ENGLISH JOKES
            elif 'joke' in query:
                joke =  pyjokes.get_joke()
                speak(joke)
    # LATESET INDIA NEWS  
            elif 'news' in query:
                speak("please wait bro, fetching the latest news")
                news()
    # SCREENSHOT 
            elif 'screenshot' in query:
                speak("bro , please tell  me the name for this screenshot file")
                name = takeCommand().lower()
                speak("please sir hold the screen for few seconds, i am taking screenshot")
                time.sleep(3)
                img=pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("im done , the screenshot is saved in our main folder ")
                
    # HIDDING AND MAKING  FILES VISIBLE 

            elif "hide all files" in query or "hide this folder" in query or "visible for everyone" in query:
                speak("sir please tell me you want to hide this folder or make it visible for everyone")
                condition = takeCommand().lower()
                if "hide" in condition:
                    os.system("attrib +h /s /d")                 
                #os.system("attrib +h /s /d") is used to set the attributes of all files and folders in the current directory (and any subdirectories) to be hidden.
                #The /s flag makes the command recursive, applying it to all subdirectories, and /d makes it apply to both files and folders.
                
                    speak("sir, all the files in this folder are now hidden.")
                elif "visible" in condition:
                    os.system("attrib -h /s /d") # for making visible files 
                    speak("sir, all the files in this folder are now visible to everyone. i wish you are taking Desicion on your own peace")
                elif "leave it" in condition or "leave for now" in condition:
                    speak("Ok sir")
    # CALCULATION USING J.A.R.V.I.S 

            elif 'do some calculation' in query or 'can you calculate' in query:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    speak("say what you want to calculate, for example: 3 plus 3")
                    print("listening...")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                my_string = r.recognize_google(audio)
                print(my_string)

                def get_operator_fn(op):
                    return {
                        '+': operator.add,#plus
                        '-': operator.sub,#minus
                        '*': operator.mul,#multiple by
                        'divided': operator.truediv,#divided
                        '/': operator.truediv
                    }[op]

                def eval_binary_expr(op1, oper, op2):
                    op1, op2 = int(op1), int(op2)
                    return get_operator_fn(oper)(op1, op2)

                result = eval_binary_expr(*(my_string.split()))
                print("Result: ", result)
                speak(f"your result is {result}")
    # ACTIVATE HOW TO DO ANYTHING MODE 
            elif 'how to do in a mode' in query:
                speak("how to do mode is activated ")
                while True:
                    speak("please tell me what you want to know")
                    how = takeCommand()
                    try:
                        if 'exit' in how or 'close' in how:
                            speak("okay sir,how to do mode is deactivated")
                            break
                        else:
                            max_results = 1
                            how_to = search_wikihow(how, max_results)
                            assert len(how_to) == 1
                            how_to[0].print()
                            speak(how_to[0].summary)
                    except Exception as e:
                        speak("sorry sir, im not able to find this")  
    # PLAYING MUSIC FROM C DRIVE USING C DRIVE PATH           
            elif 'play music' in query:
                music_dir = 'C:\Music'
                songs = os.listdir(music_dir)
                print(songs) 
                rd=random.choice(songs)   
                os.startfile(os.path.join(music_dir, rd))
    # Asking The Time
            elif 'the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")    
                speak(f"Sir, the time is {strTime}")
    #TEMPERATURE OF THE CITIES
            elif 'temperature' in query:
                city = input("Please enter the city for which you want to get the temperature: ")
                search = f"temperature in {city}"
                url = f"https://www.google.com/search?q={search}"
                r = requests.get(url)
                data = BeautifulSoup(r.text,"html.parser")
                temp = data.find("div", class_="BNeawe").text
                print(f"Current temperature in {city} is {temp}")
                speak(f"Current temperature in {city} is {temp}")
                # THIS CASE CHECK THE BATTERY PERCENTAGE 
            elif 'how much power left' in query or 'how much power we have' in query or 'battery' in query:
                battery = psutil.sensors_battery()
                percentage = battery.percent
                speak(f" our system have{percentage} percent battery")
                print(f"our system have {percentage}% battery")
                if percentage>=70:
                    speak("we have enough power to continue our work")
                elif percentage>=40 and percentage<=69:
                    speak("we should coonect our system to charging point to charge our battery")
                elif percentage>=15 and percentage<=39:
                    speak("we don't have enoough power to work ,please connect to charger")
                elif percentage<=14:
                    speak("we have very low power , please coonect to charging, the system will shutdown soon")
                # THIS CASE WILL INCREASE THE VOLUME AND DECRREASE & MUTE THE VOLLLLLUME 
            elif 'volume up' in query or 'increase volume' in query:
                pyautogui.press("volumeup")
            elif 'volume down' in query:
                pyautogui.press("volumedown")
            elif 'mute' in query or 'volume mute' in query:
                pyautogui.press("volumemute")
            elif 'unmute' in query:
                pyautogui.press("volumeunmute")
            # Recalling The "PDF" Function
            elif 'pdf reader' in query:
                pdf_reader()
                # Currency Conversion
            elif 'convert' in query:
                speak("Sure. What is the amount, currency from, and currency to? For example, 'convert 100 USD to EUR'")
                conv_query = takeCommand().lower()
                conv_query = conv_query.replace("convert", "").strip()
                conv_parts = conv_query.split(" ")
                if len(conv_parts) == 4:
                    amount = float(conv_parts[0])
                    from_currency = conv_parts[1].upper()
                    to_currency = conv_parts[3].upper()

                    converted_amount = convert_currency(amount, from_currency, to_currency)
                    if converted_amount:
                        speak(f'{amount} {from_currency} is {converted_amount} {to_currency}')
                    else:
                        speak("Sorry, there was an error converting currencies.")
                else:
                    speak("Sorry, I didn't understand the conversion request.")  
                # Recallling The Weather For Getting the temperature of the city
            elif 'weather in' in query:
                city = query.split("in ")[1]
                weather = getWeather(city)
                if weather:
                    speak(f"The temperature in {city} is {weather['temperature']} degrees Celsius, the humidity is {weather['humidity']} percent, and the wind speed is {weather['wind_speed']} kilometers per hour.")
                    print(f"The temperature in {city} is {weather['temperature']} degrees Celsius, the humidity is {weather['humidity']} percent, and the wind speed is {weather['wind_speed']} kilometers per hour.")
                else:
                    speak(f"Sorry, I could not find weather information for {city}.")


            elif 'send message' in query:
                api_key = 'YOUR API KEY'
                api_secret = 'Your API SECRET KEY'
                sender = 'Your No.'
                recipient = 'RecipentNO.'
                message = 'Hello This Is A Testing Message Using Python code'
                send_message(api_key, api_secret, sender, recipient, message)

            elif 'check stock price' in query or 'stock price' in query:
                speak("Which stock symbol do you want to check?") #APM,AAPL , AMZN ,FB ,GOOGL , MSFT , v , NFLX , NVDA, MSFT ,pm
                symbol = takeCommand()
                price = get_stock_price(symbol)
                if price is not None:
                    speak(f"The current price of {symbol.upper()} is {price:.2f} USD.")
                    print(f"The current price of {symbol.upper()} is {price:.2f} USD.")

            elif ' about us' in query or 'about' in query:
                open_webpage('Your Local HTMl WEbpage path')
                speak_webpage('Your Local HTMl WEbpage pathl')

            elif 'factor page' in query:
                webbrowser.open('Your Local HTMl WEbpage path')
                speak_webpage('Your Local HTMl WEbpage path')

            elif 'open chat' in query or 'open chatgpt' in query:
                open_chatgpt()
                print("Opening ChatGPT...")

            elif any(word in query for word in ['what is', 'where is', 'how', 'when', 'why' , 'who']):
                for word in ['what is', 'where is', 'how', 'when', 'why' ,'who']:
                    if word in query:
                        query = query.replace(word, "")
                        break
                result = get_wolframalpha_response(query)
                if result:
                    speak(result)
                    print(result)
                else:
                    speak('Sorry, I could not find an answer for that.')


            elif 'thank you' in query:
                speak("You're welcome. Have a great day!")
                webbrowser.open('Your Local HTMl WEbpage path')
                break


            
                
            

            
            

            

            

 
