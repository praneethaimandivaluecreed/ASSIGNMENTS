from pyspark import SparkContext

sc = SparkContext.getOrCreate()

lines = [
    "spark is fast",
    "spark is powerful",
    "python is easy",
    "spark is fast"
]


# creating partitions
rdd = sc.parallelize(lines)

# creating a flat map of all words inside the list
words = rdd.flatMap(lambda line: line.split())

# creating a list of tuples with each word with count1
word_pairs = words.map(lambda word: (word, 1))

r1 = word_pairs.collect()
print(r1)

#adding words
word_counts = word_pairs.reduceByKey(lambda a, b: a + b)

# action
result = word_counts.collect()

print(result)