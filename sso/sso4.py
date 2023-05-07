import datetime
import os
from flask import Flask, request, render_template, redirect, session, make_response, jsonify
from onelogin.saml2.auth import OneLogin_Saml2_Auth


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=3600)
app.config['SAML_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saml')

def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=app.config['SAML_PATH'])
    return auth

def prepare_flask_request(request):
    # If server is behind proxies or balancers, use the HTTP_X_FORWARDED fields
    return {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'script_name': request.path,
        'get_data': request.args.copy(),
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        # 'lowercase_urlencoding': True,
        'post_data': request.form.copy()
    }


@app.route('/api/userInfor', methods=['POST'])
def userInfo():
    data = request.json
    return jsonify(data)



@app.route('/login/callback', methods=['GET', 'POST'])
def login_callback():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    auth.process_response()
    auth.get_last_response_xml()
    print('Response:',auth.get_last_response_xml())
    errors = auth.get_errors()

    if len(errors) == 0 and auth.is_authenticated():
        session['user'] = auth.get_attributes()  # Save user information in session
        session['token'] = auth.get_session_index()  # Save token in session
        session.permanent = True

        # print('user:',auth.get_attributes())
        username = session['user']['http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name'][0]
        token = session['token']
        print('new',username)


        return render_template('index.html',username=username,token= token)  # Redirect to home page
    else:
        return 'Login failed'



@app.route('/', methods=['GET', 'POST'])
def index():
    if 'token' in session:
        print('已经有token')
        username = session.get('user', None)['http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name'][0]
        token = session['token']
        print('old',username)
        return render_template('index.html',username=username,token= token) # Redirect to home page if token is available
    else:
        print('获取新token')
        req = prepare_flask_request(request)
        auth = init_saml_auth(req)
        return redirect(auth.login())  # Redirect to SSO login page

if __name__ == "__main__":
    app.run('127.0.0.1', debug=True, port=8100, ssl_context=('./aixint.cn_bundle.pem', './aixint.cn.key'))
