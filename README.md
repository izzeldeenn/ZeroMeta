<p align="center">
  <a href="#arabic">🇸🇦 العربية</a> | 
  <a href="#english">🇺🇸 English</a>
</p>

---

# <a name="arabic"></a> 🇸🇦 ZeroMeta — مساعد الخصوصية وإزالة البيانات الوصفية

ZeroMeta هو مشروع مفتوح المصدر يهدف إلى مساعدتك في حماية خصوصيتك على الإنترنت عبر إزالة البيانات الوصفية (Metadata)، ومراقبة الملفات، وتشغيل طبقات متعددة من أدوات الأمان.  
يعمل التطبيق بواجهتين: **سطر الأوامر (CLI)** و **واجهة رسومية عصرية (GUI)** مبنية باستخدام **Flet**، ومتاح على كل من Linux وWindows.

---

## 🎯 **ما هو ZeroMeta؟**

ZeroMeta ليس مجرد أداة لإزالة البيانات الوصفية، بل هو **مساعد خصوصية متكامل** يمكن توسيعه بسهولة عبر نظام "طبقات ZeroMeta" الذي يسمح بإضافة خدمات أمنية جديدة دون زيادة حجم التطبيق أو تحميل المستخدم مكونات لا يحتاجها.

---

## 🧩 **طبقات ZeroMeta (ZeroMeta Layers)**

طبقات ZeroMeta هي وحدات مستقلة (Modules) يمكن تثبيتها وتشغيلها وإدارتها بسهولة داخل التطبيق.  
من أمثلتها:

- 🧹 طبقة تنظيف البيانات الوصفية  
- 👁️ طبقة مراقبة الملفات في الزمن الحقيقي  
- 🔒 طبقة أدوات الخصوصية الشبكية  
- 🚫 طبقة منع التسريبات  
- 🎭 طبقة تنقية الملفات (Sanitizer)  
- 🔍 طبقة فحص الخصوصية للملفات والمجلدات  

يتمكن المستخدم من تثبيت أو إلغاء وتحديث أي طبقة دون التأثير على التطبيق الرئيسي.

---

## 🖥️ **الواجهة الرسومية (GUI)**

واجهة ZeroMeta مبنية باستخدام **Flet**، وتتميز بـ:

- تصميم حديث يعتمد على Material Design  
- دعم الوضع الليلي والنهاري  
- لوحة تحكم مركزية Dashboard  
- شريط جانبي للتنقل  
- قسم لإدارة الطبقات  
- مراقبة مباشرة (Real-time Monitor)  
- نظام تسجيل Logs متقدم  

---

## 🧰 **سطر الأوامر (CLI)**

يوفر ZeroMeta واجهة أوامر سهلة للاستخدام:

- تنظيف البيانات الوصفية من الملفات  
- مراقبة المجلدات تلقائياً  
- تشغيل وإدارة الطبقات  
- سجل عمليات مفصل  
- وضع التشغيل في الخلفية Background Mode  

---

## 🛠️ **التثبيت**

### 1️⃣ **تثبيت ZeroMeta من المصدر**

```bash
git clone https://github.com/<YOUR_USERNAME>/zerometa.git
cd zerometa
pip install -r requirements.txt
```

### ▶️ **تشغيل الواجهة الرسومية**
```bash
python app.py
```

### 🖥️ **تشغيل سطر الأوامر**
```bash
zerometa --help
```

## 🏗️ **هيكلة الطبقات داخل المشروع**

لإضافة طبقة جديدة:
```
/layers/
    └── <اسم_الطبقة>/
        ├── layer.py
        ├── config.json
        └── ui.py (اختياري)
```
ويتعرف التطبيق عليها تلقائياً.  

## 🔧 **التقنيات المستخدمة**

- Python 3.10+
- Flet
- watchdog
- rich
- piexif / exiftool
- مكتبات إضافية لكل طبقة عند الحاجة

## 📌 **خارطة الطريق**

- واجهة Dashboard متقدمة
- إصدار أول طبقة Metadata Cleaner
- دعم macOS
- نظام متجر الطبقات
- نظام تحديث تلقائي
- مزامنة سحابية اختيارية

## 🤝 **المساهمة**

نرحّب بجميع المساهمين!  
يمكنك فتح Issue أو إرسال Pull Request.

## 📄 **الترخيص**

المشروع مرخّص تحت MIT License.

---

# <a name="english"></a> 🇺🇸 ZeroMeta — Privacy Assistant & Metadata Cleaner

ZeroMeta is an open-source privacy assistant designed to help you protect your digital footprint by removing metadata, monitoring files, and running modular privacy-enhancing services.  
It provides both a CLI and a modern GUI built with Flet, and supports Linux and Windows.

## 🎯 What is ZeroMeta?

ZeroMeta is more than a metadata remover — it is an extensible privacy companion based on a modular system called ZeroMeta Layers that allows adding new privacy and security tools without bloating the core application.

## 🧩 ZeroMeta Layers

ZeroMeta Layers are independent modules that can be installed, updated, enabled, or disabled.  
Examples include:

- 🧹 Metadata Cleaner
- 👁️ Real-time File Watcher
- 🔒 Network Privacy Tools
- 🚫 Anti-Leak Monitor
- 🎭 File Sanitizer
- 🔍 Privacy Scanner

## 🖥️ GUI Features

Built with Flet, offering:
- Modern Material-style design
- Light/Dark modes
- Sidebar navigation
- Layer management
- Real-time monitoring
- Advanced logging system

## 🧰 CLI Features

- Clean metadata from files
- Monitor folders automatically
- Manage Layers
- Background mode
- Detailed logs

## 🛠️ Installation

```bash
git clone https://github.com/<YOUR_USERNAME>/zerometa.git
cd zerometa
pip install -r requirements.txt
```

### Launch GUI
```bash
python app.py
```

### CLI
```bash
zerometa --help
```

## 🔧 Technologies

- Python 3.10+
- Flet
- watchdog
- rich
- EXIF processing libraries

## 🤝 Contributing

Contributions are welcome!

## 📄 License

MIT License.