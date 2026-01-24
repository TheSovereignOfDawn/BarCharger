from PySide6 import QtCore
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox, QRadioButton, QButtonGroup,
                               QCheckBox)
from PySide6.QtGui import QFont
from calculus import getPlatesManagement

class MyUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BarCharger v0.1")

        self.displayFont = QFont("Amasis MT Pro")
        self.displayFont.setBold(True)
        self.displayFont.setPixelSize(25)

        self.widgetCreation()
        self.layoutManagement()
        self.signalSlotConnection()

    def widgetCreation(self):
        self.desiredWeightLabel = QLabel("Charge ?")
        self.desiredWeightSpinBox = QDoubleSpinBox()
        self.desiredWeightSpinBox.setRange(0.00, 500.00)
        self.desiredWeightSpinBox.setSingleStep(0.25)
        self.desiredWeightSpinBox.setValue(100.00)
        self.recordLabel = QLabel("Record ?")
        self.recordLabel.setAlignment(QtCore.Qt.AlignRight)
        self.recordCheckBox = QCheckBox()

        self.movementChoiceLabel = QLabel("Mouvement ?")
        self.bodyweightMovementsRadioButton = QRadioButton("Muscle-up / Traction / Dip ?")
        self.bodyweightMovementsRadioButton.setChecked(True)
        self.barMovementsRadioButton = QRadioButton("Squat / Développé couché / Soulevé de terre ?")
        self.movementGroup = QButtonGroup(self)
        self.movementGroup.addButton(self.bodyweightMovementsRadioButton, 1)
        self.movementGroup.addButton(self.barMovementsRadioButton, 2)

        self.statusLabel = QLabel()
        self.statusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.statusLabel.setFont(self.displayFont)
        self.statusLabel.setStyleSheet("""
                QLabel {
                border-radius: 12px;
                border: 2px solid black;
                }
                """)

        self.calibratedStopPlatesLabel = QLabel("Stop disques calibrés ?")
        self.calibratedStopPlatesCheckBox = QCheckBox()
        self.calibratedStopPlatesCheckBox.setEnabled(False)

        self.requiredPlatesLabelList = []
        for i in range(0, 15):
            label = QLabel()
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setFont(self.displayFont)
            self.requiredPlatesLabelList.append(label)

    def layoutManagement(self):
        primaryLayout = QVBoxLayout(self)
        desiredWeightSecondaryLayout = QHBoxLayout()
        movementChoiceSecondaryLayout = QHBoxLayout()
        calibratedStopPlatesSecondaryLayout = QHBoxLayout()
        requiredPlatesSecondaryLayout = QHBoxLayout()

        desiredWeightSecondaryLayout.addWidget(self.desiredWeightLabel)
        desiredWeightSecondaryLayout.addWidget(self.desiredWeightSpinBox)
        desiredWeightSecondaryLayout.addWidget(self.recordLabel)
        desiredWeightSecondaryLayout.addWidget(self.recordCheckBox)

        movementChoiceSecondaryLayout.addWidget(self.movementChoiceLabel)
        movementChoiceSecondaryLayout.addWidget(self.bodyweightMovementsRadioButton)
        movementChoiceSecondaryLayout.addWidget(self.barMovementsRadioButton)

        calibratedStopPlatesSecondaryLayout.addWidget(self.calibratedStopPlatesLabel)
        calibratedStopPlatesSecondaryLayout.addWidget(self.calibratedStopPlatesCheckBox)

        for label in self.requiredPlatesLabelList:
            requiredPlatesSecondaryLayout.addWidget(label)

        primaryLayout.addLayout(desiredWeightSecondaryLayout)
        primaryLayout.setStretch(0, 1)
        primaryLayout.addLayout(movementChoiceSecondaryLayout)
        primaryLayout.setStretch(1, 1)
        primaryLayout.addLayout(calibratedStopPlatesSecondaryLayout)
        primaryLayout.setStretch(2, 1)
        primaryLayout.addWidget(self.statusLabel)
        primaryLayout.setStretch(3, 2)
        primaryLayout.addLayout(requiredPlatesSecondaryLayout)
        primaryLayout.setStretch(4, 5)

    def signalSlotConnection(self):
        self.desiredWeightSpinBox.valueChanged.connect(self.updatePlatesDisplay)
        self.recordCheckBox.checkStateChanged.connect(self.updatePlatesDisplay)
        self.movementGroup.idClicked.connect(self.updatePlatesDisplay)
        self.movementGroup.idClicked.connect(self.calibratedStopPlatesCheckBoxManagement)
        self.calibratedStopPlatesCheckBox.checkStateChanged.connect(self.updatePlatesDisplay)

    def getPlateColor(self, plateWeight):
        color = ""
        match (plateWeight):
            case 25:
                color = "red"
            case 20:
                color = "blue"
            case 15:
                color = "yellow"
            case 10:
                color = "green"
            case 5:
                color = "white"
            case 2.5:
                color = "black"
            case 1.25 | 0.5 | 0.25:
                color = "grey"
            case _:
                color = "purple"

        return color

    def resetPlateLabels(self):
        for label in self.requiredPlatesLabelList:
            label.setStyleSheet("")
            label.clear()

    @QtCore.Slot()
    def updatePlatesDisplay(self):
        isBodyweightMovement = self.bodyweightMovementsRadioButton.isChecked()
        areCalibratedStopPlatesUsed = self.calibratedStopPlatesCheckBox.isChecked()
        platesRequiredDict, isDesiredWeightOk = getPlatesManagement(self.desiredWeightSpinBox.value(), isBodyweightMovement,
                                                 areCalibratedStopPlatesUsed, self.recordCheckBox.isChecked())
        platesList = [float(k) for k, v in platesRequiredDict.items() for _ in range(v)]
        self.resetPlateLabels()
        if (isDesiredWeightOk):
            self.statusLabel.setText("La charge indiquée respecte les règles de compétition.")
            for i in range(0, len(platesList)):
                self.requiredPlatesLabelList[i].setText(str(platesList[i]) + " kg")
                backgroundColor = self.getPlateColor(platesList[i])
                textColor = "black"
                if (backgroundColor == "black"):
                    textColor = "white"
                self.requiredPlatesLabelList[i].setStyleSheet(f"""
                QLabel {{
                border-radius: 12px;
                border: 2px solid black;
                color: {textColor};
                background-color: {backgroundColor};
                }}
                """)
        else:
            self.statusLabel.setText("La charge indiquée ne respecte pas les règles de compétition.")

    @QtCore.Slot()
    def calibratedStopPlatesCheckBoxManagement(self):
        if (self.barMovementsRadioButton.isChecked()):
            self.calibratedStopPlatesCheckBox.setEnabled(True)
        else:
            self.calibratedStopPlatesCheckBox.setEnabled(False)
            self.calibratedStopPlatesCheckBox.setChecked(False)
        self.resetPlateLabels()
        self.updatePlatesDisplay()


