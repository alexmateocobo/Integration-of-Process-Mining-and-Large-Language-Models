import os
from dotenv import load_dotenv
from llm_utils import (
    query_gpt4o_with_image,
    query_gpt4_with_svg,
    query_gpt4_with_bpmn
)

load_dotenv()

if __name__ == "__main__":
    model_folder = "data/process_models/01-Dispatch-of-goods"

    print("▶ BPMN:\n", query_gpt4_with_bpmn(
        os.path.join(model_folder, "Dispatch-of-goods.bpmn"),
        "Please summarize the process shown in this BPMN file in plain language."
    ))

    print("\n▶ SVG:\n", query_gpt4_with_svg(
        os.path.join(model_folder, "Dispatch-of-goods.svg"),
        "Please extract and summarize the visible activities in this BPMN diagram."
    ))

    print("\n▶ PNG:\n", query_gpt4o_with_image(
        os.path.join(model_folder, "Dispatch-of-goods.png"),
        "Please describe the process in this diagram as if explaining it to a new employee."
    ))