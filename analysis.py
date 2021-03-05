import hashlib

def subRecurse

def substitutioncipher(letter,shift):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    

def cymapper(dword):
    maplist = list()
    cymap = "sgquntivdbejrozhpyfclwxmka"
    abcmap = "abcdefghijklmnopqrstuvwxyz"
    for x in cymap:
        maplist.append(x)
    cw = ''
    for dl in dword:
        if dl in abcmap:
            index = abcmap.find(dl)
            cw+=str(maplist[index])
        else:
            cw+=dl
    return cw



def main():
    encryptext = open('encrypted.txt','r')
    
    shadow = open('shadow','r')
    dictionary = open('dictionary.txt','r')

    mapping = substitutioncypher(encryptext)
    user = shadow.readlines()[6]
    psswd = user.split(":")[1]
    encrypt_store = []
    for line in dictionary.readlines():
        word = line.strip()
        mappedword = cymapper(word)
        if dictionaryHelper(mappedword,psswd):
            break

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
    if user_pass in ap:
        print("Fuck yes: ")
        print("Here's the password you beast ---> ",word)
        return True
    return False
    





if __name__ == "__main__":
    main()
