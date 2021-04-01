from redisearch import GeoFilter, GeoField, Client, Query, IndexDefinition, TextField, NumericField
# AutoCompleter, Suggestion, aggregation, reducers, TagField

import redis

# python3 pip install redisearch
# https://github.com/RediSearch/redisearch-pyhistory
# see https://github.com/redis-developer/demo-movie-app-redisearch-python for more search example code
# http://geohash.gofreerange.com/  <-- helpful to find long lat
# kick off a container running search:  docker run -p 6379:6379 redislabs/redismod &

def printResult(comment, res, query):
    print('\n********\n'+comment)
    print('\tCharacters submitted: -->  '+query.query_string())
    
    if(res.total>0):
        print('\ntotal # results: ' +str(res.total)) 
        print(res.docs)
        #print('city: ' +res.docs[0].city)
        #print('state: ' +res.docs[0].state)
    elif(res.total<1):
        print('no result for that ^ query\n')
        #print('score: ' +str(res.docs[0].score))


# Creating a client with a given index name
client = Client("idx:cities:test_index")

try:
    client.drop_index()
except:
    print('index does not exist yet - no worries...')

# IndexDefinition auto-indexes any hashes with keys that have a matching prefix
definition = IndexDefinition(
   prefix=['addr:'],
   language='English'
   )

# Creating the index definition and schema
client.create_index(
(
    TextField("city", weight=5.0, phonetic_matcher='dm:en'), 
    TextField("state", weight=1.0),
    TextField("search_terms_city", weight=2.0, phonetic_matcher='dm:en'),
    GeoField('loc')
),
stopwords = [],
definition=definition)

# Create the alias 
client.aliasadd("idx:cities")


# Indexing a document for RediSearch 2.0+
client.redis.hset('addr:1',
                mapping={
                    'city': 'San Francisco',
                    'state': 'CA',
                    'search_terms_city': 'SFO,S.F.O.,SF,San Frn,frisco',
                    'loc': "-122.419,37.774"
                })
client.redis.hset('addr:2',
                mapping={
                    'city': 'Los Angeles',
                    'state': 'CA',
                    'search_terms_city': 'Los Angls,LA,Los Angels',
                    'loc': "-118.129,33.897"
                })
client.redis.hset('addr:3',
                mapping={
                    'city': 'San Jose',
                    'state': 'CA',
                    'search_terms_city': 'SanJose',
                    'loc': "-121.859,37.291"
                })
client.redis.hset('addr:4',
                mapping={
                    'city': 'Albuquerque',
                    'state': 'NM',
                    'search_terms_city': 'Abq,Albekerke',
                    'loc': "-106.640,35.064"
                })


comment= '1: Simple search: Query(\'SFO\').with_scores()'
q = Query('SFO').with_scores()
res = client.search(q)

# the result has the total number of results, and a list of documents
printResult(comment,res,q)

# Searching with complex parameters:
comment = '2: Query(\'SFO\').verbatim().no_content().with_scores().paging(0, 5)'
q = Query('SFO').verbatim().no_content().with_scores().paging(0, 5)
res = client.search(q)
printResult(comment,res,q)

comment = '3: Query(\'%%fisco%%\').with_scores()'
q = Query('%%fisco%%').with_scores()
res = client.search(q)
printResult(comment,res,q)

comment = '4: Query(\'sfo\').with_scores()'
q = Query('sfo').with_scores()
res = client.search(q)
printResult(comment,res,q)

comment = '5: Query(\'CA\').with_scores()'
q = Query('CA').with_scores()
res = client.search(q)
printResult(comment,res,q)

comment = '5a: Query(\'CA\').add_filter(GeoFilter(\'loc\', -118.1294 , 33.8979, 100)).with_scores()'
q = Query('CA').add_filter(GeoFilter('loc', -118.1294 , 33.8979, 100)).with_scores()
res = client.search(q)
printResult(comment,res,q)

comment = '5b: Query(\'CB\').add_filter(GeoFilter(\'loc\', -118.1294 , 33.8979, 100)).with_scores()'
q = Query('CB').add_filter(GeoFilter('loc', -118.1294 , 33.8979, 100)).with_scores()
res = client.search(q)
printResult(comment,res,q)

comment = '5c: Query(\'%%CB%%\').add_filter(GeoFilter(\'loc\', -118.1294 , 33.8979, 100)).with_scores()'
q = Query('%%CB%%').add_filter(GeoFilter('loc', -118.1294 , 33.8979, 100)).with_scores()
res = client.search(q)
printResult(comment,res,q)


comment = '6: Query(\'alb*\').with_scores()'
q = Query('alb*').with_scores()
res = client.search(q)
printResult(comment,res,q)

comment = '7: Query(\'san francisco\').no_content().verbatim().with_scores()'
q = Query('san francisco').no_content().verbatim().with_scores()
res = client.search(q)
printResult(comment,res,q)

comment = '7a: Query(\'san bubba francisco\').with_scores()'
q = Query('san bubba francisco').with_scores()
res = client.search(q)
printResult(comment,res,q)

comment = '8: Query(\'francisco san\').with_scores()'
q = Query('francisco san').with_scores()
res = client.search(q)
printResult(comment,res,q)

comment = '9: Query(\'albakurki\').with_scores()'
q = Query('albakurki').with_scores()
res = client.search(q)
printResult(comment,res,q)

comment = '10: Query(\'%%sajo%%\').with_scores()'
q = Query('%%sajo%%').with_scores()
res = client.search(q)
printResult(comment,res,q)

comment = '11: Query(\'%%sajo%%\').with_scores().limit_ids(\'addr:3\')'
q = Query('%%sajo%%').with_scores().limit_ids('addr:3')
res = client.search(q)
printResult(comment,res,q)

if __name__ == '__main__':
    print('\n\nEnd of Program')