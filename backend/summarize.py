import ollama

#need id number from here, willgive previewdata

def summarize(str): 
    response = ollama.chat(model='llama2', messages=[
    {
        'role': 'user',
        'content': 'extract all the sentences comes after "comment" in the following message:\n' 
        + str 
        + '\n then try to summarize each comments into several keywords followed by a summarized sentence of comment'
    }
    ])
    return response['message']['content']
    
