user = "root"
password="1234"
url = "jdbc:mysql://localhost:3306/mysql"
driver = "com.mysql.cj.jdbc.Driver"

get_url = "/Housing/data/json/"

detail = spark.read.json(get_url+"detail.json")
competition = spark.read.json(get_url+"competition.json")
convinient = spark.read.josn(get_url+"convinient.json")
park = spark.read.json(get_url+"park.json")
subway = spark.read.json(get_url+"subway2.json")
school = spark.read.json(get_url+"school.json")
mart = spark.read.json(get_url+"mart.json")
bus = spark.read.json(get_url+"bus.json")


