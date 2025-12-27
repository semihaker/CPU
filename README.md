# 🖥️ İşlem Zamanlama Analiz Aracı (Process Scheduling Analysis Tool)

Bu proje, işletim sistemleri dersinde öğrenilen CPU zamanlama algoritmalarını görselleştiren ve karşılaştıran kapsamlı bir simülasyon uygulamasıdır. Üç farklı zamanlama algoritmasını (FCFS, SRTF, RR) gerçek zamanlı olarak simüle eder, görselleştirir ve istatistiksel olarak karşılaştırır.

## 📋 İçindekiler

- [Özellikler](#özellikler)
- [Gereksinimler](#gereksinimler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Algoritmalar](#algoritmalar)
- [Proje Yapısı](#proje-yapısı)
- [Teknik Detaylar](#teknik-detaylar)
- [Ekran Görüntüleri ve Özellikler](#ekran-görüntüleri-ve-özellikler)
- [Geliştirici Notları](#geliştirici-notları)

## ✨ Özellikler

### 🎯 Temel Özellikler

- **3 Zamanlama Algoritması Desteği:**
  - **FCFS (First Come First Served)**: İlk gelen ilk hizmet alır
  - **SRTF (Shortest Remaining Time First)**: En kısa kalan süreye sahip işlem öncelikli
  - **RR (Round Robin)**: Zaman dilimi (quantum) tabanlı döngüsel zamanlama

- **Görselleştirme:**
  - Gerçek zamanlı Gantt diyagramı animasyonu
  - CPU durumu görselleştirmesi (çalışıyor, boşta, context switch)
  - Hazır kuyruğu (ready queue) görselleştirmesi
  - İşlem zaman çizelgesi grafiği

- **Performans Metrikleri:**
  - Ortalama bekleme süresi (Average Waiting Time)
  - Ortalama dönüş süresi (Average Turnaround Time)
  - Algoritma karşılaştırma grafikleri

- **Bilimsel Test Modülü:**
  - Monte Carlo simülasyonu (N=30)
  - İstatistiksel hipotez testi (T-Test)
  - 3 algoritmanın aynı anda karşılaştırılması
  - Performans sıralaması ve anlamlılık analizi

- **Esnek Veri Yönetimi:**
  - Önceden tanımlı senaryolar
  - Manuel işlem ekleme
  - CSV dosyası desteği
  - 30 işlemli büyük test veri seti

### 🎨 Kullanıcı Arayüzü

- Modern, karanlık tema arayüz
- Türkçe dil desteği
- Sezgisel kontrol paneli
- Gerçek zamanlı animasyon
- İnteraktif grafikler

## 📦 Gereksinimler

Bu projeyi çalıştırmak için aşağıdaki Python kütüphanelerine ihtiyacınız vardır:

- **Python 3.7+**
- **tkinter** (genellikle Python ile birlikte gelir)
- **matplotlib** (grafik ve görselleştirme)
- **numpy** (matplotlib bağımlılığı, otomatik yüklenir)

### Gerekli Kütüphaneleri Yükleme

```bash
pip install matplotlib
```

**Not:** Windows'ta tkinter genellikle Python kurulumu ile birlikte gelir. Linux'ta ayrıca yüklemeniz gerekebilir:

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

## 🚀 Kurulum

1. **Projeyi klonlayın veya indirin:**
   ```bash
   git clone <repository-url>
   cd "isletim sistemleri"
   ```

2. **Gerekli kütüphaneleri yükleyin:**
   ```bash
   pip install matplotlib
   ```

3. **Uygulamayı çalıştırın:**
   ```bash
   python main.py
   ```

## 📖 Kullanım

### Temel Kullanım

1. **Uygulamayı Başlatma:**
   - `main.py` dosyasını çalıştırın
   - Uygulama açıldığında varsayılan olarak "Büyük Test (30 İşlem)" senaryosu yüklenecektir

2. **Senaryo Seçimi:**
   - Üst panelden bir senaryo seçin:
     - **Normal / Dengeli Senaryo**: 4 işlemli standart test
     - **Konvoy Etkisi (FCFS Hatası)**: FCFS algoritmasının zayıf yönlerini gösteren senaryo
     - **Büyük Test (30 İşlem - Yüksek Yük)**: Stres testi için 30 işlemli veri seti

3. **Algoritma ve Parametre Ayarlama:**
   - **Algoritma**: FCFS, SRTF veya RR seçin
   - **Kuantum (Q)**: Round Robin için zaman dilimi (varsayılan: 2)
   - **CS Maliyeti**: Context switch maliyeti (varsayılan: 1)

4. **Simülasyonu Başlatma:**
   - "▶ BAŞLAT" butonuna tıklayın
   - Animasyon otomatik olarak başlayacak ve işlemlerin zaman çizelgesi görselleştirilecektir

5. **Manuel İşlem Ekleme:**
   - PID, Geliş Zamanı (AT) ve Süre (BT) değerlerini girin
   - "+" butonuna tıklayın
   - Hafıza değeri otomatik olarak rastgele atanacaktır

### Bilimsel Test Modülü

1. **Test Penceresini Açma:**
   - Ana ekranda "🧪 Bilimsel Test" butonuna tıklayın

2. **Algoritma Seçimi:**
   - 3 farklı algoritma seçin (A, B, C)
   - Her biri için FCFS, SRTF veya RR seçebilirsiniz

3. **Testi Çalıştırma:**
   - "🧪 3'LÜ ANALİZİ BAŞLAT" butonuna tıklayın
   - Sistem 30 kez Monte Carlo simülasyonu çalıştıracak
   - Sonuçlar:
     - Performans sıralaması
     - Ortalama bekleme süreleri
     - T-Test sonuçları
     - İstatistiksel anlamlılık analizi

### Sonuçları İnceleme

- **Sol Panel:**
  - Gantt diyagramı: Her işlemin zaman çizelgesi
  - CPU durumu: Gerçek zamanlı işlem durumu

- **Sağ Panel:**
  - İşlem listesi: Tüm işlemlerin metadata'sı
  - Simülasyon sonuçları: Ortalama bekleme ve dönüş süreleri
  - Performans karşılaştırması: Farklı algoritmaların karşılaştırma grafiği

## 🔬 Algoritmalar

### 1. FCFS (First Come First Served)

**Açıklama:** İlk gelen işlem ilk hizmet alır. Basit ve adil bir algoritmadır.

**Özellikler:**
- Non-preemptive (kesintisiz)
- Basit implementasyon
- Konvoy etkisi sorunu olabilir

**Kullanım Senaryoları:**
- Basit sistemler
- Eşit öncelikli işlemler
- Öğretim amaçlı

### 2. SRTF (Shortest Remaining Time First)

**Açıklama:** En kısa kalan süreye sahip işlem öncelik alır. Preemptive (kesintili) bir algoritmadır.

**Özellikler:**
- Preemptive
- Minimum ortalama bekleme süresi
- Starvation (açlık) sorunu olabilir

**Kullanım Senaryoları:**
- Minimum bekleme süresi istenen durumlar
- İnteraktif sistemler

### 3. RR (Round Robin)

**Açıklama:** Her işleme eşit zaman dilimi (quantum) verilir. Zaman dilimi dolunca bir sonraki işleme geçilir.

**Özellikler:**
- Preemptive
- Adil zaman paylaşımı
- Quantum değeri performansı etkiler

**Kullanım Senaryoları:**
- Zaman paylaşımlı sistemler
- İnteraktif uygulamalar
- Çok kullanıcılı sistemler

## 📁 Proje Yapısı

```
isletim-sistemleri/
│
├── main.py                 # Ana uygulama dosyası
├── ornek_veri_30.csv       # 30 işlemli test veri seti
└── README.md               # Bu dosya
```

### Dosya Açıklamaları

- **main.py**: Tüm uygulama mantığı, GUI ve algoritmalar bu dosyada
- **ornek_veri_30.csv**: CSV formatında 30 işlemli test verisi (PID, Arrival_Time, Burst_Time, Memory_MB)

## 🔧 Teknik Detaylar

### Kod Yapısı

Uygulama 4 ana bölümden oluşur:

1. **Veri Yapıları (ServerProcess Sınıfı)**
   - İşlem bilgilerini tutan sınıf
   - PID, varış zamanı, burst time, hafıza, kalan süre, bitiş zamanı

2. **Algoritma Motoru**
   - `solve_logic()`: Hesaplama için algoritma motoru
   - `solve_logic_visual()`: Görselleştirme için zaman çizelgesi üreten versiyon

3. **Bilimsel Test Modülü (HypothesisWindow)**
   - Monte Carlo simülasyonu
   - İstatistiksel analiz (T-Test)
   - 3 algoritmanın karşılaştırılması

4. **Ana Arayüz (CPULabApp)**
   - GUI bileşenleri
   - Animasyon sistemi
   - Grafik görselleştirme

### Algoritma Detayları

#### Context Switch (Bağlam Değiştirme)
- İşlem değiştiğinde CS maliyeti uygulanır
- Varsayılan: 1 zaman birimi
- Ayarlanabilir parametre

#### Quantum (Zaman Dilimi)
- Sadece Round Robin için geçerlidir
- Varsayılan: 2 zaman birimi
- Küçük quantum: Daha fazla context switch
- Büyük quantum: FCFS'ye yaklaşır

### Performans Metrikleri

- **Bekleme Süresi (Waiting Time)**: İşlemin hazır kuyruğunda beklediği toplam süre
  ```
  Waiting Time = Finish Time - Arrival Time - Burst Time
  ```

- **Dönüş Süresi (Turnaround Time)**: İşlemin sisteme girişinden çıkışına kadar geçen süre
  ```
  Turnaround Time = Finish Time - Arrival Time
  ```

## 📊 Ekran Görüntüleri ve Özellikler

### Ana Ekran Özellikleri

- **Üst Kontrol Paneli:**
  - Senaryo seçici
  - Manuel işlem ekleme
  - Algoritma ve parametre ayarları
  - Simülasyon kontrol butonları

- **Sol Görselleştirme Alanı:**
  - CPU donanım görselleştirmesi
  - Hazır kuyruğu animasyonu
  - Gantt diyagramı (zaman çizelgesi)

- **Sağ İstatistik Paneli:**
  - İşlem listesi tablosu
  - Simülasyon sonuçları
  - Performans karşılaştırma grafiği

### Bilimsel Test Modülü Özellikleri

- 3 algoritmanın aynı anda seçilmesi
- 30 iterasyonlu Monte Carlo simülasyonu
- İstatistiksel analiz çıktıları
- Performans sıralaması
- T-Test sonuçları ve anlamlılık değerlendirmesi

## 💡 Geliştirici Notları

### Senaryo Açıklamaları

1. **Normal / Dengeli Senaryo:**
   - 4 işlem
   - Dengeli varış ve burst time dağılımı
   - Genel amaçlı test için uygun

2. **Konvoy Etkisi Senaryosu:**
   - FCFS algoritmasının zayıf yönünü gösterir
   - Uzun bir işlem kısa işlemleri bloklar
   - SRTF ve RR bu durumda daha iyi performans gösterir

3. **Büyük Test (30 İşlem):**
   - Stres testi için tasarlanmıştır
   - Yüksek yük simülasyonu
   - Gerçek dünya senaryolarına yakın

### İyileştirme Önerileri

- [ ] CSV dosyasından veri yükleme özelliği
- [ ] Daha fazla zamanlama algoritması ekleme (Priority, SJF, vb.)
- [ ] Sonuçları dosyaya kaydetme
- [ ] Daha detaylı istatistiksel analiz (ANOVA, vb.)
- [ ] Çoklu CPU desteği
- [ ] İşlem öncelik seviyeleri

### Bilinen Sınırlamalar

- Maksimum işlem sayısı: Sınırsız (ancak performans etkilenebilir)
- Animasyon hızı: Sabit (12ms per frame)
- CSV formatı: Sadece belirli format desteklenir

## 📝 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## 👨‍💻 Geliştirici

İşletim Sistemleri Dersi Projesi

---

**Not:** Bu uygulama, işletim sistemleri dersinde öğrenilen CPU zamanlama algoritmalarını görselleştirmek ve karşılaştırmak amacıyla geliştirilmiştir. Gerçek sistem performansı farklılık gösterebilir.

