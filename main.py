from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
import sys
import pygame

class GalacticQuestGame(QWidget):
    def __init__(self):
        super().__init__()

        self.background = "In the year 2123, humankind has developed the technology to travel across galaxies. As the captain of the spacecraft Pegasus, the player's mission is to explore the Andromeda galaxy and find a new habitable planet for humanity to colonize."
        self.introduction = "Welcome to the Pegasus, Captain. \nThe crew and the entire human race are counting on your wisdom and courage to secure a future for us in the Andromeda galaxy. \nWe have prepared three possible routes for this journey. \nChoose wisely.\n"

        self.label = QLabel(self.background + "\n" + self.introduction)
        self.label.setWordWrap(True)

        self.start_button = QPushButton("Start Galactic Quest!")
        self.start_button.clicked.connect(self.start_game)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

    def start_game(self):
        self.start_button.setParent(None)  # remove the start button

        self.route_a_button = QPushButton("Choose Route A")
        self.route_a_button.clicked.connect(self.route_a)

        self.route_b_button = QPushButton("Choose Route B")
        self.route_b_button.clicked.connect(self.route_b)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.route_a_button)
        self.layout.addWidget(self.route_b_button)

        self.label.setText("Take the safe, long route. This will use less fuel but takes longer and you may run out of supplies.\n\nTake the risky, shorter route. This is quicker but consumes more fuel and there's the chance of encountering unknown dangers.")

    def route_a(self):
        self.route_a_button.setParent(None)
        self.route_b_button.setParent(None)
        

        self.investigate_signal_button = QPushButton("Investigate Distress Signal")
        self.investigate_signal_button.clicked.connect(self.investigate_signal)

        self.ignore_signal_button = QPushButton("Ignore Distress Signal")
        self.ignore_signal_button.clicked.connect(self.ignore_signal)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.investigate_signal_button)
        self.layout.addWidget(self.ignore_signal_button)

        self.label.setText("A distress signal is intercepted from a nearby spaceship. Do you want to proceed and investigate?")

    def investigate_signal(self):
        self.investigate_signal_button.setParent(None)
        self.ignore_signal_button.setParent(None)

        self.negotiate_button = QPushButton("Try to negotiate with the pirates")
        self.negotiate_button.clicked.connect(self.negotiate)

        self.battle_button = QPushButton("Engage in a space battle")
        self.battle_button.clicked.connect(self.battle)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.negotiate_button)
        self.layout.addWidget(self.battle_button)

        self.label.setText("You encounter alien pirates who try to hijack the ship. You have two options")

    def ignore_signal(self):
        self.investigate_signal_button.setParent(None)
        self.ignore_signal_button.setParent(None)

        self.layout.addWidget(self.label)

        self.label.setText("You decide to stay focused on the mission and continue on")

    def negotiate(self):
        self.negotiate_button.setParent(None)
        self.battle_button.setParent(None)

        self.layout.addWidget(self.label)

        self.label.setText("Success: Gain alien allies and valuable resources for the mission")

    def battle(self):
        self.negotiate_button.setParent(None)
        self.battle_button.setParent(None)

        self.layout.addWidget(self.label)

        self.label.setText("Failure: Lose crew members and critical supplies")

    def route_b(self):
        self.route_a_button.setParent(None)
        self.route_b_button.setParent(None)
        

        self.inspect_anomaly_button = QPushButton("Inspect the anomaly")
        self.inspect_anomaly_button.clicked.connect(self.inspect_anomaly)

        self.avoid_anomaly_button = QPushButton("Avoid the anomaly and alter the course")
        self.avoid_anomaly_button.clicked.connect(self.avoid_anomaly)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.inspect_anomaly_button)
        self.layout.addWidget(self.avoid_anomaly_button)

        self.label.setText("A strange spatial anomaly is detected ahead. Do you want to inspect the anomaly?")

    def inspect_anomaly(self):
        self.inspect_anomaly_button.setParent(None)
        self.avoid_anomaly_button.setParent(None)

        self.take_risk_button = QPushButton("Take the risk and fly through the wormhole.")
        self.take_risk_button.clicked.connect(self.take_risk)

        self.take_detour_button = QPushButton("Take a detour around the wormhole.")
        self.take_detour_button.clicked.connect(self.take_detour)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.take_risk_button)
        self.layout.addWidget(self.take_detour_button)

        self.label.setText("The anomaly is a wormhole that can get you to Andromeda much faster, but the ship could also get damaged. Choose your next step.")

    def avoid_anomaly(self):
        self.inspect_anomaly_button.setParent(None)
        self.avoid_anomaly_button.setParent(None)

        self.layout.addWidget(self.label)

        self.label.setText("You decide to stay focused on the mission and continue on")

    def take_risk(self):
        self.take_risk_button.setParent(None)
        self.take_detour_button.setParent(None)

        self.layout.addWidget(self.label)

        self.label.setText("Success: Reach Andromeda in record time and locate the habitable planet.")

    def take_detour(self):
        self.take_risk_button.setParent(None)
        self.take_detour_button.setParent(None)

        self.layout.addWidget(self.label)

        self.label.setText("Failure: Severe ship damage, causing mission failure and getting stranded in space.")



pygame.mixer.init()

pygame.mixer.music.load("surveillance.mp3")

pygame.mixer.music.play(-1)

app = QApplication(sys.argv)

game = GalacticQuestGame()
game.show()

sys.exit(app.exec_())