from utils import Handler
import cgi

def rot13(s): 
    upper = {"A":"N","B":"O","C":"P","D":"Q","E":"R","F":"S","G":"T",
             "H":"U","I":"V","J":"W","K":"X","L":"Y","M":"Z","N":"A",
             "O":"B","P":"C","Q":"D","R":"E","S":"F","T":"G","U":"H",
             "V":"I","W":"J","X":"K","Y":"L","Z":"M"}
    lower = {"a":"n","b":"o","c":"p","d":"q","e":"r","f":"s","g":"t",
             "h":"u","i":"v","j":"w","k":"x","l":"y","m":"z","n":"a",
             "o":"b","p":"c","q":"d","r":"e","s":"f","t":"g","u":"h",
             "v":"i","w":"j","x":"k","y":"l","z":"m"}
    init_string = s
    new_string = ""
    length = len(s)
    for i in range(0,length):
        if init_string[i] in lower:
            new_string += lower[init_string[i]]
        elif init_string[i] in upper:
            new_string += upper[init_string[i]]
        else:
            new_string += init_string[i]
    return new_string

class Rot13Handler(Handler): 
    def get(self):
        self.render("Rot13Template.html")
    def post(self):
        text = self.request.get("text")
        cipher = rot13(text)
        escaped = {"escaped": cgi.escape(cipher, True)}
        self.render("Rot13Template.html", **escaped)