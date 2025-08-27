import fastapi
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse  # Add this import
import pandas as pd
from pydantic import BaseModel, validator, ConfigDict
from challenge.model import DelayModel
from typing import List

app = fastapi.FastAPI()
model = DelayModel()

# Custom exception handler to convert 422 to 400
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("Custom exception handler triggered!")  # Debug line
    if exc.errors():
        first_error = exc.errors()[0]
        error_msg = f"{first_error['loc'][-1]}: {first_error['msg']}"
    else:
        error_msg = "Validation error"
    
    # Return a JSONResponse instead of raising HTTPException
    return JSONResponse(
        status_code=400,
        content={"detail": error_msg}
    )

class Flight(BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES: int
    
    model_config = ConfigDict(extra='forbid')  # Reject unknown fields
    
    # api-test validators
    @validator('MES')
    def validate_mes(cls, v):
        if not 1 <= v <= 12:
            raise ValueError('MES must be between 1 and 12')
        return v
    
    @validator('TIPOVUELO')
    def validate_tipovuelo(cls, v):
        if v not in ['I', 'N']:
            raise ValueError('TIPOVUELO must be either "I" or "N"')
        return v
    
    @validator('OPERA')
    def validate_opera(cls, v):
        valid_airlines = [
            'Grupo LATAM', 
            'Sky Airline', 
            'Aerolineas Argentinas', 
            'Copa Air', 
            'Latin American Wings', 
            'Avianca', 
            'JetSmart SPA',
            'Gol Trans',
            'American Airlines',
            'Air Canada',
            'Iberia',
            'Delta Air',
            'Air France',
            'Aeromexico',
            'United Airlines',
            'Oceanair Linhas Aereas',
            'Alitalia',
            'K.L.M.',
            'British Airways',
            'Qantas Airways',
            'Lacsa',
            'Austral',
            'Plus Ultra Lineas Aereas'
        ]
        if v not in valid_airlines:
            raise ValueError(f'OPERA must be one of the valid airlines: {valid_airlines}')
        return v

class FlightsRequest(BaseModel):
    flights: List[Flight]

class Prediction(BaseModel):
    predict: list

@app.get("/", status_code=200)
async def root():
    return {"message": "LATAM Challenge Flight Delay Prediction API OK!"}

@app.post("/predict", status_code=200, response_model=Prediction)
async def post_predict(flights_request: FlightsRequest):
    try:
        # Convert list of flights to DataFrame
        flights_dict = [flight.dict() for flight in flights_request.flights]
        df = pd.DataFrame(flights_dict)
        
        features = model.preprocess(df)
        prediction = model.predict(features)
        
        return Prediction(predict=prediction)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))