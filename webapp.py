
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.db import djangoforms
from google.appengine.api import users
import wsgiref.handlers

import app_db

class SightingForm(djangoforms.ModelForm):
    class Meta:
        model = app_db.Sighting
        exclude = ['which_user']

class SightingInputPage(webapp.RequestHandler):
    def get(self):
        html = template.render('templates/header.html', {'title': 'Get Enhanced User Experience'})
        html = html + template.render('templates/form_start.html', {})
        html = html + str(SightingForm(auto_id=False))     
        html = html + template.render('templates/form_end.html', {'sub_title': 'Submit Sighting'})
        html = html + template.render('templates/footer.html', {'links': ''})
        self.response.out.write(html)

    def post(self): 
        new_sighting = app_db.Sighting()
        new_sighting.name = self.request.get('name')
        new_sighting.email = self.request.get('email')
        new_sighting.date = self.request.get('date')
        new_sighting.time = self.request.get('time')
        new_sighting.location = self.request.get('location')
        new_sighting.fin_type = self.request.get('fin_type')
        new_sighting.whale_type = self.request.get('whale_type')
        new_sighting.blow_type =self.request.get('blow_type')
        new_sighting.wave_type = self.request.get('wave_type')
        new_sighting.which_user = users.get_current_user()
        new_sighting.nickname = self.request.get('nickname')

        new_sighting.put()
        
        html = template.render('templates/header.html', {'title': 'Thank you!'})
        html = html + "<p>Thank you for providing your sighting data.</p>"
        html = html + template.render('templates/footer.html',
                                      {'links': 'Enter <a href="/">another form filling </a>.'})
        self.response.out.write(html)        
        


def main():
    app=webapp.WSGIApplication([('/.*', SightingInputPage)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == '__main__':
    main()
