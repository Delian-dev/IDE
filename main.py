from window import *
import sys
from Highlighter.highlighter import cPlusPlusHighlighter
from algorithms import ALGORITHMS
from FileSystem.file_methods import *
from shortcuts import ShortcutManager
from FileSystem.folder_open import initialize_sidebar_and_splitter, open_folder
from Styles import style
from Functions.toggle_terminal import toggle_terminal

def insert_algorithm(editor, algorithm_code):
    """Insert algorithm code at the current cursor position in the editor"""
    cursor = editor.textCursor()
    cursor.insertText(algorithm_code)
    editor.setTextCursor(cursor)

def get_current_editor(tab_widget): #asta e pt ca am incercat sa fac posibilitatea de a avea mai multe taburi deschise - momentan a fost cam fail
    """Get the current editor from the active tab"""
    return tab_widget.currentWidget()

def comment_line_or_selection(editor):
    """ Daca nu e nimic selectat, comenteaza linia curenta, altfel comenteaza toate liniile selectate 
        In cazul in care linia/selectia este deja comentata, o de-comenteaza """
    cursor = editor.textCursor()
    if not cursor.hasSelection():
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        lines = [cursor.selectedText()]
    else:
        start_selection = cursor.selectionStart()
        end_selection = cursor.selectionEnd()

        start_cursor = QTextCursor(editor.document())
        start_cursor.setPosition(start_selection)
        start_cursor.movePosition(QtGui.QTextCursor.StartOfBlock)

        end_cursor = QTextCursor(editor.document())
        end_cursor.setPosition(end_selection)
        end_cursor.movePosition(QtGui.QTextCursor.EndOfBlock)

        cursor.setPosition(start_cursor.position())
        cursor.setPosition(end_cursor.position(), QtGui.QTextCursor.KeepAnchor)
        lines = cursor.selectedText().split('\u2029')  

    if all(line.strip().startswith("//") for line in lines):
        new_lines = [line.replace("//", "", 1) for line in lines]
    else:
        new_lines = ["//" + line for line in lines]

    cursor.insertText("\n".join(new_lines))
    editor.setTextCursor(cursor)


if __name__ == "__main__":
    # f = open("testingCode.cpp", "r")
    # testText = f.readlines()
    # test = "".join(testText)
    # f.close()
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, False)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.setStyleSheet(style.MAIN_WINDOW_STYLE)
    MainWindow.showMaximized()
    MainWindow.show()

    # pe aici am aplicat styling-ul ala mizerabil
    ui.tree_view.setStyleSheet(style.PLACEHOLDER_STYLE)
    ui.terminal.setStyleSheet(style.PLACEHOLDER_STYLE)

    for button in ui.buttons:
        button.setStyleSheet(style.BUTTON_STYLE)

    ui.buttons[19].clicked.connect(lambda: toggle_terminal(ui.terminal, ui.terminal_splitter)) #terminal toggle button (ultimul din zona 2)

    editor = ui.plainTextEdit.text_edit
    # editor.setPlainText(test)
    

    editor.setStyleSheet(style.EDITOR_STYLE)
    # editor.setStyleSheet()
    font = editor.font()
    font.setPointSize(style.EDITOR_FONT_SIZE)
    editor.setFont(font)    
    highlighter = cPlusPlusHighlighter(ui.plainTextEdit, editor.document())
    ui.plainTextEdit.highlighter = highlighter

    ui.terminal.setStyleSheet(style.TERMINAL_STYLE)
    

    # Initialize the ShortcutManager - see the shortcuts.py file for more details :)
    shortcut_manager = ShortcutManager(MainWindow)
    
    # Add shortcuts with descriptive names and default key sequences
    shortcut_manager.add_shortcut("New File", "Ctrl+N", ui.handle_new_file)
    shortcut_manager.add_shortcut("Open File", "Ctrl+O", ui.handle_open_file)
    shortcut_manager.add_shortcut("Save File", "Ctrl+S", ui.handle_save_file)
    shortcut_manager.add_shortcut("Save File As", "Ctrl+Shift+S", ui.handle_save_file_as)
    shortcut_manager.add_shortcut("Open Folder", "Ctrl+K", lambda: open_folder(ui.file_model, ui.tree_view))
    shortcut_manager.add_shortcut("Run Code", "F5", lambda: ui.run_code())
    shortcut_manager.add_shortcut("Comment line", "Ctrl+/", lambda: comment_line_or_selection(editor))
    
    # Connect button 1 to open the shortcut settings dialog
    ui.buttons[0].setText("Shortcuts")
    ui.buttons[0].setToolTip("Configure keyboard shortcuts")
    ui.buttons[0].clicked.connect(shortcut_manager.show_config_dialog)
    
    # Connect algorithm actions to their respective functions
    # Sorting algorithms
    ui.actionBubbleSort.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Sorting"]["Bubble Sort"]))
    ui.actionInsertionSort.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Sorting"]["Insertion Sort"]))
    ui.actionQuickSort.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Sorting"]["Quick Sort"]))
    ui.actionMergeSort.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Sorting"]["Merge Sort"]))
    
    # Searching algorithms
    ui.actionBinarySearch.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Searching"]["Binary Search"]))
    ui.actionLinearSearch.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Searching"]["Linear Search"]))
    
    # Data structures
    ui.actionLinkedList.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Data Structures"]["Linked List"]))
    ui.actionStack.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Data Structures"]["Stack"]))
    ui.actionQueue.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Data Structures"]["Queue"]))
    
    # Graph algorithms
    ui.actionBFS.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Graph Algorithms"]["BFS"]))
    ui.actionDFS.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Graph Algorithms"]["DFS"]))
    
    # Dynamic programming
    ui.actionFibonacci.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Dynamic Programming"]["Fibonacci"]))
    ui.actionKnapsack.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Dynamic Programming"]["Knapsack"]))
    
    # Other algorithms
    ui.actionPrimeCheck.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Other"]["Prime Check"]))
    ui.actionGCD.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Other"]["GCD"]))
    

    # Connect Files actions to their respective functions
    #Si aici si in shortcuts apelam acum handler functions din window.py - care manevreaza sistemul de filebar si apeleaza functiile din file_methods.py
    #ik codul e un mess trebuie sa ii mai dam refactor ca at this rate ajungem cu 70% din proiect in window.py
    ui.actionNewFile.triggered.connect(
        ui.handle_new_file
    )
    ui.actionOpenFile.triggered.connect(
        ui.handle_open_file
    )
    ui.actionSaveFile.triggered.connect(
        ui.handle_save_file
    )
    ui.actionSaveFileAs.triggered.connect(
        ui.handle_save_file_as
    )
    ui.actionOpenFolder.triggered.connect(
        lambda: (open_folder(ui.file_model, ui.tree_view), ui.tree_view.show())
    )

    editor.show()
    sys.exit(app.exec_())
