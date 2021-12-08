# TempPyRest

This is a small API for sensor data like temperature and humidity.

Example:

```bash
curl 127.0.0.1:5000/kj2 -X PUT -d '{"temp": "23.3", "humi": "33"}' -H "Content-Type: application/json"
# {'success': 'Data saved.'}
```
## Explanation
`127.0.0.1:5000` - Network address depending where the service is running.  
`/kj2` - Example key. Each sensor must have its own key. Must be available in the database.  
`-X PUT` - Data is only transmitted in json format.  
`-d '{"temp": "23.3", "humi": "33"}'` - Data attributes in JSON format.  
`-H "Content-Type: application/json"` - Tells in which content-type format the data will be passed to the api.  
`{'success': 'Data saved.'}` - Response will be in JSON format.

## Available data attributes
`temp` - Requested, float type, Temperature  
`humi` - Requested, float type, Humidity  
`date` - Possible, datatime ISO format, Date with Time
