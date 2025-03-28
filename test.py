import time
import pyautogui
import pywinauto
from pywinauto.application import Application
import datetime

# =================================================================
# Tổng hợp đường dẫn hình ảnh cần kiểm tra
# =================================================================
IMAGE_PATHS = {
    'login_screen': r'C:\Users\Acer\Downloads\Python\tk\images\login_screen.png',
    'server_north': r'C:\Users\Acer\Downloads\Python\tk\images\server_north.png',
    'x_button': r'C:\Users\Acer\Downloads\Python\tk\images\x_button.png',
    'review_map': r'C:\Users\Acer\Downloads\Python\tk\images\review_map.png',
    'rpk_button': r'C:\Users\Acer\Downloads\Python\tk\images\rpk_button.png',
    'event_button': r'C:\Users\Acer\Downloads\Python\tk\images\event_button.png',
    'confirm_button': r'C:\Users\Acer\Downloads\Python\tk\images\confirm_button.png',
    'ok_button': r'C:\Users\Acer\Downloads\Python\tk\images\ok_button.png',
}

current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# =================================================================
# Định nghĩa lớp Game chứa các tọa độ thao tác
# =================================================================


class Game:
    def __init__(self):
        self.account_field = (600, 600)         # Tọa độ ô nhập tài khoản
        self.password_field = (600, 635)        # Tọa độ ô nhập mật khẩu
        # Tọa độ chọn server Bắc
        self.server_north = (850, 560)
        # Tọa độ chọn lại server
        self.re_select_server = (1743, 13)
        # Tọa độ nút X giới thiệu map mới
        self.x_review_btn = (1226, 85)
        # Tọa độ thanh sự kiện
        self.event_nav = (669, 164)
        # Tọa độ điểm danh rpk
        self.attendance_btn = (1130, 220)
        # Tọa độ nút X khung sự kiện
        self.x_event_btn = (1452, 87)
        # Tọa độ xác nhận đồ hết hạn
        self.confirm_btn = (955, 450)
        # Tọa độ nút OK
        self.ok_btn = (961, 420)
        # Tọa độ nút mở sự kiện rpk
        self.rpk_button = (1220, 90)
        self.close_button = (1901, 15)
        self.close_login_button = (1479, 197)


game = Game()
truyKich = pywinauto.Application()

# =================================================================
# Hàm ghi log
# =================================================================


def logToFile(message):
    with open(f"C:/Users/Acer/Downloads/Python/tk/check_attendance/checking_attendance_{current_date}_2.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")

# =================================================================
# Hàm kiểm tra sự xuất hiện của hình ảnh (dùng nếu cần thiết)
# =================================================================


def waitForImage(image_path, timeout=10, check_interval=0.5, confidence=0.8):
    start_time = time.time()
    while True:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if location is not None:
            return location
        if time.time() - start_time > timeout:
            return None
        time.sleep(check_interval)

# =================================================================
# Các hàm thao tác với game (không kiểm tra hình ảnh)
# =================================================================


def runGame():
    truyKich.start("D:\\TK\\TruyKich\\WDlauncher.exe")


def writeAccount(account_obj):
    # Nhập thông tin đăng nhập từ đối tượng account_obj
    pyautogui.moveTo(*game.account_field)
    time.sleep(0.5)
    pyautogui.click()
    pyautogui.typewrite(account_obj["acc"])
    pyautogui.moveTo(*game.password_field)
    time.sleep(0.5)
    pyautogui.click()
    pyautogui.typewrite(account_obj["pass"])
    pyautogui.press('enter')


def selectServerNorth():
    pyautogui.moveTo(*game.server_north)
    time.sleep(0.5)
    pyautogui.click()


def click(coordinates):
    pyautogui.moveTo(coordinates)
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(0.5)


def moveAndScroll(coords, total_scroll, target_image, step=50):
    x, y = coords
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown()
    scrolled = 0
    sign = 1 if total_scroll > 0 else -1
    while abs(scrolled) < abs(total_scroll):
        delta = min(step, abs(total_scroll) - abs(scrolled)) * sign
        scrolled += delta
        pyautogui.moveTo(x, y + scrolled, duration=0.2)
        if target_image and pyautogui.locateOnScreen(target_image, confidence=0.8):
            break
    pyautogui.mouseUp()


def closeTruyKich():
    pyautogui.moveTo(*game.close_button)
    time.sleep(0.5)
    pyautogui.click()


def closeLogin():
    pyautogui.moveTo(*game.close_login_button)
    time.sleep(0.5)
    pyautogui.click()


def reSelectServerNorth():
    pyautogui.moveTo(*game.re_select_server)
    time.sleep(0.5)
    pyautogui.click()
    pyautogui.moveTo(*game.server_north)
    time.sleep(0.5)
    pyautogui.click()

# =================================================================
# Hàm main thực hiện quy trình cho từng tài khoản
# =================================================================


def main(account_obj):
    try:
        runGame()

        # Kiểm tra hiện màn hình login và điền tài khoản mật khẩu
        if not waitForImage(IMAGE_PATHS['login_screen'], timeout=30):
            logToFile(
                f"Tài khoản {account_obj['acc']}: Không mở được màn hình login")
            closeLogin()
            return
        writeAccount(account_obj)

        # Kiểm tra hiện khung chọn server và chọn server Bắc
        if not waitForImage(IMAGE_PATHS['server_north'], timeout=10):
            logToFile(
                f"Tài khoản {account_obj['acc']}: Tài khoản, mật khẩu không chính xác")
            closeLogin()
            return
        selectServerNorth()

        # Kiểm tra vào sảnh, nếu sau 60s không hiện khung map thì chọn lại server và quét tiếp
        if not waitForImage(IMAGE_PATHS['x_button'], timeout=60):
            reSelectServerNorth()
            if not waitForImage(IMAGE_PATHS['x_button'], timeout=60):
                logToFile(
                    f"Tài khoản {account_obj['acc']}: Không vào được game")
                return

        loop_start_time = time.time()
        b1_done = False
        b2_done = False
        b3_done = False
        b4_done = False
        b5_done = False
        b6_done = False
        b7_done = False

        while not b7_done:
            if time.time() - loop_start_time > 60:
                logToFile(f"Tài khoản {account_obj['acc']}: Lỗi check sự kiện")
                closeTruyKich()
                return

            if not b1_done:
                if pyautogui.locateOnScreen(IMAGE_PATHS['review_map'], confidence=0.8):
                    click(game.x_review_btn)
                    b1_done = True

            if not b2_done:
                if pyautogui.locateOnScreen(IMAGE_PATHS['x_button'], confidence=0.8):
                    click(game.x_event_btn)
                    b2_done = True

            if not b3_done:
                if pyautogui.locateOnScreen(IMAGE_PATHS['confirm_button'], confidence=0.8):
                    click(game.confirm_btn)
                    b3_done = True

            if not b4_done:
                if pyautogui.locateOnScreen(IMAGE_PATHS['ok_button'], confidence=0.8):
                    click(game.ok_btn)
                    b4_done = True

            if not b5_done:
                if pyautogui.locateOnScreen(IMAGE_PATHS['event_button'], confidence=0.8):
                    moveAndScroll(game.event_nav, 500,
                                  IMAGE_PATHS['rpk_button'])
                    b5_done = True

            if not b6_done:
                location = pyautogui.locateOnScreen(
                    IMAGE_PATHS['rpk_button'], confidence=0.8)
                if location:
                    click((location.left + location.width // 2,
                          location.top + location.height // 2))
                    b6_done = True

            if b6_done and not b7_done:
                time.sleep(1)
                click(game.attendance_btn)
                click(game.attendance_btn)
                b7_done = True

            time.sleep(0.5)

        time.sleep(2)
        closeTruyKich()
        logToFile(
            f"Tài khoản {account_obj['acc']} đã điểm danh ngày {current_date}")

    except Exception as e:
        logToFile(
            f"Lỗi trong quá trình thực thi tài khoản {account_obj['acc']}: {e}")
        closeTruyKich()


# =================================================================
# Danh sách các tài khoản cần đăng nhập
# Mỗi phần tử là một đối tượng có 2 key: acc và pass
# =================================================================

# Chứa các acc bị lỗi chạy lúc 12h

result = [
   
    {"acc": "regs49", "pass": "takitorj"},
    {"acc": "regs51", "pass": "takitorj"},
    {"acc": "regs53", "pass": "takitorj"},
    {"acc": "regs54", "pass": "takitorj"},
    {"acc": "regs55", "pass": "takitorj"},
    {"acc": "regs56", "pass": "takitorj"},
    {"acc": "regs57", "pass": "takitorj"},
    {"acc": "regs58", "pass": "takitorj"},
    {"acc": "regs59", "pass": "takitorj"},
    {"acc": "regs60", "pass": "takitorj"},
    {"acc": "regs61", "pass": "takitorj"},
    {"acc": "regs63", "pass": "takitorj"},
    {"acc": "regs64", "pass": "takitorj"},
    {"acc": "regs65", "pass": "takitorj"},
    {"acc": "regs67", "pass": "takitorj"},
    {"acc": "regs68", "pass": "takitorj"},
    {"acc": "regs70", "pass": "takitorj"},
    {"acc": "regs71", "pass": "takitorj"},
    {"acc": "regs72", "pass": "takitorj"},
    {"acc": "regs73", "pass": "takitorj"},
    {"acc": "regs74", "pass": "takitorj"},
    {"acc": "regs75", "pass": "takitorj"},
    {"acc": "regs76", "pass": "takitorj"},
    {"acc": "regs78", "pass": "takitorj"},
    {"acc": "regs79", "pass": "takitorj"},
    {"acc": "regs80", "pass": "takitorj"},
    {"acc": "regs81", "pass": "takitorj"},
    {"acc": "regs82", "pass": "takitorj"},
    {"acc": "regs83", "pass": "takitorj"},
    {"acc": "regs84", "pass": "takitorj"},
    {"acc": "regs85", "pass": "takitorj"},
    {"acc": "regs86", "pass": "takitorj"},
    {"acc": "regs87", "pass": "takitorj"},
    {"acc": "regs88", "pass": "takitorj"},
    {"acc": "regs89", "pass": "takitorj"},
    {"acc": "regs90", "pass": "takitorj"},
    {"acc": "regs91", "pass": "takitorj"},
    {"acc": "regs92", "pass": "takitorj"},
    {"acc": "regs93", "pass": "takitorj"},
    {"acc": "regs94", "pass": "takitorj"},
    {"acc": "regs95", "pass": "takitorj"},
    {"acc": "regs96", "pass": "takitorj"},
    {"acc": "regs97", "pass": "takitorj"},
    {"acc": "regs99", "pass": "takitorj"},
    {"acc": "regs102", "pass": "takitorj"},
    {"acc": "regs103", "pass": "takitorj"},
    {"acc": "regs104", "pass": "takitorj"},
    {"acc": "regs105", "pass": "takitorj"},
    {"acc": "regs106", "pass": "takitorj"},
    {"acc": "regs107", "pass": "takitorj"},
    {"acc": "regs108", "pass": "takitorj"},
    {"acc": "regs109", "pass": "takitorj"},
    {"acc": "regs110", "pass": "takitorj"},
    {"acc": "regs111", "pass": "takitorj"},
    {"acc": "regs112", "pass": "takitorj"},
    {"acc": "regs113", "pass": "takitorj"},
    {"acc": "regs114", "pass": "takitorj"},
    {"acc": "regs115", "pass": "takitorj"},
    {"acc": "regs116", "pass": "takitorj"},
    {"acc": "regs117", "pass": "takitorj"},
    {"acc": "regs118", "pass": "takitorj"},
    {"acc": "regsrole2037", "pass": "takitorj"},
    {"acc": "regsrole2064", "pass": "takitorj"},
    {"acc": "regsrole20166", "pass": "takitorj"},
    {"acc": "regsreg03", "pass": "takitorj"}
]

# =================================================================
# Vòng lặp chạy qua danh sách tài khoản
# =================================================================
if __name__ == '__main__':
    for account in result:
        time.sleep(3)
        main(account)
