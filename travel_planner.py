from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class Attraction:
    name: str
    category: str
    cost: int
    rating: float


@dataclass
class FoodPlace:
    name: str
    cuisine: str
    cost: int
    rating: float


@dataclass
class City:
    name: str
    type: str
    budget_level: str
    attractions: List[Attraction]
    foods: List[FoodPlace]
    avg_hotel_cost: int
    transport_cost: int
    tags: List[str]


knowledge_base = {
    "Jaipur": City(
        name="Jaipur",
        type="heritage",
        budget_level="medium",
        attractions=[
            Attraction("Amber Fort", "historical", 300, 4.8),
            Attraction("Hawa Mahal", "historical", 100, 4.6),
            Attraction("City Palace", "museum", 200, 4.5),
            Attraction("Jantar Mantar", "science", 150, 4.4),
        ],
        foods=[
            FoodPlace("Laxmi Misthan Bhandar", "rajasthani", 250, 4.7),
            FoodPlace("Chokhi Dhani", "traditional", 700, 4.6),
            FoodPlace("Rawat Mishthan Bhandar", "snacks", 150, 4.5),
        ],
        avg_hotel_cost=2500,
        transport_cost=1200,
        tags=["heritage", "culture", "family", "food"]
    ),
    "Goa": City(
        name="Goa",
        type="beach",
        budget_level="medium",
        attractions=[
            Attraction("Baga Beach", "beach", 0, 4.7),
            Attraction("Basilica of Bom Jesus", "historical", 0, 4.6),
            Attraction("Dudhsagar Falls", "nature", 400, 4.8),
            Attraction("Fort Aguada", "historical", 100, 4.5),
        ],
        foods=[
            FoodPlace("Fish Thali Spot", "seafood", 400, 4.8),
            FoodPlace("Britto's", "continental", 900, 4.7),
            FoodPlace("Mum's Kitchen", "goan", 700, 4.6),
        ],
        avg_hotel_cost=3000,
        transport_cost=1800,
        tags=["beach", "nightlife", "food", "relax"]
    ),
    "Delhi": City(
        name="Delhi",
        type="metro",
        budget_level="all",
        attractions=[
            Attraction("Red Fort", "historical", 150, 4.7),
            Attraction("Qutub Minar", "historical", 150, 4.8),
            Attraction("India Gate", "monument", 0, 4.7),
            Attraction("Lotus Temple", "architecture", 0, 4.5),
        ],
        foods=[
            FoodPlace("Paranthe Wali Gali", "street food", 200, 4.8),
            FoodPlace("Karim's", "mughlai", 500, 4.7),
            FoodPlace("Saravana Bhavan", "south indian", 300, 4.6),
        ],
        avg_hotel_cost=3500,
        transport_cost=1500,
        tags=["metro", "shopping", "history", "food"]
    ),
    "Manali": City(
        name="Manali",
        type="hill station",
        budget_level="medium",
        attractions=[
            Attraction("Solang Valley", "adventure", 500, 4.8),
            Attraction("Hadimba Temple", "temple", 50, 4.5),
            Attraction("Rohtang Pass", "snow", 1000, 4.7),
            Attraction("Old Manali", "village", 0, 4.4),
        ],
        foods=[
            FoodPlace("Johnson's Cafe", "continental", 600, 4.6),
            FoodPlace("Cafe 1947", "italian", 800, 4.7),
            FoodPlace("The Lazy Dog", "multi-cuisine", 700, 4.5),
        ],
        avg_hotel_cost=2800,
        transport_cost=2000,
        tags=["snow", "adventure", "couple", "nature"]
    ),
    "Kerala": City(
        name="Kerala",
        type="nature",
        budget_level="medium",
        attractions=[
            Attraction("Alleppey Backwaters", "nature", 1200, 4.9),
            Attraction("Munnar Tea Gardens", "nature", 300, 4.8),
            Attraction("Thekkady", "wildlife", 600, 4.6),
            Attraction("Kovalam Beach", "beach", 0, 4.5),
        ],
        foods=[
            FoodPlace("Kerala Sadya Center", "kerala", 300, 4.8),
            FoodPlace("Sea View Restaurant", "seafood", 600, 4.6),
            FoodPlace("Rice Boat", "traditional", 900, 4.7),
        ],
        avg_hotel_cost=3200,
        transport_cost=2200,
        tags=["nature", "family", "relax", "food"]
    )
}


def normalize_budget(budget: int) -> str:
    if budget <= 8000:
        return "low"
    elif budget <= 20000:
        return "medium"
    return "high"


def score_city(city: City, interests: List[str], budget: int, days: int) -> float:
    score = 0.0

    city_tags = set(city.tags)
    user_tags = set(interests)

    matched_tags = city_tags.intersection(user_tags)
    score += len(matched_tags) * 5

    if city.budget_level == "all":
        score += 2

    user_budget_level = normalize_budget(budget)

    if user_budget_level == "low" and city.budget_level == "medium":
        score -= 2
    elif user_budget_level == "low" and city.budget_level == "high":
        score -= 5
    elif user_budget_level == "medium" and city.budget_level == "high":
        score -= 2

    estimated_cost = estimate_trip_cost(city, days)
    if estimated_cost <= budget:
        score += 10
    else:
        score -= 10

    avg_rating = (
        sum(a.rating for a in city.attractions) / len(city.attractions) +
        sum(f.rating for f in city.foods) / len(city.foods)
    ) / 2

    score += avg_rating

    if "food" in user_tags:
        score += 2
    if "history" in user_tags and city.type in ["heritage", "metro"]:
        score += 3
    if "nature" in user_tags and city.type in ["nature", "hill station", "beach"]:
        score += 3
    if "adventure" in user_tags and city.type in ["hill station", "nature"]:
        score += 3
    if "relax" in user_tags and city.type in ["beach", "nature"]:
        score += 2

    return score


def estimate_trip_cost(city: City, days: int) -> int:
    attraction_cost = sum(a.cost for a in city.attractions[:min(days, len(city.attractions))])
    food_cost = sum(f.cost for f in city.foods[:min(days, len(city.foods))])
    hotel_cost = city.avg_hotel_cost * days
    transport_cost = city.transport_cost
    return attraction_cost + food_cost + hotel_cost + transport_cost


def build_itinerary(city: City, days: int) -> List[Tuple[str, str, str]]:
    itinerary = []

    attractions = sorted(city.attractions, key=lambda x: x.rating, reverse=True)
    foods = sorted(city.foods, key=lambda x: x.rating, reverse=True)

    for day in range(days):
        attraction = attractions[day % len(attractions)]
        food = foods[day % len(foods)]

        if day == 0:
            plan = "Arrival, hotel check-in, city local sightseeing"
        elif day == days - 1:
            plan = "Shopping and return preparation"
        else:
            plan = "Full day sightseeing"

        itinerary.append((f"Day {day + 1}", attraction.name, food.name + " | " + plan))

    return itinerary


def recommend_cities(interests: List[str], budget: int, days: int) -> List[Tuple[str, float, int]]:
    city_scores = []

    for city in knowledge_base.values():
        score = score_city(city, interests, budget, days)
        cost = estimate_trip_cost(city, days)
        city_scores.append((city.name, score, cost))

    city_scores.sort(key=lambda x: x[1], reverse=True)
    return city_scores


def explain_recommendation(city: City, interests: List[str], budget: int, days: int) -> None:
    print("\nRecommended Destination:", city.name)
    print("Type:", city.type)
    print("Tags:", ", ".join(city.tags))
    print("Estimated Cost:", estimate_trip_cost(city, days))
    print("Budget Available:", budget)

    print("\nTop Attractions:")
    for a in sorted(city.attractions, key=lambda x: x.rating, reverse=True):
        print("-", a.name, "|", a.category, "| rating:", a.rating, "| cost:", a.cost)

    print("\nFood Suggestions:")
    for f in sorted(city.foods, key=lambda x: x.rating, reverse=True):
        print("-", f.name, "|", f.cuisine, "| rating:", f.rating, "| cost:", f.cost)

    print("\nSuggested Itinerary:")
    itinerary = build_itinerary(city, days)
    for day, place, activity in itinerary:
        print(day + ":", place, "->", activity)


def get_user_input():
    print("AI BASED TRAVEL PLANNER")
    print("=" * 40)

    interests = input("Enter interests separated by comma (example: history,food,nature): ")
    interests = [x.strip().lower() for x in interests.split(",") if x.strip()]

    budget = int(input("Enter total budget in rupees: "))
    days = int(input("Enter number of travel days: "))

    return interests, budget, days


def main():
    interests, budget, days = get_user_input()

    print("\nSearching best destination based on your preferences...")
    results = recommend_cities(interests, budget, days)

    print("\nTop Recommendations:")
    for i, (name, score, cost) in enumerate(results[:3], start=1):
        print(f"{i}. {name} | Score: {round(score, 2)} | Estimated Cost: {cost}")

    best_city_name = results[0][0]
    best_city = knowledge_base[best_city_name]

    explain_recommendation(best_city, interests, budget, days)


if __name__ == "__main__":
    main()