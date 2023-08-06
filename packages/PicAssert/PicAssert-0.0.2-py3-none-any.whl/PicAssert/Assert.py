"""
PicAssert图片断言工具：
anchor： 测码范晔
联系邮箱： 1538379200@qq.com
当前版本：v 0.0.2
通过图片拓展断言方式
PicAsssert会将图片在全局做一次模板匹配行为，当查找的图片大于或者等于设置的阈值的时候，程序将返回True，
当全局匹配的图片匹配度低于所设置的阈值时，程序将启动特征匹配模式，对前面相似度较近的区域进行截图，再次进行特征分析，
如果特征分析的结果判断为图片相似，程序将返回True，否则返回False
程序依赖 opencv、pillow 进行图片的处理

**使用说明**：
1、Assert类中最好设置一下 InitDPI ，以元祖或者列表的形式，写上当前编写代码设备的分辨率，提升兼容性
2、PicAssert的Assert类，如果添加了driver，则识别为selenium操作，将使用selenium进行截图，代码可以无头模式运行，但为了提升稳定性，
  请将窗口设置为当前编写代码的设备的分辨率大小，设置selenium浏览器窗口大小代码为：
  dr.set_window_size(1920, 1080)
  Assert类如果没有添加任何参数，则默认截取设备的全屏，可以在其他gui代码中运行，注意不能关闭当前显示的屏幕
3、使用图片断言会返回一个布尔值，True为找到当前图片，False为未找到图片

**使用**
实例化Assert类：
ps = Assert()  # ps = Assert(driver=driver)
ps.assert_exist("./test.png", 0.7)
assert_exist有两个形参
第一个参数：pic_path  需要判断的图片保存路径
第二个参数：threshold  断言阈值，当前默认 0.7，可调制0到1的区间，1为100%，请尽量控制在0.6到0.9之间

**使用流程**
1、正常编写代码，将需要断言的地方，使用工具进行截图，截图尽量不会包含其他可变的干扰，将其保存在一个路径中
2、导入PicAssert包，实例化Assert类，使用assert_exist，传入前面截图路径
3、获取返回值
4、运行完成，将在项目目录下，新建一个.assert_cache文件夹，下面有success和fail文件夹，成功断言放在success中，失败在fail中，程序每次运行会清空缓存文件

**selenium代码使用示例**
from SafeDriver.drivers import driver, option
import time
from PicAssert.Assert import Assert
dr = driver()
ps = Assert(dr)
dr.get("https://www.baidu.com")
time.sleep(2)
p1_res = ps.assert_exist(r"D:\test.png")     # ps.assert_exist(r"D:\test.png", 0.8)
if p1_res is True:
    print("图片存在")
else
    print("图片不存在")
"""
import cv2
from PIL import ImageGrab, Image
import time
from pathlib import Path
import os
import shutil
from typing import Union


class Assert:
    __pic_width = 0
    __pic_height = 0

    InitDPI = (1920, 1080)

    def __init__(self, driver=None):
        self.__driver = driver
        cache_path = Path.cwd().resolve()/'.assert-cache'
        success_path = cache_path/'success'
        fail_path = cache_path/'fail'
        shutil.rmtree(cache_path, ignore_errors=True)
        cache_path.mkdir(exist_ok=True)
        success_path.mkdir(exist_ok=True)
        fail_path.mkdir(exist_ok=True)
        self.__cache_path = os.fspath(cache_path)
        self.__seccess_path = os.fspath(success_path)
        self.__fail_path = os.fspath(fail_path)

    def __get_shot(self) -> str:
        """
        获取当前页面的截图，如果设置了driver，将使用selenium的截图方法
        :return: 图片路径名称
        """
        now_time = time.strftime("%Y%m%d%H%M%S")
        filename = "PICASSERT-" + now_time + ".png"
        filename = self.__cache_path + '/' + filename
        if not self.__driver:
            all_screen = ImageGrab.grab()
            all_screen.save(filename)
        else:
            self.__driver.get_screenshot_as_file(filename)
        image = Image.open(filename)
        x, y = image.size
        if self.__pic_width != x and self.__pic_height != y:
            self.__pic_width = x
            self.__pic_height = y
            if self.InitDPI[0] != self.__pic_width:
                self.__scale = self.InitDPI[0]/self.__pic_width
            else:
                self.__scale = 1
        return filename

    def assert_exist(self, pic_path: str, threshold: Union[int, float] = 0.7) -> Union[bool, None]:
        """
        进行图片匹配，判断是否存在此图片
        程序将先进行模板匹配，找到截图对应的区域，如果匹配值小于设定的阈值，程序会将最接近的区域进行截图，重新进行特征点匹配，也小于0.1才返回False
        匹配成功图片保存在.assert-cache/success中
        失败保存在.assert-cache/fail中
        :param pic_path: 当前需要进行匹配的图片
        :param threshold: 阈值，0~1区间
        :return: bool
        """
        pic_cache_path = self.__get_shot()
        try:
            picname_color = cv2.imread(pic_cache_path)
            picname = cv2.cvtColor(picname_color, cv2.COLOR_RGB2GRAY)
            tmp = cv2.imread(pic_path, 0)
            w, h = tmp.shape[::-1]
            w = int(w / self.__scale)
            h = int(h / self.__scale)
            tmp = cv2.resize(tmp, (w, h))
            res = cv2.matchTemplate(picname, tmp, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            cv2.rectangle(picname_color, (max_loc), (max_loc[0]+w, max_loc[1]+h), (0, 0, 255), 3)
            checkpic = pic_path.replace("\\", '/').split('/')[-1]
            if max_val > threshold:
                cv2.imwrite(self.__seccess_path + "/" + "OK-" + checkpic, picname_color)
                return True
            else:
                try:
                    picname_cut = picname[max_loc[1]:max_loc[1] + h, max_loc[0]:max_loc[0] + w]
                    orb = cv2.ORB_create()
                    kp1, des1 = orb.detectAndCompute(tmp, None)
                    kp2, des2 = orb.detectAndCompute(picname_cut, None)
                    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
                    matchs = bf.knnMatch(des1, trainDescriptors=des2, k=2)
                    good_match = [x for x, y in matchs if x.distance < 0.75 * y.distance]
                    sim = len(good_match) / len(matchs)
                    if sim >= 0.1:
                        cv2.imwrite(self.__seccess_path + "/" + "OK-" + checkpic, picname_color)
                        return True
                    else:
                        cv2.imwrite(self.__fail_path + "/" + "Fail-" + checkpic, picname_color)
                        return False
                except:
                    cv2.imwrite(self.__fail_path + "/" + "Fail-" + checkpic, picname_color)
                    return False
        except Exception as e:
            print("程序运行出错：", e)
        finally:
            Path(pic_cache_path).unlink(missing_ok=True)