from flask import Flask, render_template, request, url_for
from werkzeug.exceptions import HTTPException
from fonction import translate

app = Flask(__name__)


@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        p=''
        state=0
        return render_template('index.html',text= p, state=state)
    elif request.method == 'POST':
        p=request.form['corpus']
        response = translate(p)
        if type(response) != list:
            state=1
            return render_template('index.html',text = p, state=state, response=response)
        else:
            state=2
            message="Je ne connais pas le mot '{}', Je suis désolé que mon apprentissage ne soit pas venu jusqu'ici..".format(response[1][0])
            return render_template('index.html',text = p, state=state, message =message)



if __name__ == '__main__':
    app.run(debug=True)