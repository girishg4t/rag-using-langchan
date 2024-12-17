from fastapi import FastAPI, UploadFile
from query import insert_pdf_to_db, query_similar_sentences

app = FastAPI()


@app.post("/v1/upload")
async def insert_pdf(file: UploadFile):
    pdf_path = f"/tmp/{file.filename}"
    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    insert_pdf_to_db(pdf_path)
    return {"message": "PDF data inserted successfully."}


@app.get("/v1/matches")
async def get_matches(sentence: str, limit: int = 5):
    results = query_similar_sentences(sentence, limit)
    return {"matches": results}


@app.get("/")
async def root():
    return {"message": "Welcome to the Vector Database API"}

# Start the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
