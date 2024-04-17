import ollama

#need id number from here, willgive previewdata

def summarize(strt): 
    response = ollama.chat(model='llama3', messages=[
    {
        'role': 'user',
        'content': 'extract all the sentences comes after "comment" in the following message:\n' 
        + strt 
        + '\n then try to summarize each comments into several keywords followed by a summarized sentence of comment'
    }
    ])
    print(response['message']['content'])
    return response['message']['content']
    
#summarize("hi there mfs i die now")
