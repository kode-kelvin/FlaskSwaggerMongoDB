# status codes
from crypt import methods
from src.status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR
# import all requirements
from distutils.log import debug
from http import client
from decouple import config
from flask import Flask, make_response, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY_APP')

# some functions
def randomNumb():
    id = randint(1_000, 999_999)
    return id

# connect to our Database and settings (credentials)
user_name = config('BD_USERNAME')
user_password = config('DB_PASSWORD')

connect_link = f"mongodb+srv://{user_name}:{user_password}@cluster0.8poqlow.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connect_link)


# instantiate db
db = client.blogapi

# to access the todos collections
blog = db.blogs


# error handlers
@app.errorhandler(HTTP_404_NOT_FOUND)
def handle_404(e):
    return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

@app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
def handle_500(e):
    return jsonify({'error': 'Something went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR


# get all blogs
@app.route('/api/v1.0/blogape/blogs', methods=["GET"])
def all_blogs():
    all_blogs = blog.find().sort("created", -1)
    data = []
    for i in all_blogs:
        data.append({
        'id': i["blog_id"],
        'title': i['title'],
        'description': i['description'],
        'created': i['created']
        })
    return jsonify(data), HTTP_200_OK

# get single blog
@app.route('/api/v1.0/blogape/blog/<oid>', methods=["GET"]) 
def single_blog(oid):
    try:
        singleBlog = blog.find_one({'_id': ObjectId(oid)})
        if not singleBlog:
            return jsonify({'error':'Invalid blog id'}), HTTP_400_BAD_REQUEST
    except AttributeError:
        return jsonify({'error':'Blog id missing'}), HTTP_400_BAD_REQUEST
    return jsonify(
        {
            "id": singleBlog['blog_id'],
            "title": singleBlog['title'],
            "description": singleBlog['description']
        }
    ), HTTP_200_OK


# update a blog
@app.route('/api/v1.0/blogape/blog/<oid>', methods=["PUT"]) 
def update_blog(oid):
    try:
        singleBlog = blog.find_one({'_id': ObjectId(oid)})
        if not singleBlog:
            return jsonify({'error':'Invalid blog id'}), HTTP_400_BAD_REQUEST

        title = request.json.get('title', None)
        description = request.json.get('description', None)
        if not title:
            return jsonify({'error': "Missing a title"}), HTTP_400_BAD_REQUEST
        if not description:
            return jsonify({'error': "Missing a description"}), HTTP_400_BAD_REQUEST   
        if isinstance(title, (int, float)):
            return jsonify({'error': "Title can't be integer"}), HTTP_400_BAD_REQUEST
        if isinstance(description, (int, float)):
            return jsonify({'error': "Description must be a string"}), HTTP_400_BAD_REQUEST

        blog.update_one({"_id": ObjectId(oid)}, {"$set": {
            "title": title,
            "description": description
           
        }}), HTTP_201_CREATED        
    except AttributeError:
        return jsonify({'error':'Blog id missing'}), HTTP_400_BAD_REQUEST
    return jsonify({'message':'Blog successfully updated'}), HTTP_200_OK


# Delete single blog
@app.route('/api/v1.0/blogape/blog/<oid>', methods=["DELETE"]) 
def delete_blog(oid):
    try:
        singleBlog = blog.find_one({'_id': ObjectId(oid)})
        if not singleBlog:
            return jsonify({'error':'Invalid blog id'}), HTTP_400_BAD_REQUEST
        blog.find_one_and_delete({"_id": ObjectId(oid)})
    except AttributeError:
        return jsonify({'error':'Blog id missing'}), HTTP_400_BAD_REQUEST
    return jsonify({'message':'Blog successfully deleted'}), HTTP_200_OK

        
# create the blog
@app.route('/api/v1.0/blogape/blog', methods=["POST"])
def add_blog():
    try:
        title = request.json.get('title', None)
        description = request.json.get('description', None)
        if not title:
            return jsonify({'error': "Missing a title"}), HTTP_400_BAD_REQUEST
        if not description:
            return jsonify({'error': "Missing a description"}), HTTP_400_BAD_REQUEST   
        if isinstance(title, (int, float)):
            return jsonify({'error': "Title can't be integer"}), HTTP_400_BAD_REQUEST
        if isinstance(description, (int, float)):
            return jsonify({'error': "Description must be a string"}), HTTP_400_BAD_REQUEST
        new_blog = {
            "blog_id": randomNumb(),
            "title": title,
            "description": description,
            "created": datetime.datetime.utcnow()
        }
        blog.insert_one(new_blog)
    except AttributeError:
        return jsonify({'error':'Provide blog details in JSON format in the request body'}), HTTP_400_BAD_REQUEST
    return jsonify({'message': 'blog created'}),HTTP_201_CREATED

if __name__=="__main__":
    app.run(debug=True)