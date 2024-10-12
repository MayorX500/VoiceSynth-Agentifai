# modules/ssml/builder.py

from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
import xml.dom.minidom

class SSMLBuilder:
    def __init__(self, voice_name="en-SophiaNN"):
        self.speak = Element("speak")
        self.voice_name = voice_name
        self.voice_element = SubElement(self.speak, "voice", {"name": self.voice_name})
    
    def add_text(self, text):
        """Add plain text to the SSML"""
        text_element = SubElement(self.voice_element, "text")
        text_element.text = text

    def add_break(self, time_ms=500):
        """Add a pause (break) with specified duration in milliseconds"""
        SubElement(self.voice_element, "break", {"time": f"{time_ms}ms"})

    def add_emphasis(self, text, level="moderate"):
        """Add emphasized text with the specified level"""
        emphasis = SubElement(self.voice_element, "emphasis", {"level": level})
        emphasis.text = text

    def add_prosody(self, text, pitch="medium", rate="medium", volume="medium"):
        """Add prosody elements to modify the speech's pitch, rate, and volume"""
        prosody = SubElement(self.voice_element, "prosody", {
            "pitch": pitch,
            "rate": rate,
            "volume": volume
        })
        prosody.text = text

    def add_say_as_time(self, text):
        """Add text with 'say-as' format for interpreting as time"""
        say_as = SubElement(self.voice_element, "say-as", {"interpret-as": "time"})
        say_as.text = text

    def add_say_as_date(self, text, format="dmy"):
        """Add text with 'say-as' format for interpreting as date"""
        say_as = SubElement(self.voice_element, "say-as", {"interpret-as": "date", "format": format})
        say_as.text = text
    
    def get_ssml_string(self):
        """Return a pretty-printed SSML string with newlines and indentation"""
        ssml_str = tostring(self.speak, encoding="unicode")
        dom = xml.dom.minidom.parseString(ssml_str)
        return dom.toprettyxml(indent="    ")

    def save_to_file(self, filename="ssml_output.xml"):
        """Save the SSML to a file with proper formatting"""
        pretty_ssml = self.get_ssml_string()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(pretty_ssml)

# Example usage:
if __name__ == "__main__":
    ssml = SSMLBuilder(voice_name="en-SophiaNN")
    ssml.add_text("Welcome to our company! Our office hours are from ")
    ssml.add_say_as_time("9 am")
    ssml.add_text(" till ")
    ssml.add_say_as_time("7 pm")
    ssml.add_text(", Monday to Friday.")
    ssml.add_break(time_ms=500)
    ssml.add_emphasis("Thank you for choosing us!", level="strong")
    
    # Print the SSML output (well-formatted)
    print(ssml.get_ssml_string())
    
    # Save the SSML to a file
    ssml.save_to_file("example_ssml.xml")
