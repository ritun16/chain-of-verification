# ⛓ chain-of-verification 💡
How Chain-of-Verification (CoVe) works and how to implement it using Python 🐍 + Langchain 🔗 + OpenAI 🦾 + Search Tool 🔍

📄 **Article**: [I highly recommend reading this article before diving into the code.](https://medium.com/@sourajit16-02-93/chain-of-verification-cove-understanding-implementation-e7338c7f4cb5)

## Architecture
![CoVe_Architecture](https://github.com/ritun16/chain-of-verification/assets/44939374/3efc0f5a-b7c6-4655-8a0e-e16c01cac97e)



## 🚀 Getting Started
1. **Clone the Repository**
2. **Install Dependencies**: 
    ```bash
    python3 -m pip install -r requirements.txt
    ```
3. **Set Up OpenAI API Key**: 
    ```bash
    export OPENAI_API_KEY='sk-...'
    ```
4. **Run the Program**: 
    ```bash
    cd src/
    python3 main.py --question "Who are some politicians born in Boston?"
    ```

## 🛠 Other Arguments
```bash
python3 main.py --question "Who are some politicians born in Boston?" --llm-name "gpt-3.5-turbo-0613" --temperature 0.1 --max-tokens 500 --show-intermediate-steps
```
- --question: This is the original query/question asked by the user
- --llm-name: The OpenAI model name the user wants to use
- --temperature: You know it 😉
- --max-tokens: Tou know it as well 😉
- --show-intermediate-steps: Activating this will alow printing of the intermediate results such as `baseline response`, `verification questions and answers`.

# Few ways to improve
This implementation provides a comprehensive guide for you to modify according to your need and use case. Although below are some of the ideas you can employ to make it more robust and effective.
1. **Prompt Engineering**: 

❤️ If this repository helps, please star ⭐, and share ✔️! <br>
If you also found the [article](https://medium.com/@sourajit16-02-93/chain-of-verification-cove-understanding-implementation-e7338c7f4cb5) informative and think it could be beneficial to others, I'd be grateful if you could like 👍, follow 👉, and share✔️ the piece with others. <br>
Happy coding!
