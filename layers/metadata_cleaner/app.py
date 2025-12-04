#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path
import threading
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox,
    QTextEdit, QProgressBar, QCheckBox, QGroupBox, QTabWidget, 
    QFrame, QSizePolicy, QSpacerItem, QStyle, QSizePolicy
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject, QRunnable, QThreadPool, QSize
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette, QLinearGradient, QGradient, QPixmap
from metadata_remover import MetadataRemover

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal(dict)
    progress = pyqtSignal(int)
    status = pyqtSignal(str)

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
        self.signals = WorkerSignals()
        self.scan_results = []
        self.scanned_files = []  # To store files with metadata
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("أداة إزالة البيانات الوصفية")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(800, 600)
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                right: 10px;
                padding: 0 5px;
                color: #374151;
            }
            QPushButton {
                background-color: #4f46e5;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 500;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #4338ca;
            }
            QPushButton:disabled {
                background-color: #9ca3af;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
                background-color: white;
            }
            QProgressBar {
                border: 1px solid #d1d5db;
                border-radius: 3px;
                text-align: center;
                background-color: #f3f4f6;
            }
            QProgressBar::chunk {
                background-color: #4f46e5;
                width: 10px;
                margin: 0.5px;
            }
            QTabWidget::pane {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 10px;
                background: white;
            }
            QTabBar::tab {
                background: #e5e7eb;
                border: 1px solid #d1d5db;
                padding: 8px 16px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 4px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 2px solid #4f46e5;
            }
        """)
        
        # Set RTL layout
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("أداة إزالة البيانات الوصفية")
        header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #1f2937;
            padding: 10px 0;
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Create tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                min-width: 120px;
                padding: 8px 16px;
            }
        """)
        
        # Single file tab
        self.setup_single_file_tab()
        
        # Directory scan tab
        self.setup_scan_tab()
        
        # Add tabs to main layout
        layout.addWidget(self.tabs, 1)
        
        # Connect signals
        self.signals.status.connect(self.update_status)
        
        # Initialize thread pool
        self.threadpool = QThreadPool()
    
    def setup_single_file_tab(self):
        """Set up the single file tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 20, 15, 15)
        layout.setSpacing(15)
        
        # File selection group
        file_group = QGroupBox("اختيار الملف")
        file_layout = QHBoxLayout()
        file_layout.setSpacing(10)
        
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("حدد مسار الملف...")
        self.path_edit.textChanged.connect(self.update_buttons)
        
        browse_btn = QPushButton("استعراض الملفات")
        browse_btn.setIcon(self.style().standardIcon(getattr(QStyle.StandardPixmap, 'SP_DirIcon')))
        browse_btn.clicked.connect(self.browse_files)
        
        file_layout.addWidget(self.path_edit, 1)
        file_layout.addWidget(browse_btn)
        file_group.setLayout(file_layout)
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)
        
        self.show_metadata_btn = QPushButton("عرض البيانات الوصفية")
        self.show_metadata_btn.setIcon(self.style().standardIcon(getattr(QStyle.StandardPixmap, 'SP_FileDialogInfoView')))
        self.show_metadata_btn.setEnabled(False)
        self.show_metadata_btn.clicked.connect(self.show_metadata)
        
        self.remove_btn = QPushButton("حذف البيانات الوصفية")
        self.remove_btn.setIcon(self.style().standardIcon(getattr(QStyle.StandardPixmap, 'SP_TrashIcon')))
        self.remove_btn.setEnabled(False)
        self.remove_btn.clicked.connect(self.remove_metadata)
        
        action_layout.addWidget(self.show_metadata_btn)
        action_layout.addWidget(self.remove_btn)
        action_layout.addStretch()
        
        # Output area
        output_group = QGroupBox("النتائج")
        output_layout = QVBoxLayout()
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("ستظهر هنا نتائج العملية...")
        
        # Clear button
        clear_btn = QPushButton("مسح النتائج")
        clear_btn.setIcon(self.style().standardIcon(getattr(QStyle.StandardPixmap, 'SP_DialogResetButton')))
        clear_btn.clicked.connect(self.clear_log)
        
        output_layout.addWidget(self.output_text)
        output_layout.addWidget(clear_btn, 0, Qt.AlignmentFlag.AlignLeft)
        output_group.setLayout(output_layout)
        
        # Add widgets to layout
        layout.addWidget(file_group)
        layout.addLayout(action_layout)
        layout.addWidget(output_group, 1)
        
        # Add tab
        self.tabs.addTab(tab, "ملف واحد")
    
    def setup_scan_tab(self):
        """Set up the directory scan tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 20, 15, 15)
        layout.setSpacing(15)
        
        # Directory selection group
        dir_group = QGroupBox("اختيار المجلد")
        dir_layout = QHBoxLayout()
        
        self.scan_path_edit = QLineEdit()
        self.scan_path_edit.setPlaceholderText("حدد مجلد للمسح...")
        
        browse_btn = QPushButton("استعراض المجلدات")
        browse_btn.setIcon(self.style().standardIcon(getattr(QStyle.StandardPixmap, 'SP_DirIcon')))
        browse_btn.clicked.connect(self.browse_directory)
        
        dir_layout.addWidget(self.scan_path_edit, 1)
        dir_layout.addWidget(browse_btn)
        dir_group.setLayout(dir_layout)
        
        # Scan options
        options_group = QGroupBox("خيارات المسح")
        options_layout = QVBoxLayout()
        
        self.recursive_checkbox = QCheckBox("بحث متكرر في المجلدات الفرعية")
        self.recursive_checkbox.setChecked(True)
        
        options_layout.addWidget(self.recursive_checkbox)
        options_group.setLayout(options_layout)
        
        # Scan button
        self.scan_btn = QPushButton("بدء المسح")
        self.scan_btn.setIcon(self.style().standardIcon(getattr(QStyle.StandardPixmap, 'SP_MediaPlay')))
        self.scan_btn.clicked.connect(self.start_scan)
        
        # Results area
        results_group = QGroupBox("نتائج المسح")
        results_layout = QVBoxLayout()
        
        self.scan_results = QTextEdit()
        self.scan_results.setReadOnly(True)
        self.scan_results.setPlaceholderText("ستظهر هنا نتائج المسح...")
        
        results_layout.addWidget(self.scan_results)
        results_group.setLayout(results_layout)
        
        # Add widgets to layout
        layout.addWidget(dir_group)
        layout.addWidget(options_group)
        layout.addWidget(self.scan_btn, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(results_group, 1)
        
        # Add tab
        self.tabs.addTab(tab, "مسح المجلدات")
    
    def update_status(self, message):
        """Update status bar with message"""
        self.statusBar().showMessage(message, 3000)  # Show message for 3 seconds
    
    def update_buttons(self):
        """Update button states based on current selection"""
        path = self.path_edit.text().strip()
        is_file = os.path.isfile(path)
        self.show_metadata_btn.setEnabled(is_file)
        self.remove_btn.setEnabled(is_file)
    
    def browse_files(self):
        """Open file dialog to select file"""
        file_filter = "الملفات المدعومة (*.jpg *.jpeg *.png *.tiff *.webp *.bmp *.gif *.pdf *.doc *.docx)"
        
        path, _ = QFileDialog.getOpenFileName(
            self,
            "اختر ملفًا",
            "",
            file_filter
        )
        
        if path:  # User didn't cancel
            self.path_edit.setText(path)
            self.clear_log()
    
    def browse_directory(self):
        """Open directory dialog to select folder for scanning"""
        path = QFileDialog.getExistingDirectory(self, "اختر مجلدًا")
        if path:  # User didn't cancel
            self.scan_path_edit.setText(path)
            self.scan_results.clear()
    
    def clear_log(self):
        """Clear the output text area"""
        self.output_text.clear()
    
    def log(self, message):
        """Add message to output text area"""
        self.output_text.append(message)
        self.output_text.verticalScrollBar().setValue(
            self.output_text.verticalScrollBar().maximum()
        )
    
    def show_metadata(self):
        """Show metadata for selected file"""
        path = self.path_edit.text().strip()
        if not path or not os.path.isfile(path):
            QMessageBox.critical(self, "خطأ", "الرجاء تحديد ملف صالح")
            return
        
        self.clear_log()
        self.log(f"جاري تحميل البيانات الوصفية لـ: {path}")
        
        # Run in a separate thread
        worker = Worker(self._show_metadata_thread, path)
        worker.signals.result.connect(self._handle_metadata_result)
        worker.signals.error.connect(self.show_error)
        self.threadpool.start(worker)
    
    def _show_metadata_thread(self, path):
        """Thread function to show metadata"""
        try:
            metadata = self.remover.get_metadata(path)
            if not metadata:
                return {"error": "لا توجد بيانات وصفية في الملف المحدد.", "metadata": {}}
            
            # Format the metadata for display
            result = ["البيانات الوصفية للملف:", "-" * 30]
            for key, value in metadata.items():
                if isinstance(value, (str, int, float, bool)):
                    result.append(f"{key}: {value}")
                elif isinstance(value, dict):
                    result.append(f"{key}:")
                    for subkey, subvalue in value.items():
                        result.append(f"  {subkey}: {subvalue}")
            
            return {"success": True, "message": "\n".join(result), "metadata": metadata}
            
        except Exception as e:
            return {"error": f"حدث خطأ أثناء قراءة البيانات الوصفية: {str(e)}", "metadata": {}}
    
    def _handle_metadata_result(self, result):
        """Handle the result of metadata retrieval"""
        if "error" in result:
            self.log(result["error"])
        else:
            self.log(result["message"])
    
    def remove_metadata(self):
        """Remove metadata from selected file"""
        path = self.path_edit.text().strip()
        if not path or not os.path.isfile(path):
            QMessageBox.critical(self, "خطأ", "الرجاء تحديد ملف صالح")
            return
        
        reply = QMessageBox.question(
            self,
            'تأكيد',
            'هل أنت متأكد من رغبتك في حذف البيانات الوصفية لهذا الملف؟',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.clear_log()
            self.log(f"جاري حذف البيانات الوصفية لـ: {path}")
            
            # Run in a separate thread
            worker = Worker(self._remove_metadata_thread, path, True)
            worker.signals.result.connect(self._handle_remove_result)
            worker.signals.error.connect(self.show_error)
            self.threadpool.start(worker)
    
    def _remove_metadata_thread(self, path, overwrite):
        """Thread function to remove metadata from file"""
        try:
            success, message = self.remover.remove_metadata(path, overwrite)
            return {"success": success, "message": message}
        except Exception as e:
            return {"error": f"حدث خطأ أثناء حذف البيانات الوصفية: {str(e)}"}
    
    def _handle_remove_result(self, result):
        """Handle the result of metadata removal"""
        if "error" in result:
            self.log(result["error"])
        else:
            self.log(result["message"])
    
    def start_scan(self):
        """Start scanning directory for files with metadata"""
        path = self.scan_path_edit.text().strip()
        if not path or not os.path.isdir(path):
            QMessageBox.critical(self, "خطأ", "الرجاء تحديد مجلد صالح")
            return
        
        self.scan_results.clear()
        self.scan_btn.setEnabled(False)
        self.scan_btn.setText("جاري المسح...")
        
        # Run in a separate thread
        worker = Worker(self._scan_directory, path)
        worker.signals.result.connect(self._handle_scan_result)
        worker.signals.error.connect(self.show_error)
        worker.signals.finished.connect(lambda: self.scan_btn.setEnabled(True))
        worker.signals.finished.connect(lambda: self.scan_btn.setText("بدء المسح"))
        self.threadpool.start(worker)
    
    def _scan_directory(self, path):
        """Scan directory for files with metadata"""
        try:
            results = []
            recursive = self.recursive_checkbox.isChecked()
            
            if recursive:
                for root, _, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if self.remover.is_supported_file(file_path):
                            metadata = self.remover.get_metadata(file_path)
                            if metadata:
                                results.append((file_path, metadata))
            else:
                for item in os.listdir(path):
                    file_path = os.path.join(path, item)
                    if os.path.isfile(file_path) and self.remover.is_supported_file(file_path):
                        metadata = self.remover.get_metadata(file_path)
                        if metadata:
                            results.append((file_path, metadata))
            
            return {"success": True, "results": results}
            
        except Exception as e:
            return {"error": f"حدث خطأ أثناء مسح المجلد: {str(e)}"}
    
    def _handle_scan_result(self, result):
        """Handle the result of directory scan"""
        if "error" in result:
            self.scan_results.append(f"خطأ: {result['error']}")
        else:
            results = result.get("results", [])
            if not results:
                self.scan_results.append("لم يتم العثور على ملفات تحتوي على بيانات وصفية.")
            else:
                self.scan_results = [f"تم العثور على {len(results)} ملف يحتوي على بيانات وصفية:\n"]
                self.scanned_files = results  # Store the files for potential removal
                
                for i, (file_path, metadata) in enumerate(results, 1):
                    self.scan_results.append(f"{i}. {file_path}")
                
                # Add Remove All button if we found files with metadata
                if hasattr(self, 'remove_all_btn'):
                    self.remove_all_btn.setVisible(True)
                
        # Update the results display
        self.update_scan_results()
    
    def show_error(self, message):
        """Show error message"""
        QMessageBox.critical(self, "خطأ", message)

def main():
    app = QApplication(sys.argv)
    
    # Set application font
    font = QFont()
    font.setFamily("Arial")
    font.setPointSize(10)
    app.setFont(font)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show the main window
    window = MetadataRemoverGUI()
    window.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
