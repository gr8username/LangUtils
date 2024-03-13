from aqt.utils import showInfo
import os
import aqt
import utilsNData
import SimplyTranslate
import ReversoHandler
import json
from ReversoResultDisplay import show_reverso_result_display_dialog

SWITCH_LANG_IMAGE = aqt.qt.QIcon(os.path.dirname(__file__) + "/images/switch-order-icon-resized.png")
LICENSE_FILE = os.path.dirname(__file__) + "/LICENSE.txt"

# code is really messy, please forgive
class translate_gui_gen(aqt.QDialog):
    def __init__(self, editor):
        self.init = True
        self.editor = editor
        self.editorWindow = editor.parentWindow
        super().__init__(self.editorWindow)
        super().setWindowTitle("LangUtils")

    def setEditorFields(self, field0, field1):
        note = self.editor.note
        note.fields[0] = field0
        note.fields[1] = field1
        self.editor.setNote(note)
    def returnInputField(self) -> aqt.QPlainTextEdit:
        if not hasattr(self, "inputField"):
            self.inputField = aqt.QPlainTextEdit()
            self.inputField.setObjectName("Translation-text-input-field")
            return self.inputField
        else:
            return self.inputField

    def addLanguageSelector(self, layout) -> None:  #TODO: switch to QGridLayout setup
        boxData = aqt.qt.QGridLayout()
        firstLayoutLabel1 = aqt.qt.QLabel()
        firstLayoutLabel1.setText("Source Language")
        firstLayoutLabel1.adjustSize()
        boxData.addWidget(firstLayoutLabel1, 0, 0)
        self.firstLayoutCombo = aqt.qt.QComboBox()
        self.firstLayoutCombo.setObjectName("source-lang-select")
        self.firstLayoutCombo.addItems(utilsNData.getSourceLanguageList())
        self.firstLayoutCombo.setStyleSheet("combobox-popup: 0")
        self.firstLayoutCombo.setMaxVisibleItems(15)
        boxData.addWidget(self.firstLayoutCombo, 1, 0)
        secondLayoutLabel = aqt.qt.QLabel() # ignore the name, we're using grid layout now!
        secondLayoutLabel.setText("Target Language")
        secondLayoutLabel.adjustSize()
        boxData.addWidget(secondLayoutLabel, 0, 2)
        self.secondLayoutCombo = aqt.qt.QComboBox()
        self.secondLayoutCombo.setObjectName("target-lang-select")
        self.secondLayoutCombo.addItems(utilsNData.getTargetLanguageList())
        self.secondLayoutCombo.setStyleSheet("combobox-popup: 0")
        self.secondLayoutCombo.setMaxVisibleItems(15)
        boxData.addWidget(self.secondLayoutCombo, 1, 2)
        ## create in-between switch button here
        switch_button_layout = aqt.qt.QVBoxLayout()
        label_switch = aqt.qt.QLabel()
        self.switch_button_widget = aqt.qt.QPushButton()
        self.switch_button_widget.setAutoDefault(False)  # thanks to this https://stackoverflow.com/questions/44005056/how-to-make-qpushbutton-not-to-be-triggered-by-enter-keyboard-key guy on stackoverflow
        self.switch_button_widget.setDefault(False)
        self.switch_button_widget.setIcon(SWITCH_LANG_IMAGE)
        self.switch_button_widget.resize(70, 70)
        self.switch_button_widget.clicked.connect(self.swap_translate_combo_boxes)
        #
        boxData.setColumnStretch(0, 2)
        boxData.setColumnStretch(2, 2)
        boxData.addWidget(self.switch_button_widget, 1, 1)
        layout.addLayout(boxData)

    def swap_translate_combo_boxes(self):
        new_second_box_index = utilsNData.get_index_from_combo(self.firstLayoutCombo.currentText(), self.secondLayoutCombo)
        new_first_box_index = utilsNData.get_index_from_combo(self.secondLayoutCombo.currentText(), self.firstLayoutCombo)
        if new_second_box_index is None or new_first_box_index is None:  # terminate if either are none
            return
        self.firstLayoutCombo.setCurrentIndex(new_first_box_index)
        self.secondLayoutCombo.setCurrentIndex(new_second_box_index)

    def createLayout2(self):
        switch_button_widget = aqt.qt.QPushButton()
        switch_button_widget.setIcon(SWITCH_LANG_IMAGE)
        switch_button_widget.resize(70, 70)
        switch_button_widget.clicked.connect(self.switch_button_dict)
        layout2 = aqt.qt.QVBoxLayout()
        label_reverso = aqt.qt.QLabel()
        label_reverso.setText("Dictionary results are taken from reverso.net's online dictionary.")
        label_reverso.setMaximumHeight(60)
        label_reverso.adjustSize()
        ### logical separation, for readable purposes
        label1 = aqt.QLabel()
        label1.setText("Source language")
        label1.adjustSize()
        text_field_box_layout = aqt.qt.QHBoxLayout()
        text_field_box_label = aqt.qt.QLabel()
        text_field_box_label.setText("Enter word: ")
        text_field_box_label.adjustSize()
        text_field_box_label.setMaximumHeight(40)
        text_field_box_layout.addWidget(text_field_box_label)
        self.dict_combo_box_source = aqt.qt.QComboBox()
        self.dict_combo_box_source.addItems(utilsNData.reverso_return_source_langs())
        self.dict_combo_box_source.setObjectName("dict_combo_box_source")
        self.dict_combo_box_target = aqt.qt.QComboBox()
        self.dict_combo_box_target.addItems(utilsNData.reverso_return_target_langs())
        self.dict_combo_box_target.setObjectName("dict_combo_box_target")
        ##
        label2 = aqt.QLabel()
        label2.setText("Target language")
        label2.adjustSize()
        label2.setMaximumHeight(30)
        label1.setMaximumHeight(30)
        ##
        language_entry_grid = aqt.qt.QGridLayout()
        # vertical_box_layouts[0].addWidget(label1)  ## we have switched to grid layout for this, rather than nested layouts
        # vertical_box_layouts[0].addWidget(self.dict_combo_box_source)
        # vertical_box_layouts[1].addWidget(label2)
        # vertical_box_layouts[1].addWidget(self.dict_combo_box_target)
        # ##
        # for item in vertical_box_layouts:
        #     horizontal_box_layout.addLayout(item)
        language_entry_grid.addWidget(label1, 0, 0)
        language_entry_grid.addWidget(self.dict_combo_box_source, 1, 0)
        language_entry_grid.addWidget(label2, 0, 2)
        language_entry_grid.addWidget(self.dict_combo_box_target, 1, 2)
        language_entry_grid.addWidget(switch_button_widget, 1, 1)
        language_entry_grid.setColumnStretch(0, 2)
        language_entry_grid.setColumnStretch(2, 2)
        self.dict_text_box = aqt.qt.QLineEdit()
        # self.dict_text_box.editingFinished.connect(self.dict_entry_event)
        self.submit_button = aqt.qt.QPushButton()
        self.submit_button.setObjectName("GetTranslations")
        self.submit_button.setText("Get example sentences!")
        self.submit_button.clicked.connect(self.dict_entry_event)
        layout2.addWidget(label_reverso)
        layout2.addLayout(language_entry_grid)
        text_field_box_layout.addWidget(self.dict_text_box)
        layout2.addLayout(text_field_box_layout)
        layout2.addWidget(self.dict_text_box)
        layout2.addWidget(self.submit_button)
        return layout2

    def switch_button_dict(self):
        new_source_index = utilsNData.get_index_from_combo(self.dict_combo_box_target.currentText(), self.dict_combo_box_source)
        new_target_index = utilsNData.get_index_from_combo(self.dict_combo_box_source.currentText(), self.dict_combo_box_target)
        if new_target_index is None or new_source_index is None:
            return
        self.dict_combo_box_source.setCurrentIndex(new_source_index)
        self.dict_combo_box_target.setCurrentIndex(new_target_index)

    def create_license_layout(self):
        layout = aqt.qt.QVBoxLayout()
        license_text_box = aqt.qt.QPlainTextEdit()
        license_file_object = open(LICENSE_FILE, 'r')
        license_text = license_file_object.read()
        license_file_object.close()
        license_text_box.setPlainText(license_text)
        license_text_box.setReadOnly(True)
        layout.addWidget(license_text_box)
        return layout

    def dict_entry_event(self):
        text = self.dict_text_box.text()
        utilsNData.set_default_reverso_source_language(self.dict_combo_box_source.currentText())
        utilsNData.set_default_reverso_target_language(self.dict_combo_box_target.currentText())
        source_selection = self.dict_combo_box_source.currentText().lower()
        target_selection = self.dict_combo_box_target.currentText().lower()
        examples = ReversoHandler.reverso_get_examples(source_selection, target_selection, text)
        # showInfo("Source: " + source_selection + "\nTarget: " + target_selection + "\nText: " + text)  # test code, no longer required :D
        # showInfo(json.dumps(examples))
        if len(examples.dict) > 0:
            show_reverso_result_display_dialog(self, examples)
        else:
            aqt.utils.showWarning("Cannot retrieve results for the chosen words, please try again!")

    def returnBottomBar(self) -> aqt.QHBoxLayout:
        bar = aqt.qt.QHBoxLayout()
        button1 = aqt.qt.QPushButton("&Preview")
        button1.setObjectName("Preview selected translation")
        button1.clicked.connect(self.onPreviewButtonPress)
        bar.addWidget(button1)
        button2 = aqt.qt.QPushButton("Add")
        button2.setObjectName("Add translated text to card")
        button2.clicked.connect(self.onButtonPress)
        bar.addWidget(button2)
        self.flipCardTranslateCheckbox = aqt.qt.QCheckBox()
        self.flipCardTranslateCheckbox.setText("Flip card order")
        bar.addWidget(self.flipCardTranslateCheckbox)
        return bar

    def createTabs(self, layout1, layout2, layout3):
        self.tabs = aqt.qt.QTabWidget()
        self.tab1 = aqt.qt.QWidget()  # change back to aqt.qt.QWidget() if needed!!!
        self.tab2 = aqt.qt.QWidget()
        self.tab3 = aqt.qt.QWidget()
        self.tab1.setLayout(layout1)
        self.tab2.setLayout(layout2)
        self.tab3.setLayout(layout3)
        self.tabs.addTab(self.tab1, "Translation")
        self.tabs.addTab(self.tab2, "Dictionary Lookup")
        self.tabs.addTab(self.tab3, "License Info")
        self.tabs.resize(300, 200)  # idk?
        self.layout.addWidget(self.tabs)

    def showMeNow(self):
        self.layout = aqt.qt.QVBoxLayout()
        self.tab1layout = aqt.qt.QVBoxLayout(self)
        self.tab2layout = self.createLayout2()
        self.tab3layout = self.create_license_layout()
        label = aqt.qt.QLabel()
        label.setText("This will automatically translate text and add it to a field (using a Simplytranslate instance set to Google's engine)."
                      "\nDefault order of cards is original text on the front, with translated version on the back, flip the order using the checkbox at the bottom.")
        label.setWordWrap(True)
        # label.setContentsMargins(10, 28, 10, 28)
        label.adjustSize()
        self.tab1layout.addWidget(label)
        self.addLanguageSelector(self.tab1layout)
        self.tab1layout.addWidget(self.returnInputField())
        self.tab1layout.addLayout(self.returnBottomBar())
        self.createTabs(self.tab1layout, self.tab2layout, self.tab3layout)
        self.setLayout(self.layout)
        self.resize(600, 500)
        return self
    def onButtonPress(self):
        second_editor_data = SimplyTranslate.simply_translate_data(utilsNData.languageToCode(str(self.firstLayoutCombo.currentText())),
                                                                   utilsNData.languageToCode(str(self.secondLayoutCombo.currentText())),
                                                                   str(self.inputField.toPlainText()))
        if self.flipCardTranslateCheckbox.isChecked():
            self.setEditorFields(str(second_editor_data), str(self.inputField.toPlainText()))
        else:
            self.setEditorFields(str(self.inputField.toPlainText()), second_editor_data)
        utilsNData.set_default_source_language(str(self.firstLayoutCombo.currentText()))
        utilsNData.set_default_target_language(str(self.secondLayoutCombo.currentText()))
        super().close()
    def onPreviewButtonPress(self):
        res = SimplyTranslate.simply_translate_data(
            utilsNData.languageToCode(str(self.firstLayoutCombo.currentText())),
            utilsNData.languageToCode(str(self.secondLayoutCombo.currentText())),
            str(self.inputField.toPlainText()))
        if self.flipCardTranslateCheckbox.isChecked():
            showInfo("Front: " + str(self.inputField.toPlainText())
                     + "\nBack: " + res)
        else:
            showInfo("Front: " + res + "\n"
                                       "Back: " + str(self.inputField.toPlainText()))

def translate_addon_button_clicked(editor):
    if editor.currentField is None:
        showInfo("Please select a field in which to enter the translated information")
    else:
        window = translate_gui_gen(editor)
        window = window.showMeNow()
        window.show()
