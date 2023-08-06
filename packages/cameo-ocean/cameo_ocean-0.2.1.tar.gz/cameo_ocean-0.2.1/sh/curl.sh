rm -fr data
time curl -d '
{
  "id": "cameo_0005",
  "manufacturerId": "vision",
  "lat": "24.173244",
  "lon": "120.575615",
  "alt": 3,
  "time": "2022-04-26 09:44:08",
  "deviceType": "微型感測器",
  "county": "雲林縣",
  "attributes": [
      {
      "key": "area",
      "value": "測試"
    },
    {
      "key": "areaType",
      "value": "一般社區"
    },
    {
      "key": "town",
      "value": "斗六市"
    }
  ],
  "data": [
    {
      "sensor": "pm2_5",
      "value": "16.34",
      "unit": "ug/m3"
    },
    {
      "sensor": "temperature",
      "value": 23.2,
      "unit": "°C"
    },
    {
      "sensor": "humidity",
      "value": 60.7,
      "unit": "%"
    },
    {
      "sensor": "voltage",
      "value": 3,
      "unit": ""
    }

  ]
}
' -H "Content-Type: application/json" -X POST http://localhost:20430/api/log_msgpack/
