from utils import Handler, Wiki

class WikiHandler(Handler): 
    def get(self, page=None):
        if not page:
            self.redirect("/welcome")
            return
        current_user = self.check_cookie()
        if not current_user:
            current_user = ""
        wiki = self.get_wiki(page)
        if wiki:
            content = wiki.content
            date = wiki.date
            self.render("wiki.html", date=date, content=content, current_user=current_user, current_page=page)
        else:
            self.redirect("/_edit/%s"%page)

class Wiki_Id_Handler(Handler):
    def get(self, page=None, num=None):
        if not page:
            self.redirect("/welcome")
            return
        if not num:
            self.redirect("/%s"%page)
            return
        current_user = self.check_cookie()
        if not current_user:
            current_user = ""
        wiki = self.get_wiki_by_id(num)
        if wiki:
            content = wiki.content
            date = wiki.date
            self.render("wiki.html", date=date, content=content, current_user=current_user, current_page=page+"/"+num)
        else:
            self.redirect("/_edit/%s"%page)

class EditHandler(Handler):
    def get(self, page=None):
        if not page:
            self.redirect("/welcome")
            return
        current_user = self.check_cookie()
        if not current_user:
            self.redirect("/login/%s"%page)
            return
        wiki = self.get_wiki(page)
        if wiki:
            content = wiki.content
            self.render("edit.html", content=content, current_page=page, current_user=current_user)
        else:
            self.render("edit.html", current_page=page, current_user=current_user)
    
    def post(self, page=None):
        if not page:
            self.redirect("/welcome")
            return
        current_user = self.check_cookie()
        if not current_user:
            self.redirect("/login/%s"%page)
            return
        content = self.request.get("content")
        if len(content)<1:
            error = "Please enter some content"
            self.render("edit.html", content=content, current_page=page, current_user=current_user, error=error)
            return
        a = Wiki(content=content, url=page, user=current_user)
        a.put()
        self.redirect("/%s"%page)

class Edit_Id_Handler(Handler):
    def get(self, page=None, num=None):
        if not page:
            self.redirect("/welcome")
            return
        if not num:
            self.redirect("/%s/%s"%(page,num))
            return
        current_user = self.check_cookie()
        if not current_user:
            self.redirect("/login/%s/%s"%(page,num))
            return
        wiki = self.get_wiki_by_id(num)
        if wiki:
            content = wiki.content
            self.render("edit.html", content=content, current_page=page+"/"+num, current_user=current_user)
        else:
            self.render("edit.html", current_page=page, current_user=current_user)
    
    def post(self, page=None, num=None):
        if not page:
            self.redirect("/welcome")
            return
        current_user = self.check_cookie()
        if not current_user:
            self.redirect("/login/%s"%page)
            return
        content = self.request.get("content")
        if len(content)<1:
            error = "Please enter some content"
            self.render("edit.html", content=content, current_page=page, current_user=current_user, error=error)
            return
        a = Wiki(content=content, url=page, user=current_user)
        a.put()
        self.redirect("/%s"%page)

class HistoryHandler(Handler):
    def get(self, page=None):
        if not page:
            self.redirect("/welcome")
            return
        current_user = self.check_cookie()
        if not current_user:
            current_user = ""
        edits = self.get_wiki_history(page)
        if edits:
            self.render("history.html", current_user=current_user, current_page=page, edits=edits)
        else:
            self.redirect("/%s"%page)
            

class ErrorHandler(Handler):
    def get(self, page=None):
        if not page:
            self.redirect("/welcome")
            return
        current_user = self.check_cookie()
        if not current_user:
            self.render("error.html", current_page=page)
            return
        self.redirect("/%s"%page)

