from ctypes import *
from ctypes.util import find_library


output_max_id = 0
output_callbacks = {}
# int (*output)(const char *buf, int len, ikcpcb *kcp, void *user)
@CFUNCTYPE(c_int, POINTER(c_char), c_int, c_void_p, c_void_p)
def output_callback(data_ptr, data_len, kcp_id, user):
    if user is None:
        return
    cb = output_callbacks.get(user)
    if not cb:
        return
    cb(data_ptr[:data_len], data_len)
    return 0


ikcp_lib = None
def load_clib(filename):
    global ikcp_lib
    lib = cdll.LoadLibrary(filename)

    lib.ikcp_create.argtypes = [c_int32, c_void_p]
    lib.ikcp_create.restype = c_void_p

    lib.ikcp_release.argtypes = [c_void_p]
    lib.ikcp_release.restype = None

    lib.ikcp_setoutput.argtypes = [c_void_p, c_void_p]
    lib.ikcp_setoutput.restype = None

    lib.ikcp_recv.argtypes = [c_void_p, POINTER(c_char), c_int]
    lib.ikcp_recv.restype = c_int

    lib.ikcp_send.argtypes = [c_void_p, POINTER(c_char), c_int]
    lib.ikcp_send.restype = c_int

    lib.ikcp_update.argtypes = [c_void_p, c_int32]
    lib.ikcp_update.restype = None

    lib.ikcp_check.argtypes = [c_void_p, c_int32]
    lib.ikcp_check.restype = None

    lib.ikcp_input.argtypes = [c_void_p, POINTER(c_char), c_long]
    lib.ikcp_input.restype = c_int

    lib.ikcp_flush.argtypes = [c_void_p]
    lib.ikcp_flush.restype = None

    lib.ikcp_peeksize.argtypes = [c_void_p]
    lib.ikcp_peeksize.restype = c_int

    lib.ikcp_setmtu.argtypes = [c_void_p, c_int]
    lib.ikcp_setmtu.restype = c_int

    lib.ikcp_wndsize.argtypes = [c_void_p, c_int, c_int]
    lib.ikcp_wndsize.restype = c_int

    lib.ikcp_waitsnd.argtypes = [c_void_p]
    lib.ikcp_waitsnd.restype = c_int

    lib.ikcp_nodelay.argtypes = [c_void_p, c_int, c_int, c_int, c_int]
    lib.ikcp_nodelay.restype = c_int

    ikcp_lib = lib


class Ikcp:
    def __init__(self, conv, output) -> None:
        self.conv = conv
        global output_max_id
        if not ikcp_lib:
            raise Exception(u"ikcp_lib is None 请限加载动态库。 执行load_clib。 详情：https://gitee.com/l00n00l/kcp ")
        output_max_id = output_max_id + 1
        self._kcp_id = output_max_id
        self._kcp = ikcp_lib.ikcp_create(conv, output_max_id)
        ikcp_lib.ikcp_setoutput(self._kcp, output_callback)
        output_callbacks[output_max_id] = output

        self.recv_buf = None
        self.recv_buf_size = 0
        self.current = 0

    def __del__(self):
        if self._kcp is not None:
             ikcp_lib.ikcp_release(self._kcp)
        if self._kcp_id is not None and output_callbacks.get(self._kcp_id) is not None:
            del output_callbacks[self._kcp_id]
    
    def recv(self, size = 64 * 1024):
        if size != self.recv_buf_size:
            self.recv_buf = bytes(size)
            self.recv_buf_size = size
        data_len = ikcp_lib.ikcp_recv(self._kcp, self.recv_buf, size)
        if data_len > 0:
            return self.recv_buf, data_len
        return None, data_len
    
    def send(self, data : bytes)->int:
        return ikcp_lib.ikcp_send(self._kcp, data, len(data)) == 0

    def update(self, elapse):
        self.current = (self.current + elapse) % 0x7FFFFFFF
        ikcp_lib.ikcp_update(self._kcp, self.current)

    def check(self, current:int):
        return ikcp_lib.ikcp_check(self._kcp, current)

    def input(self, data:bytes)->bool:
        return ikcp_lib.ikcp_input(self._kcp, data, len(data)) == 0

    def flush(self):
        ikcp_lib.ikcp_flush(self._kcp)
    
    def peeksize(self):
        u'''
        获取接收队列中下一个消息的大小
        '''
        return ikcp_lib.ikcp_peeksize(self._kcp)

    def setmtu(self, mtu:int):
        u'''
        设置最大传输单元, 大小超过mtu的数据要分片传输
        '''
        return ikcp_lib.ikcp_setmtu(self._kcp, mtu)

    def windowsize(self, send_window_size:int, receive_window_size:int):
        u'''
        设置窗口大小
        * send_window_size 发送窗口大小
        * receive_window_size 接收窗口大小
        '''
        return ikcp_lib.ikcp_wndsize(self._kcp, send_window_size, receive_window_size)

    def nodelay(self, nodelay:int, interval:int, resend:int, nc:int):
        u'''
        ### 最快: nodelay(1, 20, 2, 1)
        * nodelay: 0表示关闭nodelay(默认值), 1:开启
        * interval: 内部更新时间间隔（单位：毫秒）(默认100ms)
        * resend: 开启或关闭快速重传 0:关闭（默认） 1: 开启
        * nc: 是否开启拥塞控制 0:关闭(默认) 1:开启
        '''
        return ikcp_lib.ikcp_nodelay(self._kcp, nodelay, interval, resend, nc)


def test():
    import time
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


if __name__ == "__main__":
    test()


