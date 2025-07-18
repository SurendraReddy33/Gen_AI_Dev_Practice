## Query Operations
 
**This table summarizes the most commonly used query operations in MongoDB:**
 
| Operator / Method        | Description                                     | Example Usage                                         |
|--------------------------|-------------------------------------------------|--------------------------------------------------------|
| `{ field: value }`       | Match documents where `field` equals `value`   | `{ name: "John" }`                                |
| `$gt`, `$lt`, `$gte`, `$lte` | Comparison (greater/less than)                | `{ age: { $gt: 18 } }`                                |
| `$ne`                    | Not equal to                                    | `{ status: { $ne: "inactive" } }`                     |
| `$in`, `$nin`            | Match values in/not in a list                   | `{ city: { $in: ["Vijayawada", "Hyderabad"] } }`      |
| `$and`                   | Combine multiple conditions (AND)              | `{ $and: [{ age: { $gt: 18 } }, { status: "active" }] }` |
| `$or`                    | Match any condition (OR)                       | `{ $or: [{ age: { $lt: 18 } }, { status: "inactive" }] }` |
| `$not`                   | Negate a condition                             | `{ age: { $not: { $gt: 30 } } }`                      |
| `$exists`                | Check if field exists                          | `{ email: { $exists: true } }`                        |
| `$regex`                 | Pattern matching (like SQL LIKE)               | `{ name: { $regex: "^S" } }`                          |
| `find().limit()`         | Limit number of results                        | `db.users.find().limit(5)`                           |
| `find().sort()`          | Sort results ascending/descending              | `db.users.find().sort({ age: -1 })`                  |
| `find().count()`         | Count number of matching documents             | `db.users.find({ age: { $gt: 20 } }).count()`         |
| `findOne()`              | Fetch a single document                        | `db.users.findOne({ name: "John" })`              |
 
> 📝 Use `db.collection.find(query)` to apply most of the above queries.