from flask import Flask, session, redirect, url_for, render_template, request
from markupsafe import Markup

app = Flask(__name__, static_folder='static')
app.secret_key = '850457ba6a2f8a18beec9463f57515bd'

daftarGejala = {
    'G01': 'Mual pada perut',
    'G02': 'Nyeri di ulu hati',
    'G03': 'Perut kembung',
    'G04': 'Sendawa berlebih',
    'G05': 'Sulit tidur',
    'G06': 'Anemia',
    'G07': 'BAB berwarna hitam',
    'G08': 'Sering Cegukan',
    'G09': 'Sakit tenggorokan',
    'G10': 'Mudah merasa kenyang',
    'G11': 'Kadar gula darah tidak terkontrol',
    'G12': 'Asam dan pahit pada mulut',
    'G13': 'Muntah darah',
    'G14': 'BAB Berdarah',
    'G15': 'Penurunan berat badan',
    'G16': 'Diare Kronis',
    'G17': 'Kelelahan / Lemas',
    'G18': 'Nyeri atau Ketidaknyamanan di Perut Bagian Atas',
    'G19': 'Dada terasa seperti terbakar',
    'G20': 'Sulit menarik napas',
    'G21': 'Muntah',
    'G22': 'Sakit perut',
    'G23': 'Bau mulut',
    'G24': 'Suara serak',
    'G25': 'Tidak bisa menghabiskan makanan dalam porsi banyak',
    'G26': 'Demam',
    'G27': 'Sakit kepala',
    'G28': 'Nyeri otot dan sendi',
    'G29': 'Tidak nafsu makan'
}

daftarPenyakit = {
    'A01': 'Tukak Lambung',
    'A02': 'Gastroparesis',
    'A03': 'GERD (Gastroesophageal Reflux Disease)',
    'A04': 'Gastritis',
    'A05': 'Kanker lambung',
    'A06': 'Sindrom Dispepsia',
    'A07': 'Maag',
    'A08': 'Gastroentritis',
}

solusiPenyakit = {
    'S01': 'Memperbanyak konsumsi sayur, biji-bijian, dan buah yang mengandung vitamin A dan C; Mengonsumsi makanan yang mengandung probiotik; Hindari makanan pedas, asam, dan berlemak; Berhenti merokok; Hindari alkohol; Mengelola stress dengan baik; Istirahat yang cukup.',
    'S02': 'Makan dalam porsi kecil dan sering; Hindari makanan tinggi serat dan lemak; Mengkonsumsi makanan lunak atau cair; Mengunyah makanan hingga halus; Mengonsumsi minuman dengan kandungan gula dan garam yang cukup; Tidak mengonsumsi minuman bersoda; Tidak merokok; Tidak langsung berbaring hingga 2 jam setelah makan.',
    'S03': 'Makan dalam porsi kecil dan sering; hindari makanan pedas, berlemak, dan asam; Hindari makan sebelum tidur; Menurunkan berat badan jika kelebihan berat badan; Menghindari penggunaan pakaian ketat; Tidak merokok; Tidak mengonsumsi minuman alkohol; Tidur dengan posisi menyamping ke kiri atau menggunakan bantal tambahan; Mengonsumsi obat antasida.',
    'S04': 'Menjaga kehigienisan lingkungan dan makanan yang dikonsumsi; Makan dalam porsi kecil dan sering; Hindari makanan pedas, berlemak, dan asam; Tidak berbaring setelah makan, minimal tunggu 2-3 jam setelah makan; Mengelola stres dengan teknik relaksasi; Hindari alkohol dan merokok; Menghindari konsumsi obat pereda nyeri tanpa resep dokter.',
    'S05': 'Operasi; Kemoterapi; Dukungan nutrisi untuk menjaga berat badan dan kesehatan; Konseling untuk dukungan emosional dan psikologis; Radioterapi; Terapi target.',
    'S06': 'Mengonsumsi antasida; Penghambat pompa proton (PPI) atau H2-receptor antagonists; Menghindari makanan pemicu gejala seperti makanan berlemak, pedas, atau asam; Mengurangi stress atau kecemasan',
    'S07': 'Kurangi makanan berlemak dan pedas; Kurangi konsumsi minuman beralkohol dan berkafein, Tidur setidaknya selama 7 jam setiap malam; Berolahraga secara teratur dan berhenti merokok.',
    'S08': 'memperbanyak minum air putih dan mengonsumsi makanan bernutrisi; dianjurkan untuk makan dalam porsi kecil namun sering; hindari mengonsumsi susu, yogurt, kopi, alkohol, keju, serta makanan pedas, berserat tinggi, atau tinggi lemak; mengonsumsi oralit',
}

rules = {
    'A01': {'gejala': ['G01', 'G21', 'G02', 'G03', 'G04', 'G19', 'G10', 'G15', 'G20', 'G17'], 'solusi': 'S01'},
    'A02': {'gejala': ['G01', 'G21', 'G02', 'G19', 'G22', 'G11', 'G03', 'G10', 'G15'], 'solusi': 'S02'},
    'A03': {'gejala': ['G19', 'G01', 'G21', 'G23', 'G24', 'G02', 'G03', 'G05', 'G09', 'G12'], 'solusi': 'S03'},
    'A04': {'gejala': ['G02', 'G03', 'G01', 'G21', 'G10', 'G07', 'G13'], 'solusi': 'S04'},
    'A05': {'gejala': ['G01', 'G02', 'G03', 'G04', 'G06', 'G13', 'G14', 'G15', 'G10', 'G07', 'G17'], 'solusi': 'S05'},
    'A06': {'gejala': ['G10', 'G20', 'G25', 'G03'], 'solusi': 'S06'},
    'A07': {'gejala': ['G02', 'G03', 'G10', 'G04', 'G12', 'G19', 'G01'], 'solusi': 'S07'},
    'A08': {'gejala': ['G26', 'G27', 'G01', 'G22', 'G28', 'G29'], 'solusi': 'S08'},
}

def evaluate_gejala(gejala_list):
    for diagnosis, rule in rules.items():
        if all(gejala in gejala_list for gejala in rule['gejala']):
            return diagnosis
    return None

# ROUTE WEBSITE

# INDEX
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# TUKAK LAMBUNG
@app.route('/tukaklambung')
def tukak_lambung():
    return render_template('tukak.html')

# GASTROPARESIS
@app.route('/gastroparesis')
def gastroparesis():
    return render_template('gastroparesis.html')

# GERD
@app.route('/gerd')
def gerd():
    return render_template('gerd.html')

# GASTRITIS
@app.route('/gastritis')
def gastritis():
    return render_template('gastritis.html')

# KANKER LAMBUNG
@app.route('/kanker')
def kanker_lambung():
    return render_template('kanker.html')

# SINDROM DISPEPSIA
@app.route('/dispepsia')
def sindrom_dispepsia():
    return render_template('dispepsia.html')

# MAAG
@app.route('/maag')
def maag():
    return render_template('maag.html')

# GASTROENTERITIS
@app.route('/gastroentritis')
def gastroentritis():
    return render_template('gastroentritis.html')


@app.route('/identitas', methods=['POST', 'GET'])
def identitas():
    if request.method == 'POST':
        # Ambil data dari form
        nama_lengkap = request.form.get('nama_lengkap')
        tanggal_lahir = request.form.get('tanggal_lahir')
        no_handphone = request.form.get('no_handphone')
        tanggal_diagnosa = request.form.get('tanggal_diagnosa')
        alamat = request.form.get('alamat')
        
        # Validasi data
        if not all([nama_lengkap, tanggal_lahir, no_handphone, tanggal_diagnosa, alamat]):
            return render_template('identitas.html', error="Harap isi semua field")

        # Simpan data di sesi
        session['nama_lengkap'] = nama_lengkap
        session['tanggal_lahir'] = tanggal_lahir
        session['no_handphone'] = no_handphone
        session['tanggal_diagnosa'] = tanggal_diagnosa
        session['alamat'] = alamat

        # Debugging: Print data session untuk memastikan tersimpan
        print(session)

        # Arahkan ke form diagnosis
        return redirect(url_for('form_diagnosis'))

    return render_template('identitas.html')


@app.route('/form', methods=['POST', 'GET'])
def form_diagnosis():
    if request.method == 'POST':
        name = request.form.get('nama_lengkap')
        session['nama_lengkap'] = name
        tanggal_lahir = request.form.get('tanggal_lahir')
        session['tanggal_lahir'] = tanggal_lahir
        no_handphone = request.form.get('no_handphone')
        session['no_handphone'] = no_handphone
        tanggal_diagnosa = request.form.get('tanggal_diagnosa')
        session['tanggal_diagnosa'] = tanggal_diagnosa
        alamat = request.form.get('alamat')
        session['alamat'] = alamat
    questions = daftarGejala
    return render_template('form.html', questions=questions)



@app.route('/hasil', methods=['POST'])
def hasil_diagnosis():
    
    if request.method == 'POST':
        logs = []

        # Loop through all the gejala and check if they are selected ('ya')
        for key in daftarGejala.keys():
            pilihan = request.form.get(key)
            if pilihan == 'ya':
                logs.append(key)

        # Save the selected gejala in the session
        session['logs'] = logs

        # Evaluate the selected gejala to determine the diagnosis
        diagnosis = evaluate_gejala(logs)
        if diagnosis:
            # If a diagnosis is found, get the disease and solution
            terjangkitPenyakit = daftarPenyakit[diagnosis]
            solusi_id = rules[diagnosis]['solusi']
            solusiPenyakitnya = solusiPenyakit[solusi_id]
            return render_template("hasil.html", 
                                   terjangkitPenyakit=terjangkitPenyakit, 
                                   solusiPenyakitnya=solusiPenyakitnya,
                                   show_modal=True)  # Add flag to trigger modal

        # If no diagnosis can be determined
        terjangkitPenyakit = "Maaf, sistem kami belum dapat menentukan penyakit Anda, periksakan ke dokter untuk mendapatkan hasil diagnosa yang lebih akurat."
        return render_template("hasil.html", 
                               terjangkitPenyakit=terjangkitPenyakit,
                               show_modal=True)  # Add flag to trigger modal

    return redirect(url_for('form_diagnosis'))
    

if __name__ == '__main__':
    app.run(debug=True)
