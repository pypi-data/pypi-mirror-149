from typing import Optional, List, Dict, Union

from pydantic import BaseModel


class ExecutionResult(BaseModel):
    has_values: bool
    sql: str
    result: Optional[Union[List[Dict], Dict]]
