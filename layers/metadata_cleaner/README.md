# ZeroMeta - مزيل البيانات الوصفية

A simple and easy-to-use tool to remove metadata from various file types with a user-friendly GUI.  
أداة بسيطة وسهلة الاستخدام لإزالة البيانات الوصفية من الملفات المختلفة مع واجهة مستخدم رسومية سهلة الاستخدام.

## المميزات | Features

- **يدعم إزالة البيانات الوصفية من أنواع متعددة من الملفات**  
  **Supports metadata removal from various file types:**
  - **الصور | Images:** JPG, PNG, TIFF, WebP, BMP, GIF
  - **المستندات | Documents:** PDF, DOC, DOCX, ODT, XLS, XLSX, ODP, PPT, PPTX
  - **الأرشيفات | Archives:** ZIP, TAR, GZ, 7Z, RAR
  - **الملفات الصوتية | Audio:** MP3, WAV, OGG, FLAC, M4A
  - **مقاطع الفيديو | Video:** MP4, MOV, AVI, MKV, WMV, FLV
- **واجهة مستخدم رسومية سهلة الاستخدام**  
  **User-friendly graphical interface**
- **دعم كامل للغة العربية (واجهة من اليمين لليسار)**  
  **Full Arabic language support (Right-to-Left interface)**
- **إمكانية عرض البيانات الوصفية قبل الحذف**  
  **View metadata before deletion**
- **خيار الكتابة فوق الملف الأصلي أو حفظه كملف جديد**  
  **Option to overwrite original file or save as new**

## المتطلبات | Requirements

- **Python 3.6 أو أحدث | Python 3.6 or later**
- **PyQt6**
- **Pillow** (للتعامل مع ملفات الصور | For image processing)

## التثبيت | Installation

1. **قم بتثبيت المتطلبات باستخدام الأمر التالي:**  
   **Install the required packages using the following command:**
   ```bash
   pip install PyQt6 Pillow