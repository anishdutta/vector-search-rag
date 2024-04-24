import fitz # install using: pip install PyMuPDF
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from pymongo import MongoClient
import time
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
import concurrent.futures
import tqdm
from src.search.model import SearchResult
from fastapi_cache.decorator import cache

from src.utils.utils import cache_key_generator

class Search_Service:

    def __init__(self):
        self.doc_path = "./test_pdfs"
        self.save_dir = './out'
        self.output_directory = "./summaries"
        self.mongo_client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.mongo_client["admin"]
        self.vector_collection = self.db["vectors"] # save as an index



    @cache(expire=60, key_builder=cache_key_generator)
    async def search(self, company: str, topic: str, question: str)->SearchResult:
        file_name = company + '.pdf'
        texts = self.get_raw_pdf(file_name)
        dir_name = os.path.join(self.save_dir, file_name.split('.pdf')[0])
        isVectorExist = self.create_directory_if_not_exists(dir_name)
        if not isVectorExist:
            self.create_vectors(texts, file_name)

        # Until facing permission issue
        # self.save_vectors_to_mongodb(vectors)
        
        # Concurrently retrieve keywords and summary
        with concurrent.futures.ThreadPoolExecutor() as executor:
            keywords_future = executor.submit(self.retrive_keywords, dir_name, topic)
            summary_future = executor.submit(self.retrive_summary, dir_name, topic, question)
            
            keywords = keywords_future.result()
            summary = summary_future.result()

        response = {
            'keywords': keywords,
            'summary': summary
        }
        return response
    
    def get_raw_pdf(self,file_name:str)->list[str]:
        raw_texts = ''
        with fitz.open(os.path.join(self.doc_path, file_name)) as doc:
            for page in doc:
                page_text = page.get_text()
                if len(page_text) < 100:
                    continue  # Skip saving if shard size is less than 100 characters
                raw_texts += page_text
        return self.create_chunks(raw_texts)
    
    def retrive_keywords(self,file_name:str,topic):
        chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
        embeddings = OpenAIEmbeddings()
        query = f"List down all keywords related to ${topic}, add mention each keyword sparated by commas."
        db = FAISS.load_local(file_name,embeddings,allow_dangerous_deserialization=True)
        docs = db.similarity_search(query)
        keywords = chain.run(input_documents=docs, question=query)
        print(keywords)
        words = [word.strip() for word in keywords.split(",")]
        result = {}
        index = 0
        for i, word in enumerate(words):
            if (i % 10) == 0:
                index += 1
            if index not in result:
                result[index] = []
            if(word == ''): continue
            result[index].append(word)
        print(keywords)
        return result
    
    def retrive_summary(self,file_name:str,topic,question):
        chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
        embeddings = OpenAIEmbeddings() #1536 * float(32)
        final_combine_prompt=f'''
        Please summarize the document:
        Provide a final summary of the entire document with these important points on ${topic}.
        Add a Generic Title,
        Start the precise summary with an introduction and provide the answer to this question : ${question}
        '''
        db = FAISS.load_local(file_name,embeddings,allow_dangerous_deserialization=True)
        docs = db.similarity_search(final_combine_prompt)
        answer = chain.run(input_documents=docs, question=final_combine_prompt)

        print(answer)
        return answer

    def create_vectors(self, texts, file_name:str)->any:
        embeddings = OpenAIEmbeddings() 
        text_chunks = self.chunks(texts, 250) # adjust based on rate-limit set on open AI
        docsearch = None
        print(len(texts))
        for (index, chunk) in tqdm.tqdm(enumerate(text_chunks)):
            print(len(chunk))
            if index == 0:
                docsearch = FAISS.from_texts(chunk, embeddings)
                continue
            else:
                print('Going to sleep')
                time.sleep(60) # wait for a minute to not exceed any rate limits
                docsearch.add_texts(chunk)
        dir_name = os.path.join(self.save_dir, file_name.split('.pdf')[0])
        self.create_directory_if_not_exists(dir_name)
        docsearch.save_local(dir_name)
        return docsearch
    
    def create_directory_if_not_exists(self,directory_path:str)->bool:
        """
        Creates a directory if it does not exist.

        Args:
            directory_path (str): The path of the directory to be created.
        """
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Directory '{directory_path}' created.")
            return False
        else:
            print(f"Directory '{directory_path}' already exists.")
            return True

    def chunks(self,lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
         

    def create_chunks(self, raw_text:str):
        text_splitter = CharacterTextSplitter(        
            separator = "\n",
            chunk_size = 1000,
            chunk_overlap  = 200,
            length_function = len,
        )
        return text_splitter.split_text(raw_text)
    
    def create_document_chunks(self, raw_text:str)->list[any]:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=20)
        return text_splitter.create_documents([raw_text])

    
    def save_vectors_to_mongodb(self, vectors):
        for vector in vectors:
            vector_data = {
                "vector": vector.tolist()  # Convert numpy array to list
            }
            self.vector_collection.insert_one(vector_data)

    def custom_summary(self,file_name,chunks)->str:
        llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
        chunks_prompt="""
        Please summarize the below speech:
        Speech:`{text}'
        Summary:
        """
        map_prompt_template=PromptTemplate(input_variables=['text'],template=chunks_prompt)
        final_combine_prompt='''
        Provide a final summary of the entire speech with these important points.
        Add a Generic Motivational Title,
        Start the precise summary with an introduction and provide the
        summary in number points for the speech.
        Speech: `{text}`
        '''
        final_combine_prompt_template=PromptTemplate(input_variables=['text'],template=final_combine_prompt)

        print("Going to summarize now")
        chain = load_summarize_chain(
            llm,
            chain_type='map_reduce',
            map_prompt=map_prompt_template,
            combine_prompt=final_combine_prompt_template,
            verbose=False
        )
        summary = chain.run(chunks)
        output_file_path = os.path.join(self.output_directory, f"{file_name}_summary.txt")
        print("Saving now", summary)
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(summary)

        return summary


