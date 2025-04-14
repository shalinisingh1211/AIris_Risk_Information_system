from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub

def extract_info_rag(vectordb, query: str):
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})
    llm = HuggingFaceHub(repo_id="tiiuae/falcon-7b-instruct")
    
    prompt = PromptTemplate.from_template("Use the following context to answer: {context}\n\n{question}")
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    
    return qa_chain.run(query)