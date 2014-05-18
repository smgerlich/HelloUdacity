from utils import Handler, Entry

class BlogHandler(Handler): 
    def get(self):
        posts, delay = self.get_posts()
        if self.request.url.endswith('.json'):
            json_text = [p.as_dict() for p in posts]
            json_text += [{"Queried":"%s seconds ago"%delay}]
            self.render_json(json_text)
        else:
            self.render('BlogTemplate.html', posts=posts, time=delay)

class NewpostHandler(Handler):
    def get(self):
        self.render('NewpostTemplate.html')

    def post(self):
        newpost = {"subject":"",
           "content":"",
           "error":""
           }
        content = self.request.get("content")
        subject = self.request.get("subject")
        if not content or not subject:
            newpost["error"] = "Please provide a subject and body"
            newpost["subject"] = subject or ""
            newpost["content"] = content or ""
            self.render('NewpostTemplate.html', **newpost)
        else:
            a = Entry(subject = subject, content = content)
            a.put()
            permalink = str(a.key().id())
            self.update_post_cache(permalink) 
            self.redirect("/blog/%s" %permalink)

class PermalinkHandler(Handler):
    def get(self, perma):
        # perma is the id of the blog entry passed in through the URI pattern recognition
        posts, delay = self.get_posts(perma)
        if self.request.url.endswith('.json'):
            self.render_json([posts.as_dict(), {"Queried":"%s seconds ago"%delay}])
        else:
            self.render("PermaLinkTemplate.html", post=posts, time=delay)

class CacheFlushHandler(Handler):
    def get(self):
        self.flush_post_cache()
        self.redirect("/blog")