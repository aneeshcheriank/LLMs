## Vector Databases
- to store and query vectorized data raipidly
- data as vectors in multi-dimentional space
- vectors encapsulate essential attributes of the items they represent
- useful for
    - similarity search
    - nearest neighbours queries
    - assessing distance/similarity between vectors

### Vector database and data storage
- vector db stores vectors, depict each data item.
- each number signifies various attributes or featuers of the object
- the image depicts how these vectors are formed
![alt text](img/image.png)

### Vector libraries
- in memory vector databases
- vector dbs use pre-configured algoritms to store and update data
- the vector dbs have full CRUD (reate, read, update and delete) capabilities

## Relationship databases
- organize data into rows and columns
- SQL
- managing structured data (relationships are well-defined)

### data storage
- data in tables, each data point respresets a distinct entry or relationship
- row: record, column: a property or attribute
- tables connect each other using  keys (main and foreign)
    - **main key**: the unique identifier in a table (not null, once assigned will not change)
    - **foreign key**: record in a table that point to the main key in another table

![alt text](img/image1.png)
- manipulate the rows and columns using
    - SELECT, INSERT, UPDATE, DELETE operations

## Comparision between relationship and vector dbs
|Function|Traditional databases|Vector databases|
|---|---|---|
|Data Representation|Traditional databases organize data in a structured format using tables, rows, and columns, ideal for relational data.|Vector databases represent data as multi-dimensional vectors, efficiently encoding complex and unstructured data like images, text, and sensor data.|
|Data Search and Retrieval|SQL queries are suited for traditional databases with structured data.|Vector databases specialize in similarity searches and retrieving vectorized data, facilitating tasks like image retrieval, recommendation systems, and anomaly detection.|
|Indexing|Traditional databases employ indexing methods like B-trees for efficient data retrieval.|Vector databases use indexing structures like metric trees and hashing suited for high-dimensional spaces, enhancing nearest-neighbor searches and similarity assessments.|
|Scaleability|Scaling traditional databases can be challenging, often requiring resource augmentation or data sharding.|Vector databases are designed for scalability, especially in handling large datasets and similarity searches, using distributed architectures for horizontal scaling.|
|Applications|Traditional databases are pivotal in business applications and transactional systems where structured data is processed.|Vector databases shine in analyzing vast datasets, supporting fields like scientific research, natural language processing, and multimedia analysis.|
