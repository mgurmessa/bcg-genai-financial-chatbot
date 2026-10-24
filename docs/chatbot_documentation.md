# GFC Financial Chatbot: Prototype Documentation

## How it works
The chatbot is a Python script that answers five predefined questions about Apple, Microsoft, or Tesla. It loads the financial data from Task 1 (`data/financial_data.csv`) with pandas and uses if-elif statements to match the user's question to a response. Each response looks up the relevant FY2025 figures and, where needed, calculates a ratio or year-over-year change before returning a sentence.

- **State:** the user picks a company at the start, and the chatbot remembers it for every question until the user types "change company."
- **Error handling:** if the user enters a company that isn't in the data, the chatbot asks again. If a question doesn't match, it lists the questions it can answer.
- **Input matching:** questions are compared without regard to capitalization, extra spaces, or a trailing question mark.

## Predefined queries

| Query | Response |
|---|---|
| What is the total revenue? | FY2025 total revenue |
| How has net income changed over the last year? | Percentage change in net income from FY2024 to FY2025, with both amounts |
| What is the net margin? | FY2025 net income as a percentage of revenue |
| What is the debt ratio? | FY2025 total liabilities as a percentage of total assets |
| What is the operating cash flow? | FY2025 cash flow from operating activities |

## Running it
From the repo folder, run `python financial_chatbot.py` in a terminal or `%run financial_chatbot.py` in a Jupyter cell. Type "quit" to exit.

## Limitations
- Questions must match the predefined wording. Rephrased questions like "How much revenue did Apple make?" are not recognized.
- Answers cover FY2025 only (and FY2024 for the net income comparison). Earlier years aren't available through the chatbot.
- Only one company can be discussed at a time, so there are no side-by-side comparisons.
- The chatbot reports numbers without context. For example, it doesn't explain that Tesla's large drop in net income partly reflects one-time items, which the Task 1 analysis identified.
- Fiscal years end in different months for each company, so "FY2025" covers a different 12-month period for Apple, Microsoft, and Tesla.

## Possible improvements
Natural language processing would let users phrase questions freely, and adding context notes, year selection, and company comparisons would make the answers more useful. A simple web interface built with Flask could also display charts of each metric's trend.
