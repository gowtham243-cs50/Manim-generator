from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
import subprocess
import re

# === Create Visualization Agent ===
def create_visualization_agent():
    # Step 1: Initialize LLM
    llm = ChatOpenAI(
        model = "deepseek/deepseek-r1-0528",
        openai_api_key="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",
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.7,
        max_tokens=5000,

    )
    memory = ConversationBufferMemory(memory_key="chat_history",output_key="python_code",return_messages=True)

    # Step 2: Prompt for explanation
    prompt_question_explained = PromptTemplate(
        input_variables=["question","chat_history"],
        template="""
    You are an expert in creating STEM visualizations using Manim (Community Edition ≥ 0.17). Your task is to write clean, readable Python code that visually explains STEM concepts using Manim — without relying on LaTeX-based elements. Follow these guidelines:

    1. **Do not use LaTeX or MathTex.** Use `Text` for all text elements.
    2. Visualize the key ideas using simple shapes, number lines, arrows, graphs, and transitions.
    3. Emphasize **step-by-step animations** that make the problem and its solution intuitive.
    4. Label diagrams using plain text — format equations as ASCII-style expressions (e.g., "f(x) = sin(x)").
    5. Comment the code to explain each visual step.
    6. Define your scene inside a standard Manim `Scene` class (e.g., `class STEMScene(Scene):`).
    7. Stick to **core Manim features only** — no plugins or LaTeX dependencies.
    8. Prioritize conceptual clarity and visual pacing over exact notation.

    Input : {question}    
    
    ### Output:
    (→ Your Manim code using `Text`, `Line`, `Arrow`, `NumberLine`, `Graph`, etc.)

    """

    )


    code_generation_chain = LLMChain(
        llm=llm,
        prompt=prompt_question_explained,
        verbose=True,
        memory=memory,
        output_key="python_code"
    )

    return code_generation_chain



# === Run the agent chain ===
def run_visualization_chain(question: str):
    agent = create_visualization_agent()
    output = agent.run(question=question)
    print("\n🧑‍💻 Final Output (Python Code):\n")
    print(output)

    code = extract_code(output)
    with open("generated_code.py", "w") as f:
        f.write(code)

    try:
        execute_generated_code(code)
    except Exception as e:
        self_heal_and_retry(str(e), code, max_retries=4)

# === Extract code from markdown-style blocks ===
def extract_code(markdown_text: str) -> str:
    match = re.search(r"```(?:python)?\n(.*?)```", markdown_text, re.DOTALL)
    return match.group(1).strip() if match else markdown_text.strip()

# === Self Healing Logic ===
def self_heal_and_retry(error_message: str, faulty_code: str, max_retries: int = 4):
    print("\n⚠️ Error encountered during execution. Initiating self-healing...\n")
    print(f"Error message: {error_message}")
    
    # Create a new LLM instance for code correction
    llm = ChatOpenAI(
        model = "deepseek/deepseek-r1-0528",
        openai_api_key="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",
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.7,
        max_tokens=5000,

    )    
    # Create prompt for code fixing
    fix_prompt = PromptTemplate(
        input_variables=["code", "error", "attempt"],
        template="""
        You are an expert Python programmer specializing in visualization library manim.
        
        This is attempt {attempt} to fix the code.
        
        The following Python code has generated an error:
        
        ```python
        {code}
        ```
        
        The error message is:
        {error}
        
        Please fix the code to address this error. Return only the corrected code without explanations or markdown formatting.
        Make sure the visualization still accomplishes the original task while fixing the issue.
        
        If this is a repeated attempt, try a different approach to solve the error.
        """
    )
    
    current_code = faulty_code
    
    for attempt in range(1, max_retries + 1):
        print(f"\n🔧 Attempt {attempt}/{max_retries}: Fixing code...\n")
        
        # Create and run the fix chain
        fix_chain = LLMChain(llm=llm, prompt=fix_prompt)
        result = fix_chain({"code": current_code, "error": error_message, "attempt": attempt})
        fixed_code = extract_code(result['text'])
        
        # Save the fixed code
        with open("generated_code.py", "w") as f:
            f.write(fixed_code)
        
        try:
            execute_generated_code(fixed_code)
            print(f"\n✅ Self-healing successful on attempt {attempt}! Code now runs without errors.\n")
            return  # Success, exit the function
        except Exception as e:
            new_error = str(e)
            print(f"\n❌ Attempt {attempt} failed with error: {new_error}\n")
            
            # Update the error message and code for the next attempt
            error_message = new_error
            current_code = fixed_code
            
            # If this was the last attempt, break
            if attempt == max_retries:
                print(f"\n💀 All {max_retries} self-healing attempts failed.")
                print("Final error:", new_error)
                print("Please review the code manually or try a different approach.")
                break

# === Execute based on the visualization library used ===
def execute_generated_code(code: str):
    if "from manim" in code or "import manim" in code:
        scene_class_match = re.search(r"class\s+(\w+)\(Scene\)", code)
        scene_class = scene_class_match.group(1) if scene_class_match else None

        if scene_class:
            result = subprocess.run(
                ["manim", "-pql", "generated_code.py", scene_class],
                text=True,
                capture_output=True,
            )
            print("🎬 Manim Output:\n", result.stdout)
        else:
            raise ValueError("No Manim scene class found.")
    elif any(lib in code for lib in ["import matplotlib", "import seaborn", "import plotly"]):
        result = subprocess.run(
            ["python", "generated_code.py"],
            check=True,
            text=True,
            capture_output=True,
        )
        print("📊 Static Visualization Output:\n", result.stdout)
    else:
        raise ValueError("No supported visualization library detected.")

# === Entry Point ===
if __name__ == "__main__":
    question_input = "Visualise a covolution operation on a 3 channel input"
    run_visualization_chain(question_input)
