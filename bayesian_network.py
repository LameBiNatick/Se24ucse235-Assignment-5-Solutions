from itertools import product

weather_prob = {
    "Good": 0.7,
    "Bad": 0.3
}

budget_prob = {
    "High": 0.6,
    "Low": 0.4
}

travel_prob = {

    ("Good", "High"): 0.95,
    ("Good", "Low"): 0.75,

    ("Bad", "High"): 0.50,
    ("Bad", "Low"): 0.10
}


def probability_of_travel():

    total = 0

    for weather, budget in product(
        weather_prob,
        budget_prob
    ):

        p_weather = weather_prob[weather]
        p_budget = budget_prob[budget]

        p_travel = travel_prob[
            (weather, budget)
        ]

        total += (
            p_weather *
            p_budget *
            p_travel
        )

    return total


print("=" * 50)
print("BAYESIAN NETWORK EXAMPLE")
print("=" * 50)

print(
    "\nProbability of travelling =",
    round(
        probability_of_travel(),
        4
    )
)