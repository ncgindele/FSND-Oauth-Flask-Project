from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from functools import wraps
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
from flask import session as login_session
import random
import string

# Used for Oauth
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('google_client_secrets.json', 'r').read())[
    'web']['client_id']

APPLICATION_NAME = "Item Catalog"

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Decarator function to require login by user

def login_required(f):
    @wraps(f)
    def login_validation(*args, **kwargs):
        if 'username' not in login_session:
            return redirect(url_for('showLogin'))
        return f(*args, **kwargs)
    return login_validation

# Display functions

@app.route('/')
@app.route('/all')
def showCategories():
    cats = session.query(Category).order_by(asc(Category.name)).all()
    if 'username' not in login_session:
        return render_template('showCategories_public.html', categories=cats)
    else:
        return render_template('showCategories.html', categories=cats,
                               current_user=login_session['user_id'])


@app.route('/category/<int:category_id>/all')
def showItems(category_id):
    cat = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).order_by(asc(Item.year)).all()
    if 'username' not in login_session:
        return render_template('showItems_public.html', category=cat,
                               items=items)
    return render_template('showItems.html', category=cat, items=items,
                           current_user=login_session['user_id'])

@app.route('/myitems')
@login_required
def myItems():
    # Displays the current user's items
    items = session.query(Item).filter_by(
        user_id=login_session['user_id']).all()
    user = session.query(User).filter_by(id=login_session['user_id']).one()
    return render_template('myItems.html', items=items, user=user)


# Create, edit, delete functions

@app.route('/category/new', methods=['GET', 'POST'])
@login_required
def newCategory():
    if request.method != 'POST':
        return render_template('newCategory.html')
    cat = Category(name=request.form['name'], user_id=login_session['user_id'])
    session.add(cat)
    session.commit()
    flash('%s has been added' % cat.name)
    return redirect(url_for('showCategories'))


@app.route('/item/new', methods=['GET', 'POST'])
@login_required
def newItem():
    if request.method != 'POST':
        cats = session.query(Category).order_by(Category.name)
        return render_template('newItem.html', categories=cats)
    cat = session.query(Category).filter_by(
        name=request.form['category']).one()
    item = Item(user_id=login_session['user_id'], category_id=cat.id,
                name=request.form['name'], icon=request.form['icon'],
                year=request.form['year'],
                description=request.form['description'])
    session.add(item)
    session.commit()
    flash('%s has been added' % item.name)
    return redirect(url_for('showItems', category_id=cat.id))


@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def editCategory(category_id):
    cat = session.query(Category).filter_by(id=category_id).one()
    if cat.user_id != login_session['user_id']:
        returnScript = '''<script>function unauthorized() {alert('You are not
                        authorized to edit this category.');}</script>
                        <body onload='unauthorized()'>'''
        return returnScript
    if request.method != 'POST':
        return render_template('editCategory.html', category=cat)
    cat.name = request.form['name']
    session.add(cat)
    session.commit()
    flash('%s has been updated.' % cat.name)
    return redirect(url_for('showCategory', category_id=cat.id))


@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def editItem(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if item.user_id != login_session['user_id']:
        returnScript = '''<script>function unauthorized() {alert('You are not
                        authorized to edit this item.');}</script>
                        <body onload='unauthorized()'>'''
        return returnScript
    if request.method != 'POST':
        cats = session.query(Category).all()
        return render_template('editItem.html', item=item, categories=cats,
                               user=login_session['user_id'])
    else:
        item.name = request.form['name']
        item.year = request.form['year']
        item.icon = request.form['icon']
        item.description = request.form['description']
        session.add(item)
        session.commit()
        flash('%s has been updated' % item.name)
        return redirect(url_for('showItem', item_id=item.id))


@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteCategory(category_id):
    cat = session.query(Category).filter_by(id=category_id).one()
    if cat.user_id != login_session['user_id']:
        returnScript = '''<script>function unauthorized() {alert('You are not
                        authorized to delete this category.');}</script>
                        <body onload='unauthorized()'>'''
        return returnScript
    if request.method != 'POST':
        return render_template('deleteCategory.html', category=cat)
    session.delete(cat)
    session.commit()
    flash('%s has been deleted' % cat.name)
    return redirect(url_for('showCategories'))


@app.route('/item/<int:item_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if item.user_id != login_session['user_id']:
        returnScript = '''<script>function unauthorized() {alert('You are not
                        authorized to edit this item.');}</script>
                        <body onload='unauthorized()'>'''
        return returnScript
    if request.method != 'POST':
        return render_template('deleteItem.html', item=item,
                               user=login_session['user_id'])
    else:
        cat_id = item.category_id
        session.delete(item)
        session.commit()
        flash('%s has been deleted' % item.name)
        return redirect(url_for('showCategory', category_id=cat_id))


# Routing functions that return JSON objects

@app.route('/all/JSON')
def allCategoriesJSON():
    cats = session.query(Category).all()
    return jsonify(Categories=[cat.serialize for cat in cats])


@app.route('/category/<int:category_id>/all/JSON')
def showItemsJSON(category_id):
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Items=[item.serialize for item in items])


@app.route('/category/<int:category_id>/<int:item_id>JSON')
def singleItemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)


# Login and logout functions

@app.route('/login')
def showLogin():
    # adapted from lesson 11.5
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/logout')
def logout():
    try:
        login_session['provider']
        if login_session['provider'] == 'google':
            response = gdisconnect()
            if response:
                return response
            else:
                flash("Successfully logged out")
                return redirect(url_for('showCategories'))
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            flash("You are now logged out. Come back soon!")
            return redirect(url_for('showCategories'))
    except:
        flash("Can't log you out 'cause you never logged in")
        return redirect(url_for('showCategories'))


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Adapted from lesson 11.9
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        # Go from authorization code to credentials object
        oauth_flow = flow_from_clientsecrets(
            'google_client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Validate token
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify identity of token
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    print(data['name'])
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # Adapted from lesson 12.6
    user_id = getIDFromEmail(data['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    flash("you are now logged in as %s" % login_session['username'])
    return welcomeUser(login_session)


@app.route('/gdisconnect')
def gdisconnect():
    # Adapted from lesson 11.10
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'No access token stored'
        response = make_response(json.dumps(
            'Current user is not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'Access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is %s' % result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return None
    else:
        response = make_response(json.dumps('Failed to revoke token', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    # Adapted from lession 13.6
    if request.args.get('state') != login_session['state']:
        # Used to protect against cross-site reference forgery attacks
        response = make_response(json.dumps('Invalid login state'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print('access_token received %s' % access_token)
    # Swap the temporary token for a long-term token
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_secret']
    url = '''https://graph.facebook.com/oauth/access_token?grant_type=fb_
            exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s'''
    url = url % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    # Remove expiration tag
    token = result.split(',')[0].split(':')[1].replace('"', '')
    url = '''https://graph.facebook.com/v2.8/me?
            access_token=%s&fields=name,id,email''' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['username'] = data['name']
    try:
        login_session['email'] = data['email']
    except:
        pass
    login_session['facebook_id'] = data['id']
    login_session['provider'] = 'facebook'
    login_session['access_token'] = token

    # Retrieve facebook picture
    url = '''https://graph.facebook.com/v2.8/me/picture?
            access_token=%s&redirect=0&height=200&width=200''' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data['data']['url']

    # Create user if none exists
    user_id = getIDFromEmail(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    flash("you are now logged in as %s" % login_session['username'])
    return welcomeUser(login_session)


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    url = 'https://graph.facebook.com/%s/permissions' % facebook_id
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['facebook_id']


# Helper functions

def getIDFromEmail(email):
    # Adapted from lesson 12.4
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    # Adapted from lesson 12.4
    user = session.query(User).filter_by(id=user_id).one()
    return user


def createUser(login_session):
    # Adapted from lesson 12.4
    newUser = User(name=login_session['username'], email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def welcomeUser(login_session):
    output = ''
    output += '<h2>Welcome, '
    output += login_session['username']
    output += '!</h2>'
    output += '<img src="'
    output += login_session['picture']
    output += '''" style="width: 300px; height: 300px; border-radius: 150px;
                -webkit-border-radius: 150px;-moz-border-radius: 150px;">'''
    return output


if __name__ == '__main__':
    app.secret_key = 'oooh_ahhhh'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
