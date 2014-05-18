from utils import Users, Handler
import re


class SignupHandler(Handler): 
    def get(self, page=None):
        if not page:
            page = ""
        if self.check_cookie():
            self.response.delete_cookie('user')
        self.render("SignupTemplate.html", page=page)
    def post(self, page=None):
        if not page:
            page = ""
        user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        pword_re = re.compile(r"^.{3,20}$")
        email_re = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
        username = self.request.get("username", None)
        password = self.request.get("password", None)
        verify = self.request.get("verify", None)
        email = self.request.get("email", None)
        signup_dict = {}
        if email:
            if email_re.match(email):
                if user_re.match(username) and pword_re.match(password) and password == verify:
                    if self.check_for_user(username):
                        signup_dict["username"] = username
                        signup_dict["u_error"] = "This username already exists. Please choose another username or <a href='/login'>login</a>."
                        signup_dict["email"] = email
                        signup_dict["page"] = page
                        self.render("SignupTemplate.html", **signup_dict)
                        return
                    else:
                        salt = self.salt()
                        password_hash = self.password_hash(username, password, salt)
                        a = Users(user_name=username, password_hash=password_hash, salt=salt, user_email=email)
                        a.put()
                        cookie = self.make_secure_val(username)
                        self.response.set_cookie('user', cookie)
                        if page:
                            self.redirect("/%s"%page)
                            return
                        self.redirect("/welcome")
                        return
        if not email:
            if user_re.match(username) and pword_re.match(password) and password == verify:
                if self.check_for_user(username):
                    signup_dict["username"] = username
                    signup_dict["u_error"] = "This username already exists. Please choose another username or <a href='/login'>login</a>."
                    signup_dict["page"] = page
                    self.render("SignupTemplate.html", **signup_dict)
                    return
                else:
                    salt = self.salt()
                    password_hash = self.password_hash(username, password, salt)
                    a = Users(user_name=username, password_hash=password_hash, salt=salt)
                    a.put()
                    cookie = self.make_secure_val(username)
                    self.response.set_cookie('user', cookie)
                    if page:
                        self.redirect("/%s"%page)
                        return
                    self.redirect("/welcome")
                    return
        if username: 
            if not user_re.match(username):
                signup_dict["u_error"] = "Please enter a valid username"
            else:
                signup_dict["username"] = username
        if not username:
            signup_dict["u_error"] = "Please enter a valid username"
        if not password or not pword_re.match(password):
            signup_dict["p_error"] = "Please enter a valid password"
        if password and not password == verify:
            signup_dict["p_error"] = ""
            signup_dict["pc_error"] = "The password and verify did not match"
        if email: 
            if email_re.match(email):
                signup_dict["email"] = email
            else:
                signup_dict["e_error"] = "The email you entered was invalid."
        signup_dict["page"] = page
        self.render("SignupTemplate.html", **signup_dict)
