# CourseComparator

## What does our project do?

Users can type in a class course and be returned a list of instructors with stats.
Users can click to learn more about a particular professor, and be returned a short summary of reviews from RateMyProfessor.
Users can post comments on certain classes as well as view past comments


## What is our motivation?

Although the class might be the same in title, the actual experience of the class is heavily dictated by the specific instructor. Our project aims to smoothen the process of picking a section by combining the information from rate my professor and regarding the instructors of a course  and provide a platform for students to communicate.



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
