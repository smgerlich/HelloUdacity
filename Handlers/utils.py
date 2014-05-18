import webapp2 
import os
from google.appengine.ext import db
from google.appengine.api import memcache
import jinja2
import random
import string
import hashlib
import hmac
import json
import time

jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
t = "7gHdDXkjSKDLFnDSlISDNLSDNDioiSDfn98897SSDF98Dskdsf06dsfklSDkld765"


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    
    def render_str(self, template, **params):
        t=jinja_environment.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
    
    def hash_str(self, s):
        return hmac.new("t", s).hexdigest()
    
    def make_secure_val(self, s):
        return "%s|%s" %(s, self.hash_str(s))
    
    def check_secure_val(self, cookie_val):
        if cookie_val:
            val = cookie_val.split('|')[0]
            if cookie_val == self.make_secure_val(val):
                return val
        else:
            return None

    def render_json(self, d):
        json_text = json.dumps(d)
        self.response.headers.add("Content-Type", "application/json")
        self.response.out.write(json_text)

    def check_cookie(self):
        """returns user_name, if called with valid 'user' cookie in the header, else returns None"""
        user_name = self.check_secure_val(self.request.cookies.get("user", None))
        if user_name:
            return user_name
        else:
            return None
    
    def user_login(self, username, password):
        reply = {}
        user = Users.all().filter("user_name", username).get()
        if user:
            if self.password_validate(user, password):
                reply["status"] = True
                reply["cookie"] = self.make_secure_val(username)
                return reply
        reply["status"] = False
        return reply

    def password_validate(self, user, password):
        return user.password_hash == self.password_hash(user.user_name, password, user.salt)

    def salt(self): 
        salt = ''
        i = 0
        while i<5:
            salt += random.choice(string.letters)
            i += 1
        return salt
    
    def password_hash(self, username, password, salt):
        password_hash = hashlib.sha256(username+password+salt).hexdigest()
        return password_hash

    def check_for_user(self, username):
        a = Users.all().filter('user_name', username).get()
        if a:
            return True
        else:
            return False
    
    def get_wiki(self, page=None):
        if page:
            content = Wiki.all().filter("url", page).order("-date").get()
        else:
            content = Wiki.all().order("-date").get()
        if content:
            return content
        else:
            return None
    
    def get_wiki_history(self, page):
        content = Wiki.all().filter("url", page).order("-date").run(limit=30)
        if content:
            return content
        else:
            return None
    
    def get_wiki_by_id(self, num):
        if num:
            wiki = Wiki.get_by_id(int(num))
        if wiki:
            return wiki
        else:
            return None
    
    def get_posts(self, post_id = None):
        if post_id:
            key = str(post_id)
        else:
            key = 'top_posts'
        time_key = "%s_time"%key
        posts = memcache.get(key)#@UndefinedVariable
        if posts is None:
            self.update_post_cache(post_id = post_id)
            posts = memcache.get(key)#@UndefinedVariable 
        delay = int(time.time()) - memcache.get(time_key)#@UndefinedVariable
        if post_id:
            return posts, delay
        else:
            return list(posts), delay
    
    def update_post_cache(self, post_id = None):
        key = 'top_posts'
        time_key = "%s_time"%key
        posts = list(Entry.all().order("-created").run(limit=10))
        posts_time = int(time.time())
        memcache.set_multi({key:posts, time_key: posts_time}) #@UndefinedVariable
        if post_id:
            key = str(post_id)
            time_key = "%s_time"%key
            posts = Entry.get_by_id(int(post_id))
            posts_time = int(time.time())
            memcache.set_multi({key:posts, time_key: posts_time}) #@UndefinedVariable
    
    def flush_post_cache(self):
        memcache.flush_all()#@UndefinedVariable
    
class Users(db.Model):
    user_name = db.StringProperty()
    password_hash = db.StringProperty()
    salt = db.StringProperty()
    user_email = db.EmailProperty()

class Entry(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    
    def as_dict(self):
        d = {'subject': self.subject,
             'content': self.content,
             'created': self.created.strftime("%c")}
        return d

class Wiki(db.Model):
    user = db.StringProperty()
    content = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add = True)
    url = db.StringProperty()
    



