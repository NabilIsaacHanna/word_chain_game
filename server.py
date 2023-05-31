import socket
import threading  # to create and manage threads


def play_word_chain(conn1, conn2):  # takes two connections
    player1_score = 0
    player2_score = 0

    for round_num in range(1, 4):  # Play 3 rounds
        word = ""
        player_turn = conn1
        other_player = conn2

        for turn in range(1, 6):  # Each player can enter up to 5 words per round
            # recieve input from user and decode it , strip to eliminate white spaces
            response = player_turn.recv(1024).decode().strip()
            # end game if one entered 0
            if response == "0":
                player_turn.sendall("Game ended by player.".encode())
                other_player.sendall("Game ended by opponent.".encode())
                print("Game over!")
                return
            # if the response is empty
            if not response:
                player_turn.sendall("Invalid word! You lose this round.".encode())
                other_player.sendall(
                    "Opponent entered an invalid word! You earn a point.".encode()
                )
                # if a player entered an invalid word , increase the score of the other
                if player_turn == conn1:
                    player2_score += 1
                else:
                    player1_score += 1
                break
            # if the start of the word doesn't match the last of the previous word -->invalid
            if turn > 1 and response[0] != word[-1]:
                player_turn.sendall("Invalid word! You lose this round.".encode())
                other_player.sendall(
                    "Opponent did not start with the correct letter! You earn a point.".encode()
                )
                if player_turn == conn1:
                    player2_score += 1
                else:
                    player1_score += 1
                break
            # message is sent to the other player indicating the word entered by the current player.
            word = response
            other_player.sendall(
                f"Player {player_turn.getpeername()[1]} entered: {word}\n".encode()
            )
            # player turn swapped
            player_turn, other_player = other_player, player_turn
    # Once all rounds are completed, the final scores of the players are sent to them
    conn1.sendall(f"Game over! Your score: {player1_score}".encode())
    conn2.sendall(f"Game over! Your score: {player2_score}".encode())

    conn1.close()
    conn2.close()


def start_server():
    host = ""
    port = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    print("Waiting for players...")

    conn1, addr1 = server_socket.accept()
    print(f"Player 1 connected: {addr1}")
    conn1.sendall("Welcome! You are Player 1.".encode())

    conn2, addr2 = server_socket.accept()
    print(f"Player 2 connected: {addr2}")
    conn2.sendall("Welcome! You are Player 2.".encode())

    threading.Thread(target=play_word_chain, args=(conn1, conn2)).start()


if __name__ == "__main__":
    start_server()
