# Satellite
Simple simulator, which uses evolution algorithm to find the best starting parameters for satellite.

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
You can provide json file with starting parameters as input argument.
```bash
python3 video.py simulation.json
```
If no file name is specified default config.json will be used.

##Example of JSON file with planets stats(default config.json):
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