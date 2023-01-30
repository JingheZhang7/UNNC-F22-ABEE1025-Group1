#!/usr/bin/python3
# -*- encoding_utf-8 -*-
try:
    import warnings

    warnings.filterwarnings("ignore")

except:
    raise Exception('Not mouduel named warnings,install warnings using the pip install command')

try:
    import sys
except:
    raise Exception('Not mouduel named sys,install sys using the pip install command')

    pass

try:
    from PyQt5.QtWidgets import (QToolButton, QFrame, QVBoxLayout, QHBoxLayout, QGridLayout, QApplication, QTextEdit,
                                 QSizePolicy, QLineEdit)
    from PyQt5.QtGui import QIntValidator, QTextOption, QTextCursor

except:
    raise Exception('Not mouduel named PyQt5,install PyQt5 using the pip install command')

    pass

# from sympy import symbols, Matrix, solve, diff, eye
try:
    from sympy import *
except:
    raise Exception('Not mouduel named sympy,install sympy using the pip install command')

    pass


class Button(QToolButton):
    """
    Create a class for the new button: Button
    """

    def __init__(self, text, parent=None):
        super(Button, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)

    def sizeHint(self):
        "Set size of button"
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 50)
        size.setWidth(max(size.width(), size.height()))
        return size


class Calc(QFrame):
    """
    Create a calculator window class
    """

    NumDigitButtons = 10

    def __init__(self):
        super().__init__()
        self.initData()
        self.initUI()
        self.initConnect()

    def initData(self):
        """
        Initialization data if necessary
        :return: None
        """
        pass
        return

    def initUI(self):
        """
        Initialization UI
        :return: None
        """
        self.layout = QVBoxLayout()
        self.createDisplayBox()
        self.createInputBox()

        self.setLayout(self.layout)
        self.show()
        return

    def initConnect(self):
        """
        Initialization connect
        :return: None
        """
        self.input.textChanged.connect(self.cursorChange)
        return

    def cursorChange(self):
        """
        Monitor cursor
        :return: None
        """
        print('cursorChange')
        cursor = self.input.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.input.setTextCursor(cursor)
        return

    def createDisplayBox(self):
        """
        Create display box and set layout
        :return: None
        """
        layout = QHBoxLayout()
        self.input = QTextEdit()
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setWordWrapMode(QTextOption.NoWrap)

        layout.addWidget(self.input)
        layout.addWidget(self.output)
        layout.setStretch(1.5, 1)
        self.layout.addLayout(layout)
        return

    def createInputBox(self):
        """
        Create inputBox and buttons
        :return: None
        """
        layout = QGridLayout()
        self.digitButtons = []
        for i in range(Calc.NumDigitButtons):
            self.digitButtons.append(self.createButton(str(i),
                                                       self.digitClicked))

        self.reverseButton = self.createButton("Inverse",
                                               self.reverseOperateClicked)
        self.powButton = self.createButton("Pow:",
                                           self.powOperatorClicked)
        self.powLineEdit = QLineEdit()
        self.powLineEdit.setValidator(QIntValidator())
        self.transposeButton = self.createButton("Transpose",
                                                 self.transposeOperatorClicked)
        self.eigenvectButton = self.createButton("Eigenvectors",
                                                 self.eigenvectOperatorClicked)
        self.eigenvalButton = self.createButton("Eigenvalues",
                                                self.eigenvalOperatorClicked)
        self.rankButton = self.createButton("Rank",
                                            self.rankOperatorClicked)
        self.detButton = self.createButton("Determinant",
                                           self.detOperatorClicked)
        self.rrefButton = self.createButton("RREF",
                                            self.rrefOperatorClicked)
        self.blankSpaceButton = self.createButton(" ",
                                                  self.blankOperatorClicked)
        self.EnterButton = self.createButton("Enter",
                                             self.EnterOperatorClicked)
        self.clearButton = self.createButton("Clear",
                                             self.clearOperatorClicked)
        self.minusButton = self.createButton("-",
                                             self.minuxOperatorClicked)

        for i in range(1, Calc.NumDigitButtons):
            row = ((9 - i) / 3) + 2
            column = ((i - 1) % 3) + 1
            layout.addWidget(self.digitButtons[i], row, column)

        layout.addWidget(self.digitButtons[0], 5, 1)
        layout.addWidget(self.reverseButton, 2, 4)
        layout.addWidget(self.powButton, 1, 1)
        layout.addWidget(self.powLineEdit, 1, 2, 1, 2)
        layout.addWidget(self.transposeButton, 1, 4)
        layout.addWidget(self.eigenvectButton, 3, 5)
        layout.addWidget(self.eigenvalButton, 4, 5)
        layout.addWidget(self.rankButton, 3, 4)
        layout.addWidget(self.detButton, 1, 5)
        layout.addWidget(self.rrefButton, 2, 5)
        layout.addWidget(self.blankSpaceButton, 5, 2, 1, 2)
        layout.addWidget(self.EnterButton, 4, 4)
        layout.addWidget(self.clearButton, 5, 5)
        layout.addWidget(self.minusButton, 5, 4)

        self.layout.addLayout(layout)
        return

    def formateInput(self, inputText):
        """
        Process input text box content
        :return: list after processing
        """
        inputText.strip()
        print("inputText", inputText, type(inputText))
        inputText += ' \n'
        listForMat = list()
        templist = list()
        currentNum = ''
        for char in inputText:
            print(char)
            if char.isalnum():
                currentNum += char

            if char == '-':
                currentNum += char

            if char.isspace():
                if currentNum.isalnum() or currentNum[1:].isalnum():
                    templist.append(int(currentNum))
                currentNum = ''

            if char == '\n' and len(templist) != 0:
                listForMat.append(templist)
                templist = []

        return listForMat

    def formatOutput(self, matrix):
        """
        Process output text box content
        :return: list after processing
        """
        output = ''
        row, column = matrix.shape
        print(column)
        count = 0
        for i in matrix:
            print(count)
            if count % column == 0 and count != 0:
                output += '\n'
            output += str(i) + '  '
            count += 1
        return output

    def reverseOperateClicked(self):
        """
        Finding the inverse matrix
        :return: None
        """
        text = self.input.toPlainText()
        print('text :', text)
        listForMat = self.formateInput(text)
        print(listForMat)
        A = Matrix(listForMat)
        # It's not a square matrix or you can't invert the rank
        if A.shape[0] != A.shape[1] or A.rank() != A.shape[0]:
            self.abortOperation()
            return
        reverse_A = A ** -1
        output = self.formatOutput(reverse_A)

        self.output.setPlainText(output)
        return

    def abortOperation(self):
        """
        Set abnormal result
        :return: None
        """
        self.output.setPlainText("####")
        return

    def powOperatorClicked(self):
        """
        Pow
        :return: None
        """

        n = self.powLineEdit.text()
        if n.isalnum():
            text = self.input.toPlainText()
            listForMat = self.formateInput(text)
            A = Matrix(listForMat)

            # Can't raise it to the power unless it's square
            if A.shape[0] != A.shape[1]:
                self.abortOperation()
                return
            output = ''
            output_forhuman = ''
            eigenvalmap = A.eigenvals()
            iseigenvals_int = True

            for key in eigenvalmap.keys():
                if key % 1 != 0:
                    print('isinstance(key, int):', key)
                    iseigenvals_int = False
                    break

            if iseigenvals_int and A.rank() > 1:
                try:
                    answer = pow_Matrix(A, int(n))
                    A = answer[0]
                    output_forhuman = str(answer[1])
                    output = output_forhuman + '\n \n'

                except Exception:
                    A = A ** int(n)
            else:
                A = A ** int(n)
            output += self.formatOutput(A)
            self.output.setPlainText(output)
        return

    def transposeOperatorClicked(self):
        """
        Transpose
        :return: None
        """
        text = self.input.toPlainText()
        print('text :', text)
        listForMat = self.formateInput(text)
        print(listForMat)
        A = Matrix(listForMat)
        print(A)
        A = Matrix(A)
        transpose_A = A.T
        output = self.formatOutput(transpose_A)

        self.output.setPlainText(output)
        return

    def eigenvectOperatorClicked(self):
        """
        Eigenvect
        :return: None
        """
        text = self.input.toPlainText()
        listForMat = self.formateInput(text)
        A = Matrix(listForMat)
        # Can't find an eigenvector without being square
        if A.shape[0] != A.shape[1]:
            self.abortOperation()
            return
        eigenvectList = A.eigenvects()
        output = ''
        for i in range(len(eigenvectList)):
            output += 'Eigenvalue:' + str(eigenvectList[i][0])
            output += ' ,Number:' + str(eigenvectList[i][1])
            output += ' ,Eigenvector: \n'
            for j in range(len(eigenvectList[i][2])):  # There could be multiple eigenvectors
                output += self.formatOutput(eigenvectList[i][2][j]) + ' '
                output += '\n'
                output += ' '
                output += '\n'

            output += '\n'

        self.output.setPlainText(output)
        return

    def eigenvalOperatorClicked(self):
        """
        Calculate eigenvalues
        :return: None
        """
        text = self.input.toPlainText()
        listForMat = self.formateInput(text)
        A = Matrix(listForMat)
        # Can't find eigenvalues without square matrices
        if A.shape[0] != A.shape[1]:
            self.abortOperation()
            return
        eigenvalmap = A.eigenvals()
        output = ''
        for val, num in eigenvalmap.items():
            for i in range(num):
                output += str(val) + ' '
        self.output.setPlainText(output)
        return

    def rankOperatorClicked(self):
        """
        Calculate rank
        :return: None
        """
        text = self.input.toPlainText()
        listForMat = self.formateInput(text)
        A = Matrix(listForMat)

        rank = A.rank()
        output = str(rank)
        self.output.setPlainText(output)
        return

    def detOperatorClicked(self):
        """
        Calculate det(determinant)
        :return: None
        """
        text = self.input.toPlainText()
        listForMat = self.formateInput(text)
        A = Matrix(listForMat)
        # Can't find a determinant without a square matrix
        if A.shape[0] != A.shape[1]:
            self.abortOperation()
            return
        det = A.det()
        output = str(det)
        self.output.setPlainText(output)
        return

    def rrefOperatorClicked(self):
        """
        Calculate rref result
        :return: None
        """
        text = self.input.toPlainText()
        listForMat = self.formateInput(text)
        A = Matrix(listForMat)

        rrf_matrix = A.rref()[0]
        output = self.formatOutput(rrf_matrix)
        self.output.setPlainText(output)
        return

    def blankOperatorClicked(self):
        """
        Add space if clicked button of blank
        :return:
        """
        text = self.input.toPlainText()
        text += ' '
        self.input.setPlainText(text)
        return

    def EnterOperatorClicked(self):
        """
        Add line break if clicked button of 'Enter'
        :return:
        """
        text = self.input.toPlainText()
        text += '\n'
        self.input.setPlainText(text)
        return

    def minuxOperatorClicked(self):
        """
        Add minus if clicked button of '-'
        :return:
        """
        text = self.input.toPlainText()
        text += '-'
        self.input.setPlainText(text)
        return

    def clearOperatorClicked(self):
        """
        Clear all if clicked button of 'Clear'
        :return:
        """
        self.output.setPlainText('')
        self.input.setPlainText('')
        self.powLineEdit.setText('')
        return

    def createButton(self, text, member):
        """
        Use to quickly create a button instance
        :return:
        """
        button = Button(text)
        button.clicked.connect(member)
        return button

    def digitClicked(self):
        """
        To numerical
        :return:
        """
        clickedButton = self.sender()
        digitValue = int(clickedButton.text())
        self.input.setPlainText(self.input.toPlainText() + str(digitValue))
        return


def getYuExpression(n):
    """
    An expression to obtain the remainder after determining the eigenvalue
    The  count is one less than the eigenvalue count, and range defaults to the penultimate
    :param n: number of pow
    :return: expression result
    """
    symbolsList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
    expression = symbols(symbolsList[0])
    for i in range(1, n):
        sysmbos_value = symbols(symbolsList[i])
        tmp = sysmbos_value * symbols("x") ** (i)
        expression += tmp
    print('expression:', expression)
    return expression


def findSame(numlist):
    """
    Input eigenvalue graph
    Output the number of the most repetitions, and the most repetitions
    :param numlist: eigenvalue graph
    :return: the number of the most repetitions, and the most repetitions
    """
    maxSame = 0
    for tzz, same_num in numlist.items():
        if maxSame < same_num:
            maxSame = same_num
            maxSameNum = tzz
    res = (maxSameNum, maxSame)
    return res


def calEquation(A, expression, tzz, same_num, same_nums):
    """
    Solving equations

    """
    expressionList = list()
    for key in tzz.keys():
        expressionList.append(expression.subs('x', key))

    for i in range(same_nums - 1):
        dify = diff(expression, symbols('x'))
        expression = dify
        print('dify :', dify)
        expressionList.append(dify.subs('x', same_num))
    print('expressionList: ', expressionList)

    # sympy.solve the system of equations with sympy.solve
    answers = solve(expressionList)
    print('answers', answers)

    answerList = list()
    human_answerList = list()

    # Format a,b,c... with a list.

    for key, value in answers.items():
        if key == symbols('a'):
            human_answerList.append((key, value))
            size = A.rank()
            tmp = eye(size)
            value = value * tmp
            answerList.append((key, value))
        else:
            answerList.append((key, value))
            human_answerList.append((key, value))

    # Add variable x to the list with the value A
    tmp = (symbols('x'), A)
    answerList.append(tmp)
    res = (answerList, human_answerList)
    return res


def pow_Matrix(A, n):
    """
    Exponents of matrices
    :param A:matrix
    :param n:number of pow
    :return: result
    """
    tzz = A.eigenvals()  # Return value is a dictionary, eigenvalue: multiplicity of the root
    rank = A.rank()  # Get the rank of the matrix A
    yu_expression = getYuExpression(rank)  # Obtain an expression for the remainder

    same_num, same_nums = findSame(tzz)
    print('same_num:', same_num, '  same_nums:', same_nums)

    expression = symbols("x") ** n - yu_expression
    print(expression)

    result = calEquation(A, expression, tzz, same_num, same_nums)
    answerList = result[0]
    human_answeList = result[1]
    print('answerList :', answerList)
    answer = yu_expression.subs(answerList)
    print('answer: ', answer)
    human_answer = yu_expression.subs(human_answeList)
    return (answer, human_answer)


if __name__ == '__main__':
    # main
    app = QApplication(sys.argv)
    calc = Calc()
    sys.exit(app.exec_())
