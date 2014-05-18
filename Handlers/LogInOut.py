from utils import Handler


class LogoutHandler(Handler):
    def get(self, page = None, num=None):
        if self.check_cookie():
            self.response.delete_cookie('user')
        if page and num:
            self.redirect("/%s/%s"%(page, num))
        elif page:
            self.redirect("/%s"%page)
        else:
            self.redirect("/welcome")

class LoginHandler(Handler):
    def get(self, page=None, num=None):
        if self.check_cookie():
            self.response.delete_cookie('user')
        if page and num:
            self.render("LoginTemplate.html", page=page+"/"+num)
        elif page:
            self.render("LoginTemplate.html", page=page)
        else:
            self.render("LoginTemplate.html")
    def post(self, page=None, num=None):
        username = self.request.get("username", None)
        password = self.request.get("password", None)
        if username and password: 
            reply = self.user_login(username, password)
            if reply['status']:
                self.response.set_cookie('user', reply['cookie'])
                if page and num:
                    self.redirect("/%s/%s"%(page,num))
                elif page:
                    self.redirect("/%s"%page)
                else:
                    self.redirect("/welcome")
                return
        self.render("LoginTemplate.html", error = "Login Error! Please provide valid credentials")
