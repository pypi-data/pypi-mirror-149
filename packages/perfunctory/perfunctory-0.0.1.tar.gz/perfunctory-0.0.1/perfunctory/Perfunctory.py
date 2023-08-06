


# not install reired
import datetime
import platform
import uuid
import zipfile


class Perfunctory:
    def __init__(self):
        self.days = {"0": "Monday",
                    "1": "Tuesday",
                    "2": "Wednesday",
                    "3": "Thursday", 
                    "4": "Friday", 
                    "5": "Saturday", 
                    "6": "Sunday"}
        self.months = {"1": "January",
                        '2':'February',
                        '3':'March',
                        '4':'April',
                        '5':'May',
                        '6':'June',
                        '7':'July',
                        '8':'August',
                        '9':'September',
                        '10':'October',
                        '11':'November',
                        '12':'December'}
    def time(self):
        return {'time': datetime.datetime.now().strftime('%I:%M %p')}
    def date(self):
        today = datetime.date.today()
        weekday = str(today.weekday())
        day = str(today.day)
        month = str(today.month)
        year = str(today.year)
        x = {'strdate':f'{self.days[weekday]},  {day} {self.months[month]} {year}','data': {'weekday': self.days[weekday], 'date': day, 'month': self.months[month], 'year': year}}
        return x
    @staticmethod
    def textToMorse(text):
        text = text.lower()
        x = {
        "a": ".-",
        "b": "-...",
        "c": "-.-.",
        "d": "-..",
        "e": ".",
        "f": "..-.",
        "g": ".-",
        "h": "....",
        "i": "..",
        "j": ".---",
        "k": "-.-",
        "l": ".-..",
        "m": "--",
        "n": "-.",
        "o": "---",
        "p": ".--.",
        "q": "--.-",
        "r": ".-.",
        "s": "...",
        "t": "-",
        "u": "..-",
        "v": "...-",
        "w": ".--",
        "x": "-..-",
        "y": "-.--",
        "z": "--..",
        " ": " ",}
        o = []
        for i in range(len(text)):
            if text[i] in x.keys():
                o.append(x.get(text[i]))
            else:
                o.append(text[i])
        return o
    @staticmethod
    def ageCalculator(year=1988, month=11, day=18):
        today = datetime.datetime.now().date()
        date_of_birth = datetime.date(year, month, day)
        age = int((today - date_of_birth).days / 365.25)
        return {'age': age}
    @staticmethod
    def systemInfo():
            try:
                processor = platform.processor()
                architecture = platform.architecture()
                machine = platform.machine()
                network_name = platform.node()
                information = platform.platform()
                operating_system = platform.system()
                python_on_system = platform.python_build()
                aggreated_info = {'processor': processor, 'architecture': architecture, 'machine': machine, 'network_name': network_name, 'information': information, 'operating_system': operating_system, 'python_on_system': python_on_system}
                return aggreated_info
            except:
                return "Sorry, could not get system information"
    @staticmethod
    def intToBinary(n):
        return bin(n)[2:]
    @staticmethod
    def uniqueID():
        # hex32 = uuid.uuid4().hex
        # uuidv4 = uuid.uuid4()
        return str(uuid.uuid4())
    @staticmethod
    def makeZip(file_name, file_path):
        with zipfile.ZipFile(file_name, 'w') as zf:
            zf.write(file_path)
        return {'info': {'zip file created': file_name}}
    @staticmethod
    def makeUnzip(file_name, file_path):
        with zipfile.ZipFile(file_name, 'r') as zf:
            zf.extractall(file_path)
        return {'info': {'zip file extracted': file_name}}
