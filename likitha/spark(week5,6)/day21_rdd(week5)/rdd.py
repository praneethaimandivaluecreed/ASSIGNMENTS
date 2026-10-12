from pyspark.sql import SparkSession



# Create Spark Session


spark = (
    SparkSession.builder
    .appName("Day03_RDD_Word_Count")
    .master("local[4]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

sc = spark.sparkContext



# Input data


sentences = [
    "Spark makes data processing fast",
    "Spark processes data using distributed computing",
    "RDD is a distributed data structure",
    "Spark uses RDD transformations and actions",
    "Transformations are lazy in Spark"
]



#  Create RDD


text_rdd = sc.parallelize(sentences, 4)

print("INITIAL RDD")


print("Number of partitions:", text_rdd.getNumPartitions())



# flatMap()


words_rdd = text_rdd.flatMap(
    lambda line: line.lower().split()
)


print("AFTER flatMap()")


print("Sample words:")
print(words_rdd.take(10))



# map()
# Convert each word into (word, 1)


word_pairs = words_rdd.map(
    lambda word: (word, 1)
)


print("AFTER map()")


print(word_pairs.take(10))



# reduceByKey()


word_counts = word_pairs.reduceByKey(
    lambda x, y: x + y
)


print("AFTER reduceByKey()")


print("reduceByKey() introduces a SHUFFLE.")

print("Word count partitions:",
      word_counts.getNumPartitions())



# Sort the results


sorted_counts = word_counts.sortBy(
    lambda pair: pair[1],
    ascending=False
)


print("AFTER sortBy()")


#Sorting requires data redistribution and can cause a shuffle.



# ACTION



#FINAL WORD COUNT"


results = sorted_counts.collect()

for word, count in results:
    print(f"{word:20} -> {count}")



#  Other actions



#RDD ACTIONS


print("Total unique words:", word_counts.count())

print("First 5 results:", sorted_counts.take(5))



#Stop Spark


spark.stop()
