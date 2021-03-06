import hashlib
import random as rand

SHDW = 'shadow'
PSSWD = 'passwords.txt'
DICT = 'dictionary.txt'


#Caesar shifter function
def caesarShifter(word,shift):
    decrypted = ''
    for letter in word: #for each letter in the word
        if letter.isalpha():
            num = ord(letter)
            num -= shift #shift correspondingly

            
            if letter.isupper():
                if num > ord('Z'): #need to reset to loop if it goes past edge case
                    num -= 26
                elif num < ord('A'): 
                    num += 26
            elif letter.islower(): #upper and low have different edge cases
                if num > ord('z'):
                    num -= 26
                elif num < ord('a'):
                    num += 26
            decrypted += chr(num) #converts num to alphabet
        else: decrypted += letter #appends letter to word being formed.
    return decrypted


def leetFunc(word): #this is base function
    leetlist = list()
    leetRecurse(word, leetlist, '')
    answerlist = list()
    return leetlist
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
              ['7'],[],[],['3'],['8'],['4'],['2']] #letters that resemble number, had to play around with this one
                                                   #blank spaces are irrelevant and was just easier to index
    
    #gave me trouble and I thought weren't relevant, so made iterater skip these letters
    taboo = ['c','C','D','d','F','f','k','K','n','P','p','q','Q','r','u','v','w','N','R','U','V','W','X']

    for letter in word: 
        if letter.isalpha() and letter not in taboo:
            if letter.isupper():
                index = ord(letter) - 65 #used this to get corresponding number from mapper array
                                         #subtracting 65 and 79 for bottom one started index at 0
            else:
                index = ord(letter) - 97

            for x in mapper[index]: #if there were more than one number in sub array
                leetlist.append(prev+x)
                leetRecurse(word[(word.find(letter)+1):], leetlist, prev+x) #has to recurse through all options 
                                                                            #using current string for future use too
        else: #if letter was a number
            leetlist.append(prev+letter)
            leetRecurse(word[(word.find(letter)+1):], leetlist, prev+letter)


def salting(word):
    saltlist = list()
    salted = "00000" #arbitrary value
    saltingRecurse(len(salted), salted, saltlist,'') #salt list contains all permutations of each digit place 0-9
    finalsalt = list()
    for x in saltlist:
        finalsalt.append(word+x) #prepends dictionary word to each permutation in saltlist
    return finalsalt
        


def saltingRecurse(wlen, salted, saltlist,prev):
    for num in salted:
        for x in range(0,10): #range (0,9) only goes to 8
            if wlen == len(prev+str(x)): #add only qualified length strings to list
                saltlist.append(prev+str(x)) #prev stores current string for future recursions
            saltingRecurse(wlen, salted[(salted.find(num)+1):], saltlist, prev+str(x)) #update prev and add updated list



#Main Dictionary that calls conditionally LEET and Salt
def dictionaryBrute(user_id, user_pass_enc, caesar, salt, leet):
    dictionary = open(DICT,"r")
    found_passwords = list()
    for line in dictionary.readlines():
        word = line.strip()
        if caesar: #caesar shift
            for shift in range(26): #26 alphabets, so can be shifted max 26 positions
                word = caesarShifter(word,shift) #caesarShifter function returns shifted word
                if dictionaryHelper(word, user_id, user_pass_enc) and word not in found_passwords:
                    found_passwords.append(word)
                    return True
        elif salt: #loops through all 100,000 permutations appended to dictionary word
            saltlist = salting(word) #salting function called to return list
            for saltword in saltlist:
                if dictionaryHelper(saltword, user_id, user_pass_enc) and saltword not in found_passwords:
                    found_passwords.append(saltword) #to prevent duplicates
                    return True
        elif leet:
            leetvar = leetFunc(word) #leetFunc returns all permutations of "word" in leetvar list
            for leetword in leetvar:
                if dictionaryHelper(leetword, user_id, user_pass_enc) and leetword not in found_passwords:
                    found_passwords.append(leetword)
                    return True
        else:
            if dictionaryHelper(word, user_id, user_pass_enc) and word not in found_passwords:
                found_passwords.append(word)
                return True
    return False

#Second work horse of this program
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
    ap.append(hash(word))
    #use this in analysis.py as well
    #just checks if user hashed password is in a list of all the possible hashed passwords for a dictionary word
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

        # calls on functions.
        #********************* Important *********************************
        # if you run this, my user2 will take a very long time to work, so 
        # commenting out the last if will allow the others to run
        # leet takes quite a while to run too
        if not dictionaryBrute(user_id, user_pass_enc, False, False, False): #Regular Dictionary
            if not dictionaryBrute(user_id,user_pass_enc,True, False, False): #Caesar Shift
                if user_id != "user2": #segfaults on leet if its user2, so comment out ***important****
                #leet takes a while for user4 but eventually gets it
                    if not dictionaryBrute(user_id, user_pass_enc, False, False, True): #Leet
                    #if not dictionaryBrute(user_id, user_pass_enc, False, True, False): #Salt
                        print("\n\nXXXXXXXX Nothing Found XXXXXXXXXX\n\n")



if __name__ == '__main__':
    main()

