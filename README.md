<div align="center">
  <a href="#arabic">
    <img src="./logo.png" alt="ZeroMeta Logo" width="200"/>
  </a>
  
  <h1>ZeroMeta</h1>
  <h3>Privacy Assistant & Metadata Management Platform</h3>
  
  <p>
    <a href="#arabic">🇸🇦 العربية</a> • 
    <a href="#english">🇺🇸 English</a> •
    <a href="#-project-structure">🏗️ Project Structure</a> •
    <a href="#-getting-started">🚀 Getting Started</a>
  </p>
  
  <p>
    <a href="https://github.com/yourusername/zerometa/stargazers">
      <img src="https://img.shields.io/github/stars/yourusername/zerometa?style=social" alt="GitHub stars">
    </a>
    <a href="https://github.com/yourusername/zerometa/blob/main/LICENSE">
      <img src="https://img.shields.io/github/license/yourusername/zerometa" alt="License">
    </a>
    <a href="https://pypi.org/project/zerometa/">
      <img src="https://img.shields.io/pypi/v/zerometa" alt="PyPI">
    </a>
  </p>
</div>

---

<a name="arabic"></a>
# 🛡️ ZeroMeta — منصة حماية الخصوصية القابلة للتوسعة

ZeroMeta هو مشروع مفتوح المصدر يهدف إلى مساعدتك في حماية خصوصيتك على الإنترنت عبر إزالة البيانات الوصفية (Metadata)، ومراقبة الملفات، وتشغيل طبقات متعددة من أدوات الأمان.  
يعمل التطبيق بواجهتين: **سطر الأوامر (CLI)** و **واجهة رسومية عصرية (GUI)** مبنية باستخدام **Flet**، ومتاح على كل من Linux وWindows.

---

## 🎯 **ما هو ZeroMeta؟**

ZeroMeta هو **منصة حماية خصوصية متكاملة** تتيح لك التحكم الكامل في بصمتك الرقمية. نحن لسنا مجرد أداة لإزالة البيانات الوصفية، بل منصة متكاملة قابلة للتخصيص والتوسع.

### المميزات الرئيسية:
- 🧩 **نظام طبقات قابل للتوسعة** - أضف ميزات جديدة عبر نظام الطبقات
- 🖥️ **واجهة مستبدية بديهية** - بنيت باستخدام Flet
- 🛡️ **حماية شاملة** - من إزالة البيانات الوصفية إلى مراقبة الملفات
- 🚀 **خفيف وسريع** - يحمل فقط الميزات التي تحتاجها
- 🔄 **يعمل في الخلفية** - مراقبة مستمرة للملفات

---

## **طبقات ZeroMeta (ZeroMeta Layers)**

طبقات ZeroMeta هي وحدات مستقلة (Modules) يمكن تثبيتها وتشغيلها وإدارتها بسهولة داخل التطبيق.  
من أمثلتها:

- **طبقة تنظيف البيانات الوصفية**  
- **طبقة مراقبة الملفات في الزمن الحقيقي**  
- **طبقة أدوات الخصوصية الشبكية**  
- **طبقة منع التسريبات**  
- **طبقة تنقية الملفات (Sanitizer)**  
- **طبقة فحص الخصوصية للملفات والمجلدات**  

يتمكن المستخدم من تثبيت أو إلغاء وتحديث أي طبقة دون التأثير على التطبيق الرئيسي.

---

## 🖥️ **الواجهة الرسومية**

تم بناء واجهة ZeroMeta باستخدام **Flet** لتوفير تجربة مستبددة سلسة وعصرية:

### لوحة التحكم الرئيسية
- 📊 **نظرة عامة** - إحصائيات سريعة عن النشاط
- 🛠️ **إدارة الطبقات** - تفعيل/تعطيل/تكوين الطبقات
- 📂 **مدير الملفات** - تصفح ومعالجة الملفات

### الميزات المتقدمة
- 🌓 **وضع الظلام/الفاتح** - دعم كامل للوضعين
- 🔔 **إشعارات فورية** - تنبيهات فورية للأحداث المهمة
- 📊 **تقارير تفصيلية** - تحليلات عن النشاط والملفات
- 🔄 **مزامنة سحابية** - احتفظ بإعداداتك أينما ذهبت (اختياري)  

---

## 💻 **واجهة سطر الأوامر (CLI)**

ZeroMeta يوفر واجهة أوامر قوية للتحكم الكامل:

### الأوامر الأساسية
```bash
# إدارة الطبقات
zerometa layers list                # عرض الطبقات المثبتة
zerometa layers install <name>      # تثبيت طبقة جديدة
zerometa layers remove <name>       # إزالة طبقة

# التحكم بالطبقات
zerometa layer <name> start         # تشغيل طبقة
zerometa layer <name> stop          # إيقاف طبقة
zerometa layer <name> status        # حالة الطبقة

# إدارة الخدمة
zerometa daemon start               # تشغيل الخدمة الخلفية
zerometa daemon stop                # إيقاف الخدمة الخلفية
zerometa daemon status              # حالة الخدمة
```

### أمثلة عملية
```bash
# تشغيل منظف البيانات الوصفية على مجلد
zerometa layer metadata clean /path/to/folder

# مراقبة مجلد للتغييرات
zerometa layer watcher add /path/to/watch
```  

---

## 🚀 **التثبيت والإعداد**

### المتطلبات الأساسية
- Python 3.10 أو أحدث
- pip (مدير حزم بايثون)
- Git (للتثبيت من المصدر)

### التثبيت باستخدام pip
```bash
pip install zerometa
```

### التثبيت من المصدر
```bash
# استنساخ المستودع
git clone https://github.com/yourusername/zerometa.git
cd zerometa

# تثبيت المتطلبات
pip install -r requirements.txt

# تثبيت التطبيق
pip install -e .
```

### بدء الاستخدام
```bash
# تشغيل الواجهة الرسومية
zerometa gui

# أو استخدام سطر الأوامر
zerometa --help
```

## 🏗️ **هيكلة المشروع**

```
/zerometa/
├── core/                     # النواة الأساسية
│   ├── layer_manager.py      # إدارة تحميل وتشغيل الطبقات
│   ├── installer.py          # تثبيت/حذف الطبقات
│   ├── api_bridge.py         # ربط واجهة المستخدم مع الطبقات
│   └── config_manager.py     # إدارة الإعدادات
│
├── layers/                   # مجلدات الطبقات
│   ├── metadata_cleaner/     # مثال: منظف البيانات الوصفية
│   │   ├── layer.py         # كود الطبقة الأساسي
│   │   ├── ui.py            # واجهة المستخدم
│   │   └── config.json      # إعدادات الطبقة
│   └── ...
│
├── ui/                      # واجهة المستخدم الرسومية
│   ├── pages/              # صفحات التطبيق
│   │   ├── dashboard.py    # لوحة التحكم
│   │   ├── layers.py       # إدارة الطبقات
│   │   └── settings.py     # الإعدادات
│   └── components/         # مكونات واجهة المستخدم
│
├── services/               # الخدمات الخلفية
│   └── watcher.py         # مراقبة الملفات
│
└── tests/                  # الاختبارات
```

## 🛠️ **التقنيات المستخدمة**

### الأساسية
- **Python 3.10+** - لغة البرمجة الأساسية
- **Flet** - لواجهة المستخدم الرسومية
- **watchdog** - مراقبة الملفات
- **rich** - واجهة سطر الأوامر المطورة
- **piexif/exiftool** - معالجة البيانات الوصفية

### إضافية
- **aiohttp** - للاتصالات الشبكية
- **PyYAML** - لمعالجة ملفات التكوين
- **loguru** - نظام تسجيل متقدم
- **pytest** - للاختبارات

## 🚀 **خارطة الطريق**

### المرحلة الحالية (v0.1.0)
- [x] هيكلة المشروع الأساسية
- [x] نظام الطبقات الأساسي
- [x] واجهة سطر الأوامر (CLI)
- [ ] واجهة المستخدم الرسومية الأساسية

### القادم قريباً
- [ ] نظام متجر الطبقات
- [ ] دعم أنظمة التشغيل الإضافية (macOS)
- [ ] واجهة برمجة التطبيقات (API)
- [ ] التوثيق الكامل

### المستقبل
- [ ] المزامنة السحابية
- [ ] الإضافات المخصصة
- [ ] دعم الأجهزة المحمولة

## 🤝 **كيفية المساهمة**

نرحب بجميع المساهمات! إليك كيفية المساعدة:

1. **الإبلاغ عن الأخطاء**
   - افتح Issue جديداً وصف المشكلة بالتفصيل
   - أضيف لقطات شاشة إن أمكن

2. **تطوير ميزات جديدة**
   - انسخ المشروع (Fork)
   - أنشئ فرعاً جديداً للميزة
   - أرسل Pull Request

3. **تحسين الوثائق**
   - صحح الأخطاء اللغوية
   - أضف أمثلة توضيحية
   - حسن تنسيق الوثائق

### إرشادات المساهمة
1. اتبع [PEP 8](https://www.python.org/dev/peps/pep-0008/)
2. اكتب تعليقات واضحة للكود
3. أضف اختبارات لوظائفك الجديدة
4. قم بتحديث الوثائق ذات الصلة

## 📄 **الترخيص**

هذا المشروع مرخص تحت [رخصة MIT](LICENSE).

```
MIT License

Copyright (c) 2023 ZeroMeta Team

يُسمح بالاستخدام، النسخ، التعديل، الدمج، النشر، التوزيع، والترخيص من الباطن
لبرنامج ZeroMeta والوثائق المرتبطة به ("البرنامج") لأي غرض كان، بما في ذلك
الأغراض التجارية، شريطة أن تشمل جميع النسخ أو الأجزاء المهمة من البرنامج
الإشعار التالي:

حقوق النشر (c) 2023 ZeroMeta Team

يُمنح الإذن، مجاناً، لأي شخص يحصل على نسخة من هذا البرنامج والملفات
الوثائقية المرتبطة به ("البرنامج")، بالتعامل مع البرنامج دون قيود، بما في ذلك
على سبيل المثال لا الحصر الحق في استخدام ونسخ وتعديل ودمج ونشر وتوزيع
وترخيص من الباطن و/أو بيع نسخ من البرنامج، والسماح للأشخاص الذين يتم تزويدهم
بالبرنامج بذلك، شريطة أن يتم تضمين الإشعار أعلاه وإشعار حقوق الملكية
هذا في جميع النسخ أو الأجزاء المهمة من البرنامج.

يتم توفير البرنامج "كما هو"، دون أي ضمان من أي نوع، صريح أو ضمني،
بما في ذلك على سبيل المثال لا الحصر ضمانات قابلية التسويق، والملاءمة
لغرض معين وعدم الانتهاك. في أي حال لن يكون أصحاب حقوق النشر أو
المساهمون مسؤولين عن أي مطالبة أو أضرار أو مسؤولية أخرى، سواء في
إطار عقد أو ضرر أو غير ذلك، الناشئة عن أو في اتصال مع البرنامج أو
الاستخدام أو المعاملات الأخرى في البرنامج.
```

---

# <a name="english"></a> 🔒 ZeroMeta — Privacy Assistant & Metadata Cleaner

<div align="center">
  <p>An open-source privacy platform that helps you take control of your digital footprint through powerful metadata management and privacy tools.</p>
  
  <p>
    <a href="#quick-start">Quick Start</a> •
    <a href="#documentation">Documentation</a> •
    <a href="#contributing">Contributing</a> •
    <a href="https://github.com/yourusername/zerometa/issues">Issues</a>
  </p>
  
  <p>
    <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python 3.10+">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome">
  </p>
</div>

## 🌟 Features

- **Modular Architecture** - Extend functionality with ZeroMeta Layers
- **Cross-Platform** - Works on Linux, Windows, and soon macOS
- **Dual Interface** - Modern GUI and powerful CLI
- **Real-time Protection** - Monitor files and directories
- **Open Source** - Transparent and community-driven

## 🚀 Quick Start

### Installation
```bash
# Install from PyPI
pip install zerometa

# Or from source
git clone https://github.com/yourusername/zerometa.git
cd zerometa
pip install -e .
```

### Basic Usage
```bash
# Launch the GUI
zerometa gui

# Or use the CLI
zerometa --help

# Install a layer
zerometa layers install metadata_cleaner

# Start a layer
zerometa layer metadata_cleaner start
```

## 📚 Documentation

### Project Structure
```
zerometa/
├── core/                  # Core functionality
│   ├── layer_manager.py   # Layer management
│   ├── installer.py       # Layer installation
│   └── ...
├── layers/               # Layer packages
│   └── metadata_cleaner/ # Example layer
├── ui/                   # GUI components
└── tests/                # Test suite
```

### Creating a Layer
1. Create a new directory in `layers/`
2. Add these files:
   - `layer.py` - Main layer code
   - `config.json` - Layer configuration
   - `ui.py` - (Optional) Custom UI components

Example `layer.py`:
```python
from core.layer import BaseLayer

class MyLayer(BaseLayer):
    name = "My Awesome Layer"
    
    def start(self):
        """Start the layer"""
        print("Layer started!")
    
    def stop(self):
        """Stop the layer"""
        print("Layer stopped!")
```

## 🤝 Contributing

We welcome all contributions! Here's how you can help:

1. Report bugs by opening an issue
2. Suggest new features
3. Submit pull requests
4. Improve documentation

### Development Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/zerometa.git
cd zerometa

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <p>Made with ❤️ by the ZeroMeta Team</p>
  <p>
    <a href="https://github.com/yourusername/zerometa">GitHub</a> •
    <a href="https://discord.gg/your-invite">Discord</a> •
    <a href="https://twitter.com/yourusername">Twitter</a>
  </p>
</div>

## ZeroMeta Layers

ZeroMeta Layers are independent modules that can be installed, updated, enabled, or disabled.  
Examples include:

- Metadata Cleaner
- Real-time File Watcher
- Network Privacy Tools
- Anti-Leak Monitor
- File Sanitizer
- Privacy Scanner

## GUI Features

Built with Flet, offering:
- Modern Material-style design
- Light/Dark modes
- Sidebar navigation
- Layer management
- Real-time monitoring
- Advanced logging system

## CLI Features

- Clean metadata from files
- Monitor folders automatically
- Manage Layers
- Background mode
- Detailed logs

## Installation

```bash
git clone https://github.com/izzeldeen/zerometa.git
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

## Technologies

- Python 3.10+
- Flet
- watchdog
- rich
- EXIF processing libraries

## Contributing

Contributions are welcome!

## License

MIT License.