from flask import Flask, render_template, request, redirect, url_for, session
import requests
import secret
import setting
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'XXXXXXXXXXXXX'
DEBUG=False
setting_dict = setting.get_setting(debug=DEBUG)
@app.route('/')
def index():
    return render_template('index.html', setting=setting_dict)

@app.route('/redirect')
def myredirect():
    code = request.args.get('code')
    if not code:
        return "code is not provided", 400
    url_prefix = setting_dict["url_prefix"]
    token_url = f"https://foursquare.com/oauth2/access_token?client_id={secret.consumer_key}&client_secret={secret.consumer_secret}&grant_type=authorization_code&redirect_uri={url_prefix}/main&code={code}"
    
    response = requests.get(token_url)
    print(response.content)
    
    if response.status_code != 200:
        return f"Error fetching token: {response.text}", 500

    access_token = response.json().get("access_token")
    
    if not access_token:
        return "Error extracting access token", 500
    session["access_token"] = access_token
    return redirect(url_for("main"))

@app.route('/main')
def main():
    access_token = session.get("access_token")
    if not access_token:
        return "access_token is not provided", 400
    return render_template("main.html", access_token=access_token, setting=setting_dict)

@app.route('/get_checkins')
def get_checkins():
    url = "https://api.foursquare.com/v2/users/self/checkins"
    params = {
        "v": "20230818",
        "oauth_token": session.get("access_token")
    }
    response = requests.get(url, params=params)
    return response.content

@app.route('/get_checkin_detail')
def get_checkin_detail():
    checkinid = request.args.get('checkinid')
    url = f"https://api.foursquare.com/v2/checkins/{checkinid}"
    params = {
        "v": "20230818",
        "oauth_token": session.get("access_token")
    }
    response = requests.get(url, params=params)
    return response.content

if __name__ == '__main__':
    app.run(debug=DEBUG, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))