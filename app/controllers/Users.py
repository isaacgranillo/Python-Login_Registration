from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)

        self.load_model('UserModel')
    
    def index(self):
        return self.load_view('index.html')

    def create(self): 
        user_info = {
        "first_name" : request.form['first_name'], 
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : request.form['password'],
        "password_confirm" : request.form['password_confirm']
        }
    
        create_status = self.models['UserModel'].create_user(user_info)
        
        if create_status['status'] == True:
            session['id'] = create_status['user']['id']
            session['first_name'] = create_status['user']['first_name']

            return redirect('users/show')

        else:
            for message in create_status['errors']:
                flash(message, 'errors')
            return redirect('/')

    def signin(self):
        signin_cred = {
        "email": request.form['email'],
        "password": request.form['password']

        }

        login_status=self.models['UserModel'].login_user(signin_cred)
        if login_status['status']==True:
            session['id']=login_status['user']['id']
            session['first_name']=login_status['user']['first_name']
            return redirect ('/users/show')
        else:
            for message in login_status['errors']:
                flash(message, 'errors')
            return redirect ('/')

    def show(self):
        return self.load_view('show.html')

    def signout(self):
        session.pop('id')
        session.pop('first_name')
        return redirect ('/')

        

