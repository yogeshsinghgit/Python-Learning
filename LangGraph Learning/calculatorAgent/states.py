from pydantic import BaseModel
from typing import List, Optional, Dict

class CalculatorState(BaseModel):
    user_input: str
    
    numbers: List[int] = []
    operations: List[str] = []
    
    steps: List[Dict] = []
    
    intermediate_result: Optional[int] = None
    final_result: Optional[int] = None