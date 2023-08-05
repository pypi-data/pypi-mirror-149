# pyframes
Python package for interfacing with the frames.ai database.

Create an account at [spothole.sensorit.io](https://spothole.sensorit.io) to get started.

## Install
```
pip3 install pyframes
```

## Examples
1. Sign in to your account [here](https://spothole.sensorit.io/sign_in).
2. Get your JWT [here](https://spothole.sensorit.io/api/).

```
import pyframes
fm = pyframes.FramesManager()

# replace with your acquired JWT 
fm.set_jwt("<JWT>")

# find some record ids in Cape Town
ids = fm.search(lat=-33.918861, lon=18.423300, radius=1000)
print(ids)

# print some info about the record
record = fm.get_record(ids[0])
print(record.id, record.uint32_t_created)
```
