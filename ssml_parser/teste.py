import re
from num2words import num2words
import sys

def parse_ssml(ssml_text,lang):
    replacements = {
        r"<speak>": "", r"</speak>": "",
        r"<break time=\"(\d+)(ms|s)\"\/>": lambda m: f"[pause for {m.group(1)} second(s)]",
        r"<say-as interpret-as=\"characters\">(.*?)</say-as>": lambda m: " ".join(m.group(1)),
        r"<say-as interpret-as=\"cardinal\">(.*?)</say-as>": lambda m: num2pal(int(m.group(1)), "cardinal", lang),
        r"<say-as interpret-as=\"ordinal\">(.*?)</say-as>": lambda m: num2pal(int(m.group(1)), "ordinal", lang),
        #r"<say-as interpret-as=\"fraction\">(.*?)</say-as>": lambda m: num2pal(int(m.group(1)), "fraction"), not implemented in the lib
        r"<say-as interpret-as=\"currency\">(.*?)</say-as>": lambda m: num2pal(int(m.group(1)), "currency", lang), 
        r"<sub alias=\"(.*?)\">(.*?)</sub>": lambda m: m.group(1),
        r"<audio src=\"(.*?)\">(.*?)</audio>": "[audio file plays]",
        r"<p>": "", r"</p>": "",
        r"<s>": "", r"</s>": ""
    }

    for pattern, replacement in replacements.items():
        ssml_text = re.sub(pattern, replacement, ssml_text) if isinstance(replacement, str) else re.sub(pattern, replacement, ssml_text)
    
    ssml_text = re.sub(r"<.*?>", "", ssml_text)
    
    return ssml_text.strip()

def num2pal(num, type, language):
    """Convert number to words based on the given type (cardinal, ordinal, etc.)."""
    if type == "cardinal":
        return num2words(num,lang=language, to="cardinal")
    elif type == "ordinal":
        return num2words(num,lang=language, to="ordinal")
    elif type == "currency":
        return num2words(num,lang=language, to="currency")
    elif type == "fraction":
        return num2words(num, to="fraction")
    else:
        return str(num)



def main():
    n = len(sys.argv)
    if(n<3):
        print("Wrong usage: python program.py \"file\" \"language\"")
    
    file_path=sys.argv[1]
    lang=sys.argv[2]


    strings = ""
    try:
        with open(file_path, 'r') as file:
            for line in file:
                strings += line  # Use += to concatenate each line
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return

    print(strings)
    print("parsed:")
    print(parse_ssml(strings, lang))



if __name__=="__main__":
    main()
