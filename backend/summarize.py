import ollama

#need id number from here, willgive previewdata


def find_comments(dictionary):
    comments = []

    def find_in_dict(dictionary):
        for key, value in dictionary.items():
            if isinstance(value, list):
                for l in value:
                    find_in_dict(l)
            if key == "comment":
                comments.append(value)
            if isinstance(value, dict):
                find_in_dict(value)

    find_in_dict(dictionary)
    return comments

def summarize(json_str): 
    comments = find_comments(json_str)
    summ = ''
    for i in range(3):
        comment = comments[i]
        response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': '''summarize the following comment into three keywords and a sentence following the format: Keywords : Summarized Comment.
            Just return the answer as the format above and do not add any other information:''' + comment
        }
        ])
        summ += response['message']['content']
        summ += '\n'
    return summ
    
