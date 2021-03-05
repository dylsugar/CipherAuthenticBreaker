import hashlib

SHDW = 'shadow'
PSSWD = 'passwords.txt'
DICT = 'dictionary.txt'

def caesarShifter(word,shift):
    decrypted = ''
    for letter in word:
        if letter.isalpha():
            num = ord(letter)
            num -= shift

            if letter.isupper():
                if num > ord('Z'):
                    num -= 26
                elif num < ord('A'):
                    num += 26
            elif letter.islower():
                if num > ord('z'):
                    num -= 26
                elif num < ord('a'):
                    num += 26
            decrypted += chr(num)
        else: decrypted += letter
    return decrypted


def leetFunc(word):
    leetlist = list()
    leetRecurse(word, leetlist, '')
    answerlist = list()

    for x in leetlist:
        allalpha = False
        for y in x:
            if y.isalpha():
                if y.isupper() or y.islower():
                    allalpha=True
                else:
                    break
            else:
                break
        if allalpha:
            if len(x) == len(word):
                answerlist.append(x)
    return answerlist

def leetRecurse(word,leetlist,prev):
    mapper = [['4'],['8'],[],['0'],['3'],[],['6','9'],['4'],['1'],
              ['9','7'],[],['1','7'],['3'],[],['0'],[],[],[],['5'],
              ['7'],[],[],['3'],['8'],['4'],['2']]
    taboo = ['c','C','D','d','F','f','k','K','n','P','p','q','Q','r','u','v','w','N','R','U','V','W','X']
    for letter in word:
        if letter.isalpha() and letter not in taboo:
            if letter.isupper():
                index = ord(letter) - 65
            else:
                index = ord(letter) - 97

            for x in mapper[index]:
                leetlist.append(prev+x)
                leetRecurse(word[(word.find(letter)+1):], leetlist, prev+x)
        else:
            leetlist.append(prev+letter)
            leetRecurse(word[(word.find(letter)+1):], leetlist, prev+letter)


def salting(word):
    saltlist = list()
    salted = word[(len(word)-5):]
    unsalted = word[:(len(word)-5)]
    onlynums = True
    for s in unsalted:
        if s.isalpha():
             onlynums = False
             break
    if onlynums:
        saltingRecurse(len(salted), salted, saltlist,'')
    finalsalt = list()
    for x in saltlist:
        finalsalt.append(unsalted+x)
    return finalsalt
        


def saltingRecurse(wlen, salted, saltlist,prev):
    for num in salted:
        for x in range(0,9):
            if wlen == len(prev+str(x)):
                saltlist.append(prev+str(x))
            saltingRecurse(wlen, salted[(salted.find(num)+1):], saltlist, prev+str(x))


def dictionaryBrute(user_id, user_pass_enc, caesar, salt, leet):
    dictionary = open(DICT,"r")
    found_passwords = list()
    for line in dictionary.readlines():
        word = line.strip()
        if caesar:
            for shift in range(26):
                word = caesarShifter(word,shift)
                if dictionaryHelper(word, user_id, user_pass_enc) and word not in found_passwords:
                    found_passwords.append(word)
                    return True
        elif salt:
            saltlist = salting(word)
            for saltword in saltlist:
                if dictionaryHelper(saltword, user_id, user_pass_enc) and saltword not in found_passwords:
                    found_passwords.append(saltword)
                    return True
        elif leet:
            leetvar = leetFunc(word)
            for leetword in leetvar:
                if dictionaryHelper(leetword, user_id, user_pass_enc) and leetword not in found_passwords:
                    found_passwords.append(leetword)
                    return True
        else:
            if dictionaryHelper(word, user_id, user_pass_enc) and word not in found_passwords:
                found_passwords.append(word)
                return True
    return False

def dictionaryHelper(word, user_id, user_pass_enc):
    ap = list()
    ap.append(hashlib.sha1(word.encode()).hexdigest())
    ap.append(hashlib.sha384(word.encode()).hexdigest())
    ap.append(hashlib.sha224(word.encode()).hexdigest())
    ap.append(hashlib.sha256(word.encode()).hexdigest())
    ap.append(hashlib.sha512(word.encode()).hexdigest())
    ap.append(hashlib.md5(word.encode()).hexdigest())
    ap.append(hashlib.blake2b(word.encode()).hexdigest())
    ap.append(hashlib.blake2s(word.encode()).hexdigest())
    if user_pass_enc in ap:
        print("$$$$$$$$--PASSWORD FOUND--$$$$$$$$$$")
        print("User: ",user_id)
        print("Password: ",word)
        print("************************************\n")
        return True
    return False





def main():
    shadow = open(SHDW,"r")
    pass_crack = open(PSSWD,"r")

    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Shadow File: ", SHDW)
    print("Dictionary File: ", DICT)
    print("Password Output File: ", pass_crack)
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")

    for x in shadow:
        user = x.split(":")
        user_id = user[0]
        user_pass_enc = user[1].strip()
        found_pass = False
        if not dictionaryBrute(user_id, user_pass_enc, False, False, False): #Regular Dictionary
            if not dictionaryBrute(user_id,user_pass_enc,True, False, False): #Caesar Shift
                if not dictionaryBrute(user_id, user_pass_enc, False, True, False): #Salted
                    #if not dictionaryBrute(user_id, user_pass_enc, False, False, True): #Leet
                    print("\n\nXXXXXXXX Nothing Found XXXXXXXXXX\n\n")



if __name__ == '__main__':
    main()

