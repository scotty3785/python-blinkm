from flask import Flask, render_template, request
from os import curdir
from blinkm import blinkm
app = Flask(__name__)

colors = ['Red', 'Blue', 'Green']
bm = blinkm()


@app.route("/")
def main():
    global colors
    templateData = { 'colors' : colors }
    return render_template('main.html', **templateData)

@app.route('/<color>/<state>')
def color_change(color,state):
    global colors
    if color == 'Red':
        bm.goToRGB((255,0,0))
    elif color == 'Green':
        bm.goToRGB((0,255,0))
    elif color == 'Blue':
        bm.goToRGB((0,0,255))
    else:
        bm.goToRGB((0,0,0))
    templateData = {'colors' : colors,'new_color':color}
    return render_template('main.html',**templateData)
    


if __name__ == "__main__":
    print(curdir)
    app.run(host='0.0.0.0', port=81, debug=True)
