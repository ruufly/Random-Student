from tkinter import *
from tkinter import messagebox, filedialog, simpledialog, colorchooser, ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
import pickle
from sys import argv
import os
import random
from urllib import request
import json
import yaml
import json
import time
import winsound
import shutil
import configparser
import ctypes
import threading


global version
version = "v2.0"


def getPath(path):
    return os.path.join(os.path.dirname(__file__), path)


def raiseError(title, information):
    messagebox.showerror(title, information)
    mode = "a"
    if not os.path.exists(getPath("error.log")):
        mode = "w"
    with open(getPath("error.log"), mode) as f:
        f.write(
            "%s: %s\n"
            % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), information)
        )


try:
    shutil.rmtree(getPath("temp"))
except FileNotFoundError:
    pass


rewrite = False
global setting
setting = {}
if os.path.exists(getPath("setting.json")):
    with open(getPath("setting.json"), "r") as f:
        try:
            setting = json.load(f)
        except Exception:
            rewrite = True
    if type(setting) == dict:
        for i in [
            "CDrawNumber",
            "Algorithm",
            "Background",
            "Foreground",
            "NameForeground",
            "DownloadFrom",
            "Language",
        ]:
            if not i in setting:
                rewrite = True
    else:
        rewrite = True
else:
    rewrite = True
if rewrite:
    if type(setting) != dict:
        setting = {}
    setting.update(
        {
            "CDrawNumber": 10,
            "Algorithm": "old",
            "Background": "#F8FAED",
            "Foreground": "#525059",
            "NameForeground": {"N": "#525059", "C": "#FBA346", "U": "#92B42A"},
            "DownloadFrom": "github",
            "Language": "zh-CN",
        }
    )
    with open(getPath("setting.json"), "w") as f:
        json.dump(setting, f)


if not os.path.exists(getPath(os.path.join("language", setting["Language"] + ".yml"))):
    raiseError("Error", "Cannot load the language file!")
    exit(1)

with open(
    getPath(os.path.join("language", setting["Language"] + ".yml")),
    "r",
    encoding="utf-8",
) as f:
    global lang
    lang = yaml.safe_load(f)

with open(
    getPath(os.path.join("language", "zh-CN.yml")),
    "r",
    encoding="utf-8",
) as f:
    global m_lang
    m_lang = yaml.safe_load(f)


def getLang(text):
    if text in lang:
        return lang[text]
    elif text in m_lang:
        return m_lang[text]
    else:
        raiseError("Error", "Cannot get the language information: %s" % (text))


global langDict
global langSList
global langSDict
with open(
    getPath(os.path.join("language", "languages.json")), "r", encoding="utf-8"
) as f:
    langDict = json.load(f)
langSList = []
langSDict = {}
for i in langDict:
    langSList.append(langDict[i]["show"])
    langSDict[langDict[i]["show"]] = i


if not os.path.exists(getPath("api.yml")):
    raiseError("Error", "Cannot load the API file!")
    exit(1)

with open(getPath("api.yml"), "r", encoding="utf-8") as f:
    global api
    api = yaml.safe_load(f)

try:
    global logics
    logics = api["logics"]
    global logicDList
    logicDList = []
    global logicDDict
    logicDDict = {}
    for i in logics:
        if logics[i]["show"]:
            logicDList.append(logics[i]["description"][setting["Language"]])
        logicDDict[logics[i]["description"][setting["Language"]]] = i
except KeyError:
    raiseError("Error", "Invalid API!")
    # exit(1)


global pwd
pwd = "123456"
try:
    with open(getPath("password.pkl"), "rb") as f:
        pwd = pickle.load(f)
except Exception:
    messagebox.showinfo(getLang("rdsMessage"), getLang("resetPwd"))
    with open(getPath("password.pkl"), "wb") as f:
        pickle.dump("123456", f)
    pwd = "123456"


root = Tk(className="random student")
root.geometry(
    "%dx%d"
    % (
        langDict[setting["Language"]]["rootSize"],
        langDict[setting["Language"]]["rootSize"],
    )
)
root.title("Random Student")
root.attributes("-topmost", 1)
root.resizable(0, 0)

root.configure(background=setting["Background"])


rewrite = False
studentList = {"version": version, "students": {}}
if os.path.exists(getPath("student.pkl")):
    with open(getPath("student.pkl"), "rb") as f:
        try:
            studentList = pickle.load(f)
            if not "version" in studentList:
                messagebox.showinfo(
                    getLang("rdsMessage"), getLang("oldVersionList"), parent=root
                )
                _studentList = {"version": version, "students": {}}
                for i in studentList:
                    name = i[:-1]
                    tag = "N"
                    if name[-1] == "]":
                        tag = name[-2]
                        name = name[:-3]
                    _studentList["students"][name] = tag
                studentList = _studentList
                rewrite = True
        except Exception:
            rewrite = True
else:
    rewrite = True
if rewrite:
    with open(getPath("student.pkl"), "wb") as f:
        pickle.dump(studentList, f)

historyList = []

os.makedirs(getPath("temp"))
with open(getPath("temp\\history.tmp"), "wb") as f:
    pickle.dump(historyList, f)


class GetNames(object):
    def __init__(self, name="rds"):
        self.name = name


global getNames
getNames = GetNames()


def trueRandom(
    student: dict,
    history: dict,
    isCdraw: bool = False,
    isTest: bool = False,
    CdrawTime: int = 0,
) -> list:
    times = 1
    if isCdraw:
        times = CdrawTime
    data = student["students"]
    names = tuple(data.keys())
    returnBack = []
    for i in range(times):
        returnBack.append(names[random.randint(0, len(data) - 1)])
    return returnBack


def randomWithCNU(
    student: dict,
    history: dict,
    isCdraw: bool = False,
    isTest: bool = False,
    CdrawTime: int = 0,
) -> list:
    times = 1
    if isCdraw:
        times = CdrawTime
    data = student["students"]
    names = tuple(data.keys())
    returnBack = []
    for i in range(times):
        now_time = 0
        now_get = names[random.randint(0, len(data) - 1)]
        while now_get in returnBack:
            now_get = names[random.randint(0, len(data) - 1)]
            while data[now_get] == "C" and now_time < 100:
                now_get = names[random.randint(0, len(data) - 1)]
                while data[now_get] == "N":
                    if random.randint(0, 3) == random.randint(0, 3):
                        break
                    now_get = names[random.randint(0, len(data) - 1)]
                now_time += 1
        returnBack.append(now_get)
    return returnBack


setattr(getNames, "logic::test::etr", trueRandom)

setattr(getNames, "logic::test::tr_with_CNU", randomWithCNU)


setattr(
    getNames,
    "lol",
    lambda: (
        messagebox.showerror(
            "ERROR?",
            "ERROR 0x00114514: AN ERROR HAS OCCURRED THAT COULD PERMANENTLY RENDER YOUR DEVICE UNUSABLE...?",
        ),
        time.sleep(1),
        messagebox.showinfo("LOL", "Happy April Fools' Day!"),
    ),
)

Frame(root, height=5).pack()
studentNow = Label(
    root,
    text=getLang("rdsMessage"),
    font=("Microsoft YaHei UI", 20),
    fg=setting["Foreground"],
    bg=setting["Background"],
)
studentNow.pack()


def about(*args):
    messagebox.showinfo(
        getLang("license"),
        """Random Student v2.0

Copyright 2023-2025 distjr_, ruufly!, hz, dyt_dirt, et al.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
""",
        parent=setup,
    )


def randomName(*args):
    winsound.Beep(2000, 50)
    if api["logics"][setting["Algorithm"]]["type"] == "file":
        shouldAt = os.getcwd()
        os.chdir(getPath(""))
        with open("temp\\student.tmp", "wb") as f:
            pickle.dump(studentList, f)
        os.system(getPath(api["logics"][setting["Algorithm"]]["file"]))
        os.chdir(shouldAt)
        with open(getPath("temp\\now.tmp"), "rb") as f:
            now = pickle.load(f)[0]
    elif api["logics"][setting["Algorithm"]]["type"] == "function":
        now = getattr(getNames, api["logics"][setting["Algorithm"]]["index"])(
            studentList, historyList, False, False
        )[0]
    elif api["logics"][setting["Algorithm"]]["type"] == "foolsday":
        getattr(getNames, api["logics"][setting["Algorithm"]]["index"])()
        return
    historyList.append(
        {"name": now, "type": studentList["students"][now], "cdraw": False}
    )
    with open(getPath("temp\\history.tmp"), "wb") as f:
        pickle.dump(historyList, f)
    studentNow.config(
        text=now,
        fg=setting["NameForeground"][studentList["students"][now]],
        bg=setting["Background"],
    )
    # print(now)


def repeatedRandom(*args):
    global tenRandom
    times = setting["CDrawNumber"]
    data = studentList["students"]
    if api["logics"][setting["Algorithm"]]["type"] == "file":
        with open(getPath("temp\\cdraw.tmp"), "wb") as f:
            pickle.dump(times, f)
        shouldAt = os.getcwd()
        os.chdir(getPath(""))
        with open("temp\\student.tmp", "wb") as f:
            pickle.dump(studentList, f)
        os.system(getPath(api["logics"][setting["Algorithm"]]["file"]))
        os.chdir(shouldAt)
        with open(getPath("temp\\now.tmp"), "rb") as f:
            now = pickle.load(f)
        os.remove(getPath("temp\\cdraw.tmp"))
    elif api["logics"][setting["Algorithm"]]["type"] == "function":
        now = getattr(getNames, api["logics"][setting["Algorithm"]]["index"])(
            studentList, historyList, True, False, times
        )
    elif api["logics"][setting["Algorithm"]]["type"] == "foolsday":
        getattr(getNames, api["logics"][setting["Algorithm"]]["index"])()
        return
    tenRandom = Toplevel(root)
    tenRandom.title(getLang("repeated"))
    tenRandom.attributes("-topmost", 1)
    tenRandom.resizable(0, 0)
    tenRandom.geometry("200x%d" % (times * 40 + 40))
    tenRandom.configure(background=setting["Background"])
    for i in now:
        rep_label = Label(tenRandom, font=("Microsoft YaHei UI", 15), fg="black")
        rep_label.pack()
        root.update()
        for j in range(6):
            rep_label.config(
                text="%s" % (tuple(data.keys())[random.randint(0, len(data) - 1)]),
                fg=setting["Foreground"],
                bg=setting["Background"],
            )
            root.update()
            time.sleep(0.01)
        rep_label.config(
            text="%s" % (i),
            fg=setting["NameForeground"][studentList["students"][i]],
            bg=setting["Background"],
        )
        root.update()
        historyList.append(
            {"name": i, "type": studentList["students"][i], "cdraw": True}
        )
    winsound.Beep(2000, 50)
    with open(getPath("temp\\history.tmp"), "wb") as f:
        pickle.dump(historyList, f)
    but1 = ttk.Button(tenRandom, text="确定", command=lambda: tenRandom.destroy())
    but1.pack()


def update(show=False):
    apis = {
        "github": "https://api.github.com/repos/ruufly/Random-Student/releases/latest",
        "gitee": "https://gitee.com/api/v5/repos/distjr/random-student/releases/latest",
    }
    try:
        data = json.loads(request.urlopen(apis[setting["DownloadFrom"]]).read())
    except Exception:
        raiseError("Error", "Network Error")
        return
    if data["tag_name"] == "v2.0":
        if show:
            messagebox.showinfo(
                getLang("rdsMessage"), getLang("noNewVersion"), parent=setup
            )
    else:
        if messagebox.askyesno(
            getLang("rdsMessage"), getLang("newVersion") % data["name"], parent=setup
        ):
            updateRoot = Toplevel(root)
            updateRoot.title(getLang("downloadProgress"))
            updateRoot.geometry("300x70")
            updateRoot.attributes("-topmost", 1)
            updateRoot.resizable(0, 0)
            global ttc
            ttc = ttk.Progressbar(
                updateRoot, orient="horizontal", length=250, mode="determinate"
            )
            ttc.place(x=5, y=5)
            global utc
            utc = Label(updateRoot)
            utc.place(x=85, y=40)

            def Schedule(a, b, c):
                global ttc
                global utc
                per = 100.0 * a * b / c
                if per > 100:
                    per == 100
                ttc["value"] = per
                utc.config(
                    text=getLang("progress")
                    % ((a * b) / (1024 * 1024), c / (1024 * 1024), per)
                )
                updateRoot.update()

            def del_update(*args):
                global downloading
                if downloading:
                    pass
                else:
                    updateRoot.destroy()

            updateRoot.protocol("WM_DELETE_WINDOW", del_update)
            global downloading
            downloading = True
            request.urlretrieve(
                data["assets"][0]["browser_download_url"], "update.exe", Schedule
            )
            downloading = False
            updateRoot.destroy()
            messagebox.showinfo(
                getLang("rdsMessage"), getLang("startInstall"), parent=setup
            )
            threading.Thread(target=os.system, args=("update.exe",)).start()


def showData(all_data):
    all_data[0] = np.array(all_data[0])
    all_data[1] = np.array(all_data[1])
    all_data[2] = np.array(all_data[2])
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(4, 4))
    bplot1 = axes.boxplot(
        all_data,
        tick_labels=["Censored", "Normal", "Uped"],
        vert=True,
        patch_artist=True,
    )
    colors = ["pink", "lightblue", "lightgreen"]
    for patch, color in zip(bplot1["boxes"], colors):
        patch.set_facecolor(color)
    plt.show()


def getData():
    data = {}
    for i in studentList["students"]:
        data[i] = 0
    for i in historyList:
        data[i["name"]] += 1
    return data


def C_timeC(*args):
    data = getData()
    x = list(data.keys())
    y = [data[i] for i in x]
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.bar(x=x, height=y)
    plt.show()


def C_checkU(*args):
    data = getData()
    all_data = [[], [], []]
    for i in data:
        if studentList["students"][i] == "C":
            all_data[0].append(data[i])
        if studentList["students"][i] == "N":
            all_data[1].append(data[i])
        if studentList["students"][i] == "U":
            all_data[2].append(data[i])
    showData(all_data)


def C_checkA(*args):
    shouldAt = os.getcwd()
    config = configparser.ConfigParser()
    config.read("C_checkA.ini")
    student = {"version": version, "students": {}}
    now_type = api["logics"][setting["Algorithm"]]["type"]
    try_time = int(config["checkA_%s" % (now_type)]["try_time"])
    C_size = int(config["checkA_%s" % (now_type)]["C_size"])
    N_size = int(config["checkA_%s" % (now_type)]["N_size"])
    U_size = int(config["checkA_%s" % (now_type)]["U_size"])
    for i in range(C_size):
        student["students"][
            "".join(random.sample("abcdefghijklmnopqrstuvwxyz", 10))
        ] = "C"
    for i in range(N_size):
        student["students"][
            "".join(random.sample("abcdefghijklmnopqrstuvwxyz", 10))
        ] = "N"
    for i in range(U_size):
        student["students"][
            "".join(random.sample("abcdefghijklmnopqrstuvwxyz", 10))
        ] = "U"

    updateRoot_ = Toplevel(root)
    updateRoot_.title(getLang("checkingS"))
    updateRoot_.geometry("300x70")
    updateRoot_.attributes("-topmost", 1)
    updateRoot_.resizable(0, 0)
    global ttc_
    ttc_ = ttk.Progressbar(
        updateRoot_,
        orient="horizontal",
        length=250,
        mode="determinate",
        maximum=try_time,
        value=0,
    )
    ttc_.place(x=5, y=5)

    history_check = []
    countingS = {}

    def del_update(*args):
        global downloading
        if downloading:
            pass
        else:
            updateRoot_.destroy()

    updateRoot_.protocol("WM_DELETE_WINDOW", del_update)

    global downloading
    downloading = True

    if api["logics"][setting["Algorithm"]]["type"] == "file":
        if os.path.exists(getPath("test")):
            shutil.rmtree(getPath("test"))
        os.mkdir(getPath("test"))
        shouldAt = os.getcwd()
        os.chdir(getPath("test"))
        os.mkdir("temp")
        with open("temp\\test.tmp", "wb"):
            pass
        with open("temp\\student.tmp", "wb") as f:
            pickle.dump(student, f)
        with open("temp\\history.tmp", "wb") as f:
            pickle.dump(tuple(), f)
        for i in range(try_time):
            os.system("..\\%s" % api["logics"][setting["Algorithm"]]["file"])
            with open("temp\\now.tmp", "rb") as f:
                now = pickle.load(f)[0]
            if now in countingS:
                countingS[now] += 1
            else:
                countingS[now] = 1
            history_check.append(
                {"name": now, "type": student["students"][now], "cdraw": False}
            )
            with open("temp\\history.tmp", "wb") as f:
                pickle.dump(tuple(history_check), f)
            ttc_["value"] = i + 1
            updateRoot_.update()
        os.remove("temp\\test.tmp")
    elif api["logics"][setting["Algorithm"]]["type"] == "function":
        api_function = getattr(getNames, api["logics"][setting["Algorithm"]]["index"])
        for i in range(try_time):
            now = api_function(student, history_check, False, True)[0]
            if now in countingS:
                countingS[now] += 1
            else:
                countingS[now] = 1
            history_check.append(
                {"name": now, "type": student["students"][now], "cdraw": False}
            )
            ttc_["value"] = i + 1
            updateRoot_.update()
    elif api["logics"][setting["Algorithm"]]["type"] == "foolsday":
        getattr(getNames, api["logics"][setting["Algorithm"]]["index"])()
        return

    downloading = False

    updateRoot_.destroy()
    all_data = [[], [], []]
    for i in countingS:
        if student["students"][i] == "C":
            all_data[0].append(countingS[i])
        if student["students"][i] == "N":
            all_data[1].append(countingS[i])
        if student["students"][i] == "U":
            all_data[2].append(countingS[i])
    # print(all_data)
    showData(all_data)
    # print(countingS)
    os.chdir(shouldAt)


def C_errorC(*args):
    errorRoot = Toplevel(root)
    errorRoot.title(getLang("errorC"))
    errorRoot.attributes("-topmost", 1)
    errorRoot.resizable(0, 0)
    errorRoot.geometry("520x380")

    global sb1
    sb1 = Scrollbar(errorRoot)
    sb1.pack(side=RIGHT, fill=Y)
    global Left_ListBox_01
    Left_ListBox_01 = Listbox(errorRoot, width=80, height=15, yscrollcommand=sb1.set)
    Left_ListBox_01.pack(side=LEFT, fill=BOTH, expand=True)
    sb1.config(command=Left_ListBox_01.yview)

    with open(getPath("error.log"), "r") as f:
        errors = f.readlines()
        if len(errors):
            for item in errors:
                Left_ListBox_01.insert("end", item[:-1])
        else:
            Left_ListBox_01.insert("end", "(empty)")


def counting(*args):
    countingWin = Toplevel(root)
    countingWin.title(getLang("counting"))
    countingWin.attributes("-topmost", 1)
    countingWin.resizable(0, 0)
    countingWin.geometry("%dx220" % (langDict[setting["Language"]]["countingX"]))
    shouldX = langDict[setting["Language"]]["shouldX"]
    ttk.Button(countingWin, text=getLang("timeC"), command=C_timeC).place(x=5, y=15)
    ttk.Button(countingWin, text=getLang("checkU"), command=C_checkU).place(x=5, y=55)
    ttk.Button(countingWin, text=getLang("checkA"), command=C_checkA).place(x=5, y=95)
    ttk.Button(countingWin, text=getLang("errorC"), command=C_errorC).place(x=5, y=135)
    ttk.Label(countingWin, text=getLang("timeCD")).place(x=shouldX, y=20)
    ttk.Label(countingWin, text=getLang("checkUD")).place(x=shouldX, y=60)
    ttk.Label(countingWin, text=getLang("checkAD")).place(x=shouldX, y=100)
    ttk.Label(countingWin, text=getLang("errorCD")).place(x=shouldX, y=140)


def individuation(*args):
    shouldSetting = setting.copy()
    indWin = Toplevel(root)
    indWin.geometry("260x230")
    indWin.title(getLang("individuationWin"))
    indWin.attributes("-topmost", 1)
    indWin.resizable(0, 0)

    indWin.configure(background=setting["Background"])

    lfg = Label(
        indWin,
        text=getLang("Foreground"),
        font=("Microsoft YaHei UI", 15),
        bg=setting["Background"],
        fg=setting["Foreground"],
    )
    lfg.place(x=10, y=10)
    lfs = {
        "N": Label(
            indWin,
            text=getLang("NameForeground_N"),
            font=("Microsoft YaHei UI", 15),
            bg=setting["Background"],
            fg=setting["NameForeground"]["N"],
        ),
        "C": Label(
            indWin,
            text=getLang("NameForeground_C"),
            font=("Microsoft YaHei UI", 15),
            bg=setting["Background"],
            fg=setting["NameForeground"]["C"],
        ),
        "U": Label(
            indWin,
            text=getLang("NameForeground_U"),
            font=("Microsoft YaHei UI", 15),
            bg=setting["Background"],
            fg=setting["NameForeground"]["U"],
        ),
    }
    nowY = 50
    for i in lfs:
        lfs[i].place(x=10, y=nowY)
        nowY += 40

    def fg(*args):
        setting["Foreground"] = colorchooser.askcolor(
            color=setting["Foreground"], title=getLang("choseColor")
        )[1]
        lfg.config(fg=setting["Foreground"])

    def fs(mode):
        setting["NameForeground"][mode] = colorchooser.askcolor(
            color=setting["NameForeground"][mode], title=getLang("choseColor")
        )[1]
        lfs[mode].config(fg=setting["NameForeground"][mode])

    def bg(*args):
        setting["Background"] = colorchooser.askcolor(
            color=setting["Background"], title=getLang("choseColor")
        )[1]
        indWin.configure(background=setting["Background"])
        lfg.config(bg=setting["Background"])
        for i in lfs:
            lfs[i].config(bg=setting["Background"])
        indWin.update()

    def colorOK(*args):
        messagebox.showinfo(
            getLang("individuationWin"), getLang("indDone"), parent=indWin
        )
        with open(getPath("setting.json"), "w", encoding="utf-8") as f:
            json.dump(setting, f)
        indWin.destroy()

    def indWin_del(*args):
        global setting
        setting = shouldSetting
        indWin.destroy()

    ttk.Button(indWin, text=getLang("setIt"), command=fg).place(x=160, y=10)
    ttk.Button(indWin, text=getLang("setIt"), command=lambda: fs("N")).place(
        x=160, y=50
    )
    ttk.Button(indWin, text=getLang("setIt"), command=lambda: fs("C")).place(
        x=160, y=90
    )
    ttk.Button(indWin, text=getLang("setIt"), command=lambda: fs("U")).place(
        x=160, y=130
    )
    ttk.Button(indWin, text=getLang("bgSetIt"), command=bg).place(x=10, y=170)

    ttk.Button(indWin, text=getLang("okay"), command=colorOK).place(x=160, y=170)
    indWin.protocol("WM_DELETE_WINDOW", indWin_del)


symbolUnchecked = ImageTk.PhotoImage(
    Image.open(getPath("img\\MaterialSymbolsLightCheckBoxOutlineBlank.png")).resize(
        (20, 20)
    )
)
symbolChecked = ImageTk.PhotoImage(
    Image.open(getPath("img\\MaterialSymbolsLightCheckBoxOutlineRounded.png")).resize(
        (20, 20)
    )
)


def manage(*args):
    win = Toplevel(root)
    win.title(getLang("manageStudents"))
    win.attributes("-topmost", 1)
    win.resizable(0, 0)
    win.geometry("720x320")

    rcFrame = Frame(win)  # , height=400)
    columns = ["studentName", "studentType"]
    global sb2
    sb2 = Scrollbar(rcFrame)
    sb2.pack(side=RIGHT, fill=Y)
    global table
    table = ttk.Treeview(rcFrame, columns=columns, yscrollcommand=sb2.set)
    table.heading("#1", text=getLang("studentName"))
    table.heading("#2", text=getLang("studentType"))
    table.pack(fill=BOTH, side=LEFT, expand=True)
    sb2.config(command=table.yview)

    table.tag_configure("checked", image=symbolChecked)
    table.tag_configure("unchecked", image=symbolUnchecked)

    def on_checkbox_changed(*args):
        item_id = table.focus()
        checkbox_state = table.item(item_id, "tag")
        if len(checkbox_state) == 0:
            return
        if checkbox_state[0] == "checked":
            table.item(item_id, tags=("unchecked",))
        else:
            table.item(item_id, tags=("checked",))

    table.bind("<<TreeviewSelect>>", on_checkbox_changed)

    rcFrame.pack(fill=X)
    global typeDict
    typeDict = {"N": "Normal", "C": "Censored", "U": "Uped"}
    global retypeDict
    retypeDict = {"Normal": "N", "Censored": "C", "Uped": "U"}
    global nowStudentList
    nowStudentList = studentList.copy()

    def init():
        for i in nowStudentList["students"]:
            table.item(
                table.insert(
                    "", END, values=(i, typeDict[nowStudentList["students"][i]])
                ),
                tags=("unchecked",),
            )

    init()

    def getSelected():
        times = 0
        for i in table.get_children(None):
            if table.item(i, "tag")[0] == "checked":
                times += 1
        return times

    def allSelect(select: bool):
        for i in table.get_children(None):
            table.item(i, tags=("checked" if select else "unchecked",))

    def invert(*args):
        for i in table.get_children(None):
            checkbox_state = table.item(i, "tag")
            if checkbox_state[0] == "checked":
                table.item(i, tags=("unchecked",))
            else:
                table.item(i, tags=("checked",))

    def change(Type):
        for i in table.get_children(None):
            if table.item(i, "tag")[0] == "checked":
                table.item(i, values=(table.item(i, "values")[0], typeDict[Type]))
                nowStudentList["students"][table.item(i, "values")[0]] = Type

    def delete(*args):
        if getSelected() == 0:
            return
        if messagebox.askyesno(
            getLang("deleteStudent"), getLang("deleteStudent_text"), parent=win
        ):
            for i in table.get_children(None):
                if table.item(i, "tag")[0] == "checked":
                    # table.item(i, values=("deleted", "deleted"))
                    del nowStudentList["students"][table.item(i, "values")[0]]
                    table.delete(i)

    def changeName(*args):
        if getSelected() == 0:
            return
        elif getSelected() != 1:
            messagebox.showinfo(
                getLang("changeName"), getLang("shouldSelectOne"), parent=win
            )
            return
        else:
            putin = simpledialog.askstring(
                title=getLang("changeName"), prompt=getLang("enterName"), parent=win
            )
            if putin == None:
                return
            if putin in list(nowStudentList["students"].keys()):
                messagebox.showinfo(
                    getLang("changeName"), getLang("haveExist"), parent=win
                )
                return
            for i in table.get_children(None):
                if table.item(i, "tag")[0] == "checked":
                    Type = nowStudentList["students"][table.item(i, "values")[0]]
                    del nowStudentList["students"][table.item(i, "values")[0]]
                    table.item(i, values=(putin, typeDict[Type]))
                    nowStudentList["students"][putin] = Type
            allSelect(False)

    def Export(*args):
        filename = filedialog.asksaveasfilename(
            title=getLang("manage_export"),
            filetypes=[
                ("Random Student data file", "*.rsd"),
                ("Random Student connect file", "*.rdc"),
                ("All types", "*.*"),
            ],
            defaultextension=".rsd",
            parent=win,
        )
        if not filename:
            return
        exportData = {}
        for i in table.get_children(None):
            if table.item(i, "tag")[0] == "checked":
                exportData[table.item(i, "values")[0]] = retypeDict[
                    table.item(i, "values")[1]
                ]
        if os.path.splitext(filename)[1] == ".rdc":
            exportData = {"version": version, "students": exportData}
        with open(filename, "wb") as f:
            pickle.dump(exportData, f)

    def Import(*args):
        filename = filedialog.askopenfilename(
            title=getLang("changeToImport"),
            filetypes=[("Random Student data file", "*.rsd"), ("All types", "*.*")],
            parent=win,
        )
        if not filename:
            return
        with open(filename, "rb") as f:
            filedata = pickle.load(f)
        if messagebox.askyesno(
            getLang("changeToImport"), getLang("changeIt"), parent=win
        ):
            nowStudentList["students"].update(filedata)
            for i in table.get_children(None):
                table.delete(i)
            init()

    def New(*args):
        newWin = Toplevel(win)
        newWin.title(getLang("changeToNew"))
        newWin.attributes("-topmost", 1)
        newWin.resizable(0, 0)
        newWin.geometry("400x130")
        Label(newWin, text=getLang("nameIs")).place(x=10, y=10)
        Label(newWin, text=getLang("typeIs")).place(x=10, y=50)
        global enName
        enName = ttk.Entry(newWin)
        enName.place(x=100, y=5)
        global typesValue
        typesValue = StringVar()
        typesBox = ttk.Combobox(
            newWin, textvariable=typesValue, state="readonly", width=30
        )
        typesBox.place(x=100, y=45)
        typesTuple = ("Normal", "Censored", "Uped")
        typesBox["value"] = typesTuple

        def newOK(*args):
            if enName.get() in nowStudentList["students"]:
                messagebox.showinfo(
                    getLang("changeToNew"), getLang("haveExist"), parent=newWin
                )
                return
            if not typesBox.get() in typesTuple:
                messagebox.showinfo(
                    getLang("changeToNew"), getLang("typesShouldType"), parent=newWin
                )
                return
            newName = enName.get()
            newType = retypeDict[typesBox.get()]
            table.item(
                table.insert(
                    "", END, values=(newName, typeDict[newType])
                ),
                tags=("unchecked",),
            )
            nowStudentList["students"][newName] = newType
            messagebox.showinfo(getLang("changeToNew"), getLang("changeToNewDone"), parent=newWin)
            newWin.destroy()

        ttk.Button(newWin, text=getLang("manage_okay"), command=newOK).place(
            x=300, y=90
        )

    def nowOK(*args):
        global studentList
        if messagebox.askyesno(getLang("manageStudents"), getLang("IsItDone"), parent=win):
            studentList = nowStudentList
            messagebox.showinfo(getLang("manageStudents"), getLang("ItIsDone"), parent=win)
            win.destroy()

    ttk.Button(win, text=getLang("changeToN"), command=lambda: change("N")).place(
        x=10, y=250
    )
    ttk.Button(win, text=getLang("changeToC"), command=lambda: change("C")).place(
        x=130, y=250
    )
    ttk.Button(win, text=getLang("changeToU"), command=lambda: change("U")).place(
        x=250, y=250
    )
    ttk.Button(win, text=getLang("changeToDelete"), command=delete).place(x=370, y=250)
    ttk.Button(win, text=getLang("changeName"), command=changeName).place(x=490, y=250)
    ttk.Button(win, text=getLang("changeToNew"), command=New).place(x=610, y=250)
    ttk.Button(win, text=getLang("allSelect"), command=lambda: allSelect(True)).place(
        x=10, y=280
    )
    ttk.Button(
        win, text=getLang("allNotSelect"), command=lambda: allSelect(False)
    ).place(x=130, y=280)
    ttk.Button(win, text=getLang("invert"), command=invert).place(x=250, y=280)
    ttk.Button(win, text=getLang("changeToImport"), command=Import).place(x=370, y=280)
    ttk.Button(win, text=getLang("manage_export"), command=Export).place(x=490, y=280)
    ttk.Button(win, text=getLang("manage_okay"), command=nowOK).place(x=610, y=280)


def Setting(*args):
    global setting
    global setup
    setup = Toplevel(root)
    setup.title(getLang("setting"))
    setup.attributes("-topmost", 1)
    setup.resizable(0, 0)
    setup.geometry("420x490")
    shouldX = langDict[setting["Language"]]["shouldX"]
    Label(setup, text=getLang("manageStudents")).place(x=5, y=20)
    ttk.Button(setup, text=getLang("manageStudentsButton"), command=manage).place(
        x=shouldX, y=15
    )
    Label(setup, text=getLang("count")).place(x=5, y=60)
    ttk.Button(setup, text=getLang("countButton"), command=counting).place(
        x=shouldX, y=55
    )
    Label(setup, text=getLang("CDraw")).place(x=5, y=100)
    sp = ttk.Spinbox(setup, from_=1, to=15)
    sp.delete(0, "end")
    sp.insert("end", str(setting["CDrawNumber"]))
    sp.config(state="readonly")
    sp.place(x=shouldX, y=95)
    Label(setup, text=getLang("logic")).place(x=5, y=140)

    global logicValue
    logicValue = StringVar()
    logicBox = ttk.Combobox(setup, textvariable=logicValue, state="readonly", width=30)
    logicBox.place(x=shouldX, y=135)
    logicBox["value"] = tuple(logicDList)
    logicBox.set(logics[setting["Algorithm"]]["description"][setting["Language"]])
    Label(setup, text=getLang("update")).place(x=5, y=180)
    ttk.Button(setup, text=getLang("updateCheck"), command=lambda: update(True)).place(
        x=shouldX, y=175
    )
    Label(setup, text=getLang("license")).place(x=5, y=220)
    ttk.Button(setup, text=getLang("licenseButton"), command=about).place(
        x=shouldX, y=215
    )
    Label(setup, text=getLang("openSource")).place(x=5, y=260)

    def github(*args):
        os.system("start https://github.com/zhuoyue2023/random-student")

    def gitee(*args):
        os.system("start https://gitee.com/distjr/random-student")

    global tp_github
    tp_github = PhotoImage(file=getPath("img\\github.gif"))
    l_github = Label(setup, image=tp_github, width=30, height=30)
    l_github.place(x=shouldX, y=255)
    l_github.bind("<Button-1>", github)
    global tp_gitee
    tp_gitee = PhotoImage(file=getPath("img\\gitee.gif"))
    l_gitee = Label(setup, image=tp_gitee, width=30, height=30)
    l_gitee.place(x=shouldX + 50, y=255)
    l_gitee.bind("<Button-1>", gitee)
    Label(setup, text=getLang("about")).place(x=5, y=300)

    def blog(*args):
        os.system("start https://ruufly.github.io/")

    global tp_blog
    tp_blog = PhotoImage(file=getPath("img\\favicon.gif"))
    l_blog = Label(setup, image=tp_blog, width=30, height=30)
    l_blog.place(x=shouldX + 50, y=295)
    l_blog.bind("<Button-1>", blog)

    def bilibili(*args):
        os.system("start https://space.bilibili.com/1159124697")

    global tp_bilibili
    tp_bilibili = PhotoImage(file=getPath("img\\bilibili.gif"))
    l_bilibili = Label(setup, image=tp_bilibili, width=30, height=30)
    l_bilibili.place(x=shouldX, y=295)
    l_bilibili.bind("<Button-1>", bilibili)
    Label(setup, text=getLang("individuation")).place(x=5, y=340)
    ttk.Button(setup, text=getLang("individuationButton"), command=individuation).place(
        x=shouldX, y=335
    )

    Label(setup, text=getLang("languageSet")).place(x=5, y=380)
    global langValue
    langValue = StringVar()
    langBox = ttk.Combobox(setup, textvariable=langValue, state="readonly", width=30)
    langBox.place(x=shouldX, y=375)
    langBox["value"] = tuple(langSList)
    langBox.set(langDict[setting["Language"]]["show"])

    Label(setup, text=getLang("downloadFrom")).place(x=5, y=420)
    global downValue
    downValue = StringVar()
    downBox = ttk.Combobox(setup, textvariable=downValue, state="readonly", width=30)
    downBox.place(x=shouldX, y=415)
    downBox["value"] = ("github", "gitee")
    downBox.set(setting["DownloadFrom"])

    def okay(*args):
        repeatTime = int(sp.get())
        newLogic = logicDDict[logicBox.get()]
        newLang = langSDict[langBox.get()]
        newDown = downBox.get()
        setting["CDrawNumber"] = repeatTime
        setting["Algorithm"] = newLogic
        setting["DownloadFrom"] = newDown
        setting["Language"] = newLang
        with open(getPath("setting.json"), "w", encoding="utf-8") as f:
            json.dump(setting, f)
        messagebox.showinfo(getLang("setting"), getLang("setDone"), parent=setup)
        setup.destroy()

    ttk.Button(setup, text=getLang("okay"), command=okay).place(x=310, y=450)


Frame(root, height=10).pack()
butRds = ttk.Button(root, text=getLang("rds"), command=randomName)
butRds.pack()
butRep = ttk.Button(root, text=getLang("repeated"), command=repeatedRandom)
butRep.pack()
butSetting = ttk.Button(root, text=getLang("setting"), command=Setting)
butSetting.pack()

# update(False)

root.mainloop()
