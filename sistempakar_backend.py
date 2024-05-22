from flask import Flask, session, redirect, url_for, render_template, request
from markupsafe import Markup

app = Flask(__name__)
app.secret_key = 'isinya password buat session'
app.static_folder = 'static'

daftarGejala = {
    'G01': 'Mual pada perut ',
    'G02': 'Nyeri di ulu hati ',
    'G03': 'Perut kembung ',
    'G04': 'Sendawa berlebih',
    'G05': 'Sulit tidur ',
    'G06': 'Anemia ',
    'G07': 'BAB berwarna hitam',
    'G08': 'Sering Cegukan ',
    'G09': 'Sakit tenggorokan ',
    'G10': 'Mudah merasa kenyang',
    'G11': 'Kadar gula darah tidak terkontrol ',
    'G12': 'Asam dan pahit pada mulut ',
    'G13': 'Muntah darah ',
    'G14': 'BAB Berdarah ',
    'G15': 'Penurunan berat badan ',
}

daftarPenyakit = {
    'A01': 'Tukak Lambung (Ulkus Peptikum)',
    'A02': 'Gastroparesis',
    'A03': 'GERD (Gastroesophageal Reflux Disease)',
    'A04': 'Gastritis',
    'A05': 'Kanker lambung',
}

solusiPenyakit = {
    'S01': 'Hindari makanan pedas, asam, dan berlemak; berhenti merokok; hindari alkohol.',
    'S02': 'Makan dalam porsi kecil dan sering; hindari makanan tinggi serat dan lemak; mengkonsumsi makanan lunak atau cair.',
    'S03': 'Makan dalam porsi kecil dan sering; hindari makanan pedas, berlemak, dan asam; hindari makan sebelum tidur; Menurunkan berat badan jika kelebihan berat badan.',
    'S04': 'Makan dalam porsi kecil dan sering; hindari makanan pedas, berlemak, dan asam; Mengelola stres dengan teknik relaksasi; hindari alkohol dan merokok.',
    'S05': 'Operasi; kemoterapi; Dukungan nutrisi untuk menjaga berat badan dan kesehatan; konseling untuk dukungan emosional dan psikologis.',
}

rules = {
    'A01': {'gejala': ['G01', 'G02', 'G03', 'G04'], 'solusi': 'S01'},
    'A02': {'gejala': ['G01', 'G02', 'G03', 'G10', 'G15'], 'solusi': 'S02'},
    'A03': {'gejala': ['G01', 'G03', 'G05', 'G09', 'G12'], 'solusi': 'S03'},
    'A04': {'gejala': ['G01', 'G02', 'G07', 'G08'], 'solusi': 'S04'},
    'A05': {'gejala': ['G02', 'G03', 'G06', 'G13', 'G14', 'G15'], 'solusi': 'S05'},
}

def checkGejala():
    pilihan = request.form.get('pilihan')
    if pilihan == 'ya':
        return True
    elif pilihan == 'tidak':
        return False
    else:
        return None

def evaluate_gejala(gejala_list):
    for diagnosis, rule in rules.items():
        if all(gejala in gejala_list for gejala in rule['gejala']):
            return diagnosis
    return None

@app.route('/')
def index():
    session.clear()
    session['gejalaPasien'] = 'G01'
    session['logs'] = []
    return render_template('index.html', link=url_for('index'))

@app.route('/welcome', methods=['POST', 'GET'])
def welcome():
    if request.method == 'POST':
        name = request.form.get('Name')
        session['namaPasien'] = name
        gejalanya = session['gejalaPasien']
        pertanyaan = daftarGejala[gejalanya]
        return render_template("welcome.html", name=name, pertanyaan=pertanyaan, link=url_for('index'))

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        gejala_terjadi = checkGejala()

        if gejala_terjadi is None:
            return redirect(url_for('diagnosa'))

        current_gejala = session['gejalaPasien']
        if gejala_terjadi:
            session['logs'].append(current_gejala)

        diagnosis = evaluate_gejala(session['logs'])
        if diagnosis:
            terjangkitPenyakit = daftarPenyakit[diagnosis]
            solusi_id = rules[diagnosis]['solusi']
            solusiPenyakitnya = "Solusi: " + solusiPenyakit[solusi_id]
            return render_template("result.html", terjangkitPenyakit=terjangkitPenyakit, solusiPenyakitnya=solusiPenyakitnya, awal=url_for('index'))
        
        # Find the next gejala ID
        current_index = list(daftarGejala.keys()).index(current_gejala)
        next_index = current_index + 1
        if next_index >= len(daftarGejala):
            terjangkitPenyakit = "Maaf Sistem kami belum bisa menjawab pertanyaan anda"
            return render_template("result.html", terjangkitPenyakit=terjangkitPenyakit, awal=url_for('index'))
        
        session['gejalaPasien'] = list(daftarGejala.keys())[next_index]
        return redirect(url_for('diagnosa'))

@app.route('/diagnosa', methods=['POST', 'GET'])
def diagnosa():
    name = session['namaPasien']
    pertanyaan = daftarGejala[session['gejalaPasien']]
    return render_template("diagnosa.html", pertanyaan=pertanyaan, name=name, link=url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)










# from flask import Flask, session, redirect, url_for, render_template, request
# from markupsafe import Markup

# app = Flask(__name__)
# app.secret_key = 'isinya password buat session'
# app.static_folder = 'static'

# daftarGejala = [
#     'Mual pada perut ',
#     'Nyeri di ulu hati ',
#     'Perut kembung ',
#     'Sendawa berlebih',
#     'Sulit tidur ',
#     'Anemia ',
#     'BAB berwarna hitam',
#     'Sering Cegukan ',
#     'Sakit tenggorokan ',
#     'Mudah merasa kenyang',
#     'Kadar gula darah tidak terkontrol ',
#     'Asam dan pahit pada mulut ',
#     'Muntah darah ',
#     'BAB Berdarah ',
#     'Penurunan berat badan ',
# ]

# daftarPenyakit = [
#     'Tukak Lambung (Ulkus Peptikum)',
#     'Gastroparesis',
#     'GERD (Gastroesophageal Reflux Disease)',
#     'Gastritis ',
#     'Kanker lambung ',
# ]

# solusiPenyakit = [
#     'Hindari makanan pedas, asam, dan berlemak; berhenti merokok; hindari alkohol.',
#     'Makan dalam porsi kecil dan sering; hindari makanan tinggi serat dan lemak; mengkonsumsi makanan lunak atau cair.',
#     'Makan dalam porsi kecil dan sering; hindari makanan pedas, berlemak, dan asam; hindari makan sebelum tidur; Menurunkan berat badan jika kelebihan berat badan.',
#     'Makan dalam porsi kecil dan sering; hindari makanan pedas, berlemak, dan asam; Mengelola stres dengan teknik relaksasi; hindari alkohol dan merokok.',
#     'Operasi; kemoterapi; Dukungan nutrisi untuk menjaga berat badan dan kesehatan; konseling untuk dukungan emosional dan psikologis.',
# ]

# rules = {
#     'A01': {'gejala': [0, 1, 2, 3]},
#     'A02': {'gejala': [0, 1, 2, 9, 14]},
#     'A03': {'gejala': [0, 2, 4, 8, 11]},
#     'A04': {'gejala': [0, 1, 6, 7]},
#     'A05': {'gejala': [1, 2, 5, 12, 13, 14]},
# }

# def checkGejala():
#     pilihan = request.form.get('pilihan')
#     if pilihan == 'ya':
#         return True
#     elif pilihan == 'tidak':
#         return False
#     else:
#         return None

# def evaluate_gejala(gejala_list):
#     for diagnosis, rule in rules.items():
#         if all(gejala in gejala_list for gejala in rule['gejala']):
#             return diagnosis
#     return None

# @app.route('/')
# def index():
#     session.clear()
#     session['gejalaPasien'] = 0
#     session['logs'] = []
#     return render_template('index.html', link=url_for('index'))

# @app.route('/welcome', methods=['POST', 'GET'])
# def welcome():
#     if request.method == 'POST':
#         name = request.form.get('Name')
#         session['namaPasien'] = name
#         gejalanya = session['gejalaPasien']
#         pertanyaan = daftarGejala[gejalanya]
#         return render_template("welcome.html", name=name, pertanyaan=pertanyaan, link=url_for('index'))

# @app.route('/result', methods=['POST', 'GET'])
# def result():
#     if request.method == 'POST':
#         gejala_terjadi = checkGejala()

#         if gejala_terjadi is None:
#             return redirect(url_for('diagnosa'))

#         current_gejala = session['gejalaPasien']
#         if gejala_terjadi:
#             session['logs'].append(current_gejala)

#         diagnosis = evaluate_gejala(session['logs'])
#         if diagnosis:
#             penyakit_index = list(rules.keys()).index(diagnosis)
#             terjangkitPenyakit = daftarPenyakit[penyakit_index]
#             solusiPenyakitnya = "Solusi: " + solusiPenyakit[penyakit_index]
#             return render_template("result.html", terjangkitPenyakit=terjangkitPenyakit, solusiPenyakitnya=solusiPenyakitnya, awal=url_for('index'))
        
#         session['gejalaPasien'] += 1
#         if session['gejalaPasien'] >= len(daftarGejala):
#             terjangkitPenyakit = "Maaf Sistem kami belum bisa menjawab pertanyaan anda"
#             return render_template("result.html", terjangkitPenyakit=terjangkitPenyakit, awal=url_for('index'))
        
#         return redirect(url_for('diagnosa'))

# @app.route('/diagnosa', methods=['POST', 'GET'])
# def diagnosa():
#     name = session['namaPasien']
#     pertanyaan = daftarGejala[session['gejalaPasien']]
#     return render_template("diagnosa.html", pertanyaan=pertanyaan, name=name, link=url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)










# from flask import Flask, session, redirect, url_for, render_template, request
# from markupsafe import Markup

# app = Flask(__name__)
# app.secret_key = 'isinya password buat session'
# app.static_folder = 'static'

# daftarGejala = [
#     'Mual pada perut ',
#     'Nyeri di ulu hati ',
#     'Perut kembung ',
#     'Sendawa berlebih',
#     'Sulit tidur ',
#     'Anemia ',
#     'BAB berwarna hitam',
#     'Sering Cegukan ',
#     'Sakit tenggorokan ',
#     'Mudah merasa kenyang',
#     'Kadar gula darah tidak terkontrol ',
#     'Asam dan pahit pada mulut ',
#     'Muntah darah ',
#     'BAB Berdarah ',
#     'Penurunan berat badan ',
# ]

# daftarPenyakit = [
#     'Tukak Lambung (Ulkus Peptikum)',
#     'Gastroparesis',
#     'GERD (Gastroesophageal Reflux Disease)',
#     'Gastritis ',
#     'Kanker lambung ',
# ]

# solusiPenyakit = [
#     'Hindari makanan pedas, asam, dan berlemak; berhenti merokok; hindari alkohol.',
#     'Makan dalam porsi kecil dan sering; hindari makanan tinggi serat dan lemak; mengkonsumsi makanan lunak atau cair.',
#     'Makan dalam porsi kecil dan sering; hindari makanan pedas, berlemak, dan asam; hindari makan sebelum tidur; Menurunkan berat badan jika kelebihan berat badan.',
#     'Makan dalam porsi kecil dan sering; hindari makanan pedas, berlemak, dan asam; Mengelola stres dengan teknik relaksasi; hindari alkohol dan merokok.',
#     'Operasi; kemoterapi; Dukungan nutrisi untuk menjaga berat badan dan kesehatan; konseling untuk dukungan emosional dan psikologis.',
# ]

# def checkGejala():
#     pilihan = request.form.get('pilihan')
#     if pilihan == 'ya':
#         return True
#     elif pilihan == 'tidak':
#         return False
#     else:
#         return None

# @app.route('/')
# def index():
#     session.pop('namaPasien', None)
#     session.pop('gejalaPasien', None)
#     session.pop('logs', None)
#     session.pop('logs2', None)
#     session['gejalaPasien'] = 0
#     session['logs'] = 0
#     session['logs2'] = 0
#     return render_template('index.html', link=url_for('index'))

# @app.route('/welcome', methods=['POST', 'GET'])
# def welcome():
#     if request.method == 'POST':
#         name = request.form.get('Name')
#         session['namaPasien'] = name
#         gejalanya = session['gejalaPasien']
#         pertanyaan = daftarGejala[gejalanya]
#         return render_template("welcome.html", name=name, pertanyaan=pertanyaan, link=url_for('index'))

# @app.route('/result', methods=['POST', 'GET'])
# def result():
#     if request.method == 'POST':
#         gejala_terjadi = checkGejala()

#         if gejala_terjadi is None:
#             return redirect(url_for('diagnosa'))

#         #=============================================================Logs 0
#         if session['logs'] == 0 and gejala_terjadi:
#             if session['gejalaPasien'] == 0:  # penyakit 1, penyakit 4, penyakit 2, penyakit 3
#                 session['gejalaPasien'] = 1
#                 session['logs'] = 1
#                 return redirect(url_for('diagnosa'))
#             elif session['gejalaPasien'] == 1:  # penyakit 5
#                 session['gejalaPasien'] = 2
#                 session['logs'] = 1
#                 return redirect(url_for('diagnosa'))

#         #=============================================================Logs 1
#         elif session['logs'] == 1 and gejala_terjadi:
#             if session['gejalaPasien'] == 1:  # penyakit 1, penyakit 4, penyakit 2
#                 session['gejalaPasien'] = 2
#                 session['logs'] = 2
#                 return redirect(url_for('diagnosa'))
#             elif session['gejalaPasien'] == 2:  # penyakit 5
#                 session['gejalaPasien'] = 5
#                 session['logs'] = 2
#                 return redirect(url_for('diagnosa'))

#         #=============================================================Logs 2
#         elif session['logs'] == 2 and gejala_terjadi:
#             if session['gejalaPasien'] == 2:  # penyakit 1, penyakit 2
#                 session['gejalaPasien'] = 3
#                 session['logs'] = 3
#                 return redirect(url_for('diagnosa'))
#             elif session['gejalaPasien'] == 6:  # penyakit 4
#                 session['gejalaPasien'] = 7
#                 session['logs'] = 3
#                 return redirect(url_for('diagnosa'))
#             elif session['gejalaPasien'] == 5:  # penyakit 5
#                 session['gejalaPasien'] = 12
#                 session['logs'] = 3
#                 return redirect(url_for('diagnosa'))
#             elif session['gejalaPasien'] == 10:  # penyakit 3
#                 session['gejalaPasien'] = 11
#                 session['logs'] = 3
#                 return redirect(url_for('diagnosa'))

#         #=============================================================Logs 3
#         elif session['logs'] == 3 and gejala_terjadi:
#             if session['gejalaPasien'] == 7:  # penyakit 4
#                 terjangkitPenyakit = daftarPenyakit[3]
#                 solusiPenyakitnya = "Solusi: " + solusiPenyakit[3]
#                 return render_template("result.html", terjangkitPenyakit=terjangkitPenyakit, solusiPenyakitnya=solusiPenyakitnya, awal=url_for('index'))
#             if session['gejalaPasien'] == 3:  # penyakit 1
#                 terjangkitPenyakit = daftarPenyakit[0]
#                 solusiPenyakitnya = "Solusi: " + solusiPenyakit[0]
#                 return render_template("result.html", terjangkitPenyakit=terjangkitPenyakit, solusiPenyakitnya=solusiPenyakitnya, awal=url_for('index'))
#             if session['gejalaPasien'] == 12:  # penyakit 5
#                 session['gejalaPasien'] = 13
#                 session['logs'] = 4
#                 return redirect(url_for('diagnosa'))
#             if session['gejalaPasien'] == 11:  # penyakit 3
#                 terjangkitPenyakit = daftarPenyakit[2]
#                 solusiPenyakitnya = "Solusi: " + solusiPenyakit[2]
#                 return render_template("result.html", terjangkitPenyakit=terjangkitPenyakit, solusiPenyakitnya=solusiPenyakitnya, awal=url_for('index'))

#         #=============================================================Logs 4
#         elif session['logs'] == 4 and gejala_terjadi:
#             if session['gejalaPasien'] == 14:  # penyakit 2
#                 terjangkitPenyakit = daftarPenyakit[1]
#                 solusiPenyakitnya = "Solusi: " + solusiPenyakit[1]
#                 return render_template("result.html", terjangkitPenyakit=terjangkitPenyakit, solusiPenyakitnya=solusiPenyakitnya, awal=url_for('index'))
#             if session['gejalaPasien'] == 13:  # penyakit 5
#                 session['gejalaPasien'] = 14
#                 session['logs'] = 5
#                 return redirect(url_for('diagnosa'))

#         #=============================================================Logs 5
#         elif session['logs'] == 5 and gejala_terjadi:
#             if session['gejalaPasien'] == 14:  # penyakit 5
#                 terjangkitPenyakit = daftarPenyakit[4]
#                 solusiPenyakitnya = "Solusi: " + solusiPenyakit[4]
#                 return render_template("result.html", terjangkitPenyakit=terjangkitPenyakit, solusiPenyakitnya=solusiPenyakitnya, awal=url_for('index'))

#         #=============================================================Logs 1
#         else:
#             terjangkitPenyakit = "Maaf Sistem kami belum bisa menjawab pertanyaan anda"
#             return render_template("result.html", terjangkitPenyakit=terjangkitPenyakit, awal=url_for('index'))

# @app.route('/diagnosa', methods=['POST', 'GET'])
# def diagnosa():
#     name = session['namaPasien']
#     pertanyaan = daftarGejala[session['gejalaPasien']]
#     return render_template("diagnosa.html", pertanyaan=pertanyaan, name=name, link=url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)
