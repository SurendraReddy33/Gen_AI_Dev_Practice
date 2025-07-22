# pip install dspy-ai
# pip install "dspy-ai[openai]"

# 📘 DSPy (Declarative Self-improving Python) – Notes
 
# 🧠 What is DSPy?
 
# DSPy is a Python framework to build modular, declarative, and self-improving workflows using large language models (LLMs). 
# It allows you to define prompts and logic in a structured way, much like defining functions. 
# Think of it as a bridge between traditional Python programming and LLM prompt engineering. 

import dspy
class HelloWorld (dspy.Predict): # dspy.Predict - A base class to define a module that takes inputs and generates outputs using an LLM.
    def __init__ (self):
        super().__init__(signature="name -> message") # Signature - Declares what the model should expect as inputs and what it should return.

    # forward() - method Implements how the output is generated using the inputs.
    def forward(self, name: str) -> str:
        return f"Hello {name}, Welcome to the Magic of DSPY"
    
predictor = HelloWorld()

print (predictor(name="Ameet"))