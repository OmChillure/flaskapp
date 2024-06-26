from flask import Flask, render_template, request ,jsonify 
from flask_cors import CORS , cross_origin
from langchain_community.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])
repo_id = "google/flan-t5-xxl"
llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 90}
)

llm_chain = LLMChain(prompt=prompt, llm=llm)

# @app.route('/')
# def home():
#     return render_template('index.html')

@app.route('/get-response')
@cross_origin()
def get_response():
    print(request.form)
    user_input = request.args.get('user_input')
    response = llm_chain.run(user_input)
    return response

if __name__ == '__main__':
    app.run(debug=True , port='5000')
