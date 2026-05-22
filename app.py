from flask import Flask, render_template

app = Flask(__name__)



# before login pages

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():    
    return render_template("beforelogin_Script_html/about_pg.html")

@app.route('/ourwork')
def ourwork():    
    return render_template("beforelogin_Script_html/ourwork_pg.html")

@app.route('/gallery')
def gallery():    
    return render_template("beforelogin_Script_html/gallery_pg.html")

@app.route('/login')
def login():    
    return render_template("beforelogin_Script_html/login_pg.html")

@app.route('/signup')
def signup():    
    return render_template("beforelogin_Script_html/signup1.html")



# donor login pages

@app.route('/donorhome')
def donarindex():    
    return render_template("donorlogin_Script_html/index.html")













if __name__ == "__main__":
    app.run(debug=True)