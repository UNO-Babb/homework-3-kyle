import random
from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for session management

# Initialize game state constants
finish_line = 100  # Total number of spaces to finish the race

def roll_dice():
    """Simulate a dice roll, returning a random number between 1 and 6."""
    return random.randint(1, 6)

@app.route('/')
def index():
    # Retrieve player positions from session or initialize them
    player1_position = session.get('player1_position', 0)
    player2_position = session.get('player2_position', 0)

    # Determine winner
    winner = None
    if player1_position >= finish_line:
        winner = "Player 1"
    elif player2_position >= finish_line:
        winner = "Player 2"

    return render_template('index.html', 
                           player1_position=player1_position, 
                           player2_position=player2_position, 
                           finish_line=finish_line, 
                           winner=winner)

@app.route('/move_player1')
def move_player1():
    player1_position = session.get('player1_position', 0)
    if player1_position < finish_line:
        player1_position += roll_dice()  # Move player 1 by a dice roll
    session['player1_position'] = player1_position
    return redirect(url_for('index'))

@app.route('/move_player2')
def move_player2():
    player2_position = session.get('player2_position', 0)
    if player2_position < finish_line:
        player2_position += roll_dice()  # Move player 2 by a dice roll
    session['player2_position'] = player2_position
    return redirect(url_for('index'))

@app.route('/reset')
def reset_game():
    # Reset game state in the session
    session['player1_position'] = 0
    session['player2_position'] = 0
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
