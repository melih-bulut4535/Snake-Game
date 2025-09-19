from tkinter import BOTTOM, LEFT, RIGHT, TOP, Button, Canvas, Frame, Label, PhotoImage, Tk
from tkinter import ttk
import random
from tkinter.font import BOLD, ITALIC

from tkinter import messagebox


def new_game():
    global player

    player = random.choice(players)
    label.config(text=player + " 'S TURN")

    for row in range(3):
        for column in range(3):
            board[row][column].config(text="", bg="SystemButtonFace")


def next_turn(row, column):
    global player

    if board[row][column]['text'] == "" and check_winner() is False:
        if player == players[0]:
            board[row][column]['text'] = player

            if check_winner() == 0:
                player = players[1]
                label.config(text=(players[1] + " 'S TURN!"))

            elif check_winner() == 1:
                label.config(text=(players[0] + " WINS!"))

            elif draw() == "Tie":
                label.config(text=+"TIE!")


        else:

            board[row][column]['text'] = player

            if check_winner() == 0:
                player = players[0]
                label.config(text=(players[0] + " 'S TURN!"))

            elif check_winner() == 1:
                label.config(text=(players[1] + " WINS!"))


            elif draw() == "Tie":
                label.config(text="TIE!")


def check_winner():

    for row in range(3):
        if board[row][0]['text'] == board[row][1]['text'] == board[row][2]['text'] != "":
            board[row][0].config(bg="green")
            board[row][1].config(bg="green")
            board[row][2].config(bg="green")
            return True

    for column in range(3):
        if board[0][column]['text'] == board[1][column]['text'] == board[2][column]['text'] != "":
            board[0][column].config(bg="green")
            board[1][column].config(bg="green")
            board[2][column].config(bg="green")
            return True

    if board[0][0]['text'] == board[1][1]['text'] == board[2][2]['text'] != "":
        board[0][0].config(bg="green")
        board[1][1].config(bg="green")
        board[2][2].config(bg="green")
        return True

    elif board[0][2]['text'] == board[1][1]['text'] == board[2][0]['text'] != "":
        board[0][2].config(bg="green")
        board[1][1].config(bg="green")
        board[2][0].config(bg="green")
        return True
    else:
        return False
        # this condition is there is no winner and no tie


# for diagonals


def empty_spaces():
    spaces = 9

    for row in range(3):
        for column in range(3):
            if board[row][column]["text"] != "":
                spaces -= 1

    if spaces == 0:
        return False

    else:
        return True

def draw():
    if empty_spaces() is False or check_winner() is False:
        for row in range(3):
            for column in range(3):
                board[row][column].config(bg="yellow")
        return "Tie"


window = Tk()
window.title("TIC-TAC-TOE")
players = ["X", "O"]
player = random.choice(players)
board = [["", "", ""],
         ["", "", ""],
         ["", "", ""]]
label = Label(text=player + " 'S TURN", font=('Ink Free', 40, BOLD), fg='#FF6600')
label.pack(side="top")

exitButton = Button(window, text="EXIT", font=('Ink Free', 20, BOLD), fg='red', command=window.destroy).pack(padx=520,
                                                                                                             pady=10,
                                                                                                             anchor="w",
                                                                                                             side="bottom")
restartButton = Button(text="RESTART", font=("Ink Free", 20, BOLD), fg='#6495ED', command=new_game)
restartButton.pack(padx=490, pady=10, anchor="w", side="bottom")

frame = Frame(window)
frame.pack()

for row in range(3):
    for column in range(3):
        board[row][column] = Button(frame, text="", font=('Ink Free', 30), width=8, height=4,
                                    command=lambda row=row, column=column: next_turn(row, column))

        board[row][column].grid(row=row, column=column)

window.mainloop()
