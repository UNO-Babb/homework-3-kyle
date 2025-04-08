#Example Flask App for a hexaganal tile game
#Logic is in this python file

from flask import Flask, render_template, request, redirect, url_for, session
import random
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
SAVE_FILE = 'savegame.json'

BOARD_SIZE = 20

@app.route('/')
def index():
    if 'positions' not in session:
        session['positions'] = [0, 0]
        session['current_player'] = 0
        session['message'] = "Player 1's turn"

    return render_template('index.html',
                           positions=session['positions'],
                           current_player=session['current_player'],
                           message=session['message'],
                           board_size=BOARD_SIZE)

@app.route('/roll')
def roll():
    positions = session.get('positions', [0, 0])
    current_player = session.get('current_player', 0)

    roll = random.randint(1, 6)
    positions[current_player] += roll

    if positions[current_player] >= BOARD_SIZE:
        positions[current_player] = BOARD_SIZE
        session['message'] = f"Player {current_player + 1} wins!"
    else:
        current_player = 1 - current_player
        session['message'] = f"Player {current_player + 1}'s turn"

    session['positions'] = positions
    session['current_player'] = current_player

    return redirect(url_for('index'))

@app.route('/save')
def save():
    data = {
        'positions': session.get('positions', [0, 0]),
        'current_player': session.get('current_player', 0)
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f)
    session['message'] = "Game Saved!"
    return redirect(url_for('index'))

@app.route('/load')
def load():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
            session['positions'] = data['positions']
            session['current_player'] = data['current_player']
            session['message'] = f"Player {data['current_player'] + 1}'s turn (loaded)"
    else:
        session['message'] = "No saved game found."
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

