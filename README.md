
## PERFORMANCE
### INGESTION IMPROVEMENTS
After taking into consideration the need to make inserts much faster and with the request that this should have good scalability and also bring the thought of handling much more data, I have researched for better options to handle MongoDB inserts without using the simple **insert_many()**.

First of all, we have implemented a pool for Mongo, this allows us to use more than one instance of a client at concurrency, which allows to make multiple inserts at the same time. Apart from that I have made python pool equivalent to the cpu number to being able to launch a pool in each of my cpu cores. Once everything is set, I set a chunksize to efficiently divide the list in parts and being able to insert each register having all pools running with data.

I have used this documentation as a reference for a good practice:
- https://vladmihalcea.com/mongodb-facts-80000-insertssecond-on-commodity-hardware/ 
- https://pymongo.readthedocs.io/en/stable/faq.html#how-does-connection-pooling-work-in-pymongo
- https://saksham-malhotra2196.medium.com/the-efficient-way-of-using-multiprocessing-with-pymongo-a7f1cf72b5b7

This procedure has been applied to both ingestion modules.

### ABOUT API REQUEST PAGINATION

I have checked both APIs docs to see if pagination was available, but as these examples are very small, they do not provide pagination, so then improvements in performance have been only on our side.  

I have not implemented the pagination for the result, as we are already giving the option to limit the results. This could be performed if needed, but I did not want to give a different format thant the one asked in the PDF.

## POSSIBLE IMPROVEMENTS TO CURRENT PROJECT

-  Orchestration with Airflow in a container that runs every 10 min or so a docker-compose up of those containers that ingest data into MongoDB.
- Using examples with more data and with pagination available