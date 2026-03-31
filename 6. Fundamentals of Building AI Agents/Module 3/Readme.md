## Pandas Dataframe Agent
- special agent in Langchain to do natural langauge querying and visaulization on pandas dataframe
- experimental module
- not suitable for production environments

```python
# load llm
llm = ...

# load dataframe
df = pd.read_csv(...)

from from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

agent = create_pandas_dataframe_agent(
    llm,
    df,
    verbose=False,
    return_intermediate_steps=True,  # set return_intermediate_steps=True so that model could return code that it comes up with to generate the chart
    handle_parsing_errors=True
)

response = agent.invoke("how many rows of data are in this file?")

# to find the model generated code
# - need to set the return_intermediate_step = True
print(response['intermediate_steps'][-1][0].tool_input.replace('; ', '\n'))
```

## SQL Agent
- Database operations
    - read and undertand database schemas
    - Retrieves schemas only from relevant 
- Query management
    - support multi-step querying
    - query fails
        - captures error
        - analyze tracebacks
        - retries the task using corrected 
- Limitations of SQL agnets
    - may not be accurate
    - complex queries require manual adjustments
    - continous testing and validation are essential
- Query process
![alt text](images/image.png)

### Setting up LangChain SQL agent
```python
# load and llm
llm = ChatGroq(...)

# create sql connection
# connection parameters
mysql_username = 'root'
mysql_password = '....'
mysql_host = '172.21.155.8'
mysql_port = '3306'
databse_name = 'Chinook'

# build a mysql uri
mysql_uri = f"mysql+mysqlconnector://{mysql_uername}:{mysql_password}@{mysql_host}:{mysql_port}/{dabase_name}"

from langchain_community.utilities.sql_database import SQLDatabase
db = SQLDatabase.from_uri(mysql_uri)

# create an sql agent
from langchain_community.agent_toolkits import create_sql_agent

agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REA_DESCRIPTION #perform a resoning before acting (react agent)
)

agent_executor.invoke("How many Albums are there in the database?")
```
- setting `verbose=True` we can see the entire thougt process of the LLM.
