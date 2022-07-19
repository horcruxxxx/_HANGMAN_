# install prettytable first using pip.
import random                           #For Selecting Random Word.
import sqlite3                          #For Creating and Mantaining of Database.
from prettytable import PrettyTable     #For Using Tables. 

conn = sqlite3.connect('_scores.db_')
#If Not connected ,then it will create a new database.Else It get connected to the existing databse.

#kidly comment out upto line 17('conn.close()') once the database wass created in your local file system OR delete the database mannualy on your system 
c=conn.cursor()
c.execute("""CREATE TABLE score(    #creating Table for the first time.
        first text,
        second text,
        third integer
        )""")
conn.commit()
conn.close()

HANGMAN_PICS = ['''
  +---+
      |
      |
      |
     ===''', '''
  +---+
  O   |
      |
      |
     ===''', '''
  +---+
  O   |
  |   |
      |
     ===''', '''
  +---+
  O   |
 /|   |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
 /    |
     ===''', '''
  +---+
  O   |
 /|\  |
 / \  |
     ===''', '''
  +---+
 [O   |
 /|\  |
 / \  |
     ===''', '''
  +---+
 [O]  |
 /|\  |
 / \  |
     ===''']        
     
#we created 4 strings which would help us to select the RANDOM word as per the difficulty level.    
words   = 'circle triangle square rhombus rectangles ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split()
Animals = 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split()
Shapes  = 'circle triangle square rhombus rectangle'.split()
Places   = 'india america russia nepal china'.split()                

def getRandomWord(wordList):
    # This function returns a random string from the passed list of strings.
    wordIndex = random.randint(0, len(wordList) - 1)
    return wordList[wordIndex]

def displayBoard(missedLetters, correctLetters, secretWord):
    print(HANGMAN_PICS[len(missedLetters)])
    print()
 
    print('Missed letters:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')
    print()

    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)): # Replace blanks with correctly guessed letters.
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

    for letter in blanks: # Show the secret word with spaces in between each letter.
        print(letter, end=' ')
    print()

def getGuess(alreadyGuessed):
    # Returns the letter the player entered. This function makes sure the player entered a single letter and not something else.
    while True:
        print('Guess a letter.')
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess

def playAgain():
    # This function returns True if the player wants to play again; otherwise, it returns False.
    print('Do you want to play again? (press y for --yes   OR    press any other key for --no)')
    return input().lower().startswith('y')
    
def start_game(difficulty,secretWord,name,missedLetters,correctLetters,Lives):
    # This function Starts the game whenever user wants to play.
    gameIsDone = False
    while True:
        displayBoard(missedLetters, correctLetters, secretWord)
    
        # Let the player enter a letter.
        guess = getGuess(missedLetters + correctLetters)
    
        if guess in secretWord:
            correctLetters = correctLetters + guess
    
            # Check if the player has won.
            foundAllLetters = True
            for i in range(len(secretWord)):
                if secretWord[i] not in correctLetters:
                    foundAllLetters = False
                    break
            if foundAllLetters:
                
                print('Yes! The secret word is "' + secretWord + '"! You have won!')
                conn = sqlite3.connect('_scores.db_')
                params = (difficulty,name,Lives-len(missedLetters))
                c=conn.cursor()
                c.execute("INSERT INTO score VALUES (?, ?, ?)", params)
                conn.commit()
                conn.close()
                gameIsDone = True
        else:
            missedLetters = missedLetters + guess
    
            # Check if player has guessed too many times and lost.
            if len(missedLetters) == Lives:
                displayBoard(missedLetters, correctLetters, secretWord)
                print('You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
                gameIsDone = True
    
        # Ask the player if they want to play again (but only if the game is done).
        if gameIsDone:
            if playAgain():
                dispay_levels()
                The_Beginnning()
                break
            else:
                break

def The_Beginnning():
    # This function ask for all the options provided by the game whenever called.
    missedLetters = ''
    correctLetters = ''
    query = int(input('select an Option\n'))
    while(query==0 or query>5):
        print('Thats not a valid option: TRY AGAIN\n')
        query = int(input())
    
    if(query==1 or query==2):       #This condition runs only when user choose "easy or medium" difficulty.
        display_word_section()
        choice = int(input('select an Option\n'))
        while(choice==0 or choice>3):
            print('Thats not a valid option: TRY AGAIN')
            choice = int(input())
        if(choice==1):
            secretWord = getRandomWord(Animals)
        elif(choice==2):
            secretWord = getRandomWord(Shapes)
        else:#(choice==3):
            secretWord = getRandomWord(Places)
        if(query==1):
            difficulty='Easy'
            start_game(difficulty,secretWord,name,missedLetters,correctLetters,8)
        else:#query==2                   '8' & '6' represents 'Total Lives' here.
            difficulty='Moderate'
            start_game(difficulty,secretWord,name,missedLetters,correctLetters,6)
        
    elif(query==3):                 #This condition runs only when user choose "Hard" difficulty.
        difficulty='Hard'
        secretWord = getRandomWord(words)
        start_game(difficulty,secretWord,name,missedLetters,correctLetters,6)
        
    elif(query==4):                 #This condition runs only when user wants to see the databse.
        Display_Hall_Of_Fame()
        
    elif(query==5):                 #This condition runs only when user wants to know about the game.
        display_About()
        
def dispay_levels():
    # This function displays The Different difficulty Levels of the Game and other options as well.
    myTable = PrettyTable(["Command", "Operatoin"])
 
    # Add rows
    myTable.add_row(["1","Play on Easy level"])
    myTable.add_row(["2","Play on Medium level"])
    myTable.add_row(["3", "Play on Hard level"])
    myTable.add_row(["4", "Hall of Fame"])
    myTable.add_row(["5", "About the Game"])
     
    print(myTable)
    print()
    # The_Beginnning()

def Display_Hall_Of_Fame():
    # This function displays the HALL_OF_FAME i.e. The database.
    conn = sqlite3.connect('_scores.db_')
    c=conn.cursor()
    c.execute("SELECT * FROM score")
    print(c.fetchall()) #displays the entire DATABASE.
    conn.commit()
    conn.close(); 
    print()
    if(playAgain()):
        dispay_levels()
        The_Beginnning()

    
def display_word_section():
    # This function displays the SETS Of SECRET WORDS.
    print("SELECT FROM THE FOLLOWING SETS Of SECRET WORDS")
    myTable = PrettyTable(["Command", "Operatoin"])
 
    # Add rows
    myTable.add_row(["1","Animal"])
    myTable.add_row(["2","Shapes"])
    myTable.add_row(["3", "Places"])
    print(myTable)
    
def display_About():
    #This function give details about the GAME.
    print("\t  ABOUT THE GAME")
    print("\t -----------------")
    print("your task is to choose a letter to identify the hidden SECRET WORD")
    print("if you are able to identify all the letters that are used in the word then YOU WON")
    print("too made the GAME more intresting for You ,We have 3 different Levels")
    myTable = PrettyTable(["LEVELS", "PROCEDURE"])
 
    # Add rows
    myTable.add_row(["1.Easy"," You can select the list from which the random word will be selected.Also the number of trails are 8"])
    myTable.add_row(["2.Moderate"," similar to Easy, but the number of trail will be reduced to 6."])
    myTable.add_row(["3.Hard", "You have no clue about the word which is selected along with that you have only 6 trials "])
    print(myTable)
    print()
    if(playAgain()):
        dispay_levels()
        The_Beginnning()
    

"""     Main function     """
#####################################
print('\t\t\t\t\t\t\t\tH A N G M A N')
print('\t\t\t\t\t\t\t------------------------------')
name       = input('Please Enter Your Name\n')
print('\n\tHi',name)
print('    Welcome to HANGMAN :-)\n')  
dispay_levels()
The_Beginnning()