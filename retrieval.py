# retrieval.py
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

def retrieve_documents(query, retriever, llm):

    # Apply Cohere reranking model
    compressor = CohereRerank(model="rerank-english-v3.0")
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=retriever
    )

    prompt = """You are a good assistant that answers questions. Your knowledge is strictly limited to the following piece of context. Use it to answer the question at the end.
    If the answer can't be found in the context, just say you don't know. *DO NOT* try to make up an answer.
    If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
    **MOST IMPORTANT: If question is not related to the context, just say "I don't know".**

    Context: {context}
    Question: {input}

    """

    prompt_template = ChatPromptTemplate.from_template(prompt)

    document_chain = create_stuff_documents_chain(llm, prompt_template)
    retrieval_chain = create_retrieval_chain(compression_retriever, document_chain)
    response = retrieval_chain.invoke({"input":query})

    return response
