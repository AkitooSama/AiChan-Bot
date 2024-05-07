def replace_word_txt(filepath, search_text, replace_text):
    with open(filepath, 'r') as file: 
        data = file.read() 
        data = data.replace(search_text, replace_text) 
    with open(filepath, 'w') as file: 
        file.write(data) 

if __name__ == "__main__":
    pass