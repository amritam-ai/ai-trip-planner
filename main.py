from openai import OpenAI
import json

client = OpenAI()

# -----------------------------
# USER INPUT + GUARDRAILS
# -----------------------------

def get_inputs():
    destination = input("Enter your destination: ")
    days = int(input("Enter number of travel days: "))
    total_budget = float(input("Enter total trip budget: ").replace(",", "").strip())

    if total_budget < 3000 or total_budget > 10000:
        print("Error: Budget must be between 3000 and 10000")
        exit()

    if days <= 0 or days > 14:
        print("Error: Days must be between 1 and 14")
        exit()

    return destination, days, total_budget


# -----------------------------
# LLM CALL (Prompt + API)
# -----------------------------

def generate_itinerary(destination, days, total_budget):
    
    daily_budget = total_budget / days

    print("\nDaily Budget:", round(daily_budget, 2))

    prompt = f"""
Create a {days}-day itinerary for a family of 3 (2 adults and one 8-year-old).

Destination: {destination}

Budget:
Total Budget: {total_budget}
Daily Budget Limit: {daily_budget:.2f}

Focus on sightseeing, food, and cultural experiences.

Return ONLY valid JSON in this format:

{{
  "itinerary": [
    {{"day": 1, "activity": "...", "location": "..."}}
  ]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.4,
        messages=[
            {"role": "system", "content": "Return ONLY valid JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    output = response.choices[0].message.content
    clean_output = output.replace("```json", "").replace("```", "").strip()

    return clean_output


# -----------------------------
# PARSE + DISPLAY
# -----------------------------

def evaluate_and_display(clean_output, days):
    try:
        data = json.loads(clean_output)

        if "itinerary" not in data:
            print("ERROR: 'itinerary' missing")
            return

        itinerary = data["itinerary"]

        if len(itinerary) != days:
            print("⚠️ Warning: Number of days does not match input")

        print("\nFinal Itinerary:\n")

        for day in itinerary:
            if "day" not in day or "activity" not in day or "location" not in day:
                print("⚠️ Missing fields")
                continue

            print(f"Day {day['day']} → {day['activity']} ({day['location']})")

    except json.JSONDecodeError:
        print("ERROR: Invalid JSON from model")


# -----------------------------
# MAIN
# -----------------------------

def main():
    destination, days, total_budget = get_inputs()

    clean_output = generate_itinerary(destination, days, total_budget)

    evaluate_and_display(clean_output, days)


if __name__ == "__main__":
    main()