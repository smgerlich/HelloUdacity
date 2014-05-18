import webapp2
import Handlers

PAGE_RE = r'(/?(?:[a-zA-Z0-9_-]+/?))'
ID_RE = r'(/?(?:[0-9]+/?))'

app = webapp2.WSGIApplication([(r"/signup/?", Handlers.SignupHandler),
                               ("/signup/"+PAGE_RE, Handlers.SignupHandler),
                               (r"/logout/?", Handlers.LogoutHandler),
                               (r"/login/?", Handlers.LoginHandler),
                               ("/login/"+PAGE_RE, Handlers.LoginHandler),
                               ("/logout/"+PAGE_RE, Handlers.LogoutHandler),
                               (r"/login/"+PAGE_RE+"/?(\d+)", Handlers.LoginHandler),
                               (r"/logout/"+PAGE_RE+"/?(\d+)", Handlers.LogoutHandler),
                               ("/_edit/"+PAGE_RE, Handlers.EditHandler),
                               ("/_edit/"+PAGE_RE+"/"+ID_RE, Handlers.Edit_Id_Handler),
                               ("/_history/"+PAGE_RE, Handlers.HistoryHandler),
                               ("/error/"+PAGE_RE, Handlers.ErrorHandler),
                               ("/"+PAGE_RE, Handlers.WikiHandler),
                               ("/"+PAGE_RE+"/"+ID_RE, Handlers.Wiki_Id_Handler),
                               ("/.*", Handlers.WikiHandler)
                               ], debug=True)


#app = webapp2.WSGIApplication([("/rot13", Handlers.Rot13Handler), 
#                               ("/blog/signup", Handlers.SignupHandler),
#                               ("/blog/newpost", Handlers.NewpostHandler),
#                               ("/blog/logout", Handlers.LogoutHandler),
#                               ("/blog/login", Handlers.LoginHandler),
#                               ("/blog/flush", Handlers.CacheFlushHandler),
#                               (r"/blog/(\d+)/?(?:.\json)?", Handlers.PermalinkHandler),
#                               ('/blog/welcome', Handlers.WelcomeHandler),
#                               (r'/blog/?(?:\.json)?', Handlers.BlogHandler),
#                               ("/.*", Handlers.OtherHandler)
#                               ], debug=True)
