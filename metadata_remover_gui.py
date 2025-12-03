#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path
import threading
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox,
    QTextEdit, QProgressBar, QCheckBox, QGroupBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject, QRunnable, QThreadPool
from PyQt6.QtGui import QFont
from metadata_remover import MetadataRemover

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal(str)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            if result:
                self.signals.result.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            self.signals.finished.emit()


class MetadataRemoverGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.remover = MetadataRemover(verbose=True)
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("إزالة البيانات الوصفية")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(700, 500)
        
        # Set RTL layout
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # File selection group
        file_group = QGroupBox("اختيار الملف أو المجلد")
        file_layout = QHBoxLayout()
        
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("حدد مسار الملف أو المجلد...")
        self.path_edit.textChanged.connect(self.update_buttons)
        
        browse_btn = QPushButton("استعراض...")
        browse_btn.clicked.connect(self.browse_files)
        
        file_layout.addWidget(self.path_edit)
        file_layout.addWidget(browse_btn)
        file_group.setLayout(file_layout)
        
        # Options group
        options_group = QGroupBox("خيارات")
        options_layout = QVBoxLayout()
        
        self.overwrite_cb = QCheckBox("الكتابة فوق الملف الأصلي")
        options_layout.addWidget(self.overwrite_cb)
        options_group.setLayout(options_layout)
        
        # Output group
        output_group = QGroupBox("الإخراج")
        output_layout = QVBoxLayout()
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont('Arial', 10))
        
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        
        output_layout.addWidget(self.output_text)
        output_layout.addWidget(self.progress)
        output_group.setLayout(output_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.show_btn = QPushButton("عرض البيانات الوصفية")
        self.show_btn.clicked.connect(self.show_metadata)
        
        self.remove_btn = QPushButton("إزالة البيانات الوصفية")
        self.remove_btn.clicked.connect(self.remove_metadata)
        
        btn_layout.addWidget(self.show_btn)
        btn_layout.addWidget(self.remove_btn)
        
        # Add all to main layout
        layout.addWidget(file_group)
        layout.addWidget(options_group)
        layout.addWidget(output_group)
        layout.addLayout(btn_layout)
        
        # Thread pool
        self.threadpool = QThreadPool()
        
        # Initial state
        self.update_buttons()
    
    def log(self, message):
        """Add message to output text area"""
        self.output_text.append(message)
        self.output_text.verticalScrollBar().setValue(
            self.output_text.verticalScrollBar().maximum()
        )
    
    def clear_log(self):
        """Clear the output text area"""
        self.output_text.clear()
    
    def update_buttons(self):
        """Update button states based on current selection"""
        has_path = bool(self.path_edit.text().strip())
        self.show_btn.setEnabled(has_path)
        self.remove_btn.setEnabled(has_path)
    
    def browse_files(self):
        """Open file dialog to select file or directory"""
        file_filter = "الملفات المدعومة (*.jpg *.jpeg *.png *.tiff *.webp *.bmp *.gif *.pdf *.doc *.docx *.odt *.xls *.xlsx *.odp *.ppt *.pptx *.zip *.tar *.gz *.7z *.rar *.mp3 *.wav *.ogg *.flac *.m4a *.mp4 *.mov *.avi *.mkv *.wmv *.flv)"
        
        path, _ = QFileDialog.getOpenFileName(
            self,
            "اختر ملفًا أو مجلدًا",
            "",
            file_filter
        )
        
        if path:  # User didn't cancel
            self.path_edit.setText(path)
            self.clear_log()
            self.log(f"تم تحديد: {path}")
    
    def show_metadata(self):
        """Show metadata for selected file"""
        path = self.path_edit.text().strip()
        if not path or not os.path.exists(path):
            QMessageBox.critical(self, "خطأ", "الرجاء تحديد ملف صالح")
            return
        
        self.clear_log()
        self.log(f"جاري تحميل البيانات الوصفية لـ: {path}")
        
        # Run in a separate thread
        worker = Worker(self._show_metadata_thread, path)
        worker.signals.result.connect(self.log)
        worker.signals.error.connect(self.show_error)
        self.threadpool.start(worker)
    
    def _show_metadata_thread(self, path):
        """Thread function to show metadata"""
        if os.path.isfile(path):
            # In a real implementation, you would capture the output
            # from MetadataRemover.show_metadata() and return it
            return "عذرًا، عرض البيانات الوصفية غير متوفر حاليًا في واجهة المستخدم الرسومية."
        return "عذرًا، لا يمكن عرض البيانات الوصفية للمجلدات. الرجاء تحديد ملف."
    
    def remove_metadata(self):
        """Remove metadata from selected file(s)"""
        path = self.path_edit.text().strip()
        if not path or not os.path.exists(path):
            QMessageBox.critical(self, "خطأ", "الرجاء تحديد ملف أو مجلد صالح")
            return
        
        self.clear_log()
        self.log(f"بدء إزالة البيانات الوصفية لـ: {path}")
        
        # Disable UI during processing
        self.set_ui_enabled(False)
        
        # Run in a separate thread
        worker = Worker(
            self._remove_metadata_thread,
            path,
            self.overwrite_cb.isChecked()
        )
        worker.signals.result.connect(self.log)
        worker.signals.error.connect(self.show_error)
        worker.signals.finished.connect(lambda: self.set_ui_enabled(True))
        self.threadpool.start(worker)
    
    def _remove_metadata_thread(self, path, overwrite):
        """Thread function to remove metadata"""
        if os.path.isfile(path):
            success, message = self.remover.remove_metadata(path, overwrite=overwrite)
            if success:
                return f"تمت إزالة البيانات الوصفية بنجاح: {message}"
            return f"فشلت إزالة البيانات الوصفية: {message}"
        return "عذرًا، هذه الميزة غير متاحة حاليًا للمجلدات."
    
    def set_ui_enabled(self, enabled):
        """Enable or disable UI elements"""
        self.path_edit.setEnabled(enabled)
        self.show_btn.setEnabled(enabled and bool(self.path_edit.text().strip()))
        self.remove_btn.setEnabled(enabled and bool(self.path_edit.text().strip()))
        self.overwrite_cb.setEnabled(enabled)
        QApplication.setOverrideCursor(
            Qt.CursorShape.WaitCursor if not enabled else Qt.CursorShape.ArrowCursor
        )
    
    def show_error(self, message):
        """Show error message"""
        QMessageBox.critical(self, "خطأ", message)


def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Set Arabic as the default language
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    
    # Create and show the main window
    window = MetadataRemoverGUI()
    window.show()
    
    # Center the window
    frame_gm = window.frameGeometry()
    screen = app.primaryScreen()
    center_point = screen.availableGeometry().center()
    frame_gm.moveCenter(center_point)
    window.move(frame_gm.topLeft())
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
