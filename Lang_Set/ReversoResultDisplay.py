from aqt.utils import showInfo
import aqt
import utilsNData
import ReversoHandler


def show_reverso_result_display_dialog(parent, reverso_result_obj: ReversoHandler.ReversoExamplesData):
    example_dict = reverso_result_obj.dict
    dia = aqt.qt.QDialog(parent)
    dia.setMinimumHeight(300)
    layout_to_set = aqt.qt.QVBoxLayout()
    this_label = aqt.qt.QLabel()
    this_label.setText("Please select which example phrase you would like to add!")
    this_label.adjustSize()
    layout_to_set.addWidget(this_label)
    radio_btn_arr = []
    grid_layout = aqt.qt.QGridLayout()
    scroll_area = aqt.qt.QScrollArea()
    scroll_area.setHorizontalScrollBarPolicy(aqt.qt.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    iterator = 0
    for key in example_dict:
        if len(key) < 4:  # fixes a weird problem with "\n." being an entry that shows up on the menu, hopefully there's no legitimate entry 3 chars long
            continue
        radio_button = aqt.qt.QRadioButton("", dia)
        radio_button.source_text = key
        radio_button.target_text = example_dict[key]
        radio_btn_arr.append(radio_button)
        label_1 = aqt.qt.QLabel()
        label_1.setText(key)
        label_1.adjustSize()
        label_1.setMaximumWidth(225)
        label_1.setWordWrap(True)
        label_2 = aqt.qt.QLabel()
        label_2.setText(example_dict[key])
        label_2.setMaximumWidth(225)
        label_2.adjustSize()
        label_2.setWordWrap(True)
        grid_layout.addWidget(radio_button, iterator, 0, alignment=aqt.qt.Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(label_1, iterator, 1)
        grid_layout.addWidget(label_2, iterator, 2)
        grid_layout.setRowMinimumHeight(iterator, 80)
        iterator +=1
    grid_layout_widget = aqt.qt.QWidget()
    grid_layout_widget.setLayout(grid_layout)
    scroll_area.setWidget(grid_layout_widget)
    meaning_label = aqt.qt.QLabel()
    meaning_label.setText("Meaning: " + reverso_result_obj.meaning)
    meaning_label.adjustSize()
    layout_to_set.addWidget(meaning_label)
    layout_to_set.addWidget(scroll_area)
    submit_handle = SubmitHandler(dia, parent, radio_btn_arr)
    button_to_submit = aqt.qt.QPushButton("&Submit")
    button_to_submit.setText("Add Card")
    button_to_submit.clicked.connect(submit_handle.handle_submit_press)
    dia.flip_checkbox = aqt.qt.QCheckBox()
    dia.flip_checkbox.setText("Flip card order")
    layout_to_set.addWidget(button_to_submit)
    layout_to_set.addWidget(dia.flip_checkbox)
    dia.setLayout(layout_to_set)
    dia.exec()

class SubmitHandler:
    def __init__(self, parent, parent_of_parent, buttons_arr):
        self.buttons = buttons_arr
        self.parent_window = parent  # not literal parent, it's complicated
        self.parent_parent = parent_of_parent
    def handle_submit_press(self):
        check_found = False
        for key in self.buttons:
            if key.isChecked():
                if self.parent_window.flip_checkbox.isChecked():
                    self.parent_parent.setEditorFields(key.target_text, key.source_text)
                    self.parent_window.close()
                else:
                    self.parent_parent.setEditorFields(key.source_text, key.target_text)
                    self.parent_window.close()
                check_found = True
        if check_found:
            self.parent_parent.close()
        else:
            aqt.utils.showWarning("You did not select an entry.")