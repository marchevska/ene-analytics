# ENE Analytics app
# Copyright 2020 Olga Marchevska
#
# Main app control and Flask-admin interface

import logging
import os

from flask import Flask, render_template
from flask_admin import Admin, AdminIndexView, BaseView, expose

from app import ene_app, db
from dash_apps import workforce


logger = logging.getLogger()


class EneIndexView(AdminIndexView):
    def is_visible(self):
        return False

    @expose('/')
    def index(self):
        return self.render("page.html", title="Main Page")


class EneIframeApp(BaseView):
    @expose('/', methods=('GET',))
    def index_view(self):
        return self.render('dash_iframe_app.html')


class EneAboutView(BaseView):
    @expose('/', methods=('GET',))
    def index_view(self):
        return self.render('about.html')


ene_admin = Admin(ene_app, name='ENE Analytics', index_view=EneIndexView(url='/'))
# ene_admin = Admin(app, name='ENE Analytics', index_view=AdminIndexView(url='/', endpoint='ene'))
ene_admin.add_sub_category(name="Basic Analytics", parent_name="")
ene_admin.add_view(EneIframeApp(name='Work Force Precentage', category='Basic Analytics',
                                url='/workforce', endpoint='workforce'))
ene_admin.add_view(EneAboutView(name='About', url='/about', endpoint='about'))


if __name__ == "__main__":
    ene_app.run(host="127.0.0.1", port=8080, debug=True)
