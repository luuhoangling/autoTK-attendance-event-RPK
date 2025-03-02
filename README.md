# 3/2/2025
## Auto Login & Điểm Danh Tự Động Cho Game Truy Kích

## Tổng Quan
Repository này chứa script tự động đăng nhập và điểm danh (roll call) cho game RPK Legend – Truy Kích. Script sử dụng thư viện pyautogui và pywinauto

## Tính Năng
- **Tự động đăng nhập:** Nhập tài khoản và mật khẩu theo định dạng (ví dụ: `regs{id}`) trong hàm `writeAccount()`.
- **Chọn server:** Tự động chọn server Bắc và xử lý chọn lại nếu cần.
- **Tự động thao tác giao diện:** Nhận diện hình ảnh và thực hiện thao tác click, cuộn trang thông qua `pyautogui`.
- **Điểm danh tự động:** Sau khi xử lý các cửa sổ pop-up, script sẽ tự động thực hiện điểm danh.
- **Ghi log:** Lưu lại quá trình thực thi và ghi nhận lỗi (nếu có) vào file log với tên chứa ngày hiện tại.

## Yêu Cầu
- Python 3.x
- Các thư viện cần cài đặt:
  - [pyautogui](https://pyautogui.readthedocs.io/)
  - [pywinauto](https://pywinauto.github.io/)
