## Gradio
- Tool for prototyping
- user-friendly web interface

### installation
- `pip install gradio`

### First Gradio Interface
```python
import gradio as gr
def greet(name, intensity):
  return "Hello, " + name + "!" * int(intensity)
demo = gr.Interface(
  fn=greet,
  inputs=["text", "slider"],
  outputs=["text"],
)
demo.launch(server_name="127.0.0.1", server_port= 7860)
```

- Interface class
    - fn: the model or the function return the result
    - inputs: Gradio components
        - should match with the number of arguments in the fuction
    - outputs: Gradio components used for the output
        - should match the number of ruetn values from the function

## Gradio's interfaces input and outputs

- Common input interfaces
  - `Checkbox`: A check box that can be set to `True` or `False`
  - `CheckboxGroup`: users can select multiple values from a predefined checkbox list
  - `Dropdown`: dropdwon where by default one value can be selected, if `multiselct` is set to `True` then more values can be selected
  - `File`: user can upload a file
  - `Image`: user can select or upload a file
  - `Radio`: Radio buttons, user can select one value
  - `Slider`: a slide bar, user can select between a minimum and a maximum
    - `value` parameter set the default value
    - `step` provides the increment value
    - `minimum` and `maximum`
  - `Textbox`: user can input a text. expandable

  

## Virtual envs
  - Option 1
    - python -m venv venv

  - Option 2
    - pip install virtualenv
    - virtualenv venv
    - source venv/bin/activate

  - Option 2 you need to manage an external lib
  - fast compared to the option 1
  - Option 1 the package is managed by python
  - Option 2,
    - can detect diff python version in your system
    - `virtualenv -p python3.10 venv