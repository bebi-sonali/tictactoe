from tkinter import *

root = Tk()
root.geometry("500x600")
root.title("Tic Tac Toe")

frame1 = Frame(root)
frame1.pack()
titlelabel = Label(frame1, text="Tic Tac Toe", font=("Arial", 31), bg="red")
titlelabel.grid(row=0, column=0)

frame2 = Frame(root)
frame2.pack()

board = {i: "" for i in range(1, 10)}

turn = "x"
game_over = False

def checkforwin(player):
    return (
        (board[1] == board[2] == board[3] == player) or
        (board[4] == board[5] == board[6] == player) or
        (board[7] == board[8] == board[9] == player) or
        (board[1] == board[4] == board[7] == player) or
        (board[2] == board[5] == board[8] == player) or
        (board[3] == board[6] == board[9] == player) or
        (board[1] == board[5] == board[9] == player) or
        (board[3] == board[5] == board[7] == player)
    )

def checkfordraw():
    return all(board[i] != "" for i in board.keys())

def restartgame():
    global board, turn, game_over
    for button in buttons:
        button["text"] = ""
        button["state"] = "normal"
    board = {i: "" for i in range(1, 10)}
    turn = "x"
    game_over = False
    for widget in frame1.winfo_children():
        if widget != titlelabel:
            widget.destroy()

def minmax(board, ismaximizing):
    if checkforwin("o"):
        return 1
    if checkforwin("x"):
        return -1
    if checkfordraw():
        return 0
    if ismaximizing:
        bestscore = -100
        for key in board.keys():
            if board[key] == "":
                board[key] = "o"
                score = minmax(board, False)
                board[key] = ""
                if score > bestscore:
                    bestscore = score
        return bestscore
    else:
        bestscore = 100
        for key in board.keys():
            if board[key] == "":
                board[key] = "x"
                score = minmax(board, True)
                board[key] = ""
                if score < bestscore:
                    bestscore = score
        return bestscore

def playComputer():
    bestscore = -100
    bestmove = 0
    for key in board.keys():
        if board[key] == "":
            board[key] = "o"
            score = minmax(board, False)
            board[key] = ""
            if score > bestscore:
                bestscore = score
                bestmove = key
    board[bestmove] = "o"
    buttons[bestmove-1]["text"] = "o"

def play(event):
    global turn, game_over
    if game_over:
        return
    button = event.widget
    button_id = buttons.index(button) + 1
    if board[button_id] == "":
        button["text"] = turn
        board[button_id] = turn
        if checkforwin(turn):
            winningLabel = Label(frame1, text=f"{turn.upper()} wins the game", bg="red", font=("Arial", 31))
            winningLabel.grid(row=0, column=0, columnspan=3)
            game_over = True
            for button in buttons:
                button["state"] = "disabled"
        elif checkfordraw():
            game_over = True
            drawLabel = Label(frame1, text="Game Draw", bg="red", font=("Arial", 31))
            drawLabel.grid(row=0, column=0, columnspan=3)
            for button in buttons:
                button["state"] = "disabled"
        else:
            turn = "o" if turn == "x" else "x"
            if turn == "o":
                playComputer()
                if checkforwin("o"):
                    winningLabel = Label(frame1, text="O wins the game", bg="red", font=("Arial", 31))
                    winningLabel.grid(row=0, column=0, columnspan=3)
                    game_over = True
                    for button in buttons:
                        button["state"] = "disabled"
                elif checkfordraw():
                    game_over = True
                    drawLabel = Label(frame1, text="Game Draw", bg="red", font=("Arial", 31))
                    drawLabel.grid(row=0, column=0, columnspan=3)
                    for button in buttons:
                        button["state"] = "disabled"
                else:
                    turn = "x"

buttons = []
for i in range(9):
    button = Button(frame2, text="", width=4, height=2, font=("Arial", 31), bg="yellow", relief=RAISED, borderwidth=5)
    button.grid(row=i // 3, column=i % 3)
    button.bind("<Button-1>", play)
    buttons.append(button)

restartbutton = Button(frame2, text="Restart Game", width=12, height=1, font=("Arial", 20), bg="brown", relief=RAISED, borderwidth=5, command=restartgame)
restartbutton.grid(row=4, column=0, columnspan=3)

root.mainloop()
