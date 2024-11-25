from flask import Flask, render_template, request, redirect 
from pymongo import MongoClient
from bson.objectid import ObjectId 

app = Flask(__name__)

client = MongoClient("mongodb+srv://mongotesting:rigorigo123@cluster0.xmy5g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0") # URL
db = client["todo_db"]
collection = db["tasks"]

@app.route('/')
def index():
    tasks = collection.find()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    collection.insert_one({"task": task})
    return redirect('/')

@app.route('/edit/<task_id>', methods=["GET"])
def edit_task(task_id):
    task = collection.find_one(
        {
            "_id": ObjectId(task_id)
        }
    )
    return render_template("edit.html", task=task)

@app.route('/update/<task_id>', methods=['POST'])
def update_task(task_id):
    new_task = request.form['task']
    collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"task": new_task}}
    )
    return redirect('/')

@app.route('/delete/<task_id>', methods=['GET'])
def delete_task(task_id):
    collection.delete_one({"_id": ObjectId(task_id)})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)