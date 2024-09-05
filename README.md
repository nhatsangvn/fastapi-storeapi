a simple RestAPI Server based on FastAPI, including:

- request/response
- database schema
- config based on env
- logging

ROUTER <==> SERVICE <==> MODEL
                |    //
              DATA 
                |
            DATABASE


### Prometheus note
#### Types
COUNTER:
- count request

GAUGE:
- count pending item
```
prom_gauge_test.inc()
time.sleep(5)
prom_gauge_test.dec()
```
- last time processed
```
prom_gauge_test.set(time.time())
```

SUMMARY:
- latency
```
start = time.time()
time.sleep(5)
prome_summary_test.observe(time.time() - start)

OR as decorator

@route.get("/test")
@prome_summary_test.time()
def ...
```

#### Naming: 
library_name_unit_suffix

