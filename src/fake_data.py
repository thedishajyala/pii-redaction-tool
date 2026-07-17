from faker import Faker


class FakeDataGenerator:
    def __init__(self):
        self.fake = Faker()
        self.replacements = {}

    def generate(self, entity_type: str, original: str) -> str:
        key = (entity_type, original)

        if key in self.replacements:
            return self.replacements[key]

        if entity_type == "EMAIL":
            fake_value = self.fake.email()

        elif entity_type == "PHONE":
            fake_value = self.fake.numerify("9#########")

        else:
            fake_value = original

        self.replacements[key] = fake_value
        return fake_value
