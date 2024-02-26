# T&T Georgia (Time & Territory) - თამაში ვიქტორინა ორისთვის ქართული თემატიკით. თამაში შედგება ორი ნაწილისგან,
# დროითი და გეოგრაფიული რაუნდებისგან,სადაც 16 კითხვაზე პასუხის გაცემის შემდეგ, დაგროვებული ქულების მიხედვით,
# იმარჯვებს მოთამაშე. თამაშის შესაქმნელად გამოყენებულია PyQt5 ბიბლიოთეკა და Python-ის რამდენიმე
# მოდული (sys, random, json ...). კითხვების შესანახად გამოყენებულია ცალკე JSON ფაილი.

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import random
import json


# ინსტრუქციის ჩასატვირთი კლასი, რომელიც თამაშის დაწყებამდე მოთამაშეებს აცნობს წესებს და დაწყების ღილაკზე დაჭერის
# შემდეგ ხურავს ინსტრუქციის ბარათს და უშვებს მთავარ კლასს (MainGame)
class InstructionCard(QWidget):
    def __init__(self, start_game_callback, parent=None):
        super().__init__(parent)
        self.start_game_callback = start_game_callback
        self.initui()

    def initui(self):
        self.setGeometry(400, 30, 1200, 900)
        self.setWindowTitle('თამაშის წესები')

        layout = QVBoxLayout()

        instructionLabel = QLabel("თქვენს წინაშეა ვიქტორინა 'დრო და ტერიტორია'. ის შედგება 8 ქრონოლოგიური და 8 გეოგრაფიული კითხვისგან.\nპირველ 8 კითხვაზე პასუხის გასაცემად, მოთამაშე 1 პასუხის გრაფაში წერს წელს (შეიყვანეთ მხოლოდ რიცხვები), ხოლო მოთამაშე 2 ირჩევს (ჩექბოქსის მონიშვნით) უფრო გვიან მოხდა მოცემული მოვლენა, თუ უფრო ადრე.\nტერიტორიულ კითხვებზე გადასვლის შემდეგ, მოთამაშე 1 უკვე ქალაქის ნომერს ირჩევს 1-დან 24-ის ჩათვლით (ისევ მხოლოდ რიცხვები შეგყავთ). მოთამაშე 2 კი, ირჩევს უფრო შორს არის სწორი ქალაქი საქართველოს გეოგრაფიული ცენტრისგან, თუ უფრო ახლოს.\n\nქალაქები უკვე დანომრილია სიშორის მიხედვით, ამიტომ დანომვრას მიაქციეთ ყურადღება. თუ თქვენი(მოთამაშე 2-ის) პასუხის ნომერი ნაკლები პირველი მოთამაშის არჩეულ ნომერზე, მაშინ მონიშნეთ ღილაკი: 'უფრო ახლოს', ხოლო თუ იმ ქალაქს, რომელსაც თქვენ ფიქრობთ, უფრო მაღალი ნომერი შეესაბამება, მონიშნეთ: 'უფრო შორს'.\n\nიგივე პასუხის გაცემა მოთამაშე 2-ს არ შეუძლია. ის მხოლოდ ირჩევს ვარიანტებიდან: უფრო ადრე, უფრო გვიან, უფრო შორს, უფრო ახლოს. ამიტომ მნიშვნელოვანია, თუ ვინ დაიწყებს თამაშს.\nმოთამაშე 1-ის (არჩევანი) და მოთამაშე 2-ის(არადანი) გასარკვევად, აირჩიეთ ორი ფერიდან ერთი: ლურჯი და მწვანე, ინსტრუქციის დახურვის შემდეგ, თამაშის ფანჯარაში თქვენი ფერების მიხედვით გაინაწილებთ როლებს.")
        instructionLabel.setFixedSize(1200, 500)
        instructionLabel.setWordWrap(True)
        instructionLabel.setStyleSheet(
            "QLabel {"
            "background-color: #fff;"
            "border: 2px solid black;"
            "padding: 10px;"
            "font-size: 18px;"
            "}"
        )
        layout.addWidget(instructionLabel)

        startButton = QPushButton("თამაშის დაწყება", self)
        startButton.clicked.connect(self.on_start_button_clicked)
        layout.addWidget(startButton)

        self.setLayout(layout)

    def on_start_button_clicked(self):
        self.close()
        self.start_game_callback()


# თამაშის მსვლელობის და ინტერფეისის შესაქმნელი კლასი, რომელიც წარმართავს მთლიან პროცესს კითხვების გამოტანიდან შედეგების
# დათვლის ჩათვლით.
class MainGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initui()
        self.current_question = 0
        self.player_1_score = 0
        self.player_2_score = 0
        self.questions = self.load_questions()
        self.display_question()

    # ინტერფეისის განმსაზღვრელი მეთოდი, რომელშიც თანმიმდევრობით განლაგდებიან კითხვის, პასუხების ველის, თუ დადასტურების
    # ღილაკის გამოსატანი ვიჯეტები. ვიჯეტების ფუნქციონალს PyQt5 უზრუნველყოფს ფარდის მიღმა.
    def initui(self):

        self.setGeometry(400, 30, 1200, 900)
        self.setWindowTitle('Time & Territory Georgia')

        self.layout = QVBoxLayout()

        self.questionLabel = QLabel("აქ გამოჩნდება კითხვა.")
        self.layout.addWidget(self.questionLabel)

        self.imageLabel = QLabel(self)
        pixmap = QPixmap('territory.png')
        scaled_pixmap = pixmap.scaled(1146, 482, Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(scaled_pixmap)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.imageLabel)

        self.player1Layout = QVBoxLayout()
        self.player1Label = QLabel("მოთამაშე 1 არის ლურჯი, მოთამაშე 2 არის მწვანე.")


        self.player1Answer = QLineEdit(self)
        self.player1Answer.setPlaceholderText("მოთამაშე 1-ის პასუხი")
        self.player1Answer.setFixedSize(300, 50)
        self.player1Answer.setStyleSheet("QLineEdit {"
                                         "border: 1px solid blue;"
                                         "border-radius: 5px;"
                                         "padding: 5px;"
                                         "color: blue;"
                                         "font-size: 14px;"
                                         "}")
        self.player1Layout.addWidget(self.player1Label)
        self.player1Layout.addWidget(self.player1Answer)
        self.player2Answer = QLineEdit(self)
        self.player2More = QRadioButton("უფრო გვიან / უფრო შორს", self)
        self.player2Less = QRadioButton("უფრო ადრე / უფრო ახლოს", self)
        self.player2More.setStyleSheet("QRadioButton { font-size: 14px; color: green;}")
        self.player2Less.setStyleSheet("QRadioButton { font-size: 14px; color: green;}")
        self.player2Group = QButtonGroup(self)
        self.player2Group.addButton(self.player2More)
        self.player2Group.addButton(self.player2Less)

        self.player2Layout = QVBoxLayout()
        self.player2Layout.addWidget(self.player2More)
        self.player2Layout.addWidget(self.player2Less)

        self.answerLayout = QHBoxLayout()
        self.answerLayout.addWidget(self.player1Label)
        self.answerLayout.addWidget(self.player1Answer)
        self.answerLayout.addLayout(self.player2Layout)
        self.layout.addLayout(self.answerLayout)

        self.submitButton = QPushButton("პასუხების დაფიქსირება", self)
        self.submitButton.clicked.connect(self.check_answers)
        self.submitButton.setStyleSheet(
            "QPushButton {"
            "padding: 10px;"
            "border: 2px solid black;"
            "border-radius: 5px;"
            "font-size: 16px;"
            "}"
        )
        self.layout.addWidget(self.submitButton)
        self.submitButton.setEnabled(False)

        self.player2More.toggled.connect(self.radio_button_checked)
        self.player2Less.toggled.connect(self.radio_button_checked)

        self.setLayout(self.layout)



    # თამაშის პირველი და მეორე რაუნდებისთვის კითხვების შემთხვევით პაკეტს ვტვირთავთ JSON ფაილებიდან და ვაგენერირებთ 8-8
    # კითხვას თითოეული სიიდან load_questions მეთოდის გამოყენებით.
    def load_questions(self):
        with open('timeQuestions.json', 'r') as time_file:
            time_questions_list = json.load(time_file)
        with open('territoryQuestions.json', 'r') as territory_file:
            territory_questions_list = json.load(territory_file)
        random_time_questions = random.sample(time_questions_list, 8)
        random_territory_questions = random.sample(territory_questions_list, 8)
        random_questions = [*random_time_questions, *random_territory_questions]
        return random_questions

    def display_question(self):
        if self.current_question < len(self.questions):
            self.questionLabel.setText(self.questions[self.current_question]['question'])
            self.questionLabel.setAlignment(Qt.AlignCenter)
            self.questionLabel.setFixedSize(1200, 150)
            self.questionLabel.setWordWrap(True)
            self.questionLabel.setStyleSheet(
                "QLabel {"
                "background-color: #fff;"
                "border: 2px solid black;"
                "padding: 10px;"
                "font-size: 18px;"
                "}"
            )
            self.player1Answer.clear()
            self.player2Answer.clear()
        else:
            self.show_result()

    # მეთოდი ამოწმებს, თუ მონიშნულია მეორე მოთამაშის ღილაკი, რათა გადავიდეს პასუხების შემოწმების ეტაპზე
    def radio_button_checked(self):
        # არ იძლევა პასუხის დაფიქსირების უფლებას, სანამ გვიან/ადრე ღილაკები არ იქნება მონიშნული
        if self.player2More.isChecked() or self.player2Less.isChecked():
            self.submitButton.setEnabled(True)
        else:
            self.submitButton.setEnabled(False)

    def check_answers(self):
        if self.current_question < len(self.questions):
            correctAnswer = self.questions[self.current_question]['answer']
            try:
                player1Answer = int(self.player1Answer.text())
                player2AnswerMore = self.player2More.isChecked()
                player2AnswerLess = self.player2Less.isChecked()

                if player1Answer == correctAnswer:
                    self.player_1_score += 1
                elif player1Answer < correctAnswer and player2AnswerMore:
                    self.player_2_score += 1
                elif player1Answer > correctAnswer and player2AnswerLess:
                    self.player_2_score += 1
                else:
                    self.player_1_score += 1

                self.current_question += 1

                if self.current_question < len(self.questions):
                    QMessageBox.information(self, "სწორი პასუხი", f"სწორი პასუხია: {correctAnswer}")
                    self.display_question()
                else:
                    self.show_result()

            except ValueError:
                QMessageBox.warning(self, "მცდარი ჩანაწერი", "შეიყვანეთ მხოლოდ რიცხვები!")
        else:
            self.show_result()

    def show_result(self):
        result_message = f"მოთამაშე 1-ის ქულა: {self.player_1_score}\nმოთამაშე 2-ის ქულა: {self.player_2_score}"
        QMessageBox.information(self, "თამაში დასრულებულია", result_message)
        self.close()


    def startGame(self):
        self.show()


def main():
    app = QApplication(sys.argv)
    quiz = MainGame()
    instructionCard = InstructionCard(start_game_callback=quiz.startGame)
    instructionCard.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
