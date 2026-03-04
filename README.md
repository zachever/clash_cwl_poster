# Generating Replays

1. make sure obs is open with correct settings
2. make sure coc is in 1440p with fullscreen
3. Open terminal in repo base directory and run:
```
cd cwl_recorder
python main.py -d 1 -s 1 -p videos/Lethal_Turtles/26_MAR -r _
```

# Stitching + Creating timestamp txt

1. Open terminal in repo base directory and run:
```
cd video_manager
python cwl_api_info.py
```