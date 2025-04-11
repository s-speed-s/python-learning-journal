class Animal:
    def __init__(self, name, species, care_level):
        self.name = name
        self.species = species
        self.care_level = care_level

    def __str__(self):
        return f"{self.name} ({self.species}) - Care Level: {self.care_level}"

class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hashFunction(self, key):
        return abs(hash(key)) % self.size

    def insert(self, animal):
        index = self.hashFunction(animal.name)
        bucket = self.table[index]

        i = 0
        while i < len(bucket):
            if bucket[i][0] == animal.name:
                bucket[i] = (animal.name, animal)
                return
            i += 1
        bucket.append((animal.name, animal))

    def get(self, name):
        index = self.hashFunction(name)
        bucket = self.table[index]

        i = 0
        while i < len(bucket):
            if bucket[i][0] == name:
                return bucket[i][1]
            i += 1
        return None

    def delete(self, name):
        index = self.hashFunction(name)
        bucket = self.table[index]

        i = 0
        while i < len(bucket):
            if bucket[i][0] == name:
                removed = bucket[i][1]
                del bucket[i]
                return removed
            i += 1
        return None

class CareLevelNode:
    def __init__(self, level):
        self.level = level
        self.animals = []
        self.left = None
        self.right = None

class CarePriorityBST:
    def __init__(self):
        self.root = None

    def insert_by_care_level(self, animal):
        self.root = self._insert(self.root, animal)

    def _insert(self, node, animal):
        if node is None:
            node = CareLevelNode(animal.care_level)
            node.animals.append(animal)
            return node
        if animal.care_level < node.level:
            node.left = self._insert(node.left, animal)
        elif animal.care_level > node.level:
            node.right = self._insert(node.right, animal)
        else:
            node.animals.append(animal)
        return node

    def retrieve_in_range(self, min_level, max_level):
        results = []
        self._retrieve_range(self.root, min_level, max_level, results)
        return results

    def _retrieve_range(self, node, min_level, max_level, results):
        if node is None:
            return
        if min_level <= node.level <= max_level:
            results.extend(node.animals)
        if node.level > min_level:
            self._retrieve_range(node.left, min_level, max_level, results)
        if node.level < max_level:
            self._retrieve_range(node.right, min_level, max_level, results)

    def increase_all_care_levels(self):
        all_animals = []
        self.rebuild_tree(self.root, all_animals)
        self.root = None
        for animal in all_animals:
            animal.care_level = min(animal.care_level + 1, 10)
            self.insert_by_care_level(animal)

    def rebuild_tree(self, node, animals):
        if node is None:
            return
        animals.extend(node.animals)
        self.rebuild_tree(node.left, animals)
        self.rebuild_tree(node.right, animals)


zoo_hash_table = HashTable()
zoo_bst = CarePriorityBST()

animals = [
    Animal("a", "a", 1),
    Animal("b", "b", 2),
    Animal("c", "c", 3),
    Animal("d", "d", 4),
    Animal("e", "e", 5),
    Animal("f", "f", 6),
    Animal("g", "g", 7),
    Animal("h", "h", 8),
    Animal("i", "i", 9),
    Animal("j", "j", 10),
]
for animal in animals:
    zoo_hash_table.insert(animal)
    zoo_bst.insert_by_care_level(animal)

print("find a:")
print(zoo_hash_table.get("a"))

print("\ndelete b:")
deleted = zoo_hash_table.delete("b")
print("Deleted:", deleted)

print("\nincreasing care levels:")
zoo_bst.increase_all_care_levels()

print("\nbasic care (1-3):")
animals_in_range = zoo_bst.retrieve_in_range(1, 3)
for animal in animals_in_range:
    print(animal)

print("\nadvanced care (4-7):")
animals_in_range = zoo_bst.retrieve_in_range(4, 7)
for animal in animals_in_range:
    print(animal)

print("\nintensive care (8-10):")
animals_in_range = zoo_bst.retrieve_in_range(8, 10)
for animal in animals_in_range:
    print(animal)

