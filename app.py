from boggle import Boggle
from flask import Flask, flash, request, render_template, redirect, session, jsonify, make_response

boggle_game = Boggle()

app = Flask(__name__)
app.config["SECRET_KEY"] = "SHHHHHHHHHHH"

@app.route('/')
def home():
    
    session['error'] = None
    error = session['error']
    print(error)
    session['answers'] = []
    session['score'] = 0

    if session.get('board'):
        board = session['board']
    else:
        session['board'] = boggle_game.make_board()
        
        
        board = session['board']
    context = {'board': board, 'error':error}
    return render_template('home.html', context=context)


@app.route('/check-word', methods=['GET'])
def check():
    board = session['board']
    data = request.args['guess']
    words = data
    result = boggle_game.check_valid_word(board, words)

    if result =='ok' and words not in session['answers']:
        session['score'] = session['score'] + len(words)
        answers = session['answers']
        answers.append(words)
        session['answers'] = answers
        session['response'] = result
        

    elif words in session['answers']:
        print(words in session['answers'])
        session['error'] = 'You already used this word.'
        session['response'] = 'You already used this word.'

    else:
        session['error'] = result
        session['response'] = result
    
    return jsonify({'result':result, 'score': session['score'], 'error': session['error'], 'answers':session['answers'], 'feedback':session['response']})

@app.route('/reset-game', methods=["POST"])
def reset():
    session.clear()
    return redirect('/')


if __name__  == "__main__":
    app.run(debug=True)