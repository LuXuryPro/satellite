# Satellite
Simple simulator, which uses evolution algorithm to find the best parameters for satellite.

## Setup:
###Clone repo
```bash
git clone https://github.com/LuXuryPro/satellite.git
```
In case of errors try using pip install to get needed libraries.

##Starting simulation
```bash
python3 video.py
```

##Example of JSON file with planets stats:
```bash
{
   "simulation":{
      "start-planet":"0",
      "destination-planet":"1",
      "planets":[
         {
            "distance-to-sun":"50",
            "mass":"10",
            "start-angle":"0"
         },
         {
            "distance-to-sun":"100",
            "mass":"20",
            "start-angle":"1.57"
         }
      ]
   }
}
```