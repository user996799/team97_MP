from model_loader import model, tokenizer, device
from explainability import analyze


text = """
The government announced a new policy that will provide financial
support to students across the country.
"""


result = analyze(
    text,
    model,
    tokenizer,
    device,
    no_of_words=5
)


print("\nPrediction:", result["prediction"])
print("Confidence:", result["confidence"])

print("\nExplanation:")

for item in result["explanation"]:
    print(
        item["word"],
        "->",
        item["weight"],
        "->",
        item["effect"]
    )
