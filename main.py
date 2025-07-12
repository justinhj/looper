import base64
import io
import os

from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import cairosvg

# --- Configuration ---
# Set your Google API key here
api_key = os.environ["GOOGLE_API_KEY"] or exit("Please set the GOOGLE_API_KEY environment variable.")

# --- Main Program Logic ---

def iterative_svg_generator(initial_prompt: str, iterations: int):
    """
    Generates an SVG from a prompt, then iteratively has the LLM identify and redraw it.

    Args:
        initial_prompt: The starting prompt for the first SVG drawing.
        iterations: The number of times to repeat the identification and redraw process.
    """

    # 1. Initialize the multimodal LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    # 2. Generate the initial SVG
    print("🎨 Generating initial SVG...")
    message = HumanMessage(
        content=[
            {"type": "text", "text": f"The user will describe a prompt for you to draw. If it does not sound like the description of a drawing simply return the word \"exit\". Otherwise draw the image as an SVG and return only the SVG text so it can be used as svg file. The prompt is: {initial_prompt}"},
        ]
    )
    response = llm.invoke([message])
    svg_code = response.content

    print("--- LLM Response for initial SVG ---")
    print(svg_code)
    print("------------------------------------")

    with open("initial_drawing.svg", "w") as f:
        f.write(svg_code)
    print("✅ Initial SVG saved as initial_drawing.svg")

    # 3. Start the iterative process
    for i in range(iterations):
        print(f"\n--- Iteration {i + 1} of {iterations} ---")

        # a. Render the SVG to a PNG image in memory
        print("🖼️ Rendering SVG to image...")
        png_output = cairosvg.svg2png(bytestring=svg_code.encode('utf-8'))
        image = Image.open(io.BytesIO(png_output))

        # b. Prepare the image for the LLM
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # c. Submit the image and new prompt to the LLM
        print("🤔 Identifying image and preparing to redraw...")
        image_message = {
            "type": "image_url",
            "image_url": f"data:image/png;base64,{img_base64}",
        }
        text_message = {
            "type": "text",
            "text": "First, in one sentence, identify the main subject of this image. Then, draw this identified subject as a new, simple SVG and return only the SVG code.",
        }

        new_response = llm.invoke([HumanMessage(content=[text_message, image_message])])
        
        # The response will likely contain the identification and the SVG code.
        # We will extract the SVG part for the next iteration.
        response_content = new_response.content
        
        # A simple way to extract the SVG code block
        try:
            svg_code = response_content[response_content.find('<svg'):response_content.rfind('</svg>') + 6]
        except (TypeError, ValueError) as e:
            print(f"Error extracting SVG in iteration {i+1}: {e}")
            print("Full response from LLM:", response_content)
            break

        # d. Save the new SVG
        output_filename = f"iteration_{i + 1}_drawing.svg"
        with open(output_filename, "w") as f:
            f.write(svg_code)
        print(f"✅ New SVG saved as {output_filename}")


if __name__ == "__main__":
    start_prompt = "A smiling sun over a green hill"
    num_iterations = 3
    iterative_svg_generator(start_prompt, num_iterations)
    print("\n🎉 Process complete.")
