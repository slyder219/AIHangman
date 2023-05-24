import openai
import random
import os 
    
class gameplay():
    def __init__(self):
        self.answer = []
        self.curWord = []
        self.guesses = []
        self.errors = []
        self.backup = ''
        self.win = False
        self.loose = False
    # we have two bools for win or lose. This updates them and is ran at the end of the gamplay loop
    def checkWin(self):
        self.win = True
        for char in self.curWord:
            if "_" in char:
                self.win = False 
        self.loose = bool(len(self.errors) >= 6)
    # checks number of current errors and prints hangman dude 
    def printBoard(self):
        numErrors = len(self.errors)
        if numErrors == 0:
            print("   ________")
            print("   |      |")
            print("   |      |")
            print("   |")
            print("   |")
            print("   |")
            print("___|___")
        elif numErrors == 1:
            print("   ________")
            print("   |      |")
            print("   |      |")
            print("   |      O")
            print("   |")
            print("   |")
            print("___|___")
        elif numErrors == 2:
            print("   ________")
            print("   |      |")
            print("   |      |")
            print("   |      O")
            print("   |      |")
            print("   |")
            print("___|___")
        elif numErrors == 3:
            print("   ________")
            print("   |      |")
            print("   |      |")
            print("   |      O")
            print("   |     /|")
            print("   |")
            print("___|___")
        elif numErrors == 4:
            print("   ________")
            print("   |      |")
            print("   |      |")
            print("   |      O")
            print("   |     /|\\")
            print("   |")
            print("___|___")
        elif numErrors == 5:
            print("   ________")
            print("   |      |")
            print("   |      |")
            print("   |      O")
            print("   |     /|\\")
            print("   |     /")
            print("___|___")
        elif numErrors == 6:
            print("   ________")
            print("   |      |")
            print("   |      |")
            print("   |      O")
            print("   |     /|\\")
            print("   |     / \\")
            print("___|___")
    # updates self.answer to a word based on user's choice of difficulty 
    def createAnswerWord(self):
        while True:
            try:
                dif = int(input("1-Easy, 2-Medium, 3-Hard, 4-Two Player? "))
                break 
            except ValueError:
                print("Please enter an integer, 1-3.")
        if dif == 1:
            num = random.randint(2, 6)
        elif dif == 2:
            num = random.randint(6, 12)
        elif dif == 3:
            num = random.randint(10, 14)
        elif dif == 4:
            num = 20

        if num < 20: 
            difDic = {1 : "easy",2 : "medium",3 : "hard"}
            difWord = difDic[dif]

            key = "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"
            openai.api_key = key
            model = "gpt-3.5-turbo"
            temp = .75
            messages = [{"role": "user", "content": f"I'm making a hangman game. Please generate an {difWord} difficulty random word with {num} letters. Your response should contain only the word with no formatting and in all lowercase."}]       
            response = openai.ChatCompletion.create(
                    model = model,
                    messages = messages,
                    temperature = temp
                    )
            textOut = response.choices[0].message.content
            textOut = textOut.lower()
            self.backup = textOut
            self.answer = list(textOut)
        elif num == 20: 
            word = input('Input word: ')
            self.backup = word
            self.answer = list(word)
    # creates self.curWord for the first time with "__"'s and tells user length of word 
    def initiate(self):
        length = len(self.answer)
        print(f"The word has a length of {length}")
        self.curWord = ["__" for i in range(length)]
    # checks a guess against the answer. Removes correct letters from answer and adds them to curWord. 
    #   handles updates to guesses and errors too
    def runGuess(self, guess):
        if guess not in self.guesses:
            if guess in self.answer:
                indices = []
                for i in range(len(self.answer)):
                    if guess in self.answer[i]:
                        indices.append(i)
                for ind in indices:
                    self.answer[ind] = "__"
                    self.curWord[ind] = guess
                self.guesses.append(guess)
            else: 
                self.guesses.append(guess)
                self.errors.append(guess)
                print("Wrong!")
        else: 
            print('You already guessed that!')
    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    # the main game loop. breaks on a win or loss 
    def runGame(self):
        while self.win == False and self.loose == False:
            self.clear_terminal()
            self.printBoard()
            print()
            for char in self.curWord:
                print(char, end = "  ")
            print(f"\n\nGuesses: {self.guesses}")
            guess = input("Enter one letter for your guess: ").lower()
            self.runGuess(guess)
            self.checkWin()
        if self.win:
            self.clear_terminal()
            print()
            for char in self.curWord:
                print(char, end = "  ")
            print("\n\nYou win!")
        elif self.loose:
            self.clear_terminal()
            print()
            print(self.backup.upper())
            print()
            self.printBoard()
            print("\nYou loose!")

def again():
    hold = input("Type anything to play again. ")
    if hold:
        return True
    else:
        return False


def main():
    
    game = gameplay()
    game.clear_terminal()
    game.createAnswerWord()
    print(game.answer)
    game.initiate()
    game.runGame()

    if again():
        main()

if __name__ == "__main__":
    main()
