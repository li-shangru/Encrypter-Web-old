from flask import Flask, render_template, request, redirect, url_for, session
from httpimport import github_repo

app = Flask(__name__)
app.secret_key = 'w845n#9V!#!!9C!n%6iY'

# Importing Encrypter remotely from GitHub
with github_repo(username='MaxsLi', repo='Encrypter', module='ED'):
    import ED


@app.route('/')
def index():
    if 'dark_theme' not in session:
        session['dark_theme'] = False
    return render_template('index.html',
                           version=ED.__version__,
                           dark_theme=session['dark_theme'])


@app.route('/about')
def about():
    return render_template('about.html', dark_theme=session['dark_theme'])


@app.route('/light_theme', methods=['POST'])
def light_theme():
    session['dark_theme'] = False
    return redirect(url_for('index'))


@app.route('/dark_theme', methods=['POST'])
def dark_theme():
    session['dark_theme'] = True
    return redirect(url_for('index'))


@app.route('/encrypt', methods=['POST'])
def encrypt():
    """
    Encrypt the given input using Encrypter
    """
    try:
        return render_template('response.html',
                               version=ED.__version__,
                               dark_theme=session['dark_theme'],
                               input=request.form['input'],
                               message="Encrypted",
                               response=ED.encrypt(request.form['input']))
    except SyntaxError as error:
        return render_template('response.html',
                               version=ED.__version__,
                               dark_theme=session['dark_theme'],
                               input=request.form['input'],
                               message="Error",
                               response=error.msg)


@app.route('/decrypt', methods=['POST'])
def decrypt():
    """
    Decrypt the Given cypher using Encrypter
    """
    try:
        return render_template('response.html',
                               version=ED.__version__,
                               dark_theme=session['dark_theme'],
                               input=request.form['input'],
                               message="Decrypted",
                               response=ED.decrypt(request.form['input']))
    except SyntaxError as error:
        return render_template('response.html',
                               version=ED.__version__,
                               dark_theme=session['dark_theme'],
                               input=request.form['input'],
                               message="Error",
                               response=error.msg)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
