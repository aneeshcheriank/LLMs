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

- Common Output
  - `gr.Textbox()`/"text"
    - an expandable text box
  - `Label`
    - used for classification tasks
    - `num_top_classes` controls the number of classes that are outputted

### code example
```python
import gradio as gr

def sentence_builder(quantity, tech_worker_type, countries, place, activity_list, morning):
    return f"""The {quantity} {tech_worker_type}s from {" and ".join(countries)} went to the {place} where they {" and ".join(activity_list)} until the {"morning" if morning else "night"}"""

demo = gr.Interface(
    fn=sentence_builder,
    inputs=[
        gr.Slider(3, 20, value=4, step=1, label="Count", info="Choose between 3 and 20"),
        gr.Dropdown(
            ["Data Scientist", "Software Developer", "Software Engineer"], 
            label="tech_worker_type", 
            info="Will add more tech worker types later!"
        ),
        gr.CheckboxGroup(["Canada", "Japan", "France"], label="Countries", info="Where are they from?"),
        gr.Radio(["office", "restaurant", "meeting room"], label="Location", info="Where did they go?"),
        gr.Dropdown(
            ["partied", "brainstormed", "coded", "fixed bugs"], 
            value=["brainstormed", "fixed bugs"], 
            multiselect=True, 
            label="Activities", 
            info="Which activities did they perform?"
        ),
        gr.Checkbox(label="Morning", info="Did they do it in the morning?"),
    ],
    outputs="text",
    examples=[
        [3, "Software Developer", ["Canada", "Japan"], "restaurant", ["coded", "fixed bugs"], True],
        [4, "Data Scientist", ["Japan"], "office", ["brainstormed", "partied"], False],
        [10, "Software Engineer", ["Canada", "France"], "meeting room", ["brainstormed"], False],
        [8, "Data Scientist", ["France"], "restaurant", ["coded"], True],
    ]
)

demo.launch(server_name="127.0.0.1", server_port= 7860)
```

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