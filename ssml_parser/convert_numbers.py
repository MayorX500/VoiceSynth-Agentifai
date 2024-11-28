import sys
from num2words import num2words

def main():
    # Check if the argument is provided
    if len(sys.argv) != 4:
        print("Usage: python3 convert_numbers.py <number> <language> <type>")
        return

    try:
        number = int(sys.argv[1])
        ordinalFlag = sys.argv[3].lower()
        language = sys.argv[2]
        print(num2words(number, lang=language, to=ordinalFlag))
        #print(num2words(number))
    except ValueError:
        print("Error: Invalid number")

if __name__ == "__main__":
    main()
