import hashlib


def cymapper(dword):
    abcmap ="abcdefghijklmnopqrstuvwxyz"
    cymap = ['s','g','q','u','n','t','i','v','d','b','e','j','r','o','z','h','p','y','f','c','l','w','x','m','k','a']
    cw = ''
    # appends each new equivalent letter to the previous
    for dl in dword:
        if dl in cymap:
            index = abcmap.find(dl) #had to flip to use abcmap bc I was using cymap before
            cw+=str(cymap[index])
        else: #if there was like a comma or a space
            cw+=dl
    return cw.strip()


def mapletters(letter): #this function just prints out the plaintext
    cymap = ['s','g','q','u','n','t','i','v','d','b','e','j','r','o','z','h','p','y','f','c','l','w','x','m','k','a']
    abcmap ="abcdefghijklmnopqrstuvwxyz"
    if letter in cymap:
        index = cymap.index(letter)
        return str(abcmap[index])
    else:
        return letter


def main():
    encryptext = open('encrypted.txt','r')
    shadow = open('shadow','r')
    dictionary = open('dictionary.txt','r')

    user = shadow.readlines()[6]
    psswd = user.split(":")[1].strip()
    encrypt_store = []
    
    #prints plaintext
    while 1: #reads every individual character
        character = encryptext.read(1)
        if not character:
            break
        print(mapletters(character),end='')
    
    
    #goes through all of dictionary
    for line in dictionary.readlines():
        word = line.strip()
        mappedword = cymapper(word)
        #print(word," ",mappedword)
        #print("\n")
        if dictionaryHelper(mappedword.strip(),psswd):
            break 
    
    #used this same helper in password_cracker.py
def dictionaryHelper(word, user_pass):
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
    
    #checks if userpassword is one of the hashed ones
    if user_pass in ap:
        print("YES, you're the best! The password ---> ",word)
        return True
    return False
    





if __name__ == "__main__":
    main()
