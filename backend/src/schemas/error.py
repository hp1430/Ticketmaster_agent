from dataclasses import dataclass

@dataclass
class ErrorResponse():
    error: str
    message: str
    success: bool = False