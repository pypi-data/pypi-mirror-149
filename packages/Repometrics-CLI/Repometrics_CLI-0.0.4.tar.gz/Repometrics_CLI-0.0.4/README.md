# RepoMetrics
***
CLI to detect selected repository files languages.
***

## How to use 

You have to be working with Python 3.8+

Install this tool by command line:
`pip install repometrics`

Once installed successfully, you may :

Option 1. Run command `repom -h` for help

Option 2. Run command `repom [path]` to detect the selected repository files language, 
it defaults to detect file type by its extension.  

Option 3. Run command `repom NA` to detect current working folders files language,
it defaults to detect file type by its extension.  

Option 4. Run command `repom [path] [-method by_content|by_extension]` to select the detect method, 
it will be either 'by_extension' or 'by_content' 



