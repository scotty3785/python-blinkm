from flask import Flask, render_template, request
from os import curdir
from blinkm import blinkm
app = Flask(__name__)

colors = {'Red':(255,0,0), 'Blue':(0,0,255), 'Green':(0,255,0),'Orange':(255,51,0)}
bm = blinkm()


@app.route("/")
def main():
    global colors
    cols = colors.keys()
    templateData = { 'colors' : cols }
    return render_template('main.html', **templateData)

@app.route('/<color>/<state>')
def color_change(color,state):
    global colors
    cols = colors.keys()
    try:
        bm.goToRGB(colors[color])
    except KeyError:
        bm.goToRGB((0,0,0))
    templateData = {'colors' : cols,'new_color':color}
    return render_template('main.html',**templateData)
    


if __name__ == "__main__":
    print(curdir)
    app.run(host='0.0.0.0', port=81, debug=True)
