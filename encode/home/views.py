from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import string
import math
def caesar_cipher(text, key):
    result = ''
    for char in text:
        if char.isalpha():
            shift = key % 26
            if char.islower():
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            else:
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        else:
            result += char
    return result


def vernam_cipher(plain_text,key):

    # convert into lower cases and remove spaces
    
    plain_text=plain_text.replace(" ","")
    key=key.replace(" ","")
    plain_text=plain_text.lower()
    key=key.lower()
    
    # conditional statements
    if(len(plain_text)!=len(key)):
        cipher_text="Lengths are different"
        
    else:
        cipher_text=""
        
        # iterating through the length
        for i in range(len(plain_text)):
            k1=ord(plain_text[i])-97
            k2=ord(key[i])-97
            s=chr((k1+k2)%26+97)
            cipher_text+=s
        return cipher_text

def encode(request):
    if request.method == 'POST':
        algorithm = request.POST['algorithm']
        input_text = request.POST['input-text']
        input_key = request.POST['input-key']

        if algorithm == 'caesar':
            result = caesar_cipher(input_text, int(input_key))
        elif algorithm == 'vernam':
            result = vernam_cipher(input_text, input_key)
        elif algorithm == 'railfence':
            result = railfence(input_text, int(input_key))
        elif algorithm == 'column':
            result = column(input_text, input_key)
        elif algorithm == 'vigenere':
            result = vigenere_encrypt(input_text, input_key)
        #elif algorithm == 'hill':
           # result = hill(input_text, input_key)
        elif algorithm == 'atbash':
            result = atbash(input_text,int(input_key))
        elif algorithm == 'playfair':
            result = playfair(input_text, input_key)
        

        return render(request, 'encode.html', {'result': result})

    return render(request, 'encode.html')
# Create your views here.
def index(request):
    return render(request, 'index.html')






def about(request):
    return HttpResponse("about page")

def learn(request):
    return HttpResponse("learn page")

def sequence(n):
    arr=[]
    i=0
    # creating the sequence required for
    # implementing railfence cipher
    # the sequence is stored in array
    while(i<n-1):
        arr.append(i)
        i+=1
    while(i>0):
        arr.append(i)
        i-=1
    return(arr)

# this is to implement the logic
def railfence(s,n):
    # converting into lower cases
    s=s.lower()

    # If you want to remove spaces,
    # you can uncomment this
    # s=s.replace(" ","")

    # returning the sequence here
    L=sequence(n)
    

    # storing L in temp for reducing additions in further steps
    temp=L
    
    # adjustments
    while(len(s)>len(L)):
        L=L+temp

    # removing the extra last indices
    for i in range(len(L)-len(s)):
        L.pop()
    

    # converting into cipher text
    num=0
    cipher_text=""
    while(num<n):
        for i in range(L.count(num)):
            # adding characters according to
            # indices to get cipher text
            cipher_text=cipher_text+s[L.index(num)]
            L[L.index(num)]=n
        num+=1
    return cipher_text
   

def column(s,key):
    
    # to remove repeated alphabets in key
    temp=[]
    for i in key:
        if i not in temp:
            temp.append(i)
    k=""
    for i in temp:
        k+=i
    
    # ceil is used to adjust the count of
    # rows according to length of message
    b=math.ceil(len(s)/len(k))
    
    # if b is less than length of key, then it will not form square matrix when
    # length of meessage not equal to rowsize*columnsize of square matrix
    if(b<len(k)):
        b=b+(len(k)-b)
    # if b is greater than length of key, then it will not from a
    # square matrix, but if less then length of key, we have to add padding
    
    arr=[['_' for i in range(len(k))]
         for j in range(b)]
    i=0
    j=0
    # arranging the message into matrix
    for h in range(len(s)):
        arr[i][j]=s[h]
        j+=1
        if(j>len(k)-1):
            j=0
            i+=1
    
    for i in arr:
        print(i)

    cipher_text=""
    # To get indices as the key numbers instead of alphabets in the key, according
    # to algorithm, for appending the elementsof matrix formed earlier, column wise.
    kk=sorted(k)
    
    for i in kk:
        # gives the column index
        h=k.index(i)
        for j in range(len(arr)):
            cipher_text+=arr[j][h]
    return cipher_text



def vigenere_encrypt(plain_text, key):
    encrypted_text = ""
    key_index = 0
    for char in plain_text:
        if char.isalpha():
            encrypted_text += chr(((ord(char.lower()) - 97 + ord(key[key_index].lower()) - 97) % 26) + 97)
            key_index = (key_index + 1) % len(key)
        else:
            encrypted_text += char
    return encrypted_text




def atbash(input_text, key):
    # create a dictionary to map each letter to its Atbash equivalent
    atbash_dict = {'a': 'z', 'b': 'y', 'c': 'x', 'd': 'w', 'e': 'v',
                    'f': 'u', 'g': 't', 'h': 's', 'i': 'r', 'j': 'q',
                    'k': 'p', 'l': 'o', 'm': 'n', 'n': 'm', 'o': 'l',
                    'p': 'k', 'q': 'j', 'r': 'i', 's': 'h', 't': 'g',
                    'u': 'f', 'v': 'e', 'w': 'd', 'x': 'c', 'y': 'b', 'z': 'a'}

    # convert the input_text to lowercase
    input_text = input_text.lower()

    # encrypt the input_text using the Atbash dictionary and the key
    cipher_text = ""
    for char in input_text:
        if char in atbash_dict:
            # shift the letter by the key value
            shifted_char = chr((ord(atbash_dict[char]) - ord('a') + key) % 26 + ord('a'))
            cipher_text += shifted_char
        else:
            cipher_text += char

    return cipher_text

def playfair(plain_text, key):
    # Call the key_generation function to generate the key_matrix
    key_matrix = key_generation(key)

    # Call the conversion function with the plain_text
    cipher_text = conversion(plain_text, key_matrix)

    return cipher_text
def key_generation(key):
    # initializing all and generating key_matrix
    main=string.ascii_lowercase.replace('j','.')
    # convert all alphabets to lower
    key=key.lower()
    
    key_matrix=['' for i in range(5)]
    # if we have spaces in key, those are ignored automatically
    i=0;j=0
    for c in key:
        if c in main:
            # putting into matrix
            key_matrix[i]+=c

            # to make sure repeated characters in key
            # doesnt include in the key_matrix, we replace the
            # alphabet into . in the main, whenever comes in iteration
            main=main.replace(c,'.')
            # counting column change
            j+=1
            # if column count exceeds 5
            if(j>4):
                # row count is increased
                i+=1
                # column count is set again to zero
                j=0

    # to place other alphabets in the key_matrix
    # the i and j values returned from the previous loop
    # are again used in this loop, continuing the values in them
    for c in main:
        if c!='.':
            key_matrix[i]+=c

            j+=1
            if j>4:
                i+=1
                j=0
                
    return(key_matrix)


# Now plaintext is to be converted into cipher text

def conversion(plain_text,key_matrix):
    # seggrigating the maeesage into pairs
    plain_text_pairs=[]
    # replacing repeated characters in pair with other letter, x
    cipher_text_pairs=[]

    # remove spaces
    plain_text=plain_text.replace(" ","")
    # convert to lower case
    plain_text=plain_text.lower()

    # RULE1: if both letters in the pair are same or one letter is left at last,
    # replace second letter with x or add x, else continue with normal pairing

    i=0
    # let plain_text be abhi
    while i<len(plain_text):
        # i=0,1,2,3
        a=plain_text[i]
        b=''

        if((i+1)==len(plain_text)):
            # if the chosen letter is last and doesnt have pair
            # then the pai will be x
            b='x'
        else:
            # else the next letter will be pair with the previous letter
            b=plain_text[i+1]

        if(a!=b):
            plain_text_pairs.append(a+b)
            # if not equal then leave the next letter,
            # as it became pair with previous alphabet
            i+=2
        else:
            plain_text_pairs.append(a+'x')
            # else dont leave the next letter and put x
            # in place of repeated letter and conitnue with the next letter
            # which is repeated (according to algo)
            i+=1
            

    for pair in plain_text_pairs:
        # RULE2: if the letters are in the same row, replace them with
        # letters to their immediate right respectively
        flag=False
        for row in key_matrix:
            if(pair[0] in row and pair[1] in row):
                # find will return index of a letter in string
                j0=row.find(pair[0])
                j1=row.find(pair[1])
                cipher_text_pair=row[(j0+1)%5]+row[(j1+1)%5]
                cipher_text_pairs.append(cipher_text_pair)
                flag=True
        if flag:
            continue

        # RULE3: if the letters are in the same column, replace them with
        # letters to their immediate below respectively
                
        for j in range(5):
            col="".join([key_matrix[i][j] for i in range(5)])
            if(pair[0] in col and pair[1] in col):
                # find will return index of a letter in string
                i0=col.find(pair[0])
                i1=col.find(pair[1])
                cipher_text_pair=col[(i0+1)%5]+col[(i1+1)%5]
                cipher_text_pairs.append(cipher_text_pair)
                flag=True
        if flag:
            continue
        #RULE:4 if letters are not on the same row or column,
        # replace with the letters on the same row respectively but
        # at the other pair of corners of rectangle,
        # which is defined by the original pair

        i0=0
        i1=0
        j0=0
        j1=0

        for i in range(5):
            row=key_matrix[i]
            if(pair[0] in row):
                i0=i
                j0=row.find(pair[0])
            if(pair[1] in row):
                i1=i
                j1=row.find(pair[1])
        cipher_text_pair=key_matrix[i0][j1]+key_matrix[i1][j0]
        cipher_text_pairs.append(cipher_text_pair)
    cipher_text = "".join(cipher_text_pairs)
    return cipher_text


def decode(request):
    if request.method == 'POST':
        algorithm = request.POST['algorithm']
        input_text = request.POST['input-text']
        input_key = request.POST['input-key']

        if algorithm == 'caesar':
            result = caesar_decrypt(input_text, int(input_key))
        elif algorithm == 'vernam':
            result = vernam_decrypt(input_text, input_key)
        elif algorithm == 'railfence':
            result = decrypt_railfence(input_text, int(input_key))
        elif algorithm == 'column':
            result = uncolumn(input_text, input_key)
        elif algorithm == 'vigenere':
            result = vigenere_decrypt(input_text, input_key)
        #elif algorithm == 'hill':
           # result = hill(input_text, input_key)
        elif algorithm == 'atbash':
            result = atbash_decrypt(input_text,int(input_key))
        elif algorithm == 'playfair':
            result = playfair_decrypt(input_text, input_key)
        

        return render(request, 'decode.html', {'result': result})

    return render(request, 'decode.html')


def caesar_decrypt(text, key):
    result = ''
    for char in text:
        if char.isalpha():
            shift = -key % 26
            if char.islower():
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            else:
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        else:
            result += char
    return result

def vernam_decrypt(cipher_text, key):
    # convert into lower cases and remove spaces
    cipher_text = cipher_text.replace(" ", "")
    key = key.replace(" ", "")
    cipher_text = cipher_text.lower()
    key = key.lower()

    # conditional statements
    if len(cipher_text) != len(key):
        plain_text = "Lengths are different"
    else:
        plain_text = ""

        # iterating through the length
        for i in range(len(cipher_text)):
            k1 = ord(cipher_text[i]) - 97
            k2 = ord(key[i]) - 97
            s = chr((k1 - k2) % 26 + 97)
            plain_text += s

    return plain_text
def sequenced(n):
    arr=[]
    i=0
    # creating the sequence required for
    # implementing railfence cipher
    # the sequence is stored in array
    while(i<n-1):
        arr.append(i)
        i+=1
    while(i>0):
        arr.append(i)
        i-=1
    return(arr)

# this is to implement the logic
def decrypt_railfence(cipher_text,n):
    # converting into lower cases
    cipher_text=cipher_text.lower()

    # If you want to remove spaces,
    # you can uncomment this
    # s=s.replace(" ","")

    # returning the sequence here
    L=sequenced(n)

    # storing L in temp for reducing additions in further steps
    # if not stored and used as below, the while loop
    # will create L of excess length
    temp=L
    
    # adjustments
    while(len(cipher_text)>len(L)):
        L=L+temp

    # removing the extra last indices
    for i in range(len(L)-len(cipher_text)):
        L.pop()
        
    # storing L.sort() in temp1
    temp1=sorted(L)
    
    

    # converting into plain text
    plain_text=""
    for i in L:
        # k is index of particular character in the cipher text
        # k's value changes in such a way that the order of change
        # in k's value is same as plaintext order
        k=temp1.index(i)
        temp1[k]=n
        plain_text+=cipher_text[k]
        
    return plain_text

def uncolumn(cipher_text, key):
    # to remove repeated alphabets in key
    temp = []
    for i in key:
        if i not in temp:
            temp.append(i)
    k = ""
    for i in temp:
        k += i

    # floor is used to adjust the count of
    # rows according to length of message
    b = math.floor(len(cipher_text) / len(k))

    # if b is less than length of key, then it will not form square matrix when
    # length of message not equal to rowsize*columnsize of square matrix
    if (b < len(k)):
        b = b + (len(k) - b)

    # if b is greater than length of key, then it will not from a
    # square matrix, but if less then length of key, we have to add padding
    arr = [['_' for i in range(len(k))]
           for j in range(b)]

    # To get indices as the key numbers instead of alphabets in the key, according
    # to algorithm, for arranging the characters column-wise.
    kk = sorted(k)

    i = 0
    j = 0
    for h in range(len(cipher_text)):
        arr[i][j] = cipher_text[h]
        j += 1
        if (j > len(k) - 1):
            j = 0
            i += 1

    plain_text = ""
    for i in kk:
        # gives the column index
        h = k.index(i)
        for j in range(b):
            plain_text += arr[j][h]

    return plain_text


def vigenere_decrypt(cipher_text, key):
    decrypted_text = ""
    key_index = 0
    for char in cipher_text:
        if char.isalpha():
            decrypted_text += chr(((ord(char.lower()) - 97 - ord(key[key_index].lower()) - 97 + 26) % 26) + 97)
            key_index = (key_index + 1) % len(key)
        else:
            decrypted_text += char
    return decrypted_text

def atbash_decrypt(cipher_text, key):
    # create a dictionary to map each letter to its Atbash equivalent
    atbash_dict = {'a': 'z', 'b': 'y', 'c': 'x', 'd': 'w', 'e': 'v',
                    'f': 'u', 'g': 't', 'h': 's', 'i': 'r', 'j': 'q',
                    'k': 'p', 'l': 'o', 'm': 'n', 'n': 'm', 'o': 'l',
                    'p': 'k', 'q': 'j', 'r': 'i', 's': 'h', 't': 'g',
                    'u': 'f', 'v': 'e', 'w': 'd', 'x': 'c', 'y': 'b', 'z': 'a'}

    # convert the cipher_text to lowercase
    cipher_text = cipher_text.lower()

    # decrypt the cipher_text using the Atbash dictionary and the key
    plain_text = ""
    for char in cipher_text:
        if char in atbash_dict:
            # shift the letter back by the key value
            shifted_char = chr((ord(char) - ord('a') - key) % 26 + ord('a'))
            plain_text += atbash_dict.get(shifted_char, shifted_char)
        else:
            plain_text += char

    return plain_text

import string

def playfair_decrypt(cipher_text, key):
    # Call the key_generation function to generate the key_matrix
    key_matrix = key_generation(key)

    # Call the decryption function with the cipher_text
    plain_text = decryption(cipher_text, key_matrix)

    return plain_text

def decryption(cipher_text, key_matrix):
    # Segregating the message into pairs
    cipher_text_pairs = [cipher_text[i:i+2] for i in range(0, len(cipher_text), 2)]
    plain_text_pairs = []

    for pair in cipher_text_pairs:
        flag = False
        # Check for same row
        for row in key_matrix:
            if pair[0] in row and pair[1] in row:
                j0 = row.find(pair[0])
                j1 = row.find(pair[1])
                plain_text_pair = row[(j0-1) % 5] + row[(j1-1) % 5]
                plain_text_pairs.append(plain_text_pair)
                flag = True
                break

        if flag:
            continue

        # Check for same column
        for j in range(5):
            col = "".join([key_matrix[i][j] for i in range(5)])
            if pair[0] in col and pair[1] in col:
                i0 = col.find(pair[0])
                i1 = col.find(pair[1])
                plain_text_pair = col[(i0-1) % 5] + col[(i1-1) % 5]
                plain_text_pairs.append(plain_text_pair)
                flag = True
                break

        if flag:
            continue

        # Check for different row and column
        i0, i1, j0, j1 = 0, 0, 0, 0
        for i in range(5):
            row = key_matrix[i]
            if pair[0] in row:
                i0 = i
                j0 = row.find(pair[0])
            if pair[1] in row:
                i1 = i
                j1 = row.find(pair[1])

        plain_text_pair = key_matrix[i0][j1] + key_matrix[i1][j0]
        plain_text_pairs.append(plain_text_pair)

    # Join pairs into plaintext
    plain_text = "".join(plain_text_pairs)

    # Remove padding
    plain_text = plain_text.replace('x', '')

    return plain_text

# Example usage

def vigenere_decrypt(cipher_text, key):
    decrypted_text = ""
    key_index = 0
    for char in cipher_text:
        if char.isalpha():
            decrypted_text += chr(((ord(char.lower()) - ord(key[key_index].lower()) + 26) % 26) + 97)
            key_index = (key_index + 1) % len(key)
        else:
            decrypted_text += char
    return decrypted_text