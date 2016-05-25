import sys

def transform_text(filename):
    LongStringQuote = 'ಠ'
    
    with open(filename, 'r') as infile:
        text = infile.read()

    lines = text.split('\n')
    newtext = ''
    for line in lines:
        if line and line[0] == ';':
            line = LongStringQuote
        newtext += ('\n' + line)
    return newtext

if __name__ == "__main__":
    script = sys.argv.pop(0)
    filename = sys.argv.pop(0)

    transform_text(filename)