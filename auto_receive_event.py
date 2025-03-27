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
    'phuc_loi_dang_nhap': r'C:\Users\Acer\Downloads\Python\tk\images\phuc_loi_dangnhap.png',
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
    with open(f"C:/Users/Acer/Downloads/Python/tk/check_attendance/checking_attendance_{current_date}.txt", "a", encoding="utf-8") as f:
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


def writeAccount(id):
    # account = 'regs' + str(id)
    pyautogui.moveTo(*game.account_field)
    time.sleep(0.5)
    pyautogui.click()
    pyautogui.typewrite(account)
    pyautogui.moveTo(*game.password_field)
    time.sleep(0.5)
    pyautogui.click()
    pyautogui.typewrite(password)
    pyautogui.press('enter')


def writeAccount2(account_obj):
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
# Hàm main thực hiện quy trình cho từng ID
# =================================================================


def main(id):
    try:
        runGame()

        # Kiểm tra hiện màn hình login và điền tài khoản mật khẩu
        if not waitForImage(IMAGE_PATHS['login_screen'], timeout=30):
            logToFile(f"ID {id}: Không mở được màn hình login")
            closeLogin()
            return  # Thoát hàm main để chuyển sang ID tiếp theo
        writeAccount(id)

        # Kiểm tra hiện khung chọn server và chọn server Bắc
        if not waitForImage(IMAGE_PATHS['server_north'], timeout=10):
            logToFile(f"ID {id}: Tài khoản, mật khẩu không chính xác")
            closeLogin()
            return
        selectServerNorth()

        # Kiểm tra vào sảnh, nếu sau 60s không hiện khung map cổ thì chọn lại server và quét tiếp
        if not waitForImage(IMAGE_PATHS['x_button'], timeout=60):
            reSelectServerNorth()
            if not waitForImage(IMAGE_PATHS['x_button'], timeout=60):
                logToFile(f"ID {id}: Không vào được game")
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
            # Kiểm tra thời gian đã trôi qua trong vòng lặp phụ
            if time.time() - loop_start_time > 60:
                logToFile(f"ID {id}: Lỗi check sự kiện")
                closeTruyKich()
                return

            # B1: Kiểm tra cửa sổ giới thiệu map (review_map) và click nút "X"
            if not b1_done:
                if pyautogui.locateOnScreen(IMAGE_PATHS['review_map'], confidence=0.8):
                    click(game.x_review_btn)
                    b1_done = True

            # B2: Kiểm tra nút X và thực hiện click nút X
            if not b2_done:
                if pyautogui.locateOnScreen(IMAGE_PATHS['x_button'], confidence=0.8):
                    click(game.x_event_btn)
                    b2_done = True

            # B3: Kiểm tra và click nút Xác nhận
            if not b3_done:
                if pyautogui.locateOnScreen(IMAGE_PATHS['confirm_button'], confidence=0.8):
                    click(game.confirm_btn)
                    b3_done = True

            # B4: Kiểm tra và click nút OK
            if not b4_done:
                if pyautogui.locateOnScreen(IMAGE_PATHS['ok_button'], confidence=0.8):
                    click(game.ok_btn)
                    b4_done = True

            # B5: Kiểm tra nút đóng khung sự kiện và cuộn trang
            if not b5_done:
                if pyautogui.locateOnScreen(IMAGE_PATHS['event_button'], confidence=0.8):
                    moveAndScroll(game.event_nav, 500,
                                  IMAGE_PATHS['rpk_button'])
                    b5_done = True

            # B6: Kiểm tra nút sự kiện rpk và click vào trung tâm nút
            if not b6_done:
                location = pyautogui.locateOnScreen(
                    IMAGE_PATHS['rpk_button'], confidence=0.8)
                if location:
                    click((location.left + location.width // 2,
                           location.top + location.height // 2))
                    b6_done = True

            time.sleep(3)
            # B7: Ấn nút tới tiệm đổi
            if (1 == 1):
                pyautogui.doubleClick(1314, 577)
            time.sleep(1)

            # B8: Đổi rpk
            time.sleep(1)
            # B7: Ấn nút tới tiệm đổi
            if (1 == 1):
                pyautogui.doubleClick(692, 254)
            time.sleep(1)

            # B10: nút X
            if (1 == 1):
                pyautogui.click(1405, 64)

            time.sleep(3)
            # B10: nút sự kiện
            if (1 == 1):
                pyautogui.click(1064, 52)

            time.sleep(1)
            # B11: Bấm cuộn tìm nút phúc lợi đăng nhâp
            if (1 == 1):
                moveAndScroll(game.event_nav, 500,
                              IMAGE_PATHS['phuc_loi_dang_nhap'])

            time.sleep(1)
            if (1 == 1):
                location = pyautogui.locateOnScreen(
                    IMAGE_PATHS['phuc_loi_dang_nhap'], confidence=0.8)
                if location:
                    click((location.left + location.width // 2,
                           location.top + location.height // 2))

            time.sleep(1)
            # Bấm để nhận
            if (1 == 1):
                coordinates = [(825, 582), (1049, 573), (1311, 586)]
                for coord in coordinates:
                    pyautogui.click(coord[0], coord[1])
                    pyautogui.click(coord[0], coord[1])
                    time.sleep(1)  # delay 1 giây giữa các tọa độ
                    b7_done = True

            time.sleep(0.5)  # Giảm tải CPU trong vòng lặp

        # Đóng game
        time.sleep(2)
        closeTruyKich()

        # Ghi log
        logToFile(f"ID {id} đã điểm danh ngày {current_date}")

    except Exception as e:
        logToFile(f"Lỗi trong quá trình thực thi ID {id}: {e}")
        closeTruyKich()


def main2(account_obj):
    try:
        runGame()

        # Kiểm tra hiện màn hình login và điền tài khoản mật khẩu
        if not waitForImage(IMAGE_PATHS['login_screen'], timeout=30):
            logToFile(
                f"Tài khoản {account_obj['acc']}: Không mở được màn hình login")
            closeLogin()
            return
        writeAccount2(account_obj)

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


ACCOUNTS = [
   
]

# =================================================================
if __name__ == '__main__':
    # Mấy con reg bán rồi
    SKIP_IDS = [11, 16, 20, 24, 25, 26, 28, 29,
                31, 34, 35, 42, 47, 50, 52, 134,  135]
    # Mấy con reg sai mk
    SKIP_IDS2 = [62, 66, 69, 77, 100, 101]
    id = 4
    max_id = 55
    while id <= max_id:
        if id in SKIP_IDS or id in SKIP_IDS2:
            # logToFile(f"ID {id} bị bỏ qua điểm danh")
            id += 1
            continue
        time.sleep(3)
        main(id)
        id += 1
