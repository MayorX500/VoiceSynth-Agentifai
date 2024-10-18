import sys
from num2words import num2words

def main():
    # Check if the argument is provided
    if len(sys.argv) != 4:
        print("Usage: python3 convert_numbers.py <number> <ordinalFlag> <language>")
        return

    try:
        number = int(sys.argv[1])
        ordinalFlag = sys.argv[2].lower() == 'true'
        language = sys.argv[3]
        print(num2words(number, ordinal=ordinalFlag, lang=language))
        #print(num2words(number))
    except ValueError:
        print("Error: Invalid number")

if __name__ == "__main__":
    main()
