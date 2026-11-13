# CTF Writeups

PWN 与 RE 题目、附件和分析记录。

## 目录

- [re](re/)：29 个条目，每题一个编号目录。
- [pwn](pwn/)：49 个条目，只分[栈](pwn/%E6%A0%88/)、[堆](pwn/%E5%A0%86/)、[内核](pwn/%E5%86%85%E6%A0%B8/)。

```text
CTF-Writeups/
├── re/
│   ├── 001.题名/
│   └── ...
└── pwn/
    ├── 栈/
    │   ├── 001.题名/
    │   └── ...
    ├── 堆/
    │   ├── 001.题名/
    │   └── ...
    └── 内核/
        ├── 001.题名/
        └── ...
```

每个分类从 001 连续编号，每题保留对应附件、脚本和已有题解。README 采用“知识点 → 题目分析 → EXP”，题内图片放在 isset/。格式参考 [Real-Simplicity / BUUCTF-Pwn](https://github.com/Real-Simplicity/BUUCTF-Pwn/tree/main/012.get_started_3dsctf_2016)。

格式化字符串题归入栈目录；存在堆对象漏洞的 VM、IoT 题归入堆目录。其他 VM／表达式栈题及全局覆盖题的具体归类说明写在题目页。

已有题解中的运行结果以原记录为准。本次调整完成静态归档检查，4 份历史脚本的 Python 版本或代码完整性问题见[检查记录](ARCHIVE_CHECKS.json)。

[归档清单](ARCHIVE_MANIFEST.json) · [题解来源](WRITEUP_SOURCES.json) · [排除清单](EXCLUDED_FILES.md)
