from os import system, name
from socket import gethostname, gethostbyname
from colorama import Back, init, Fore
from keyboard import add_hotkey, press_and_release, press, release, is_pressed
from random import randint
from mouse import move, get_position
from time import sleep

class output:
    def clear():
        try:
            if name == 'nt': 
                _ = system('cls') 
            else: 
                _ = system('clear')
        except:
            print('Failed to clear output: Unknown error')

    class print:
        def print(text):
            try:
                print(text)
            except:
                print('Failed to recognize text: Input must be a string')

        class color:
            class text_color:
                init()
                def RED(text):
                    try:
                        print(Fore.RED+text+Fore.RESET)
                        return True
                    except:
                        print('Failed to recognize text: Input must be a string')
                        return False
                def YELLOW(text):
                    try:
                        print(Fore.YELLOW+text+Fore.RESET)
                        return True
                    except:
                        print('Failed to recognize text: Input must be a string')
                        return False
                def GREEN(text):
                    try:
                        print(Fore.GREEN+text+Fore.RESET)
                        return True
                    except:
                        print('Failed to recognize text: Input must be a string')
                        return False
                def BLUE(text):
                    try:
                        print(Fore.BLUE+text+Fore.RESET)
                        return True
                    except:
                        print('Failed to recognize text: Input must be a string')
                        return False
                def CYAN(text):
                    try:
                        print(Fore.CYAN+text+Fore.RESET)
                        return True
                    except:
                        print('Failed to recognize text: Input must be a string')
                        return False
                def MAGENTA(text):
                    try:
                        print(Fore.MAGENTA+text+Fore.RESET)
                        return True
                    except:
                        print('Failed to recognize text: Input must be a string')
                        return False
                def BLACK(text):
                    try:
                        print(Fore.BLACK+text+Fore.RESET)
                        return True
                    except:
                        print('Failed to recognize text: Input must be a string')
                        return False
                def WHITE(text):
                    try:
                        print(Fore.WHITE+text+Fore.RESET)
                        return True
                    except:
                        print('Failed to recognize text: Input must be a string')
                        return False
            class background_color:
                init()
                def RED(text):
                    try:
                        print(Back.RED+text+Back.RESET)
                        return True
                    except:
                        print('Failed to recognize text: Input must be a string')
                        return False
                def YELLOW(text):
                    try:
                        print(Back.YELLOW+text+Back.RESET)
                        return True
                    except:
                        print('Failed to recognize text: Input must be a string')
                        return False
                def GREEN(text):
                    try:
                        print(Back.GREEN+text+Back.RESET)
                        return True
                    except:
                        print('Failed to recognize text: Input must be a string')
                        return False
                def BLUE(text):
                    try:
                        print(Back.BLUE+text+Back.RESET)
                        return True
                    except:
                        print('Failed to recognize text: Input must be a string')
                        return False
                def CYAN(text):
                    try:
                        print(Back.CYAN+text+Back.RESET)
                        return True
                    except:
                        print('Failed to recognize text: Input must be a string')
                        return False
                def MAGENTA(text):
                    try:
                        print(Back.MAGENTA+text+Back.RESET)
                        return True
                    except:
                        print('Failed to recognize text: Input must be a string')
                        return False
                def BLACK(text):
                    try:
                        print(Back.BLACK+text+Back.RESET)
                        return True
                    except:
                        print('Failed to recognize text: Input must be a string')
                        return False
                def WHITE(text):
                    try:
                        print(Back.WHITE+text+Back.RESET)
                        return True
                    except:
                        print('Failed to recognize text: Input must be a string')
                        return False
class ip:
    def find():
        try:
            return gethostbyname(gethostname())
        except:
            return 'An unexpected error occured'
    def get_ip():
        try:
            return gethostbyname(gethostname())
        except:
            return 'An unexpected error occured'
    class website:
        def find(URL):
            try:
                return gethostbyname(URL)
            except:
                return 'Failed to resolve IP: Invalid URL'
        def get_ip(URL):
            try:
                return gethostbyname(URL)
            except:
                return 'Failed to resolve IP: Invalid URL'

class keyboard:
    def hotkey(key, callback, suppress, trigger_release):
        try:
            add_hotkey(key, callback, suppress=suppress, trigger_on_release=trigger_release)
            return True
        except:
            print('Invalid arguments: keyboard.hotkey(key (string), callback (lambda), suppress (bool), trigger_release (bool))')
            return False
    def when_pressed(key, callback, suppress, trigger_release):
        try:
            add_hotkey(key, callback, suppress=suppress, trigger_on_release=trigger_release)
            return True
        except:
            print('Invalid arguments: keyboard.hotkey(key (string), callback (lambda), suppress (bool), trigger_release (bool))')
            return False
    class invoke:
        def press(key):
            try:
                press_and_release(key)
                return True
            except:
                print('Failed to read key: Unknown key')
                return False
        def up(key):
            try:
                release(key)
                return True
            except:
                print('Failed to read key: Unknown key')
                return False
        def down(key):
            try:
                press(key)
                return True
            except:
                print('Failed to read key: Unknown key')
                return False
    def is_invoked(key):
        try:
            return is_pressed(key)
        except:
            print('Failed to read key: Unknown key')
            return False
    
class math:
    def random(min, max):
        try:
            return randint(min,max)
        except:
            print('Failed to calculate random number: Invalid arguments')
            return False
            
class mouse:
    def position(x,y):
        try:
            move(x,y)
        except:
            print("Unable to move mouse: Invalid coordinates")
    def get_position():
        try:
            return get_position()
        except:
            print('Unable to read mouse coordinates: Unknown error')

def wait(seconds):
    try:
        sleep(seconds)
        return True
    except:
        print('Unable to wait: Argument must be an integer')
        return False