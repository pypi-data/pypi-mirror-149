# 编译(linux)
在 Linux 上， find_library() 会尝试运行外部程序(/sbin/ldconfig, gcc, objdump 以及 ld) 来寻找库文件。返回库文件的文件名。
```
git clone https://gitee.com/l00n00l/kcp.git
cd kcp
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make
mv libkcp.so /usr/local/lib/
sudo ldconfig
```

# 编译(windows)
在 Windows 上， find_library() 在系统路径中搜索，然后返回全路径，但是如果没有预定义的命名方案， find_library("c") 调用会返回 None
```
git clone https://gitee.com/l00n00l/kcp.git
cd kcp
mkdir build
cd build
cmake ..
C:\"Program Files"\"Microsoft Visual Studio"\2022\Community\Common7\IDE\devenv.exe kcp.sln /build Release

将Release 下的 kcp.dll 放到 C:\Windows\System32\kcp.dll
```


# 使用方法

```python
import time
from ctypes.util import find_library
from l0n0lkcp.ikcp import Ikcp
ret = find_library("kcp")
# load_clib("build/Release/kcp.dll")
load_clib(ret)
a = None
b = None

def test_out_puta(data, size):
    b.input(data)

def test_out_putb(data, size):
    a.input(data)

a = Ikcp(123, test_out_puta)
b = Ikcp(123, test_out_putb)

a.nodelay(1, 20, 1, 1)
b.nodelay(1, 20, 1, 1)

while True:
    a.update(10)
    b.update(10)
    a.send(b"123123")
    data, size = b.recv()
    if size > 0:
        print(data[:size], a.current)
    time.sleep(0.01)
```

