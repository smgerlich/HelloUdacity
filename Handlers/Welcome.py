from utils import Handler


class OtherHandler(Handler):
    def get(self):
        self.redirect("/blog/welcome")

class WelcomeHandler(Handler):

    def get(self):
        user = self.check_cookie()
        wiki = self.get_wiki()
        if wiki:
            title = wiki.title
            content = wiki.content
            date = wiki.date
            url = wiki.url
            user = wiki.user
            if user:
                self.render("welcome.html", current_user=user, title=title, content=content, date=date, url=url, user=user)
            else:
                self.render("welcome.html", current_user="", title=title, content=content, date=date, url=url, user=user)
        else:
            self.render("welcome.html")