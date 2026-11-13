# WDB 2018 第一阶段 · babyheap（堆 / double free · UAF）

## 来源

| 项 | 值 |
| --- | --- |
| 出处 | 2018 WDB 第一阶段（`2018WDB/第一场/pwn/babyheap.zip`） |
| 参考仓库 | <https://github.com/hacker-mao/ctf_repo/tree/master/2018WDB/第一场/pwn> |
| 二进制 | `babyheap`，stripped，非 PIE，Build ID `b8e451c57f9dd60b40dad65b3d83bf9a5ad94a14` |
| sha256 | `766e95cfdea5886882c74344231d68a5d604a8329e9831277c95f4252150d336` |
| 编译环境 | `GCC: (Ubuntu 8.1.0-5ubuntu1~16.04)`，interpreter `/lib64/ld-linux-x86-64.so.2` |
| 附件 libc | Ubuntu GLIBC **2.23-0ubuntu10**，Build ID `b5381a457906d279073822a5ceb24c4bfef94ddb`，sha256 `05b841eae6f475817ebb3b99562cd6535cc61b099350a25019cd5d3b3136881d` |
| loader | `env/ld-2.23.so`，取自 Ubuntu 16.04 `libc6_2.23-0ubuntu10_amd64.deb`，Build ID `5d7b6259552275a3c17bd4c3fd05f5a6bf40caa5` |

zip 里只有 `babyheap` 和 `libc.so.6`，**没有 loader**。这份 libc 与 Ubuntu 16.04 官方 `libc6` 包里的 `/lib/x86_64-linux-gnu/libc-2.23.so` 字节相同，所以 loader 从同一个 deb 里取，版本严格配套。题目目录的 `env/` 是自洽副本，版本目录顶层的运行库是给其它 16.04 amd64 题用的共享副本，两者内容一致。

## 保护

| 保护 | 结论 | 依据 |
| --- | --- | --- |
| PIE | 关 | ELF `e_type = ET_EXEC`，代码固定在 `0x400000` |
| Canary | 开 | 各菜单函数序言读写 `%fs:0x28`，失败走 `__stack_chk_fail` |
| NX | 开 | `GNU_STACK` 为 `rw-` |
| RELRO | Full | 有 `GNU_RELRO`，`DT_BIND_NOW` 置位 |
| 溢出 | 无 | 读入函数 `0x40092b` 最多写 `size-1` 字节并补 `\0`，`0x20` 缓冲区刚好不越界 |

## 菜单逻辑（静态）

```text
ptr[32]      @ 0x602060     // 只存指针，free 后不清零
edit_count   @ 0x6020b0     // 全局编辑次数
```

| 功能 | 入口 | 索引上限 | 行为 |
| --- | --- | --- | --- |
| 1 alloc | `0x4009a0` | ≤ 31 | 空槽 `malloc(0x20)`，读入最多 31 字节 + 结尾 `\0` |
| 2 edit | `0x400a79` | ≤ 31 | 槽非空且 `edit_count < 3` 时重写 0x20 字节，之后计数 +1 |
| 3 show | `0x400c01` | ≤ 9 | 直接 `puts(ptr)` 打印 chunk 内容 |
| 4 free | `0x400b54` | ≤ 9 | `free(ptr)`，**不把 ptr 置空** |
| 5 exit | — | — | `exit(0)` |

三个可利用点叠在一起：

1. **free 不置空** → 同一 chunk 可以重复释放，也可以继续被 show/edit 当活指针用（UAF）。
2. **show 是 `puts(ptr)`** → 释放后 chunk 里残留的 `fd`（main_arena 指针）会被当作字符串打印出来，直接泄 libc。
3. **edit 全程只有 3 次** → 分配/写数据的预算很紧，通常用 double free 把 malloc 目标挪到 `__malloc_hook`，3 次编辑够写 hook + 一个 gadget。

glibc 2.23 没有 tcache，fastbin 的 double free 只检查"当前释放的是不是 fastbin 头"，`free(A); free(B); free(A);` 即可绕过，形成 fastbin dup。

`0x20` 用户区对应 0x30 的 chunk：

```text
chunk 头 (0x10)        用户区 0x20
[prev_size][size]  [data 0x20]      ← malloc(0x20)，实际 chunk size 0x30
```

释放后前 16 字节被复用为 `fd` / `bk`；0x30 的 fastbin 只用到 `fd`。

## 本 libc 关键偏移

以下是在 `env/libc.so.6` 里实际查到的符号偏移（不是猜的，换补丁版必须重查）：

| 符号 | 偏移 |
| --- | --- |
| `__malloc_hook` | `0x3c4b10` |
| `__realloc_hook` | `0x3c4b08` |
| `__free_hook` | `0x3c67a8` |
| `system` | `0x45390` |
| `puts` | `0x6f690` |
| `_IO_2_1_stdout_` | `0x3c5620` |

## 启动（Linux VM）

```bash
PWN_ROOT="$(pwd)"     # 在 VM 里进入题型库根目录
"$PWN_ROOT/libc/2.23/amd64/ld-linux-x86-64.so.2" \
  --library-path "$PWN_ROOT/libc/2.23/amd64/wdb_2018_1st_babyheap/env" \
  "$PWN_ROOT/libc/2.23/amd64/wdb_2018_1st_babyheap/babyheap"
```

或者让脚本识别题目自带的 `env/`：

```bash
bash tools/pwn-env.sh run 2.23 amd64 libc/2.23/amd64/wdb_2018_1st_babyheap/babyheap
bash tools/pwn-env.sh gdb 2.23 amd64 libc/2.23/amd64/wdb_2018_1st_babyheap/babyheap
```

启动后会打印 `I thought this is really baby.What about u?` 和 `Loading.....`，再 `sleep(5)` 才出菜单。GDB 里用 `info sharedlibrary` 确认加载的是 `env/libc.so.6`。

## 状态

- 已验证（静态）：架构、Build ID、保护属性、菜单函数与读入函数反汇编、libc 版本与符号偏移、附件 libc 与 Ubuntu 16.04 官方包字节一致。
- 未验证：VM 内启动、GDB 调试、EXP 打通。本机是 macOS，不能执行 Linux ELF。
- 远程环境版本没有官方说明，但附件自带的就是 2.23-0ubuntu10，按"附件匹配"记。
