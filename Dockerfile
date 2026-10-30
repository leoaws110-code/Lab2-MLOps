# المرحلة الأولى: بناء وتثبيت الحزم (Builder Stage)
FROM python:3.10.12-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# المرحلة الثانية: التشغيل النهائي (Runner Stage)
FROM python:3.10.12-slim AS runner

WORKDIR /app

# نسخ الحزم المثبتة من المرحلة الأولى
COPY --from=builder /install /usr/local

# نسخ ملفات الكود والتطبيق
COPY src/ src/

# إنشاء مستخدم غير جذري (Non-root user) للأمان
RUN useradd -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# إكسبوز لبيانات المنفذ
EXPOSE 8000

# إضافة فحص الصحة (HEALTHCHECK) المطلوب في اللاب
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# تشغيل التطبيق باستخدام Uvicorn
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]