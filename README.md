# Looper

This program uses a generative AI model to create an SVG image from a text prompt. It then iteratively shows the generated image back to the model, asks it to identify the subject, and then redraw it. This process is repeated a specified number of times.

For each step, the program saves the generated SVG file and a PNG rendering of it.

## Requirements

- Python 3.12 or later
- A Google API key with the Gemini API enabled

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/looper.git
    cd looper
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You may need to create a `requirements.txt` file from `pyproject.toml` or install the dependencies listed there manually.)*

3.  **Set your Google API key:**
    ```bash
    export GOOGLE_API_KEY="your-api-key"
    ```

## Running the Program

To run the program, execute the `main.py` script:

```bash
python main.py
```

The script will generate an initial SVG and PNG based on the hardcoded prompt in `main.py`. It will then perform the iterative identification and redrawing process, saving a new SVG and PNG file for each iteration.

## Customization

You can change the initial prompt and the number of iterations by modifying these lines in `main.py`:

```python
if __name__ == "__main__":
    start_prompt = "A smiling sun over a green hill"
    num_iterations = 3
    iterative_svg_generator(start_prompt, num_iterations)
```
