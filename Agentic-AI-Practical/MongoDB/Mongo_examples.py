from pymongo import MongoClient

mongo_cluster = "mongodb+srv://surendrareddygandra3:onTwB6qFMES4HF24@genai-cluster.cb98ycb.mongodb.net/"
database_name = "test_db"
collection = "people"

client = MongoClient(mongo_cluster) #connect to mongo cluster
database = client[database_name] # connect to mongo db
people_collection = database[collection] # connect to collection

# ***************************** Insert ****************************************

insert_one_statement = { "name" : "Surendra", "age" : "23", "city" : "Hyderabad", "pincode" : "500049"}
insert_one_statement = { "name" : "Surendra", "age" : "23", "city" : "Hyderabad", "designation" : "Agentic AI Developer"}
insert_one_statement = { "name" : "Surendra"}
# people_collection.insert_one(insert_one_statement)

# ************************** Bulk Insert *****************************

# people_collection.insert_many(
#     [
#         {
#             "name" : "Surendra",
#             "designation" : "Agentic AI Developer",
#             "salary" : "50000",
#             "doj" : "01/01/2025"
#         },
#         {
#             "name" : "Surendra",
#             "designation" : "Agentic AI Developer",
#             "salary" : "50000",
#             "doj" : "01/01/2025"
#         },
#         {
#             "name" : "Gowri",
#             "designation" : "Agentic AI Developer",
#             "salary" : "50000",
#             "doj" : "01/01/2025"
#         },
#         {
#             "name" : "Vijay",
#             "designation" : "Agentic AI Developer",
#             "salary" : "50000",
#             "doj" : "01/01/2025"
#         }
#     ]
# )

# ********************* Nested Insert **********************

# people_collection.insert_one(
#     {
#         "name" : "Surendra",
#         "city" : "Hyderabad",
#         "salary" : "55000",
#         "address" : {"street" : "Hitechcity", "landmark" : "CyberTowers", "pincode" : "500050"}
#     }
# )

# ********************** Find ALl ***************************

# for document in people_collection.find():
#     print(document)

# ********************* FInd One *****************88

# document = people_collection.find_one()
# print(document)

# ****************** Find One - Filter ****************

# document = people_collection.find(
#     {
#         "name" : "Surendra",
#         "salary" : "55000"
#     }
# )
# for doc in document:
#     print(doc)

# ******************* Greater than ****************

# documents = people_collection.find(
#     {
#     "salary" : {"$gt" : "50000"}
# })
# for doc in documents:
#     print(doc)

# ********************* Find One - Sort ************

# documents = people_collection.find().sort("salary", 1)

# for doc in documents:
#     print(doc)

# document = people_collection.find_one().sort(("salary", 1))


# documents = people_collection.find().sort("salary", 1).limit(3)
# for doc in documents:
#     print(doc)


# documents = people_collection.find().sort("salary", 1)
# documents = people_collection.find({}, {"_id":0, "name": 1, "designation": 1})
# for doc in documents:
#     print(doc)

#  *************************** FInd one - Start with **************

# documents = people_collection.find({
#     "name": {"$regex" : "^G"}
# })

# for doc in documents:
#     print(doc)

# ******************** Delete *****************

people_collection.delete_one({
    "name" : "Surendra"
})

people_collection.delete_many({
    "salary" : "51000"
})