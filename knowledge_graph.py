class KnowledgeGraph:

    def __init__(self):
        self.graph = {}

    def add_relation(self, subject, relation, obj):

        if subject not in self.graph:
            self.graph[subject] = []

        self.graph[subject].append((relation, obj))

    def display(self):

        print("\nKNOWLEDGE GRAPH")

        for subject in self.graph:

            for relation, obj in self.graph[subject]:

                print(
                    subject,
                    "--",
                    relation,
                    "-->",
                    obj
                )

    def query(self, entity):

        if entity not in self.graph:
            print("No information found")
            return

        print("\nInformation about", entity)

        for relation, obj in self.graph[entity]:

            print(relation, ":", obj)


kg = KnowledgeGraph()

kg.add_relation(
    "Jaipur",
    "HAS_ATTRACTION",
    "Amber Fort"
)

kg.add_relation(
    "Jaipur",
    "HAS_ATTRACTION",
    "Hawa Mahal"
)

kg.add_relation(
    "Jaipur",
    "KNOWN_FOR",
    "Heritage"
)

kg.add_relation(
    "Goa",
    "HAS_ATTRACTION",
    "Baga Beach"
)

kg.add_relation(
    "Goa",
    "KNOWN_FOR",
    "Beaches"
)

kg.add_relation(
    "Goa",
    "KNOWN_FOR",
    "Nightlife"
)

kg.display()

kg.query("Jaipur")