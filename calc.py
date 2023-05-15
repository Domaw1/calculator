from PyQt5 import QtWidgets, QtGui
import numexpr
import qt_material
import math


class MyWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.resize(450, 200)
        self.setWindowTitle("Calculator")
        self.is_changed = False
        self.is_point = False
        self.gridlayout = QtWidgets.QGridLayout()
        self.gridlayout1 = QtWidgets.QGridLayout()
        self.buttons = [
            "C", "<--", "2nd calc", "/",
            "7", "8", "9", "*",
            "4", "5", "6", "-",
            "1", "2", "3", "+",
            "+/-", "0", ".", "="
        ]
        self.current_num = ""
        self.column = 0
        self.row = 3
        self.second_window = SecondWindow()
        self.label = QtWidgets.QLabel()
        self.label.setFont(QtGui.QFont("Times", 17))
        self.label1 = QtWidgets.QLabel()
        self.label1.setFont(QtGui.QFont("Times", 10))
        self.gridlayout1.addWidget(self.label1, 0, 0)
        self.gridlayout1.addWidget(self.label, 1, 0)
        self.new_buttons = []
        self.positions = [(i, j) for i in range(5) for j in range(4)]
        for position, name in zip(self.positions, self.buttons):
            self.button = QtWidgets.QPushButton(name)
            self.new_buttons.append(self.button)
            self.gridlayout.addWidget(self.button, *position)
        self.new_buttons[0].clicked.connect(self.clear)
        self.new_buttons[1].clicked.connect(self.del_num)
        self.new_buttons[2].clicked.connect(self.second)
        self.new_buttons[3].clicked.connect(lambda: self.add_operator("/"))
        self.new_buttons[4].clicked.connect(self.seven)
        self.new_buttons[5].clicked.connect(self.eight)
        self.new_buttons[6].clicked.connect(self.nine)
        self.new_buttons[7].clicked.connect(lambda: self.add_operator("*"))
        self.new_buttons[8].clicked.connect(self.four)
        self.new_buttons[9].clicked.connect(self.five)
        self.new_buttons[10].clicked.connect(self.six)
        self.new_buttons[11].clicked.connect(lambda: self.add_operator("-"))
        self.new_buttons[12].clicked.connect(self.one)
        self.new_buttons[13].clicked.connect(self.two)
        self.new_buttons[14].clicked.connect(self.three)
        self.new_buttons[15].clicked.connect(lambda: self.add_operator("+"))
        self.new_buttons[16].clicked.connect(self.change_sign)
        self.new_buttons[17].clicked.connect(self.zero)
        self.new_buttons[18].clicked.connect(self.point)
        self.new_buttons[19].clicked.connect(self.equal)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.gridlayout1)
        self.mainLayout.addLayout(self.gridlayout)
        self.setLayout(self.mainLayout)

    def second(self):
        self.second_window.show()
        self.close()

    def equal(self):
        if len(self.label.text()) == 0 or len(self.label1.text()) == 0:
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "Строка пуста")
            return
        try:
            if str.isdigit(self.label1.text()[-1]):
                return
            self.label1.setText(f"{self.label1.text() + self.label.text()}")
            self.label.setText(str(numexpr.evaluate(self.label1.text())))
        except SyntaxError as ex:
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", str(ex))
        except ZeroDivisionError:
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "Деление на ноль")


    def plus(self):
        if self.label.text() == "." or len(self.label.text()) == 0:
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "Строка пуста!")
        else:
            self.label1.setText(self.label.text() + "+")
            self.label.setText("")
            self.is_point = False

    def minus(self):
        if self.label.text() == ".":
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "В строке только точка!")
        else:
            self.label1.setText(self.label.text() + "-")
            self.label.setText("")
            self.is_point = False

    def divide(self):
        if self.label.text() == "." or len(self.label.text()) == 0:
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "Строка пуста!")
        else:
            self.label1.setText(self.label.text() + "/")
            self.label.setText("")
            self.is_point = False

    def multiply(self):
        if self.label.text() == "." or len(self.label.text()) == 0:
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "Строка пуста!")
        else:
            self.label1.setText(self.label.text() + "*")
            self.label.setText("")
            self.is_point = False

    def change_sign(self):
        if len(self.label.text()) == 0:
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "Строка пуста!")
            return
        if self.label.text() == "0":
            self.label.setText(self.label.text())
        else:
            if not self.is_changed and self.label.text()[0] != "-":
                self.label.setText("-" + self.label.text()[0:])
                self.is_changed = True
            else:
                self.label.setText(self.label.text().replace("-", ""))
                self.is_changed = False

    def del_num(self):
        self.label.setText(self.label.text()[:-1])

    def clear(self):
        self.label.setText("")
        self.label1.setText("")
        self.is_point = False

    def point(self):
        if not self.is_point and len(self.label.text()) == 0:
            self.label.setText(self.label.text() + "0.")
            self.is_point = True
        elif not self.is_point:
            self.label.setText(self.label.text() + ".")
            self.is_point = True

    def add_digit(self, digit):
        self.label.setText(self.label.text() + digit)
        self.current_num += digit
        self.last_btn = digit

    def add_operator(self, operator):
        if len(self.label1.text()) > 0:
            if len(self.label.text()) == 0:
                return
            self.equal()
        self.current_num = ""
        self.label1.setText(self.label.text() + operator)
        self.label.setText("")
        self.last_btn = operator
        self.is_point = False

    def zero(self):
        self.label.setText(self.label.text() + "0")

    def one(self):
        self.label.setText(self.label.text() + "1")

    def two(self):
        self.label.setText(self.label.text() + "2")

    def three(self):
        self.label.setText(self.label.text() + "3")

    def four(self):
        self.label.setText(self.label.text() + "4")

    def five(self):
        self.label.setText(self.label.text() + "5")

    def six(self):
        self.label.setText(self.label.text() + "6")

    def seven(self):
        self.label.setText(self.label.text() + "7")

    def eight(self):
        self.label.setText(self.label.text() + "8")

    def nine(self):
        self.label.setText(self.label.text() + "9")


class SecondWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.resize(450, 200)
        self.setWindowTitle("Calculator")
        self.is_changed = False
        self.is_point = False
        self.is_bracket = False
        self.gridlayout = QtWidgets.QGridLayout()
        self.gridlayout1 = QtWidgets.QGridLayout()
        self.buttons = [
            "Pi", "e", "C", "<--",
            "x^2", "1/x", "|x|",
            "sqrt(x)", "n!",  "/",
            "x^y", "7", "8", "9", "*",
            "10^x", "4", "5",  "6", "-",
            "log", "1",  "2", "3", "+",
            "ln", "+/-", "0", ".", "=", "1st"
            ]
        self.label = QtWidgets.QLabel()
        self.label.setFont(QtGui.QFont("Times", 17))
        self.label1 = QtWidgets.QLabel()
        self.label1.setFont(QtGui.QFont("Times", 10))
        self.gridlayout1.addWidget(self.label1, 0, 0)
        self.gridlayout1.addWidget(self.label, 1, 0)
        self.new_buttons = []
        self.positions = [(i, j) for i in range(7) for j in range(5)]
        for position, name in zip(self.positions, self.buttons):
            self.button = QtWidgets.QPushButton(name)
            self.new_buttons.append(self.button)
            self.gridlayout.addWidget(self.button, *position)
        self.new_buttons[0].clicked.connect(self.pi_num)
        self.new_buttons[-1].clicked.connect(self.first)
        self.new_buttons[2].clicked.connect(self.clear)
        self.new_buttons[3].clicked.connect(self.del_num)
        self.new_buttons[27].clicked.connect(self.zero)
        self.new_buttons[21].clicked.connect(self.one)
        self.new_buttons[22].clicked.connect(self.two)
        self.new_buttons[23].clicked.connect(self.three)
        self.new_buttons[16].clicked.connect(self.four)
        self.new_buttons[17].clicked.connect(self.five)
        self.new_buttons[18].clicked.connect(self.six)
        self.new_buttons[11].clicked.connect(self.seven)
        self.new_buttons[12].clicked.connect(self.eight)
        self.new_buttons[13].clicked.connect(self.nine)
        self.new_buttons[29].clicked.connect(self.equal)
        self.new_buttons[26].clicked.connect(self.change_sign)
        self.new_buttons[28].clicked.connect(self.point)
        self.new_buttons[24].clicked.connect(lambda: self.add_operator("+"))
        self.new_buttons[19].clicked.connect(lambda: self.add_operator("-"))
        self.new_buttons[14].clicked.connect(lambda: self.add_operator("*"))
        self.new_buttons[9].clicked.connect(lambda: self.add_operator("/"))
        self.new_buttons[10].clicked.connect(lambda: self.add_operator("^"))
        self.new_buttons[15].clicked.connect(self.pow_ten)
        self.new_buttons[20].clicked.connect(self.log)
        self.new_buttons[25].clicked.connect(self.ln)
        self.new_buttons[8].clicked.connect(self.factorial)
        self.new_buttons[6].clicked.connect(self.abs_num)
        self.new_buttons[7].clicked.connect(self.sqrt_num)
        self.new_buttons[4].clicked.connect(self.double)
        self.new_buttons[5].clicked.connect(self.one_x)
        self.new_buttons[1].clicked.connect(self.e)
        self.w = None
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.gridlayout1)
        self.mainLayout.addLayout(self.gridlayout)
        self.setLayout(self.mainLayout)

    def add_operator(self, operator):
        if len(self.label1.text()) > 0:
            if len(self.label.text()) == 0:
                return
            self.equal()
        self.current_num = ""
        self.label1.setText(self.label.text() + operator)
        self.label.setText("")
        self.last_btn = operator
        self.is_point = False

    def factorial(self):
        if len(self.label.text()) == 0 or self.label.text() == ".":
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "Строка пуста!")
            return
        else:
            self.label.setText(str(math.factorial(int(self.label.text()))))

    def one_x(self):
        if len(self.label.text()) == 0 or self.label.text() == ".":
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "Строка пуста!")
        else:
            self.label.setText(str(1/float(self.label.text())))

    def log(self):
        if len(self.label.text()) == 0 or self.label.text() == ".":
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "Строка пуста!")
        else:
            self.label1.setText(str(math.log(float(self.label.text()))))
            self.label.setText("")

    def ln(self):
        if len(self.label.text()) == 0 or self.label.text() == ".":
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "Строка пуста!")
        else:
            self.label1.setText(str(math.log(float(self.label.text()), math.e)))
            self.label.setText("")

    def pow_ten(self):
        if len(self.label.text()) == 0 or self.label.text() == ".":
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "Строка пуста!")
        else:
            self.label1.setText(str(10**float(self.label.text())))

    def e(self):
        self.label.setText(str(math.e))

    def double(self):
        if len(self.label.text()) == 0 or self.label.text() == ".":
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "Строка пуста!")
        else:
            self.label.setText(str(math.pow(float(self.label.text()), 2)))

    def abs_num(self):
        if len(self.label.text()) == 0 or self.label.text() == ".":
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "Строка пуста!")
        else:
            self.label.setText(str(abs(float(self.label.text()))))

    def sqrt_num(self):
        if len(self.label.text()) == 0 or self.label.text() == ".":
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "Строка пуста!")
        else:
            self.label.setText(str(math.sqrt(float(self.label.text()))))

    def pi_num(self):
        self.label.setText(str(math.pi))

    def first(self):
        if self.w is None:
            self.w = MyWindow()
            self.w.show()
            self.close()
        else:
            self.w.close()
            self.w = None

    def equal(self):
        try:
            if str.isdigit(self.label1.text()[-1]):
                return
            if self.label1.text()[-1] == "^" and len(self.label.text()) > 0:
                self.label1.setText(str(float(self.label1.text()[:-1]) ** float(self.label.text())))
                self.label.setText("")
            elif len(self.label.text()) == 0:
                QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "Ошибка")
            else:
                self.label1.setText(f"{self.label1.text() + self.label.text()}")
                self.label.setText(str(numexpr.evaluate(self.label1.text())))
        except Exception as ex:
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", str(ex))

    def plus(self):
        if self.label.text() == "." or len(self.label.text()) == 0:
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "Строка пуста!")
        else:
            self.label1.setText(self.label.text() + "+")
            self.label.setText("")
            self.is_point = False

    def minus(self):
        if self.label.text() == ".":
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "В строке только точка!")
        else:
            self.label1.setText(self.label.text() + "-")
            self.label.setText("")
            self.is_point = False

    def divide(self):
        if self.label.text() == "." or len(self.label.text()) == 0:
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "Строка пуста!")
        else:
            self.label1.setText(self.label.text() + "/")
            self.label.setText("")
            self.is_point = False

    def multiply(self):
        if self.label.text() == "." or len(self.label.text()) == 0:
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "Строка пуста!")
        else:
            self.label1.setText(self.label.text() + "*")
            self.label.setText("")
            self.is_point = False

    def change_sign(self):
        if len(self.label.text()) == 0:
            QtWidgets.QMessageBox.about(QtWidgets.QWidget(), "Ошибка", "Строка пуста!")
            return
        if self.label.text() == "0":
            self.label.setText(self.label.text())
        else:
            if not self.is_changed and self.label.text()[0] != "-" and len(self.label.text()) > 0:
                self.label.setText("-" + self.label.text())
                self.is_changed = True
            elif len(self.label.text()) > 0 and self.is_changed:
                self.label.setText(self.label.text().replace("-", ""))
                self.is_changed = False

    def del_num(self):
        self.label.setText(self.label.text()[:-1])

    def clear(self):
        self.label.setText("")
        self.label1.setText("")
        self.is_point = False

    def point(self):
        if not self.is_point and len(self.label.text()) == 0:
            self.label.setText(self.label.text() + "0.")
            self.is_point = True
        elif not self.is_point:
            self.label.setText(self.label.text() + ".")
            self.is_point = True

    def add_digit(self, digit):
        self.label.setText(self.label.text() + digit)
        self.current_num += digit
        self.last_btn = digit

    def zero(self):
        self.label.setText(self.label.text() + "0")

    def one(self):
        self.label.setText(self.label.text() + "1")

    def two(self):
        self.label.setText(self.label.text() + "2")

    def three(self):
        self.label.setText(self.label.text() + "3")

    def four(self):
        self.label.setText(self.label.text() + "4")

    def five(self):
        self.label.setText(self.label.text() + "5")

    def six(self):
        self.label.setText(self.label.text() + "6")

    def seven(self):
        self.label.setText(self.label.text() + "7")

    def eight(self):
        self.label.setText(self.label.text() + "8")

    def nine(self):
        self.label.setText(self.label.text() + "9")


if __name__ == '__main__':
    from sys import argv, exit

    app = QtWidgets.QApplication(argv)
    qt_material.apply_stylesheet(app, theme="dark_blue.xml")
    my_window = MyWindow()
    my_window.show()
    exit(app.exec_())
