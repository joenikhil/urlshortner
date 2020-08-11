from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os.path      #for checking the path
from werkzeug.utils import secure_filename

app=Flask(__name__)
app.secret_key = 'qwertymnbvc1234klnkhije'

@app.route('/')
def home():
    return render_template('home.html', codes=session.keys())

@app.route('/your-url', methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls={} #a new dictionary when there exists no urls.json file

        #checking the path exist, if so loading it same urls dictionary
        if os.path.exists('urls.json'):
            with open('urls.json') as url_file:
                urls=json.load(url_file)

        #check if the key is found in 'urls keys'
        if request.form['code'] in urls.keys():
            flash('Ahh! the shortname is already taken, please try another.')
            return redirect(url_for('home'))

        #saving a code(shortname) and url in the urls dictionary
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            fullname = request.form['code'] + secure_filename(f.filename)
            f.save('C:/Users/Nikhil/Desktop/url-shortner/static/user_files/' + fullname)
            urls[request.form['code']] = {'file':fullname}

        with open('urls.json','w') as url_file:
            json.dump(urls, url_file)   #url_file is same as 'urls.json'
            session[request.form['code']]=True  #creating sessions such that we can print the code
        return render_template('your_url.html', code=request.form['code'])  #(form in post) and (args in get) request
    else:
        return redirect(url_for('home'))    #url_for: creates url for function name home

@app.route('/<string:code>')
def redirect_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as url_file:
            urls = json.load(url_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html') , 404

@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))












#if __name__=="__main__":
#    app.run(debug=True)
