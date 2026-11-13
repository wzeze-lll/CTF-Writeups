# CTF Writeups

PWN、逆向、Web 与 Misc 的个人学习归档。

## 方向

- [Labs](Labs/)：1 个条目
- [Misc](Misc/)：3 个条目
- [PWN](PWN/)：49 个条目
- [Reverse](Reverse/)：29 个条目
- [Web](Web/)：1 个条目

## 题目格式

每题采用 `编号.题名/README.md`，正文为“知识点 → 题目分析 → EXP”，图片目录为 `isset/`。文件和已有分析随题保存。

格式参考 [Real-Simplicity / BUUCTF-Pwn](https://github.com/Real-Simplicity/BUUCTF-Pwn/tree/main/012.get_started_3dsctf_2016)。本仓库使用自己的附件和已有笔记，未复制范例题解或图片。

## 归档说明

- 来源为 buuctf、题型、D3ctf、考核、逆向 buu 五个本地目录，补入可匹配的个人题解。
- 标题未知或题型不明确的附件保留原始标识，分析状态以各题记录为准。
- Linux ELF、Windows PE 和 APK 需在对应环境中验证；本次仅整理和静态核验。已有题解中的实测表述属于原记录。
- [Environment](Environment/) 保留共享运行库，[Supporting](Supporting/) 保留未能可靠配对的辅助材料。
- 同内容二进制采用相对符号链接；正常 Git 克隆会保留，Windows 需要启用符号链接支持。
- 历史远端地址和本机用户路径已替换；公开副本不包含私钥、比赛结果文件、调试数据库和临时日志。TLS 练习需要时自行生成本地证书密钥。
- [归档清单](ARCHIVE_MANIFEST.json) 给出源目录到目标文件及 SHA-256；[排除清单](EXCLUDED_FILES.md) 列明未发布的文件和原因。

仅用于公开 CTF、课程与授权实验。

## 静态检查

83 个条目，补入 20 份已有个人题解；本地链接与符号链接均可解析，所有附件均小于 GitHub 单文件限制。4 份历史脚本存在 Python 版本或不完整代码问题，详情见 [检查记录](ARCHIVE_CHECKS.json)。这些脚本作为原始研究材料保留。
