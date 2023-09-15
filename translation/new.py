import openai
import os
openai.api_key = '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'
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        # {"role": "system", "content": "You are a helpful assistant."},
        # {"role": "user", "content": "Who won the world series in 2020?"},
        # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": """Parties:
- Party A: John Doe
- Party B: Jane Smith
Terms:
- Effective Date: September 1, 2023
- Duration: 2 years
- Jurisdiction: New York

Agreement:
This Agreement ("Agreement") is entered into by Party A and Party B on the Effective Date. Generate a legal documentation for the above prompt."""}
    ]
)
print(response['choices'][0]['message']['content'])