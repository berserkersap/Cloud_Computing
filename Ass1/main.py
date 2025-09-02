import codecs
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize the FastAPI application
app = FastAPI()

# Define the request body structure using Pydantic
class InputData(BaseModel):
    data: str

# Define the response body structure
class OutputData(BaseModel):
    result: str

@app.post("/encode", response_model=OutputData)
async def encode_string(item: InputData):
    """
    Endpoint to encode a string to its hexadecimal representation.
    Expects a JSON payload with a 'data' key.
    e.g., {"data": "hello world"}
    """
    try:
        # Perform the encoding
        input_string = item.data
        hex_encoded_string = codecs.encode(input_string.encode('utf-8'), 'hex').decode('utf-8')
        return {"result": hex_encoded_string}
    except Exception as e:
        # If something goes wrong, return a 500 internal server error
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "FastAPI server is running"}
