'''
Program: CS 1301 Lab 11
Author: Ali Vafaeian and Toan Le

Purpose:
    Create a hangman video game that uses everything we have learned so far this year

Pre-conditions:
    Generate a random word from a text file that contains many words.
    Take in an input from the user which is their guess of a letter in that word.
        Make sure that they enter a valid character, specifically a letter.


Post-conditions:
    Print the list of random numbers in a test.txt file and the prime number inside of prime.txt file
    Print everything inside of the window as well to make testing easier
'''
# rules:
# if user does not enter a valid difficulty choice, program will quit
# valid difficulty inputs are: easy/medium/hard/extreme or 1/2/3/4

import random
import requests
import pip._vendor.requests
import json

masterList = []
masterListByLength = []
def hangmanGraphic(lifeNum):
    if lifeNum == 0:
        print(" ")
        print("_______")
        print("|     |")
        print("|      ")
        print("|      ")
        print("|      ")
        print("|      ")

    elif lifeNum == 1:
        print(" ")
        print("_______")
        print("|     |")
        print("|     0")
        print("|      ")
        print("|      ")
        print("|      ")

    elif lifeNum == 1:
        print(" ")
        print("_______")
        print("|     |")
        print("|     0")
        print("|      ")
        print("|      ")
        print("|      ")

    elif lifeNum == 2:
        print(" ")
        print("_______")
        print("|     |")
        print("|     0")
        print("|     |")
        print("|      ")
        print("|      ")

    elif lifeNum == 3:
        print(" ")
        print("_______")
        print("|     |")
        print("|     0")
        print("|     |")
        print("|    / ")
        print("|      ")

    elif lifeNum == 4:
        print(" ")
        print("_______")
        print("|     |")
        print("|     0")
        print("|     |")
        print("|    / \\")
        print("|      ")

    elif lifeNum == 5:
        print(" ")
        print("_______")
        print("|     |")
        print("|     0")
        print("|    /|")
        print("|    / \\")
        print("|      ")

    else:
        print(" ")
        print("_______")
        print("|     |")
        print("|     0")
        print("|    /|\\")
        print("|    / \\")
        print("|      ")
# read text file and store words into list
def storeWordsIntoList():

    # list of 58109 words
    with open('wordlist.txt','r') as f:
        for line in f:
            temp = line.strip()
            masterList.append(temp)

    masterList.sort(key=len)


    # sort words in list into 2d list sorted by length
    dict = {}
    for word in masterList:
        if len(word) not in dict:
            dict[len(word)] = [word]
        elif len(word) in dict:
            dict[len(word)] += [word]

    for key in sorted(dict):
        masterListByLength.append(dict[key])
storeWordsIntoList()

# Get API from dictionaryapi and return the definition
def getAPI(word):
    webString = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
    #response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/life")
    response = requests.get(webString)
    if response.status_code == 200:
        text = response.json()
        #print(text)
        meaning = text[0]['meanings'][0]['definitions'][0]['definition']
        return meaning
    else:
        return 'null'



# [[1,2,3],[3,4,5]]
# return word depending on difficulty picked
def getWord(difficulty):
    temp = 0
    secretWord = 0
    # easy would return words with length from 4 to 6
    if difficulty == 'easy' or difficulty == '1':
        # randomized length of word
        temp = random.randint(2,4)
        # randomized word in that length
        secretWord = random.randint(0,len(masterListByLength[temp])-1)

    # medium would return words with length from 7 to 9
    elif difficulty == 'medium' or difficulty == '2':
        temp = random.randint(5, 7)
        secretWord = random.randint(0, len(masterListByLength[temp]) - 1)

    # hard would return words with length from 10 to 12
    elif difficulty == 'hard' or difficulty == '3':
        temp = random.randint(8, 10)
        secretWord = random.randint(0, len(masterListByLength[temp]) - 1)

    # extreme would return words with length from 13 to 15
    elif difficulty == 'extreme' or difficulty == '4':
        temp = random.randint(11, 13)
        secretWord = random.randint(0, len(masterListByLength[temp]) - 1)
    else:
        return 0
    # return the word by difficulty
    return masterListByLength[temp][secretWord]


# index 0, length 2
# index 1, length 3
# index 2, length 4
# index 3, length 5
# index 4, length 6
# index 5, length 7
# index 6, length 8
# index 7, length 9
# index 8, length 10
# index 9, length 11
# index 10, length 12

def gameRules():
    print('Welcome to the Hangman Game! \n')
    print('There are 4 difficulty modes')
    print('EASY, MEDIUM, HARD, EXTREME')
    print('Please enter the difficulty: 1, 2, 3, 4')
    difficulty = str(input('')).lower()
    return difficulty

def checkUserInput(inputStr):
    specialCharacter = "~`!@#$%^&*()_+-=[]\{}|;':\"\,./<>?"
    if len(inputStr) > 1:
        print('Please enter one character only. ')
        return ''
    elif inputStr.isdigit():
        print('Please enter a letter only. ')
        return ''
    elif inputStr in specialCharacter:
        print('Please enter a letter only. ')
        return ''
    else:
        return inputStr

def lifeGraphics(life, hangman,word):
    hangmanGraphic(life)
    if life == 2 and hangman[0] == '_':
        print("You seem like you having some trouble.")
        print("Here's a hint: ")
        print('The first letter of this word is: ',word[0])
    elif life == 4:
        print('Hmm... more trouble I see.')
        print("Here's another hint: ")
        print('This word means: ', getAPI(word))
    elif life == 6:
        hangmanGraphic(life)
        print('You gotten 6 wrong and lost!')
        #
        print(f'The word is {word}.')
        return False

def setupGame():
    # set life to 0
    life = 0
    counter = 0
    # create new string to store words that have been entered
    entered = ''

    # get secret word
    word = getWord(gameRules())
    if word == 0:
        quit('Invalid input')

    hangman = ''
    for i in range(len(word)):
        hangman += '_'
    #print(hangman)
    #print(word)
    stillPlaying = True

    while stillPlaying:
        print(hangman)
        # setup hang man

        userGuess = input('\nEnter a character ')
        validatedUserGuess = checkUserInput(userGuess)
        if str(validatedUserGuess) not in entered:
            entered += str(validatedUserGuess) + ' '
        else:
            print('You have already entered this character')

        print('You have entered',entered)
        # keep a counter of how many times user has guessed
        counter += 1
        if userGuess == validatedUserGuess:
            # if user guessed wrong, then take away a life
            if validatedUserGuess not in word:
                print('Not quite correct, try again.')
                life += 1
                print('Wrong answers left: ', (6 - life))
            for i in range(len(word)):
                if validatedUserGuess == word[i]:
                    hangman = hangman[:i] + word[i] + hangman[i + 1:]

        gameStatus = lifeGraphics(life, hangman,word)
        if gameStatus == False:
            break
        # check to see if user got everything right
        if hangman == word:
            print('You got it!')
            print('The word is', word.upper())
            print(f'It only took you {counter} tries.')
            stillPlaying = False
            return False

def playGame():
    while True:
        playGame = str(input("Do you want to play the Hangman game? Yes(1) No(2)\n"))
        if playGame == "y" or "Y" or "1":
            setupGame()
        else:
            break
        continue
playGame()
