from filinglens.llm import get_llm

llm = get_llm()

response = llm.generate(
    system="You are a helpful assistant.",
    user="Say hello in one sentence.",
)

print(response.answer)
