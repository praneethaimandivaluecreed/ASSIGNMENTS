from pyspark.sql import SparkSession


spark = (
    SparkSession.builder
    .appName("RDDWordCount")
    .master("local[*]")
    .getOrCreate()
)

sc = spark.sparkContext

lines = sc.parallelize([
    "hello spark",
    "spark is powerful",
    "hello world",
    "spark is fast"
], 4)

print("Number of partitions:", lines.getNumPartitions())


words = lines.flatMap(
    lambda line: line.split()
)


word_pairs = words.map(
    lambda word: (word, 1)
)


word_counts = word_pairs.reduceByKey(
    lambda a, b: a + b
)


results = word_counts.collect()

for word, count in sorted(results):
    print(f"{word}: {count}")


spark.stop()