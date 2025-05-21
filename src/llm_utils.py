import base64
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def query_gpt4o_with_image(image_path, task_prompt):
    base64_image = base64.b64encode(open(image_path, "rb").read()).decode("utf-8")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": task_prompt},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }},
                ],
            }
        ]
    )
    return response.choices[0].message.content

def query_gpt4_with_svg(svg_path, task_prompt):
    svg_content = open(svg_path, "r", encoding="utf-8").read()
    full_prompt = f"{task_prompt}\n\nHere is the SVG content:\n\n{svg_content}"

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

def query_gpt4_with_bpmn(bpmn_path, task_prompt):
    bpmn_content = open(bpmn_path, "r", encoding="utf-8").read()
    full_prompt = f"{task_prompt}\n\nHere is the BPMN file content:\n\n{bpmn_content}"

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content