from flask import Flask, render_template, request, redirect, url_for, session

from rulefinder.sqlmanager import SQL
from rulefinder.rulefinder import Rulefinder
from rulefinder.constants import FW, PA_KEY, FLASK_KEY, HEADINGS

app = Flask(__name__)
app.secret_key = FLASK_KEY

@app.route("/", methods=["POST", "GET"])
def index() -> render_template:
    '''
    Index route (main page)
    GET request renders a search bar 
    When POSTED, takes data from search bar and renders the data on the same page
    '''

    if request.method == "POST":
        host = FW
        key = PA_KEY

        ob = request.form["object"]
        session["object"] = ob

        finder = Rulefinder(host=host, key=key, search_obj=session["object"])
        objects = finder.find_object()

        database = SQL()
        rulelist = []

        for obj in objects:
            rule = database.excecute_sql(
                "SELECT * FROM securityrules"
                f" WHERE sourceip @> ARRAY['{obj}'] or destip @> ARRAY['{obj}']")
            rulelist.append(rule)

        database.close_connect(close_cur=True, close_DB=True, commit=False)

        return render_template('objects.html', rules=rulelist, headings=HEADINGS, objects=objects)
    return render_template('index.html')


@app.route("/home")
def home():
    '''
    Simple redirect back to search page
    When the navbar title is clicked it will redirect 
    '''
    return redirect(url_for('index'))

def main():
    app.run()

if __name__ == '__main__':
    main()