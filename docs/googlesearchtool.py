from googlesearch import search
from langchain_community.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
from typing import Type, Optional
from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
)
class GoogleSearchInput(BaseModel):
    query: str = Field(description="The query to search information in internet using google.")
    
class GoogleSearchTool(BaseTool):
    name = "GoogleSearchTool"
    description = "Search for information in internet using google search engine."
    args_schema: Type[BaseModel] = GoogleSearchInput
    

    def _run(self, query: str, run_manager:Optional[CallbackManagerForToolRun] = None) -> str:
        """Search for information in internet using google search engine."""
        search_results = search(query, num_results=5, advanced=True, lang='es')
        print(search_results)
        return list(search_results)



                    
