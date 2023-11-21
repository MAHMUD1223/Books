import werkzeug
from flask import url_for

from . import app


class Backside():
    def urls_of_all():
        from . import routes
        alldir = dir(routes)
        link = []
        for i in alldir:
            try:
                link.append(f'{url_for(i)}')
            except werkzeug.routing.exceptions.BuildError:
                pass
        return link

    @app.route('/urls')
    @app.route('/_/')
    def urls():
        from . import routes
        alldir = dir(routes)
        link = ""
        link_list = []
        for i in alldir:
            try:
                link += f'<a href=\"{url_for(i)}\">{i}</a> <br>'
                link_list.append(f'{url_for(i)}')
            except werkzeug.routing.exceptions.BuildError:
                pass
        return f'''<html>
                   <body>
                   <h1 align="center">Welcome to the Backside of The app</h1>
                   <div align="center">{link}</div><br>
                   <br> and it's endpoint data is :- {link_list} and has {len(link_list)} links
                   </body>
                   </html>'''
