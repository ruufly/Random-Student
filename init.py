import pickle

with open("setting.pkl", "wb") as f:
    pickle.dump(
        {
            "CDrawNumber": 10,
            "Algorithm": "old",
            "Background": "#F8FAED",
            "Foreground": "#525059",
            "StyleName": "Normal",
            "DownloadFrom": "github",
            "Language": "zh-CN"
        },
        f,
    )
