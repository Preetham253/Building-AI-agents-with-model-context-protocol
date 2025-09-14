#-----------------------------------------------------------------------
# Creating an MCP server with FastMCP SDK
#MCP Server that serves the code_of_conduct.pdf file
# as a MCP resource
#-----------------------------------------------------------------------

import os
from dotenv import load_dotenv
# https://gofastmcp.com/
# We will use FastMCP SDK
from fastmcp import FastMCP 
import PyPDF2

#-----------------------------------------------------------------------
#Setup the MCP Server
#-----------------------------------------------------------------------
load_dotenv()
hr_coc_mcp = FastMCP("HR-CoC-MCP-Server") #create an instance of FastMCP SDK

#-----------------------------------------------------------------------
#Setup Resources
#-----------------------------------------------------------------------
pdf_filename = "code_of_conduct.pdf"
pdf_full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), pdf_filename))
'''
__file__ = the current python file,
os.path.dirname(__file__) = the folder where this script lives in,
os.path.join(os.path.dirname(__file__), pdf_filename) = adds code_of_conduct.pdf to the folder path
then converts to absolute path
'''
pdf_uri = f"file:///{pdf_full_path.replace(os.sep, '/')}" #convert to uri as MCP prefers URIs for resources so clients can identify and reference them consistently

#Decorator to register the resource with the MCP server
@hr_coc_mcp.resource(
    uri=pdf_uri,
    name="Code of Conduct",
    description="Provides code of conduct policies for the company",
    mime_type="text/plain", 
)
'''
In MCP terms:

Resources are read-only data sources the agent can fetch (like files, documents, records).

The client can call the resource to retrieve content and use it as context for answers.
'''

#Function to handle requests for the code of conduct
def get_code_of_conduct() -> str:
    """Returns the text content of the code of conduct PDF file."""

    #Open the file and read its contents
    with open(pdf_full_path, "rb") as code_of_conduct:
        reader = PyPDF2.PdfReader(code_of_conduct)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

#Code to test the server standalone
#print(get_code_of_conduct())
#-----------------------------------------------------------------------
#Run the Server
#-----------------------------------------------------------------------
if __name__ == "__main__":
    hr_coc_mcp.run(transport="stdio")
