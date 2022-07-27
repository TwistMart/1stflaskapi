from unicodedata import name
from flask import Flask,request
from flask_restful import Resource,Api,marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__) #creating and instance of our WSGI application by using the __name__ shortcut
api=Api(app)#api= Api(app) # api class to instantiate the app we have set up

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db' 
# we have file path, database type("sqlite" or "postgresql") and the name of the database("todo.db")
db = SQLAlchemy(app)

class Task(db.Model):
    id=db.Column(db.Integer , primary_key=True)
    name=db.Column(db.String, nullable=False)


    def __repr__(self):
        return self.name # every time we call this class we make sure name is the one that represents the class



fakeDatabase = {
    1:{'name':'Clean car'},
    2:{'name':'Write blog'},
    3:{'name':'Start stream'},
}

taskFields= {
    'id': fields.Integer,
    'name':fields.String,
 
}

class Items(Resource): # class that handles request to get all items and it inherits from Resource
    @marshal_with(taskFields)
    def get(self):         
        tasks=Task.query.all() # get all the data in our models    
        return tasks
    
    @marshal_with(taskFields)
    def post(self):
        data=request.json
        task=Task(name=data['name'])
        db.session.add(task)
        db.session.commit()

        tasks=Task.query.all()
        #ItemId= len(fakeDatabase.keys())+1
        #fakeDatabase[ItemId]= {'name':data['name']}
        return tasks

class Item(Resource):
    @marshal_with(taskFields)
    def get(self,pk):
        task=Task.query.filter_by(id=pk).first() # This will return a single object from our model
        return task
    
    @marshal_with(taskFields)
    def put(self,pk):
        data=request.json
        task = Task.query.filter_by(id=pk).first()
        task.name = data['name']
        db.session.commit()
        return task
        
        #fakeDatabase[pk]['name']=data['name']    
        # return fakeDatabase

    @marshal_with(taskFields)
    def delete(self,pk):
         task = Task.query.filter_by(id=pk).first()
         db.session.delete(task)
         db.session.commit()
         tasks = Task.query.all()
         return tasks

        #del fakeDatabase[pk]
       # return fakeDatabase
    
api.add_resource(Items, '/')
api.add_resource(Item, '/<int:pk>')


if __name__ == '__main__':
    app.run(debug=True)