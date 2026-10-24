"""
GFC Financial Chatbot (rule-based prototype)
--------------------------------------------
Built for the BCG GenAI Job Simulation (Forage), Task 2.

Answers five predefined questions about Apple, Microsoft, and Tesla using
figures pulled by hand from their FY2023-FY2025 10-K filings (Task 1).

Usage:
    python financial_chatbot.py        # from a terminal
    %run financial_chatbot.py          # from a Jupyter cell
"""

import sys
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

# Look for the CSV in data/ first (repo layout), then next to the script.
# This keeps the script working whether it's run from the repo or on its own.
SCRIPT_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
CANDIDATE_PATHS = [SCRIPT_DIR / "data" / "financial_data.csv", SCRIPT_DIR / "financial_data.csv"]
DATA_PATH = next((p for p in CANDIDATE_PATHS if p.exists()), None)

if DATA_PATH is None:
    sys.exit("Could not find financial_data.csv. Place it in data/ or next to this script.")

# All figures are in USD millions. thousands="," lets pandas read values like "391,035".
df = pd.read_csv(DATA_PATH, thousands=",")

COMPANIES = ["Apple", "Microsoft", "Tesla"]

# The exact questions the bot understands. Also shown to the user as a menu.
QUESTIONS = [
    "What is the total revenue?",
    "How has net income changed over the last year?",
    "What is the net margin?",
    "What is the debt ratio?",
    "What is the operating cash flow?",
]

LATEST_YEAR = 2025
PRIOR_YEAR = 2024


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_value(company, year, column):
    """Return one figure (USD millions) for a company and fiscal year."""
    row = df[(df["Company"] == company) & (df["Fiscal Year"] == year)]
    return row[column].iloc[0]


def billions(millions):
    """Format a USD-millions value as a readable '$X.X billion' string."""
    return f"${millions / 1000:,.1f} billion"


# ---------------------------------------------------------------------------
# Core logic: match the question, compute the answer
# ---------------------------------------------------------------------------

def simple_chatbot(user_query, company):
    """Return the bot's answer for one question about the selected company."""
    # Normalize so "  What is the Debt Ratio " and "what is the debt ratio?" match
    query = user_query.lower().strip().rstrip("?")

    revenue = get_value(company, LATEST_YEAR, "Total Revenue")
    net_income = get_value(company, LATEST_YEAR, "Net Income")

    if query == "what is the total revenue":
        return f"{company}'s total revenue for FY{LATEST_YEAR} was {billions(revenue)}."

    elif query == "how has net income changed over the last year":
        prior = get_value(company, PRIOR_YEAR, "Net Income")
        change = (net_income - prior) / prior * 100        # year-over-year % change
        direction = "increased" if change > 0 else "decreased"
        return (f"{company}'s net income {direction} by {abs(change):.1f}% from "
                f"FY{PRIOR_YEAR} to FY{LATEST_YEAR}, from {billions(prior)} to {billions(net_income)}.")

    elif query == "what is the net margin":
        margin = net_income / revenue * 100                # profit kept per $1 of revenue
        return (f"{company}'s net margin for FY{LATEST_YEAR} was {margin:.1f}%, "
                f"meaning it kept about {margin:.0f} cents of profit per dollar of revenue.")

    elif query == "what is the debt ratio":
        liabilities = get_value(company, LATEST_YEAR, "Total Liabilities")
        assets = get_value(company, LATEST_YEAR, "Total Assets")
        ratio = liabilities / assets * 100                 # share of assets funded by liabilities
        return (f"{company}'s debt ratio for FY{LATEST_YEAR} was {ratio:.1f}%, "
                f"meaning that share of its assets is funded by liabilities.")

    elif query == "what is the operating cash flow":
        ocf = get_value(company, LATEST_YEAR, "Cash Flow from Operating Activities")
        return f"{company} generated {billions(ocf)} in cash from operations in FY{LATEST_YEAR}."

    # Anything unrecognized falls through to a help message listing valid questions
    return "Sorry, I can only answer these questions:\n" + "\n".join("- " + q for q in QUESTIONS)


def choose_company():
    """Prompt until the user picks a supported company. Returns None if they type 'quit'."""
    while True:
        choice = input("Which company? (Apple, Microsoft, or Tesla): ").strip()
        if choice.lower() == "quit":
            return None
        choice = choice.title()                            # "apple" -> "Apple"
        if choice in COMPANIES:
            return choice
        print("Sorry, I only have data for Apple, Microsoft, and Tesla.")


# ---------------------------------------------------------------------------
# Main chat loop
# ---------------------------------------------------------------------------

def main():
    print("GFC Financial Chatbot")
    company = choose_company()     # stays selected until the user changes it
    if company is None:
        print("Bot: Goodbye!")
        return

    print("\nYou can ask:")
    for q in QUESTIONS:
        print("-", q)
    print("Type 'change company' to switch companies, or 'quit' to exit.")

    while True:
        user_query = input(f"\n[{company}] You: ")
        command = user_query.lower().strip()

        if command == "quit":
            print("Bot: Goodbye!")
            break
        elif command == "change company":
            company = choose_company()
            if company is None:
                print("Bot: Goodbye!")
                break
        else:
            print("Bot:", simple_chatbot(user_query, company))


if __name__ == "__main__":
    main()
