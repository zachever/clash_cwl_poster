import os
import subprocess
import imageio_ffmpeg
import json
import cwl_api_info as cwl_api_info

#CLAN = "Lethal_Turtles"
CLAN = "Turtleing"
CWL_DATE = "26_MAR"
ONLY_THREE_STARS = True


directory = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.dirname(directory)

videos_dir = os.path.join(
    parent_dir,
    "cwl_recorder",
    "videos",
    CLAN,
    CWL_DATE
)

ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

file_list_path = os.path.join(videos_dir, "files.txt")

def get_duration(file_path):
    # Use ffmpeg to get duration
    result = subprocess.run(
        [
            ffmpeg_path,
            "-i", file_path
        ],
        capture_output=True,
        text=True
    )

    # Parse duration from stderr (ffmpeg prints info to stderr)
    import re
    m = re.search(r"Duration: (\d+):(\d+):(\d+).(\d+)", result.stderr)
    if m:
        h, m_, s, ms = map(int, m.groups())
        duration_seconds = h*3600 + m_*60 + s + ms/100
        return duration_seconds
    else:
        raise ValueError(f"Could not get duration for {file_path}")


def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:06.3f}"

timestamps = []
current_time = 0.0

with open(file_list_path, "w", encoding="utf-8") as f:
    try:
        for day in range(1, 8):
            for attack in range(1, 16):

                stars = cwl_api_info.get_attack_info(day, attack)["stars"]
                if ONLY_THREE_STARS and stars < 3:
                    continue

                file_name = f"attack_{attack}.mp4"
                file_path = os.path.join(videos_dir, f"day_{day}", file_name)

                if os.path.exists(file_path):
                    safe_path = file_path.replace("\\", "/")
                    f.write(f"file '{safe_path}'\n")

                    duration = get_duration(file_path)

                    timestamps.append({
                        "day": day,
                        "attack": attack,
                        "start_time_seconds": current_time,
                        "start_time_formatted": format_timestamp(current_time)
                    })

                    current_time += duration
    except Exception as e:
        print(f"An error occurred while processing videos, this may be okay if not recording all replays for whole cwl at once: {e}")

output_path = os.path.join(videos_dir, "archive.mp4")

subprocess.run([
    ffmpeg_path,
    "-f", "concat",
    "-safe", "0",
    "-i", file_list_path,
    "-c", "copy",
    output_path
], check=True)

os.remove(file_list_path)

print("Archive created successfully.\n")

def format_youtube_time(seconds):
    total_seconds = int(seconds)
    minutes = total_seconds // 60
    secs = total_seconds % 60
    return f"{minutes}:{secs:02}"

output_txt_path = os.path.join(videos_dir, "timestamps.txt")

with open(output_txt_path, "w", encoding="utf-8") as f:
    current_day = None

    for t in timestamps:
        day = t["day"]

        if day != current_day:
            if current_day is not None:
                f.write("\n")
            f.write(f"Day {day}:\n")
            current_day = day

        time_str = format_youtube_time(t["start_time_seconds"])

        attack_info = cwl_api_info.get_attack_info(t["day"], t["attack"])
        defender = attack_info["defender"]
        attacker = attack_info["attacker"]

        #line = f"{time_str} - Attack {t['attack']}: {attacker} vs {defender}\n"
        #line = f"{time_str} - {attacker} vs {defender}\n"
        line = f"{time_str} - {attacker}\n"
        f.write(line)

print("timestamps.txt created.")