import subprocess
import pandas as pd


def ping(hostname):
    result = subprocess.getoutput("ping " + hostname).encode("cp1251").decode("cp866")
    return result


hosts = [
    "yandex.ru",
    "google.com",
    "nsu.ru",
    "roboflow.com",
    "music.yandex.ru",
    "github.com",
    "e.mail.ru",
    "vk.com",
    "instagram.com",
    "wildberries.ru",
]
df = pd.DataFrame(hosts, columns=["Name"])

df["Successfull"] = "No"
df["Ping (ms)"] = "-"

for index, host in enumerate(hosts):
    result = ping(host)

    if result is None:
        continue

    lines = result.splitlines()
    pingTimes = []

    for line in lines:
        if "время=" in line:
            parts = line.split()
            for part in parts:
                if ("время=") in part:
                    pingTime = float(part.split("=")[1].replace("мс", ""))
                    pingTimes.append(pingTime)
    if pingTimes:
        avgTime = sum(pingTimes) / len(pingTimes)
        df.at[index, "Ping (ms)"] = avgTime
        df.at[index, "Successfull"] = "Yes"

print(df)
df.to_csv("ping.csv", sep=",")
