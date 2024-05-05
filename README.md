# CourseComparator

## What does our project do?

Users can type in a class course and be returned a list of instructors with stats and a summarization of the reviews. 
Users will have the option to view the full rate my professor ratings 
Users can type in a course subject and be returned the highest rated courses

## What is our motivation?

Although the class might be the same in title, the actual experience of the class is heavily dictated by the specific instructor. Our project aims to smoothen the process of picking a section by combining the information from rate my professor and the stats on gpa regarding the instructors of a course.


# Technical Architecture
![image](https://github.com/CS222-UIUC-SP24/group-project-team-25/assets/53002479/5b7ed090-6a27-4de3-9e6a-e62963f09ea8)


# To run the project:
1. Run the front-end
```
$ cd my-app
npm start
```
2. Run the backend

```
$ cd backend
python3 -m flask run
```

3. Start Ollama
   
```
$ ollama run llama3
```
- download package [here](https://ollama.com/)



# Group Members

- **Dev Patel**: Frontend work and frontend-backend connection.
- **Acelynn Zhang**: Backend work, including writing flask app and SQLite.
- **Tianyi Zhong**: Backend work, including implementing comments summary functionality.
