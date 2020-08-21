verb = "amoreux"
conj = "amoreuse"

def findWord(name, sentence):
    positions = []
    for indx, word in enumerate(sentence.split(' ')):
        if word == name:
            positions.append(indx)
    return positions[0]

# This can still be improved... maybe we might have to explicitly use exceptions for some very irregular verbs...
def strComp(a, b):
    if ("'" == b[1]):
        shorter = a if len(a) <= (len(b)-2) else b
        s = sum([a[i] != b[2+i] for i in range(len(shorter)-2)])
        if(s <= 2):
            return True
        else:
            return False
    else:
        shorter = a if len(a) <= len(b) else b
        s = sum([a[i] != b[i] for i in range(len(shorter))])
        if(s <= 2):
            return True
        else:
            return False
        # another possible solution requiring the differences in spelling are at the end
        # shorter = a if len(a) <= len(b) else b
        # diff = 0
        # for i, (ca, cb) in enumerate(zip(a, b)):
        #     if ca != cb:
        #         if i >= (len(shorter)-3):
        #             diff += 1
        #         else:
        #             return False
        # if diff <= 2:
        #     return True
        # else:
        #     return False


def sentenceHide(sentence, vocabWord):
    a = sentence.split(' ')
    if(vocabWord[0:2] == 'se'):
        vocabWord = vocabWord.replace(vocabWord[0:3], '')
    for word in a:
        word.lower()
        diff = 0
        if (len(word) <= 3):
            continue
        lastLetter = word[len(word)-1]
        punctuation = ''
        if any([lastLetter == '.', lastLetter == ',', lastLetter == ';', lastLetter == '!', lastLetter == '!']):
            punctuation = lastLetter
            diff = -1
        if (("'" == word[1]) and (word[2:4]==vocabWord[0:2])):
            shorter = word if len(word) <= (len(vocabWord)-2) else vocabWord
            diff += sum([vocabWord[i] != word[2+i] for i in range(len(shorter)-2)])
            if(diff <= 2):
                return sentence.replace(word, '[****]' + punctuation)
            else:
                continue
        else:
            shorter = word if len(word) <= len(vocabWord) else vocabWord
            diff += sum([vocabWord[i] != word[i] for i in range(len(shorter))])
            if(diff <= 2):
                return sentence.replace(word, '[****]' + punctuation)
            else:
                continue
    return sentence


intro = "je m'appelle Nathaniel Ruhl."
name = "s'appeller"
print(sentenceHide(intro, name))
# now for the Popup:
    # Popup(text=sentence)
#else: Popup(text=sentence)


def spellCheck(a, b):
    s = sum([a[i] != b[2+i] for i in range(len(shorter)-2)])
    if(s == 1):
        return True
    else:
        return False

x='je'
if any(['je'==x, 'tu'==x, 'il'==x, 'elle'==x, 'nous'==x, 'vous'==x, 'ils'==x, 'elles'==x]):
    print("success")
