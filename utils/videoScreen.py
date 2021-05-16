import sys
from PyQt5 import QtWidgets
import screens.Ui_Outsecure as u_OS
import screens.login_window as login_window
import screens.Ui_NewUser as newUser_window
import screens.Newuser as new_user
import screens.VideoThreadFoeMainWindow as video_thread_for_main_window
import screens.main_window as main_window


Login_Window = login_window.Login
Ui_Outsecure = u_OS.Ui_Outsecure
newUser_window_gui = newUser_window.Ui_NewUser
newUser_window = new_user.Newuser
video_thread_for_main_window = video_thread_for_main_window.VideoThread
main_window_obj = main_window.Detection


class Controller:
    def __init__(self):
        pass

    def show_login_page(self):
        self.login = Login_Window()
        self.login.switch_window.connect(self.show_newuser_page)
        self.login.switch_window1.connect(self.show_detection)
        self.login.show()

    def show_detection(self):
        self.detection = main_window_obj()
        self.detection.show()

    def show_newuser_page(self):
        self.newuser = new_user.Newuser()
        self.newuser.switch_window.connect(self.show_login_page)
        self.login.close()
        self.newuser.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_login_page()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
