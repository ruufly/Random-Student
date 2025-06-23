# Random Student

[![GitHub issues](https://img.shields.io/github/issues/ruufly/Random-Student.svg)](https://github.com/ruufly/Random-Student/issues) [![Github license](https://img.shields.io/github/license/ruufly/Random-Student.svg)](https://github.com/ruufly/Random-Student/blob/main/LICENSE) [![Download](https://img.shields.io/badge/downloads-main-green.svg)](https://codeload.github.com/ruufly/Random-Student/zip/main) [![Github forks](https://img.shields.io/github/forks/ruufly/Random-Student.svg)](https://github.com/ruufly/Random-Student/network) [![GitHub stars](https://img.shields.io/github/stars/ruufly/Random-Student.svg)](https://github.com/ruufly/Random-Student/stargazers)

[个人网站](https://ruufly.github.io/) | [Github 仓库](https://github.com/ruufly/Random-Student/) | [开源许可证](https://github.com/ruufly/Random-Student/blob/main/LICENSE)

> 一款基于 python 的随机学生点名器。

## 作者

以下列出了参与本项目的作者。

- [@distjr_/@ruufly!](https://github.com/ruufly)
- [@dytdirt](https://github.com/dytdirt)
- @hz

## 使用说明

本软件打开后，界面上共有 随机学生、连抽、设置 三个选项。

- 选择 随机学生 选项后，会随机抽取一名学生并将姓名显示出来；
- 选择 连抽 选项后，会弹出连抽窗口，依次显示所有被抽中的学生；
- 选择 设置 选项后，进入设置窗口。

### 设置

进入设置窗口后，共有以下选项：

- 管理学生名单：经过密码验证，可修改学生名单或将名单导出；
- 点名次数统计：可统计本次软件使用过程中的点名情况、报错情况，还可通过 高通量检验 功能，测试随机逻辑优劣性；
- 设置连抽次数：设置连抽中一次抽取学生数量（需要注意，如果设置的连抽次数大于学生总数，在某些随机逻辑下可能会出现无法预测的错误）；
- 随机逻辑：设置随机抽取使用的算法；
- 版本更新：检测新版本并安装；
- 软件许可证：查看软件的开源许可证（Apache 2.0）；
- 开放源代码：查看软件源代码（github/gitee）
- 关于作者：查看作者个人主页
- 个性化设置：设置软件的配色方案；
- 语言设置：设置软件显示语言；
- 更新包下载源：设置版本更新时下载更新包的源（github更新发布更早，gitee在国内下载速度更快）；
- 修改密码：修改管理学生名单的密码；
- 重置配置：重置用户的所有配置（设置、插件、学生名单等）以解决一些可能由配置问题导致的程序异常；
- 批量导入名单：批量导入学生名单时，请将学生名单以 `UTF-8` 编码的纯文本格式存储，每行一个学生姓名，行尾不要有空格，随后在此处打开。

### CNU系统

本软件中，每个学生都有其分类，所有学生共分为 Censored(C), Normal(N), Uped(U) 三类

- Censored 类的学生被抽取到的概率会降低（在某些随机逻辑下概率为0），请将缺席学生置于此类；
- Normal 类的学生被抽到的概率正常，请将大多数学生置于此类；
- Uped 类的学生被抽取到的概率会大幅升高，可视情况将某些学生置于此类。

### 插件系统

本软件包含插件系统，用户可自行编写插件以给本软件添加新功能。

每个插件包含本体与接口两部分，本体推荐存储在 `.\plugin\` 中，接口需在 `.\api.yml` 中声明。

#### 插件的编写

##### 随机逻辑插件

在 `.\api.yml` 的 `logics` 中添加如下内容：

```yaml
logics:
  ...
  <name>:
    description:
      zh-SI: <description(zh-SI)>
      zh-TR: <description(zh-TR)>
      en: <description(en)>
      <Language>: <description(<Language>)>
    type: "function" | "file"
    index: <index>
    file: <path>
    show: true | false
    refresh: true | false
    refreshIndex: <index>
  ...
```

各配置项的解释如下：

| 选项         | 描述                                                                                                                                                                    |
| :----------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| description  | 该逻辑的描述（请保证该项与其他插件的该项不同，用户选择随机逻辑时只能看到该项）<br />其下列有不同语言，请至少填写 `zh-SI` 的内容，这是软件找不到对应语言时的默认语言。 |
| type         | 有 `function` 和 `file` 两项，编写的插件该项均为 `file` 。                                                                                                        |
| index        | `function` 型插件特有参数，可留空。                                                                                                                                   |
| file         | `file` 型插件特有参数，请填写插件本体的路径（相对于软件根目录）                                                                                                       |
| show         | 是否在设置栏显示该插件。                                                                                                                                                |
| refresh      | `function` 型插件特有参数，可留空。                                                                                                                                   |
| refreshIndex | `function` 型插件特有参数，可留空。                                                                                                                                   |

当用户开始随机抽取学生时，系统会将学生名单转存至 `.\temp\student.tmp` ，将学生抽取历史转存至 `.\temp\history.tmp`

如果用户使用连抽，系统会将连抽次数转存至 `.\temp\cdraw.tmp`

以上数据均使用 `pickle.dump` 存储

如果用户使用高通量检验功能，则系统会创建空文件 `.\temp\test.tmp`

其中，学生名单文件格式如下：

```json
{
    "version": <version>,
    "students": {
        "name": <type>("N|C|U"),
        ...
    }
}
```

学生抽取历史文件格式如下：

```json
[
    {
        "name": <name>,
        "type": "N|C|U",
        "cdraw": true | false
    },
    ...
]
```

### 高通量检验

在 设置-点名次数统计-高通量检验 中。

通过生成大量学生，再进行大量抽取试验以检验随机逻辑的优劣性。

您可以通过修改 `C_checkA.ini` 以配置高通量检验。

该文件的配置格式如下：

```ini
[checkA_file]
try_time = <try_time>
C_size = <C_size>
N_size = <N_size>
U_size = <U_size>

[checkA_function]
try_time = <try_time>
C_size = <C_size>
N_size = <N_size>
U_size = <U_size>
```

其中， `checkA_file` 为检验 `file` 逻辑的配置，`checkA_function` 为检验 `function` 逻辑的配置， `try_time` 为随机抽取次数， `C|N|U_size` 分别为检验中生成的各类学生人数。

### 链接文件

在 设置-管理学生名单-导出 中，将学生数据导出为 Random Student connect file 后即保存为链接文件。

在正常安装本软件的前提下，直接打开链接文件，即可将链接文件中的数据作为学生名单的来源以随机抽取。

## 版本变更记录

参见 [CHANGELOG.md](https://github.com/ruufly/Random-Student/blob/main/CHANGELOG.md)
