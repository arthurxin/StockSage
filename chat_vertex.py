import vertexai
from vertexai.language_models import TextGenerationModel
from vertexai.preview.language_models import CodeGenerationModel
from vertexai.preview.language_models import TextEmbeddingModel

def vertex_chat(message):
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 768,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(
        f"""You are a portfolio manager.
        You are going to give some invest information and advice to the user.
        ```{message}```
        
        portfolio manager:
        """,
        **parameters
    )
    return response.text

def vertex_create_request_statue(message):
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(
        f"""Multi-choice problem: Define the category of the user's request?
    Categories:
    - chatting
    - one specific stock
    - news related to some stocks

    User: Tell me about your ability?
    Category: chatting

    User: How about the Apple today?
    Category: one specific stock

    User: The price of gas is increasing, which stock would be influenced?
    Category: news related to some stocks
    
    User: ```{message}```
    Category:

    """,
        **parameters
    )
    return response.text

def text_embedding(message):
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    embeddings = model.get_embeddings([message])
    for embedding in embeddings:
        vector = embedding.values
    return vector

import re
def vertex_get_stock_code(message):

    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 1024,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(
        f"""Extract the stock name from the text below in a JSON format.

    Text: How about the Apple and google today?
    JSON:[GOOG,AAPL]

    Text: {message}
    JSON:
    """,
        **parameters
    )
    stocks = re.split(",|\\[|\\]",response.text)
    stock_code = []
    for stock in stocks:
        if stock != "":
            stock_code.append(stock)
    return stock_code