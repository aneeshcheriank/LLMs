## Pandas dataframe agent
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

agent.invoke("how many rows of data are in this file?")
```