# skeleton text nlp analyer for PDF only WIP.


# search keyword in pdf and return number of keywords
# (assuming pdf carefully parsed for now)
def search(file, word):
    count = 0
    for words in file:
        if words == word:
            count += 1
    return count


# highlight keyword in pdf
# mark function will highlight keywords of pdf
def highlight(file, word):
    for words in file:
        if words == word:
            mark(word)
    
    return "complete"
