from llama_index.core import SimpleDirectoryReader

def load_data(file_path):
    documents = SimpleDirectoryReader(
        input_files=[file_path]
    ).load_data()
    return documents