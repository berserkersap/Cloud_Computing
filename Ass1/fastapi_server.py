import codecs
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize the FastAPI application
app = FastAPI()

# --- Pydantic Models for Data Validation ---
class InputData(BaseModel):
    data: str

class HexOutputData(BaseModel):
    result: str

class ReverseOutputData(BaseModel):
    reversed: str

# --- API Endpoints ---

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "FastAPI server (v2) is running with /encode and /reverse endpoints"}

# @app.post("/encode", response_model=HexOutputData)
# async def encode_string(item: InputData):
#     """
#     Endpoint to encode a string to its hexadecimal representation.
#     """
#     try:
#         input_string = item.data
#         hex_encoded_string = codecs.encode(input_string.encode('utf-8'), 'hex').decode('utf-8')
#         return {"result": hex_encoded_string}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/reverse", response_model=ReverseOutputData)
async def reverse_string(item: InputData):
    """
    NEW ENDPOINT: Reverses the input string as per the updated assignment.
    """
    try:
        input_string = item.data
        # Python's slicing is an efficient way to reverse a string
        reversed_string = input_string[::-1]
        return {"reversed": reversed_string}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
