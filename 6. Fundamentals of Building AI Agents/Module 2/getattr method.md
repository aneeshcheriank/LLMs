## Dynamically calling a function on a python object
```python
def dynamic_calling_function(file_name:str, method: str) -> str:
    func = getattr(df, method, None)

    if not callable(func):
        return f"{method} is not valid on {file_name}
    try:
        result = func()
        return str(result)
    except Exception as e:
        return f"Errror calling '{method}' on '{filename}': str(e)"
```

- the `func = getattr(df, "desirable")` find the code for the `desirable` mehtod. it poits the variable func to that spot of meomory
- if you print you will see something like `<bound method NDFrame.describe of ...>` at this location
- `callable()` checks 2 things
    - does the `getattr` mehtod returns a `None`
    - or is it found an actual function call (example df.shape) or an attribute
- In python () are call operator. this tell python take instruction stored in the variable `func` and execute them right now.