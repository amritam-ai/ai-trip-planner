from openai import OpenAI
import streamlit as st
import json

# Initialize OpenAI client
client = OpenAI()

# -----------------------------
# APP TITLE
# -----------------------------

st.title("AI Trip Planner")
st.markdown("Generate a personalized travel itinerary using AI.")

# -----------------------------
# USER INPUT
# -----------------------------

destination = st.text_input("Destination")
days = st.number_input("Number of days", min_value=1, max_value=14, value=5)
total_budget = st.number_input("Total budget", min_value=3000, max_value=10000, value=5000)

# -----------------------------
# BUTTON ACTION
# -----------------------------

if st.button("Generate Itinerary"):

    # Check if destination is entered
    if not destination:
        st.error("Please enter a destination.")
    else:
        # Deterministic logic
        daily_budget = total_budget / days

        st.write(f"Daily Budget: {round(daily_budget, 2)}")

        # Prompt creation
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

        # LLM Call with loading spinner
        with st.spinner("Generating itinerary..."):
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

        # -----------------------------
        # PARSE + DISPLAY
        # -----------------------------

        try:
            data = json.loads(clean_output)

            if "itinerary" not in data:
                st.error("Invalid response format from AI.")
            else:
                st.subheader("Itinerary")

                for day in data["itinerary"]:
                    if "day" not in day or "activity" not in day or "location" not in day:
                        st.warning("Missing fields in one of the days.")
                        continue

                    st.write(f"Day {day['day']} → {day['activity']} ({day['location']})")

        except json.JSONDecodeError:
            st.error("AI response was not valid JSON.")