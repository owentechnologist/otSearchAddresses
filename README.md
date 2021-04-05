# otSearchAddresses

This code shows simple python-based interactions with RediSearch

It creates an index and a search schema. 

It loads several hashes into Redis (which are automagically indexed)

It executes a few queries - printing out the queries and the results.

You may find these things useful:

> python3 pip install redisearch

 https://github.com/RediSearch/redisearch-pyhistory


### for more search example code: 

https://github.com/redis-developer/demo-movie-app-redisearch-python 


### helpful to find long lat:

http://geohash.gofreerange.com/  

### kick off a container running search:  

docker run -p 6379:6379 redislabs/redismod &

### these tests can be useful as references 
https://github.com/RediSearch/RediSearch/blob/master/tests/pytests/test_fuzzy.py

### discussion on the use of fuzzy queries
https://forum.redislabs.com/t/search-query-syntax-complex-query-in-one-exact-phrase-prefix-and-fuzzy/661/4
