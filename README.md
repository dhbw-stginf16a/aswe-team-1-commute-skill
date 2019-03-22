# dhbw-stginf16a-aswe-team-1-commute-skill
Commute skill for telling how to get to work

### Needed monitoring entities
 - preferences
    - preferred method of transportation (`preferred_method`)
    - (optional TBD if implemented) time tolerance in min for preferred method (How much slower preference needs to be to be discarded over fastest possibility) (`timediff_tollerated`)
    - (optional) allergies (TODO define format) (`allergies`)
 - polen
 - weather
 - calendar
 - verkehr
 - öpnv

### Proactive output
Time based trigger (optional)

### Requests

#### Get route to destinations
`type`:`commute_route`

##### request-format
 - `start_from`: String that google magically parses to an start location (Can be ommited and defaults to preference home if exists)
 - `destination`: String that google magically parses to an to location (If ommited defaults to work)
```json
{
    "payload":{
        "start_from":"DHBW",
        "destination":"Stuttgart, Hauptbahnhof"
    }
}

```
##### answer-format TBD

#### Get way of transportation
`type`:`commute_work_route`

##### request-format
 - `date`: Date to calculate when to get to work
```json
{
    "payload":{
        "date":"10.02.2019"
    }
}
```
##### answer-format TBD

#### Get latest leaving time
`type`:`commute_latest_leaving`

##### request-format
 - `arrivalTime`: Time to arrive on at destination location as unix timestamp
 - `destination`: Google search string (if ommmited defaults to work)
 - `start_from` : google search string (if ommited defaults to home)
```json
{
    "payload":{
        "arrivalTime":"29348239482390"
    }
}
```
##### answer-format TBD
