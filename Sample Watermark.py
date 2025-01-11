import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QGroupBox, QFontDialog,
                             QColorDialog, QSpinBox, QDoubleSpinBox, QFileDialog,
                             QMessageBox, QCheckBox, QRadioButton, QComboBox)
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QPoint, QSettings

class WatermarkOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setGeometry(QApplication.desktop().screenGeometry())
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.watermark_text = "Sample Watermark"
        self.watermark_font = QFont("Arial", 36)
        self.watermark_color = QColor(100, 100, 100, 128)
        self.watermark_angle = 30
        self.watermark_spacing = 200
        self.watermark_opacity = 0.5

    def setWatermarkText(self, text):
        self.watermark_text = text
        self.update()

    def setWatermarkFont(self, font):
        self.watermark_font = font
        self.update()

    def setWatermarkColor(self, color):
        self.watermark_color = color
        self.update()

    def setWatermarkAngle(self, angle):
        self.watermark_angle = angle
        self.update()

    def setWatermarkSpacing(self, spacing):
        self.watermark_spacing = spacing
        self.update()

    def setWatermarkOpacity(self, opacity):
        self.watermark_opacity = opacity
        self.watermark_color.setAlphaF(opacity)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setFont(self.watermark_font)
        painter.setPen(self.watermark_color)

        text_width = painter.fontMetrics().width(self.watermark_text)
        text_height = painter.fontMetrics().height()

        screen_width = self.width()
        screen_height = self.height()

        x = -screen_width
        while x < 2 * screen_width:
            y = -text_height
            while y < 2 * screen_height:
                painter.save()
                painter.translate(x + text_width / 2, y + text_height / 2)
                painter.rotate(self.watermark_angle)
                painter.drawText(int(-text_width / 2), int(text_height / 4), self.watermark_text)
                painter.restore()
                y += text_height + self.watermark_spacing
            x += text_width + self.watermark_spacing

class WatermarkConfig(QWidget):
    def __init__(self, overlay):
        super().__init__()
        self.overlay = overlay
        self.settings = QSettings("YourCompany", "WatermarkApp")
        self.current_language = "en"  # Default language
        self.translations = {
            "en": {
                "Watermark Configuration": "Watermark Configuration",
                "Language": "Language",
                "Select Language:": "Select Language:",
                "Text Watermark": "Text Watermark",
                "Enter Watermark Text:": "Enter Watermark Text:",
                "Select Font": "Select Font",
                "Select Color": "Select Color",
                "Common Settings": "Common Settings",
                "Stay on top": "Stay on top",
                "Angle:": "Angle:",
                "Spacing:": "Spacing:",
                "Opacity:": "Opacity:",
                "Sample Watermark": "Sample Watermark",
            },
            "zh_CN": {
                "Watermark Configuration": "水印配置",
                "Language": "语言",
                "Select Language:": "选择语言:",
                "Text Watermark": "文本水印",
                "Enter Watermark Text:": "输入水印文字:",
                "Select Font": "选择字体",
                "Select Color": "选择颜色",
                "Common Settings": "通用设置",
                "Stay on top": "保持在顶层",
                "Angle:": "角度:",
                "Spacing:": "间距:",
                "Opacity:": "透明度:",
                "Sample Watermark": "示例水印",
            }
            # 可以添加更多语言
        }

        self.setWindowTitle(self.tr("Watermark Configuration"))
        # Language Setting
        self.language_group = QGroupBox(self.tr("Language"))
        self.language_combo = QComboBox()
        self.language_combo.addItem("English", "en")
        self.language_combo.addItem("简体中文", "zh_CN")
        language_layout = QHBoxLayout()
        language_layout.addWidget(QLabel(self.tr("Select Language:")))
        language_layout.addWidget(self.language_combo)
        self.language_group.setLayout(language_layout)

        # Text Watermark Settings
        self.text_group = QGroupBox(self.tr("Text Watermark"))
        self.text_edit = QLineEdit()
        self.font_button = QPushButton(self.tr("Select Font"))
        self.color_button = QPushButton(self.tr("Select Color"))
        text_layout = QVBoxLayout()
        text_layout.addWidget(QLabel(self.tr("Enter Watermark Text:")))
        text_layout.addWidget(self.text_edit)
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.font_button)
        h_layout.addWidget(self.color_button)
        text_layout.addLayout(h_layout)
        self.text_group.setLayout(text_layout)

        # Common Settings
        self.common_group = QGroupBox(self.tr("Common Settings"))
        self.angle_spin = QSpinBox()
        self.angle_spin.setRange(0, 359)
        self.spacing_spin = QSpinBox()
        self.spacing_spin.setRange(0, 500)
        self.opacity_slider = QDoubleSpinBox()
        self.opacity_slider.setRange(0.0, 1.0)
        self.opacity_slider.setSingleStep(0.1)

        common_layout = QVBoxLayout()
        self.stay_on_top_checkbox = QCheckBox(self.tr("Stay on top"))
        common_layout.addWidget(self.stay_on_top_checkbox)
        h_layout_angle = QHBoxLayout()
        h_layout_angle.addWidget(QLabel(self.tr("Angle:")))
        h_layout_angle.addWidget(self.angle_spin)
        common_layout.addLayout(h_layout_angle)
        h_layout_spacing = QHBoxLayout()
        h_layout_spacing.addWidget(QLabel(self.tr("Spacing:")))
        h_layout_spacing.addWidget(self.spacing_spin)
        common_layout.addLayout(h_layout_spacing)
        h_layout_opacity = QHBoxLayout()
        h_layout_opacity.addWidget(QLabel(self.tr("Opacity:")))
        h_layout_opacity.addWidget(self.opacity_slider)
        common_layout.addLayout(h_layout_opacity)
        self.common_group.setLayout(common_layout)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.language_group)
        main_layout.addWidget(self.text_group)
        main_layout.addWidget(self.common_group)
        self.setLayout(main_layout)

        # Connect signals
        self.text_edit.textChanged.connect(self.overlay.setWatermarkText)
        self.font_button.clicked.connect(self.showFontDialog)
        self.color_button.clicked.connect(self.showColorDialog)
        self.angle_spin.valueChanged.connect(self.overlay.setWatermarkAngle)
        self.spacing_spin.valueChanged.connect(self.overlay.setWatermarkSpacing)
        self.opacity_slider.valueChanged.connect(self.overlay.setWatermarkOpacity)
        self.stay_on_top_checkbox.stateChanged.connect(self.toggleStayOnTop)
        self.language_combo.currentIndexChanged.connect(self.changeLanguage)

        # Load settings
        self.loadSettings()
        self.applySettingsToOverlay()
        self.updateUiText() # Initial UI text update

    def tr(self, text):
        return self.translations.get(self.current_language, {}).get(text, text)

    def updateUiText(self):
        self.setWindowTitle(self.tr("Watermark Configuration"))
        self.language_group.setTitle(self.tr("Language"))
        self.language_group.findChild(QLabel).setText(self.tr("Select Language:"))
        self.text_group.setTitle(self.tr("Text Watermark"))
        self.text_group.findChild(QLabel).setText(self.tr("Enter Watermark Text:"))
        self.font_button.setText(self.tr("Select Font"))
        self.color_button.setText(self.tr("Select Color"))
        self.common_group.setTitle(self.tr("Common Settings"))
        self.stay_on_top_checkbox.setText(self.tr("Stay on top"))
        for child in self.common_group.children():
            if isinstance(child, QLabel):
                if "Angle" in child.text():
                    child.setText(self.tr("Angle:"))
                elif "Spacing" in child.text():
                    child.setText(self.tr("Spacing:"))
                elif "Opacity" in child.text():
                    child.setText(self.tr("Opacity:"))

    def showFontDialog(self):
        font, ok = QFontDialog.getFont(self.overlay.watermark_font, self, self.tr("Select Font"))
        if ok:
            self.overlay.setWatermarkFont(font)

    def showColorDialog(self):
        color = QColorDialog.getColor(self.overlay.watermark_color, self, self.tr("Select Color"))
        if color.isValid():
            self.overlay.setWatermarkColor(color)

    def toggleStayOnTop(self, state):
        if state == Qt.Checked:
            self.overlay.setWindowFlag(Qt.WindowStaysOnTopHint)
        else:
            self.overlay.setWindowFlag(Qt.WindowStaysOnTopHint, False)
        self.overlay.show()

    def saveSettings(self):
        self.settings.setValue("watermark_text", self.text_edit.text())
        self.settings.setValue("watermark_font", self.overlay.watermark_font.toString())
        self.settings.setValue("watermark_color", self.overlay.watermark_color.name())
        self.settings.setValue("watermark_angle", self.angle_spin.value())
        self.settings.setValue("watermark_spacing", self.spacing_spin.value())
        self.settings.setValue("watermark_opacity", self.opacity_slider.value())
        self.settings.setValue("stay_on_top", self.stay_on_top_checkbox.isChecked())
        self.settings.setValue("language", self.current_language)

    def loadSettings(self):
        self.text_edit.setText(self.settings.value("watermark_text", self.tr("Sample Watermark")))
        font = QFont()
        font.fromString(self.settings.value("watermark_font", "Arial,36,-1,5,50,0,0,0,0,0"))
        self.overlay.setWatermarkFont(font)
        color = QColor(self.settings.value("watermark_color", "#64646480"))
        self.overlay.setWatermarkColor(color)
        self.angle_spin.setValue(int(self.settings.value("watermark_angle", 30)))
        self.spacing_spin.setValue(int(self.settings.value("watermark_spacing", 200)))
        self.opacity_slider.setValue(float(self.settings.value("watermark_opacity", 0.5)))
        self.stay_on_top_checkbox.setChecked(self.settings.value("stay_on_top", True) == 'true')

        saved_language = self.settings.value("language", "en")
        index = self.language_combo.findData(saved_language)
        if index != -1:
            self.language_combo.setCurrentIndex(index)
            self.current_language = saved_language

    def applySettingsToOverlay(self):
        self.overlay.setWatermarkText(self.text_edit.text())
        color = QColor(self.settings.value("watermark_color", "#64646480"))
        self.overlay.setWatermarkColor(color)
        self.overlay.setWatermarkAngle(self.angle_spin.value())
        self.overlay.setWatermarkSpacing(self.spacing_spin.value())
        self.overlay.setWatermarkOpacity(self.opacity_slider.value())
        if self.stay_on_top_checkbox.isChecked():
            self.overlay.setWindowFlag(Qt.WindowStaysOnTopHint)
        else:
            self.overlay.setWindowFlag(Qt.WindowStaysOnTopHint, False)
        self.overlay.show()

    def changeLanguage(self, index):
        self.current_language = self.language_combo.currentData()
        self.updateUiText()
        self.saveSettings()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    overlay = WatermarkOverlay()
    config_window = WatermarkConfig(overlay)
    config_window.show()

    sys.exit(app.exec_())