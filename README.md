# Portofolio Pribadi — Della Permata Prasilda

# Deskripsi Proyek
Saat ini website berupa halaman statis (murni HTML5 dan CSS3) yang menampilkan:
- Profile: data diri (nama, NPM, program studi, foto, bio, tautan sosial media).
- Experience: riwayat pengalaman organisasi dan kepanitiaan, ditampilkan dalam bentuk timeline.

# Pertanyaan Reflektif
### Tugas 1
1. Ya, saya menggunakan beberapa elemen semantik HTML5 seperti `<section>` untuk membagi konten website berdasarkan bagian, seperti About dan Experience. Penggunaan elemen semantik membantu saya membuat struktur HTML yang lebih terorganisir dan mudah dipahami, baik ketika melakukan pengembangan maupun ketika ingin melakukan perubahan pada bagian tertentu. Dengan struktur yang jelas, setiap bagian pada static web dapat memiliki fungsi dan konteksnya masing-masing.
2. Tantangan utama yang saya temukan saat membuat website responsive adalah menyesuaikan ukuran dan posisi elemen agar tetap nyaman dilihat pada layar yang lebih kecil. Beberapa elemen yang terlihat proporsional di desktop menjadi terlalu besar atau terlalu berdempetan ketika dibuka melalui mobile. Untuk mengatasinya, saya melihat kembali struktur setiap bagian dan menentukan elemen yang paling penting untuk tetap ditampilkan terlebih dahulu. Saya kemudian menyesuaikan ukuran font, spacing, lebar container, serta mengubah beberapa layout menjadi lebih sederhana agar konten tetap mudah dibaca di mobile.
3. Karena website yang dibuat masih berupa static web, informasi di dalamnya masih perlu diubah secara langsung melalui kode ketika terdapat perubahan. Hal ini membuat pengelolaan konten menjadi kurang fleksibel, terutama jika jumlah proyek atau pengalaman yang ingin ditampilkan semakin banyak. Pada iterasi selanjutnya, saya ingin menambahkan fungsionalitas dinamis, seperti mengambil data proyek atau pengalaman dari database sehingga konten dapat diperbarui tanpa harus mengubah struktur HTML secara manual.

# AI Disclosure
- Dalam pengerjaan tugas ini, saya menggunakan Claude sebagai alat bantu selama proses pengerjaan. Penggunaan AI tidak digunakan untuk membuat keseluruhan proyek secara otomatis, melainkan sebagai pendamping ketika saya mengalami kesulitan atau membutuhkan sudut pandang lain dalam menyelesaikan tugas.
- Setelah mendapatkan saran dari AI, saya tetap membaca, memahami, dan menyesuaikan hasilnya dengan kebutuhan proyek sebelum menggunakannya.
- Saya menyadari bahwa AI tidak selalu memberikan jawaban yang tepat atau sesuai dengan kebutuhan proyek. Oleh karena itu, setiap saran dari Claude tetap saya verifikasi dengan mencoba kode secara langsung dan menyesuaikannya dengan materi serta instruksi tugas. Dengan demikian, AI dalam proyek ini berperan sebagai alat bantu belajar dan pemecahan masalah, bukan sebagai pengganti proses pengerjaan dan pemahaman saya terhadap proyek.
- Prompt yang saya gunakan:
"Tolong jelaskan fungsi dari kode berikut per bagian supaya saya bisa memahami cara kerjanya."
"Saya mencoba menyelesaikan masalah ini dengan cara berikut. Tolong cek apakah logika saya sudah benar dan jelaskan bagian yang perlu diperbaiki."

##################################################################################################################

# Deskripsi Proyek
Proyek ini merupakan pengembangan lanjutan dari website portofolio pribadi, yang sebelumnya berupa halaman statis (murni HTML5 dan CSS3), menjadi aplikasi web dinamis berbasis Django. Data yang sebelumnya ditulis langsung di HTML kini disimpan dalam model dan database, lalu ditampilkan melalui view dan template secara dinamis. Website ini terdiri atas beberapa halaman:
- Profile: data diri (nama, NPM, program studi, foto, bio, tautan sosial media), yang tetap ditulis statis di template karena bersifat identitas tetap.
- Experience: riwayat pengalaman organisasi dan kepanitiaan, kini diambil dari model `Experience` dan ditampilkan dalam bentuk timeline, lengkap dengan kondisi tampilan ketika data kosong.
- Education: riwayat pendidikan, diambil dari model `Education`.
- Skills: daftar keahlian, diambil dari model `Skill`.

# Pertanyaan Reflektif
### Tugas 2
1. Saat membuka halaman portofolio, browser akan mengirim request ke server. Setelah itu, Django akan mengecek urls.py pada proyek sebagai pintu masuk utama. Biasanya, urls.py tersebut akan mengarahkan request ke urls.py yang ada di aplikasi main menggunakan include(). Selanjutnya, Django mencocokkan URL yang diminta dengan view yang sesuai. View kemudian mengambil data dari model menggunakan ORM, misalnya Experience.objects.all(), yang nantinya mengambil data dari database. Data tersebut dimasukkan ke dalam context dan dikirim ke template menggunakan render(). Setelah itu, template menggunakan Django Template Language seperti {% for %} dan {{ }} untuk menampilkan data tersebut menjadi HTML. HTML yang sudah jadi kemudian dikirim kembali ke browser dan ditampilkan kepada pengguna.
2. Data sebaiknya disimpan di model karena lebih mudah untuk dikelola dan diubah. Data tersebut bisa ditambah, diubah, atau dihapus melalui admin panel, shell, atau form tanpa harus mengubah kode program dan melakukan deploy ulang. Kalau data ditulis langsung di template, setiap ada perubahan kita harus mengedit file HTML secara manual. Hal ini juga bisa membuat kode menjadi lebih berantakan, terutama kalau jumlah datanya semakin banyak. Jadi, menyimpan data di model membuat aplikasi lebih rapi, mudah dikelola, dan lebih mudah dikembangkan ke depannya.
3. makemigrations digunakan untuk membuat file yang berisi catatan atau rencana perubahan pada struktur database berdasarkan perubahan yang kita buat di models.py. Perintah ini belum mengubah database secara langsung. Setelah itu, migrate digunakan untuk menerapkan perubahan tersebut ke database yang sebenarnya. Contohnya, jika kita mengubah field started_at dari auto_now_add=True menjadi field yang bisa diisi secara manual, kita perlu menjalankan makemigrations terlebih dahulu agar Django membuat file migrasi yang mencatat perubahan tersebut. Setelah itu, kita menjalankan migrate supaya perubahan tersebut benar-benar diterapkan pada tabel di database.

# AI Diclosure
- Dalam pengerjaan tugas ini, saya menggunakan Claude sebagai alat bantu selama proses pengerjaan. Penggunaan AI tidak digunakan untuk membuat keseluruhan proyek secara otomatis, melainkan sebagai pendamping ketika saya mengalami kesulitan atau membutuhkan sudut pandang lain dalam menyelesaikan tugas, khususnya dalam memahami alur MVT Django (model, view, template) dan proses migrasi database.
- Setelah mendapatkan saran dari AI, saya tetap membaca, memahami, dan menyesuaikan hasilnya dengan kebutuhan proyek sebelum menggunakannya, termasuk menyesuaikan nama field model, struktur template, dan tampilan CSS dengan desain yang sudah saya buat sebelumnya.
- Saya menyadari bahwa AI tidak selalu memberikan jawaban yang tepat atau sesuai dengan kebutuhan proyek. Oleh karena itu, setiap saran dari Claude tetap saya verifikasi dengan mencoba kode secara langsung di terminal maupun browser, memeriksa hasilnya, dan menyesuaikannya dengan materi serta instruksi tugas. Dengan demikian, AI dalam proyek ini berperan sebagai alat bantu belajar dan pemecahan masalah, bukan sebagai pengganti proses pengerjaan dan pemahaman saya terhadap proyek.
- Prompt yang saya gunakan:
"Tolong jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan diterima proyek hingga data ditampilkan di browser."
"Mengapa data untuk bagian portofolio sebaiknya disimpan di model dan tidak ditulis langsung di template? Jelaskan dampaknya terhadap pemeliharaan aplikasi."
"Apa perbedaan fungsi makemigrations dan migrate pada Django? Berikan contoh perubahan model yang mengharuskan menjalankan kedua perintah tersebut."

##################################################################################################################

# Deskripsi Proyek
Proyek ini merupakan pengembangan lanjutan dari website portofolio pribadi berbasis Django. Pada tugas ini, dilakukan refactoring pada template HTML dengan menerapkan konsep template inheritance menggunakan extends terhadap template utama, sehingga struktur HTML yang sama dapat digunakan kembali secara lebih efisien. Selain itu, ditambahkan fitur pengelolaan data Education melalui ModelForm, yang memungkinkan pengguna untuk menambahkan, mengubah, dan menghapus data pendidikan secara dinamis. Data pendidikan disimpan dalam database melalui model Django, kemudian disajikan dalam format JSON melalui fungsi view dengan proses serialisasi. Data JSON tersebut selanjutnya diambil dan dideserialisasi untuk ditampilkan kembali pada halaman web. Dengan demikian, website portofolio tidak hanya menampilkan informasi secara dinamis, tetapi juga menyediakan fitur pengelolaan data pendidikan melalui form yang terintegrasi dengan database.

# Pertanyaan Reflektif
### Tugas 3
1. ModelForm digunakan karena dapat membuat form dan validasi secara otomatis berdasarkan model yang ada di Django, sehingga kita tidak perlu menulis semua field dan validasi secara manual. ModelForm juga memudahkan penyimpanan data ke database menggunakan is_valid() dan save(). Sementara itu, {% csrf_token %} digunakan untuk melindungi form dari serangan CSRF, yaitu ketika pihak lain mencoba mengirimkan data tanpa izin pengguna. Jika token tidak ada atau tidak valid, Django akan menolak request tersebut.

2. JSON lebih banyak digunakan dalam pengembangan web modern karena formatnya lebih sederhana, ringkas, dan mudah dibaca dibandingkan XML. JSON juga mudah diproses oleh JavaScript dan dapat digunakan untuk pertukaran data antara backend dan frontend, sehingga cocok untuk pengembangan aplikasi web maupun mobile.

3. Alurnya dimulai ketika browser mengirim request ke endpoint JSON. View kemudian mengambil data portofolio dari model Django, misalnya Education.objects.all(). Data tersebut perlu di-serialize agar objek model Django dapat diubah menjadi format JSON yang bisa dikirim melalui HTTP dan dibaca oleh client. Setelah itu, JSON dikembalikan melalui HttpResponse dengan content_type="application/json".

# AI Diclosure
- Dalam pengerjaan tugas ini, saya menggunakan Claude sebagai alat bantu selama proses pengembangan proyek. AI digunakan sebagai pendamping ketika saya mengalami kesulitan dalam memahami dan menerapkan konsep yang dibahas pada Tutorial 03, khususnya penggunaan `ModelForm`, template inheritance dengan `extends`, serta proses penyajian data dalam format JSON dan deserialisasi data pada Django.
- Penggunaan AI tidak ditujukan untuk membuat keseluruhan proyek secara otomatis. Saya tetap mengerjakan dan mengembangkan kode secara mandiri, sementara Claude membantu memberikan penjelasan, saran perbaikan, dan alternatif solusi ketika saya mengalami kendala dalam mengimplementasikan fitur create, update, delete, dan JSON Data Delivery pada bagian Education.
- Setelah memperoleh saran dari AI, saya tetap membaca, memahami, dan menyesuaikan hasilnya dengan kebutuhan proyek. Penyesuaian tersebut mencakup struktur `ModelForm`, fungsi view, penggunaan template utama, serta tampilan form dan halaman Education agar tetap sesuai dengan desain portofolio yang telah saya buat sebelumnya.
- Saya menyadari bahwa saran dari AI tidak selalu tepat atau langsung sesuai dengan struktur proyek yang saya miliki. Oleh karena itu, setiap saran tetap saya verifikasi dengan mencoba kode secara langsung melalui terminal dan browser, memeriksa hasilnya, serta memperbaiki error yang ditemukan. Dengan demikian, AI berperan sebagai alat bantu belajar dan pemecahan masalah, bukan sebagai pengganti proses pengerjaan dan pemahaman saya terhadap proyek.
- Prompt yang saya gunakan:
"Jelaskan cara kerja ModelForm pada Django dan bagaimana cara menghubungkannya dengan model Education yang sudah ada di proyek portofolio saya. Saya ingin memahami alurnya sebelum mengimplementasikannya."
"Saya ingin menambahkan fitur create, update, dan delete untuk data Education menggunakan Django. Bisa jelaskan alur dan langkah-langkah yang perlu saya pahami agar bisa mengimplementasikannya sendiri?"
"Saya mengalami kendala saat mengimplementasikan form atau menampilkan data Education di proyek Django saya. Tolong bantu saya memahami kemungkinan penyebabnya dan berikan arahan untuk memperbaikinya tanpa langsung membuat seluruh kode proyek."

