# Prediksi Kinerja Akademik Siswa (End-to-End ML Project)

## 📖 Latar Belakang

Proyek ini adalah implementasi *end-to-end* dari siklus hidup *machine learning* (MLOps), mulai dari analisis data eksploratif, pelatihan model, hingga deployment aplikasi web secara otomatis di AWS. Tujuan utamanya adalah untuk memprediksi nilai matematika (`math_score`) siswa berdasarkan berbagai faktor demografis dan sosial-ekonomi.

Proyek ini tidak hanya berfokus pada pembangunan model yang akurat, tetapi juga pada praktik rekayasa perangkat lunak dan MLOps untuk menciptakan sistem yang andal, dapat direproduksi, dan siap untuk produksi.

**🚀 Live Demo:** [**http://Farmil002-studypredict-env.eba-dxfmwycs.ap-southeast-2.elasticbeanstalk.com/**](http://Farmil002-studypredict-env.eba-dxfmwycs.ap-southeast-2.elasticbeanstalk.com/)
*(Catatan: Aplikasi mungkin dihentikan untuk menghemat biaya. Silakan hubungi saya untuk mengaktifkannya kembali jika diperlukan.)*

---

## 🏛️ Arsitektur Sistem

Proyek ini dibangun di atas arsitektur CI/CD (Continuous Integration/Continuous Deployment) yang modern, memastikan setiap perubahan kode yang di-push ke GitHub akan secara otomatis di-deploy ke lingkungan produksi.


* **Source Control:** GitHub
* **CI/CD Pipeline:** AWS CodePipeline
* **Platform Deployment:** AWS Elastic Beanstalk
* **Infrastruktur:** Server EC2 `t3.small` dengan disk EBS 30GB

---

## ✨ Fitur Utama

* **API Prediksi:** Endpoint `/predictdata` yang menerima data siswa dalam format JSON dan mengembalikan prediksi nilai matematika.
* **Pipeline Pelatihan:** Skrip modular untuk melatih ulang model dengan data baru.
* **Deployment Otomatis:** Integrasi penuh dengan AWS CodePipeline untuk CI/CD.
* **Konfigurasi sebagai Kode:** Penggunaan `.ebextensions` untuk mengelola konfigurasi server secara otomatis (misalnya, ukuran disk dan konfigurasi `pip`).

---

## 🛠️ Teknologi yang Digunakan

* **Bahasa Pemrograman:** Python 3.9
* **Library Utama:** Scikit-learn, Pandas, NumPy, Flask, Gunicorn
* **Cloud Platform:** AWS (Elastic Beanstalk, CodePipeline, EC2, S3)

---

## 🏃‍♂️ Cara Menjalankan Secara Lokal

1.  **Clone repository ini:**
    ```bash
    git clone [https://github.com/Farmil23/mlproject.git](https://github.com/Farmil23/mlproject.git)
    cd mlproject
    ```
2.  **Buat virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # atau `venv\Scripts\activate` di Windows
    ```
3.  **Install dependensi:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Jalankan aplikasi Flask:**
    ```bash
    python app.py
    ```
5.  Aplikasi akan berjalan di `http://127.0.0.1:5000`.

---

## 🎯 Tantangan dan Pembelajaran

Selama proses deployment, saya menghadapi beberapa tantangan teknis yang memberikan pembelajaran berharga:

1.  **Masalah Izin IAM:** Awalnya, deployment gagal karena user IAM dan *service role* CodePipeline tidak memiliki izin yang cukup. Saya belajar cara men-debug error `Access Denied` dan menambahkan kebijakan yang diperlukan secara spesifik, seperti `AWSCodePipelineFullAccess` dan `AmazonEC2ReadOnlyAccess`.

2.  **`No space left on device`:** Meskipun menggunakan server dengan disk 30GB, instalasi library ML yang besar gagal karena partisi `/tmp` server yang terbatas. Solusinya adalah dengan membuat konfigurasi `.ebextensions` untuk memaksa `pip` menggunakan direktori sementara di dalam partisi utama yang lebih besar.

3.  **`InconsistentVersionWarning` pada Scikit-learn:** Model yang dilatih dengan satu versi scikit-learn menghasilkan peringatan saat dijalankan dengan versi yang berbeda di server. Ini mengajarkan pentingnya "mengunci" versi library secara spesifik di `requirements.txt` agar lingkungan development dan produksi identik.

4.  **Kegagalan Boot Gunicorn:** Aplikasi gagal dimulai karena `ModuleNotFoundError`. Setelah men-debug log `web.stdout.log`, saya menemukan bahwa `Procfile` perlu disederhanakan untuk menunjuk langsung ke `app:app`, yang menyelesaikan masalah tersebut.

Proses debugging ini memperkuat pemahaman saya tentang bagaimana berbagai layanan AWS bekerja bersama dan pentingnya konfigurasi lingkungan yang tepat untuk aplikasi produksi. 