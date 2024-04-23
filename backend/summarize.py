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

    '''response = ollama.chat(model='llama2', messages=[
    {
        'role': 'user',
        'content': 'extract all the sentences comes after "comment" in the following message:\n' 
        + str 
        + '\n then try to summarize each comments into several keywords followed by a summarized sentence of comment'
    }
    ])
    return response['message']['content']'''
    

