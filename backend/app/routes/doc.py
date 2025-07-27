import os
from fastapi import APIRouter, File, HTTPException, UploadFile, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import JSON
from app.dependencies.auth import verify_token
from app.services.doc_services import load_and_embed_doc
from app.schemas.doc_schema import AskResponse
from app.services.doc_services import upload_to_supabase_bucket
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from backend.app.schemas.doc_schema import AskResponse
from app.services.doc_services import load_and_embed_doc
from app.schemas.doc_schema import QuestionRequest
from langchain.prompts import PromptTemplate
from app.config.qdrant_client import get_user_vector_store



router = APIRouter()


@router.post("/upload_doc")
async def upload_docs(
    work: UploadFile = File(...),
    health: UploadFile = File(...),
    reflections: UploadFile = File(...),
    personal: UploadFile = File(...),
    userId = Depends(verify_token)
):
    # a dictionary to hold all files with their types
    files = {
        "work": work,
        "health": health,
        "reflections": reflections,
        "personal": personal
    }
    
    temp_paths = []
    
    try:
        # Process each file
        for file_type, upload_file in files.items():
            # Save the file temporarily TODO: (add proper file handling)
            file_path = f"/tmp/{userId}_{file_type}_{upload_file.filename}"
            with open(file_path, "wb") as f:
                content = await upload_file.read()
                f.write(content)
            temp_paths.append((file_path, file_type))  # Store path with type


        # Upload to Supabase bucket (modified to handle file types)
        for path, file_type in temp_paths:
            upload_to_supabase_bucket(path, userId, file_type)
        
        # Run RAG pipeline
        load_and_embed_doc(temp_paths, userId)
        
        return JSONResponse(
            status_code=200,
            content={"message": "Documents uploaded and processed successfully"}
        )
    
    except Exception as e:
        # Clean up temp files if something goes wrong
        for path, _ in temp_paths:
            if os.path.exists(path):
                os.remove(path)
        raise HTTPException(status_code=500, detail=str(e))


# RAG prompt
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an intelligent assistant helping a user with questions about their weekly schedule, reflections, health, work, and personal goals.

Use the context from the documents below to answer the question clearly and concisely.

Context:
{context}

Question:
{question}

Answer:"""
)


@router.post("/ask")
async def ask_question(payload: QuestionRequest, userId:str=Depends(verify_token)):
    try:
        vectorstore = get_user_vector_store(userId)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})  # Can adjust

        llm = ChatOpenAI(temperature=0, model_name="gpt-4")  # or "gpt-3.5-turbo"

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",  # can also use "map_reduce" or "refine"
            chain_type_kwargs={"prompt": prompt_template},
            return_source_documents=False  # optional: return docs for debugging
        )

        answer = qa_chain.run(payload.question)
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
