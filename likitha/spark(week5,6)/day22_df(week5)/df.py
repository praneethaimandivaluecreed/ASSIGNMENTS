from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split, lower, trim



# create spark session


spark = (
    SparkSession.builder
    .appName("Day04_DataFrame_Word_Count")
    .master("local[4]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")



# input data


sentences = [
    "Spark makes data processing fast",
    "Spark processes data using distributed computing",
    "RDD is a distributed data structure",
    "Spark uses RDD transformations and actions",
    "Transformations are lazy in Spark"
]



#  create initial database


df = spark.createDataFrame(
    [(sentence,) for sentence in sentences],
    ["sentence"]
)

print("\nINITIAL DATAFRAME")
df.printSchema()
df.show(truncate=False)



# validation


# Check for null sentences
null_count = df.filter(col("sentence").isNull()).count()

if null_count > 0:
    raise ValueError(f"Validation failed: {null_count} null sentences found.")

print("Validation passed: No null sentences.")



# transformation



words_df = df.select(
    explode(
        split(
            lower(trim(col("sentence"))),
            "\\s+"
        )
    ).alias("word")
)

print("\nAFTER EXPLODE")
words_df.show(10)



# validate words


null_words = words_df.filter(col("word").isNull()).count()

empty_words = words_df.filter(
    trim(col("word")) == ""
).count()

if null_words > 0 or empty_words > 0:
    raise ValueError(
        f"Validation failed: "
        f"{null_words} null words, "
        f"{empty_words} empty words."
    )

print("Validation passed: No null or empty words.")



#  word count


word_counts = (
    words_df
    .groupBy("word")
    .count()
    .withColumnRenamed("count", "word_count")
)

print("\nAFTER GROUP BY + COUNT")
word_counts.show()



# sort results


sorted_counts = word_counts.orderBy(
    col("word_count").desc()
)

print("\nFINAL WORD COUNT")
sorted_counts.show(truncate=False)



#  other dataframe operations


unique_words = word_counts.count()

print("Total unique words:", unique_words)

print("\nFirst 5 results:")
sorted_counts.show(5)


#  stop spark


spark.stop()