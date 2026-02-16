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
|Data Representation|||
|Data Search and Retrieval|||
|Indexing|||
|Scaleability|||
|Applications|||
