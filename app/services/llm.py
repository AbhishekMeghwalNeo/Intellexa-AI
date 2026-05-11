from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)

class LLMService:

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    @classmethod
    def llm_call_test(cls, query: str) -> str:
        
        response = cls.client.chat.completions.create(
            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "user",
                    "content": query
                }
            ],

            temperature=0
        )

        return response.choices[0].message.content

    @classmethod
    def generate_answer(
        cls,
        question: str,
        retrieved_chunks: list[str]
    ) -> str:

        context = "\n\n".join(retrieved_chunks)

        prompt = f"""
            You are a helpful AI assistant.

            Answer ONLY from the provided context.

            If the answer is not present in the context,
            say:
            "I could not find the answer in the document."

            Context:
            {context}

            Question:
            {question}
            """

        response = cls.client.chat.completions.create(
            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0
        )

        return response.choices[0].message.content
    
if __name__ == "__main__":
    
    output = LLMService.llm_call_test("What is 2 + 2? ")

    print(output)   