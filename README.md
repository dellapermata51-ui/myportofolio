# Portofolio Pribadi — Della Permata Prasilda

# Tugas 1
## Deskripsi Proyek
Saat ini website berupa halaman statis (murni HTML5 dan CSS3) yang menampilkan:
- Profile: data diri (nama, NPM, program studi, foto, bio, tautan sosial media).
- Experience: riwayat pengalaman organisasi dan kepanitiaan, ditampilkan dalam bentuk timeline.

## Pertanyaan Reflektif
### Tugas 1
1. Ya, saya menggunakan beberapa elemen semantik HTML5 seperti `<section>` untuk membagi konten website berdasarkan bagian, seperti About dan Experience. Penggunaan elemen semantik membantu saya membuat struktur HTML yang lebih terorganisir dan mudah dipahami, baik ketika melakukan pengembangan maupun ketika ingin melakukan perubahan pada bagian tertentu. Dengan struktur yang jelas, setiap bagian pada static web dapat memiliki fungsi dan konteksnya masing-masing.
2. Tantangan utama yang saya temukan saat membuat website responsive adalah menyesuaikan ukuran dan posisi elemen agar tetap nyaman dilihat pada layar yang lebih kecil. Beberapa elemen yang terlihat proporsional di desktop menjadi terlalu besar atau terlalu berdempetan ketika dibuka melalui mobile. Untuk mengatasinya, saya melihat kembali struktur setiap bagian dan menentukan elemen yang paling penting untuk tetap ditampilkan terlebih dahulu. Saya kemudian menyesuaikan ukuran font, spacing, lebar container, serta mengubah beberapa layout menjadi lebih sederhana agar konten tetap mudah dibaca di mobile.
3. Karena website yang dibuat masih berupa static web, informasi di dalamnya masih perlu diubah secara langsung melalui kode ketika terdapat perubahan. Hal ini membuat pengelolaan konten menjadi kurang fleksibel, terutama jika jumlah proyek atau pengalaman yang ingin ditampilkan semakin banyak. Pada iterasi selanjutnya, saya ingin menambahkan fungsionalitas dinamis, seperti mengambil data proyek atau pengalaman dari database sehingga konten dapat diperbarui tanpa harus mengubah struktur HTML secara manual.

## AI Disclosure
- Dalam pengerjaan tugas ini, saya menggunakan Claude sebagai alat bantu selama proses pengerjaan. Penggunaan AI tidak digunakan untuk membuat keseluruhan proyek secara otomatis, melainkan sebagai pendamping ketika saya mengalami kesulitan atau membutuhkan sudut pandang lain dalam menyelesaikan tugas.
- Setelah mendapatkan saran dari AI, saya tetap membaca, memahami, dan menyesuaikan hasilnya dengan kebutuhan proyek sebelum menggunakannya.
- Saya menyadari bahwa AI tidak selalu memberikan jawaban yang tepat atau sesuai dengan kebutuhan proyek. Oleh karena itu, setiap saran dari Claude tetap saya verifikasi dengan mencoba kode secara langsung dan menyesuaikannya dengan materi serta instruksi tugas. Dengan demikian, AI dalam proyek ini berperan sebagai alat bantu belajar dan pemecahan masalah, bukan sebagai pengganti proses pengerjaan dan pemahaman saya terhadap proyek.
- Prompt yang saya gunakan:
"Tolong jelaskan fungsi dari kode berikut per bagian supaya saya bisa memahami cara kerjanya."
"Saya mencoba menyelesaikan masalah ini dengan cara berikut. Tolong cek apakah logika saya sudah benar dan jelaskan bagian yang perlu diperbaiki."



# TUGAS 2
## Deskripsi Proyek
Proyek ini merupakan pengembangan lanjutan dari website portofolio pribadi, yang sebelumnya berupa halaman statis (murni HTML5 dan CSS3), menjadi aplikasi web dinamis berbasis Django. Data yang sebelumnya ditulis langsung di HTML kini disimpan dalam model dan database, lalu ditampilkan melalui view dan template secara dinamis. Website ini terdiri atas beberapa halaman:
- Profile: data diri (nama, NPM, program studi, foto, bio, tautan sosial media), yang tetap ditulis statis di template karena bersifat identitas tetap.
- Experience: riwayat pengalaman organisasi dan kepanitiaan, kini diambil dari model `Experience` dan ditampilkan dalam bentuk timeline, lengkap dengan kondisi tampilan ketika data kosong.
- Education: riwayat pendidikan, diambil dari model `Education`.
- Skills: daftar keahlian, diambil dari model `Skill`.

## Pertanyaan Reflektif
### Tugas 2
1. Saat membuka halaman portofolio, browser akan mengirim request ke server. Setelah itu, Django akan mengecek urls.py pada proyek sebagai pintu masuk utama. Biasanya, urls.py tersebut akan mengarahkan request ke urls.py yang ada di aplikasi main menggunakan include(). Selanjutnya, Django mencocokkan URL yang diminta dengan view yang sesuai. View kemudian mengambil data dari model menggunakan ORM, misalnya Experience.objects.all(), yang nantinya mengambil data dari database. Data tersebut dimasukkan ke dalam context dan dikirim ke template menggunakan render(). Setelah itu, template menggunakan Django Template Language seperti {% for %} dan {{ }} untuk menampilkan data tersebut menjadi HTML. HTML yang sudah jadi kemudian dikirim kembali ke browser dan ditampilkan kepada pengguna.
2. Data sebaiknya disimpan di model karena lebih mudah untuk dikelola dan diubah. Data tersebut bisa ditambah, diubah, atau dihapus melalui admin panel, shell, atau form tanpa harus mengubah kode program dan melakukan deploy ulang. Kalau data ditulis langsung di template, setiap ada perubahan kita harus mengedit file HTML secara manual. Hal ini juga bisa membuat kode menjadi lebih berantakan, terutama kalau jumlah datanya semakin banyak. Jadi, menyimpan data di model membuat aplikasi lebih rapi, mudah dikelola, dan lebih mudah dikembangkan ke depannya.
3. makemigrations digunakan untuk membuat file yang berisi catatan atau rencana perubahan pada struktur database berdasarkan perubahan yang kita buat di models.py. Perintah ini belum mengubah database secara langsung. Setelah itu, migrate digunakan untuk menerapkan perubahan tersebut ke database yang sebenarnya. Contohnya, jika kita mengubah field started_at dari auto_now_add=True menjadi field yang bisa diisi secara manual, kita perlu menjalankan makemigrations terlebih dahulu agar Django membuat file migrasi yang mencatat perubahan tersebut. Setelah itu, kita menjalankan migrate supaya perubahan tersebut benar-benar diterapkan pada tabel di database.

## AI Diclosure
- Dalam pengerjaan tugas ini, saya menggunakan Claude sebagai alat bantu selama proses pengerjaan. Penggunaan AI tidak digunakan untuk membuat keseluruhan proyek secara otomatis, melainkan sebagai pendamping ketika saya mengalami kesulitan atau membutuhkan sudut pandang lain dalam menyelesaikan tugas, khususnya dalam memahami alur MVT Django (model, view, template) dan proses migrasi database.
- Setelah mendapatkan saran dari AI, saya tetap membaca, memahami, dan menyesuaikan hasilnya dengan kebutuhan proyek sebelum menggunakannya, termasuk menyesuaikan nama field model, struktur template, dan tampilan CSS dengan desain yang sudah saya buat sebelumnya.
- Saya menyadari bahwa AI tidak selalu memberikan jawaban yang tepat atau sesuai dengan kebutuhan proyek. Oleh karena itu, setiap saran dari Claude tetap saya verifikasi dengan mencoba kode secara langsung di terminal maupun browser, memeriksa hasilnya, dan menyesuaikannya dengan materi serta instruksi tugas. Dengan demikian, AI dalam proyek ini berperan sebagai alat bantu belajar dan pemecahan masalah, bukan sebagai pengganti proses pengerjaan dan pemahaman saya terhadap proyek.
- Prompt yang saya gunakan:
"Tolong jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan diterima proyek hingga data ditampilkan di browser."
"Mengapa data untuk bagian portofolio sebaiknya disimpan di model dan tidak ditulis langsung di template? Jelaskan dampaknya terhadap pemeliharaan aplikasi."
"Apa perbedaan fungsi makemigrations dan migrate pada Django? Berikan contoh perubahan model yang mengharuskan menjalankan kedua perintah tersebut."



# TUGAS 3
## Deskripsi Proyek
Proyek ini merupakan pengembangan lanjutan dari website portofolio pribadi berbasis Django. Pada tugas ini, dilakukan refactoring pada template HTML dengan menerapkan konsep template inheritance menggunakan extends terhadap template utama, sehingga struktur HTML yang sama dapat digunakan kembali secara lebih efisien. Selain itu, ditambahkan fitur pengelolaan data Education melalui ModelForm, yang memungkinkan pengguna untuk menambahkan, mengubah, dan menghapus data pendidikan secara dinamis. Data pendidikan disimpan dalam database melalui model Django, kemudian disajikan dalam format JSON melalui fungsi view dengan proses serialisasi. Data JSON tersebut selanjutnya diambil dan dideserialisasi untuk ditampilkan kembali pada halaman web. Dengan demikian, website portofolio tidak hanya menampilkan informasi secara dinamis, tetapi juga menyediakan fitur pengelolaan data pendidikan melalui form yang terintegrasi dengan database.

## Pertanyaan Reflektif
### Tugas 3
1. ModelForm digunakan karena dapat membuat form dan validasi secara otomatis berdasarkan model yang ada di Django, sehingga kita tidak perlu menulis semua field dan validasi secara manual. ModelForm juga memudahkan penyimpanan data ke database menggunakan is_valid() dan save(). Sementara itu, {% csrf_token %} digunakan untuk melindungi form dari serangan CSRF, yaitu ketika pihak lain mencoba mengirimkan data tanpa izin pengguna. Jika token tidak ada atau tidak valid, Django akan menolak request tersebut.

2. JSON lebih banyak digunakan dalam pengembangan web modern karena formatnya lebih sederhana, ringkas, dan mudah dibaca dibandingkan XML. JSON juga mudah diproses oleh JavaScript dan dapat digunakan untuk pertukaran data antara backend dan frontend, sehingga cocok untuk pengembangan aplikasi web maupun mobile.

3. Alurnya dimulai ketika browser mengirim request ke endpoint JSON. View kemudian mengambil data portofolio dari model Django, misalnya Education.objects.all(). Data tersebut perlu di-serialize agar objek model Django dapat diubah menjadi format JSON yang bisa dikirim melalui HTTP dan dibaca oleh client. Setelah itu, JSON dikembalikan melalui HttpResponse dengan content_type="application/json".

## AI Diclosure
- Dalam pengerjaan tugas ini, saya menggunakan Claude sebagai alat bantu selama proses pengembangan proyek. AI digunakan sebagai pendamping ketika saya mengalami kesulitan dalam memahami dan menerapkan konsep yang dibahas pada Tutorial 03, khususnya penggunaan `ModelForm`, template inheritance dengan `extends`, serta proses penyajian data dalam format JSON dan deserialisasi data pada Django.
- Penggunaan AI tidak ditujukan untuk membuat keseluruhan proyek secara otomatis. Saya tetap mengerjakan dan mengembangkan kode secara mandiri, sementara Claude membantu memberikan penjelasan, saran perbaikan, dan alternatif solusi ketika saya mengalami kendala dalam mengimplementasikan fitur create, update, delete, dan JSON Data Delivery pada bagian Education.
- Setelah memperoleh saran dari AI, saya tetap membaca, memahami, dan menyesuaikan hasilnya dengan kebutuhan proyek. Penyesuaian tersebut mencakup struktur `ModelForm`, fungsi view, penggunaan template utama, serta tampilan form dan halaman Education agar tetap sesuai dengan desain portofolio yang telah saya buat sebelumnya.
- Saya menyadari bahwa saran dari AI tidak selalu tepat atau langsung sesuai dengan struktur proyek yang saya miliki. Oleh karena itu, setiap saran tetap saya verifikasi dengan mencoba kode secara langsung melalui terminal dan browser, memeriksa hasilnya, serta memperbaiki error yang ditemukan. Dengan demikian, AI berperan sebagai alat bantu belajar dan pemecahan masalah, bukan sebagai pengganti proses pengerjaan dan pemahaman saya terhadap proyek.
- Prompt yang saya gunakan:
"Jelaskan cara kerja ModelForm pada Django dan bagaimana cara menghubungkannya dengan model Education yang sudah ada di proyek portofolio saya. Saya ingin memahami alurnya sebelum mengimplementasikannya."
"Saya ingin menambahkan fitur create, update, dan delete untuk data Education menggunakan Django. Bisa jelaskan alur dan langkah-langkah yang perlu saya pahami agar bisa mengimplementasikannya sendiri?"
"Saya mengalami kendala saat mengimplementasikan form atau menampilkan data Education di proyek Django saya. Tolong bantu saya memahami kemungkinan penyebabnya dan berikan arahan untuk memperbaikinya tanpa langsung membuat seluruh kode proyek."



# TUGAS 4
## Deskripsi Proyek
Pada tugas ini, website portofolio dikembangkan dengan menambahkan sistem autentikasi, session, cookie, dan otorisasi. Fitur registrasi, login, dan logout diimplementasikan menggunakan sistem autentikasi bawaan Django (`UserCreationForm` dan `AuthenticationForm`), lengkap dengan status login pada navbar. Website juga menyimpan cookie kustom `last_login` yang mencatat waktu terakhir seorang pengguna berhasil login, serta ditampilkan pada halaman profil.

Selanjutnya, diterapkan sistem otorisasi dengan empat peran: pengunjung tanpa login (hanya dapat membaca data), pengguna biasa (dapat membaca data serta memberi/membatalkan star), Editor (memiliki hak pengguna biasa dan dapat mengubah data, tetapi tidak dapat membuat atau menghapus), serta pemilik portofolio/superuser (memiliki seluruh hak akses). Peran Editor diimplementasikan menggunakan Django Group, dengan pemeriksaan hak akses dilakukan di sisi server pada setiap fungsi `create`, `update`, dan `delete` di keempat bagian portofolio (Experience, Education, Skill, Project), serta disertai penyembunyian tombol aksi pada template bagi pengguna yang tidak berhak.

Fitur interaktif berupa pemberian star pada Project juga ditambahkan menggunakan relasi `ManyToManyField` ke model `User` bawaan Django, dengan fungsi `toggle_star` yang menangani penambahan dan pembatalan star melalui metode POST dan `{% csrf_token %}`. Selain itu, bagian Experience yang sebelumnya hanya menampilkan data kini dilengkapi dengan fitur create, update, delete, dan pencarian, mengikuti pola yang sudah diterapkan pada Education di Tugas 3, sehingga seluruh bagian portofolio memiliki fungsionalitas pengelolaan data yang konsisten. Endpoint JSON dari tugas-tugas sebelumnya tetap dipastikan berfungsi tanpa membocorkan informasi sensitif, seperti ID pengguna pada data star, dengan memanfaatkan `use_natural_foreign_keys=True`.

## AI Disclosure
- Dalam pengerjaan tugas ini, saya menggunakan Claude sebagai alat bantu selama proses pengembangan proyek. AI digunakan sebagai pendamping ketika saya mengalami kesulitan dalam memahami dan menerapkan konsep yang dibahas pada Tutorial 04, khususnya mengenai autentikasi bawaan Django, perbedaan session dan cookie, mekanisme CSRF, serta penerapan otorisasi berjenjang menggunakan Django Group pada Individual Assignment 4.
- Penggunaan AI tidak ditujukan untuk membuat keseluruhan proyek secara otomatis. Saya tetap mengerjakan dan mengembangkan kode secara mandiri, sementara Claude membantu memberikan penjelasan, menelusuri penyebab error yang saya temui (seperti `IntegrityError` pada saat menambahkan proyek baru dan kesalahan konfigurasi `CSRF_TRUSTED_ORIGINS`), serta memberikan arahan dalam menerapkan pola otorisasi peran Editor agar konsisten dengan struktur kode yang sudah saya bangun sejak Tugas 3.
- Setelah memperoleh saran dari AI, saya tetap membaca, memahami, dan menyesuaikan hasilnya dengan kebutuhan proyek. Penyesuaian tersebut mencakup penyesuaian fungsi view, struktur pemeriksaan hak akses, tampilan tombol pada template sesuai peran pengguna, serta pengujian ulang melalui `python manage.py test` dan pengujian manual pada browser untuk memastikan setiap peran (pengunjung, pengguna biasa, editor, pemilik) berperilaku sesuai checklist tugas.
- Saya menyadari bahwa saran dari AI tidak selalu tepat atau langsung sesuai dengan struktur proyek yang saya miliki, sehingga setiap saran tetap saya verifikasi dengan menjalankan kode secara langsung, memeriksa hasilnya di database dan browser, serta memperbaiki bagian yang belum sesuai sebelum saya commit ke Git. Dengan demikian, AI berperan sebagai alat bantu belajar dan pemecahan masalah, bukan sebagai pengganti proses pengerjaan dan pemahaman saya terhadap proyek.
- Prompt yang saya gunakan:
"Saya mendapatkan IntegrityError saat menambahkan proyek baru di Django. Tolong bantu saya menelusuri penyebabnya berdasarkan riwayat migration yang saya miliki, tanpa langsung menghapus data saya."
"Saya ingin menerapkan peran Editor menggunakan Django Group yang bisa mengubah data tapi tidak bisa membuat atau menghapus. Tolong jelaskan bagaimana cara memeriksa keanggotaan grup tersebut di view dan template Django saya."
"Tolong periksa apakah implementasi autentikasi, session, dan cookie pada proyek saya sudah sesuai dengan modul Tutorial 04, dan jelaskan bagian mana saja yang masih perlu diperbaiki."



# TUGAS 5
## Deskripsi Proyek
Pada tugas ini, website portofolio dikembangkan dengan menambahkan interaktivitas JavaScript pada bagian **Education**, mengikuti pola halaman Projects pada Tutorial 05. Data Education tidak lagi langsung ditampilkan dari HTML, tetapi diambil menggunakan `fetch()` dari endpoint `/api/education/`. Fitur pencarian juga dilakukan secara AJAX dengan **debouncing 300 ms** dan `AbortController` agar request yang tidak diperlukan dapat dibatalkan.

Form tambah Education dipindahkan ke dalam modal dan dikirim menggunakan Fetch API. Data divalidasi melalui `EducationForm`, dengan akses tambah data yang hanya diberikan kepada **superuser**. Sistem juga menggunakan CSRF token serta perlindungan XSS dengan `escapeHtml` dan `strip_tags`. Selain itu, fitur **star** pada Education menggunakan `ManyToManyField` untuk menyimpan pengguna yang memberikan star beserta jumlah star-nya.

Endpoint yang digunakan:
* `GET /api/education/?q=` untuk mengambil dan mencari data Education.
* `POST /education/add-ajax/` untuk menambahkan data melalui AJAX.
* `POST /education/<id>/star/` untuk memberi atau membatalkan star.

Halaman Projects, Experience, dan Skills tidak diubah. Fitur edit dan hapus Education tetap menggunakan fitur yang sudah tersedia sebelumnya.


## Pertanyaan Reflektif
### Tugas 5
1. Debouncing. Debouncing adalah teknik untuk menunda fungsi sampai pengguna berhenti melakukan suatu aktivitas dalam waktu tertentu. Pada fitur pencarian AJAX, debouncing mencegah setiap ketikan mengirim request ke server. Pada proyek ini digunakan jeda **300 ms**, sehingga request hanya dikirim setelah pengguna berhenti mengetik. Saya juga menggunakan `AbortController` untuk membatalkan request lama yang sudah tidak diperlukan.

2. `fetch()` dan `await`, `fetch()` mengembalikan **Promise**, sehingga data dari server belum langsung tersedia. `await` digunakan untuk menunggu Promise selesai sebelum kode dilanjutkan. Tanpa `await`, kode bisa berjalan sebelum data diterima dan menyebabkan hasil tidak sesuai. Penggunaan `await` juga memudahkan penanganan error dengan `try/catch`.

3. XSS (Cross-Site Scripting), XSS adalah serangan ketika data yang dimasukkan pengguna mengandung skrip berbahaya dan kemudian dijalankan di browser. Pada template Django, data biasanya otomatis di-escape, tetapi pada AJAX kita membuat HTML sendiri menggunakan JavaScript sehingga perlu melakukan escaping secara manual. Pada proyek ini digunakan `escapeHtml` di sisi JavaScript dan `strip_tags` di sisi server sebagai perlindungan tambahan.


## AI Disclosure
- Dalam pengerjaan tugas ini, saya menggunakan Claude sebagai alat bantu ketika mengalami kesulitan dalam memahami instruksi dan mencari solusi teknis. AI membantu memberikan arahan terkait implementasi fitur Education, AJAX, unit test, dan README. Saya tetap menyesuaikan seluruh saran dengan struktur kode proyek yang saya kerjakan.
- Saya menggunakan AI secara bertahap berdasarkan checklist tugas, kemudian memeriksa, menyesuaikan, dan menguji hasilnya sendiri. Perubahan juga saya kerjakan dan commit secara bertahap agar proses pengerjaan tetap terdokumentasi di Git.
- Beberapa saran awal AI tidak sesuai dengan struktur proyek saya. Setelah saya memberikan kode yang sebenarnya, saya menyesuaikan kembali bagian yang diperlukan. Saya juga memperbaiki error pada unit test, template, serta menyesuaikan test lama yang terdampak perubahan AJAX.
- Prompt yang saya gunakan:
“Saya sedang membuat fitur Education menggunakan fetch() dan JsonResponse. Bisa jelaskan bagaimana alur data dari Django ke JavaScript, dan bantu cek kenapa data yang saya terima belum tampil sesuai yang diharapkan?”
“Saya ingin membuat fitur pencarian AJAX dengan debouncing dan AbortController. Bisa jelaskan cara kerjanya dan bantu cek bagian kode ini jika request atau hasil pencariannya masih error?”
“Saya sudah menggunakan innerHTML untuk menampilkan data dari API. Bisa jelaskan risiko XSS pada kode ini dan bagaimana cara menggunakan escapeHtml atau strip_tags dengan benar?”