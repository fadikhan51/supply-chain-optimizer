from typing import Any, Optional
from fastapi.responses import JSONResponse

def standard_response(status: str = "success", data: Any = None, message: Optional[str] = None, code: int = 200):
    content = {"status": status}
    if data is not None:
        content["data"] = data
    if message is not None:
        content["message"] = message
    return JSONResponse(content=content, status_code=code)
