from socket import *
import threading
import tkinter as tk
from tkinter import *
from tkinter import Label, messagebox


def start_client():
    # retrieves the word entered in the word_entry widget and sends it to the server
    def send_word():
        word = word_entry.get()
        client_socket.sendall(word.encode())

    # it recieves the word from server and insert it in the text area
    def receive_data():
        while True:
            response = client_socket.recv(1024).decode()
            game_text.insert(END, response)
            # insert additional message to indicate that the game is over
            if "Game over!" in response:
                game_text.insert(END, "Game over!\n")
                break

    # send 0 to the server to indicate that the client wants to end the game
    def end_game():
        client_socket.sendall("0".encode())

    host = "localhost"
    port = 5555

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((host, port))

    window = Tk()

    window.title("Word Chain Game by Nabil_Isaac")
    # chat area
    game_text = Text(window, height=10, width=70)
    # display the window
    game_text.pack()
    # allow the user to input words
    word_entry = Entry(window, width=30)
    word_entry.pack()

    send_button = Button(window, text="Send", command=send_word, bg="blue", fg="white")
    send_button.pack()

    end_button = Button(window, text="End Game", command=end_game, bg="red", fg="white")
    end_button.pack()

    threading.Thread(target=receive_data).start()

    window.mainloop()


if __name__ == "__main__":
    start_client()
