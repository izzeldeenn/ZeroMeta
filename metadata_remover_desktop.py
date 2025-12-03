#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إضافة خيار 'إزالة البيانات الوصفية' إلى قائمة النقر بزر الماوس الأيمن
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from gi.repository import Nautilus, GObject

class MetadataRemoverExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        super().__init__()
        # الحصول على المسار الكامل للسكريبت الأصلي
        self.script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'metadata_remover.py')
        
    def menu_activate_cb(self, menu, file):
        """دالة تنفيذ الأمر عند النقر على الخيار في القائمة"""
        file_path = file.get_location().get_path()
        try:
            # تنفيذ أمر إزالة البيانات الوصفية
            subprocess.Popen(['python3', self.script_path, 'remove', '--overwrite', file_path])
        except Exception as e:
            print(f"Error: {e}")
    
    def get_file_items(self, window, files):
        """إضافة الخيار إلى قائمة النقر بزر الماوس الأيمن"""
        # التحقق من أن ملفًا واحدًا فقط محدد
        if len(files) != 1:
            return []
            
        file = files[0]
        
        # الحصول على امتداد الملف
        _, ext = os.path.splitext(file.get_name().lower())
        
        # دعم امتدادات الصور فقط في هذا المثال
        supported_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.webp']
        
        if ext not in supported_extensions:
            return []
            
        # إنشاء عنصر القائمة
        menu_item = Nautilus.MenuItem(
            name="MetadataRemover::RemoveMetadata",
            label="إزالة البيانات الوصفية",
            tip="إزالة البيانات الوصفية من الملف"
        )
        
        # ربط الحدث
        menu_item.connect('activate', self.menu_activate_cb, file)
        
        return [menu_item]

if __name__ == '__main__':
    print("هذا الملف يجب تثبيته كإضافة لـ Nautilus وليس تشغيله مباشرة.")
    print("يجب نسخه إلى مجلد إضافات Nautilus.")
    
    # إنشاء مجلد الإضافات إذا لم يكن موجودًا
    extensions_dir = os.path.expanduser('~/.local/share/nautilus-python/extensions')
    os.makedirs(extensions_dir, exist_ok=True)
    
    # نسخ الملف إلى مجلد الإضافات
    dest_path = os.path.join(extensions_dir, 'metadata_remover_extension.py')
    shutil.copy2(__file__, dest_path)
    
    print(f"تم تثبيت الإضافة في: {dest_path}")
    print("يرجى إعادة تشغيل Nautilus أو تسجيل الخروج ثم الدخول لتطبيق التغييرات.")
