# 知识点

内核

# 题目分析

分类：pwn / 内核。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [Makefile](Makefile)
- [bzImage](bzImage)
- [exploit.c](exploit.c)
- [exploit.py](exploit.py)
- [kernel_config](kernel_config)
- [rootfs.qcow2](rootfs.qcow2)
- [run.sh](run.sh)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

# EXP

- [exploit.c](exploit.c)
- [exploit.py](exploit.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。


本地 QEMU 测试用的 `flag` 是新建占位内容，原比赛结果文件未发布。`run.sh` 需要 QEMU/KVM 环境。
