#app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2 
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"
app.config['JSON_SORT_KEYS'] = False
 
#banco de dados criado na aws
DB_HOST = "database-biblioteca.cjafgiodewwt.us-east-1.rds.amazonaws.com"
DB_NAME = "biblioteca"
DB_USER = "aluno"
DB_PASS = "aluno123456"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

#CRUD tabela ESCREVE
@app.route('/escreve')
def Index_escreve():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT * FROM biblioteca.escreve"
    cur.execute(query) # Execute the SQL
    list_escreve = cur.fetchall()
    return render_template('index-escreve.html', list_escreve = list_escreve)
 
@app.route('/escreve/add_escreve', methods=['POST'])
def add_escreve():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        id_autor = request.form['id_autor']
        idlivro_isbn = request.form['idlivro_isbn']

        cur.execute("INSERT INTO biblioteca.escreve VALUES (%s,%s)", (id_autor, idlivro_isbn))
        conn.commit()
        flash('Escreve Added successfully')
        return redirect(url_for('Index_escreve'))

@app.route('/escreve/edit/<idAutor>/<idLivro>', methods = ['POST', 'GET'])
def get_employee_escreve(idAutor, idLivro):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('SELECT * FROM biblioteca.escreve WHERE id_autor = {0} AND idlivro_isbn = {1}'.format(idAutor, idLivro))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-escreve.html', escreve = data[0])
 
@app.route('/escreve/update/<int:idAutor>/<int:idLivro>', methods=['POST'])
def update_escreve(idAutor, idLivro):
    if request.method == 'POST':
        id_autor = request.form['id_autor']
        idlivro_isbn = request.form['idlivro_isbn']
         
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""UPDATE biblioteca.escreve 
        SET id_autor = %s,
        idlivro_isbn = %s 
        WHERE id_autor = %s AND idlivro_isbn = %s""", (id_autor, idlivro_isbn, idAutor, idLivro))
    
        flash('Escreve Updated Successfully')
        conn.commit()
        return redirect(url_for('Index_escreve'))
 
@app.route('/escreve/delete/<int:idAutor>/<int:idLivro>', methods = ['POST','GET'])
def delete_escreve(idAutor, idLivro):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('DELETE FROM biblioteca.escreve WHERE id_autor = {0} AND idlivro_isbn = {1}'.format(idAutor, idLivro))
    conn.commit()
    flash('Escreve Removed Successfully')
    return redirect(url_for('Index_escreve'))



#CRUD Autor
@app.route('/autor')
def Index_autor():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT * FROM biblioteca.autor"
    cur.execute(query)
    list_autores = cur.fetchall()
    return render_template('index-autor.html', list_autores = list_autores)
 
@app.route('/autor/add_autor', methods=['POST'])
def add_autor():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        primeiro_nome = request.form['primeiro_nome']
        sobrenome = request.form['sobrenome']
        num_autor = request.form['num_autor']

        cur.execute("INSERT INTO biblioteca.autor (primeiro_nome, sobrenome, num_autor) VALUES (%s,%s,%s)", (primeiro_nome, sobrenome, num_autor))
        conn.commit()
        flash('Autor Added Successfully')
        return redirect(url_for('Index_autor'))

@app.route('/autor/edit/<int:id>', methods = ['POST', 'GET'])
def get_employee_autor(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('SELECT * FROM biblioteca.autor WHERE id_autor = {0}'.format(id))
    data = cur.fetchall()
    cur.close()
    
    return render_template('edit-autor.html', autor = data[0])
 
@app.route('/autor/update/<id>', methods=['POST'])
def update_autor(id):
    if request.method == 'POST':
        primeiro_nome = request.form['primeiro_nome']
        sobrenome = request.form['sobrenome']
        num_autor = request.form['num_autor']
         
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute("""UPDATE biblioteca.autor 
        SET primeiro_nome = %s,
        sobrenome = %s, 
        num_autor = %s
        WHERE id_autor = %s""", (primeiro_nome, sobrenome, num_autor, id))
    
        flash('Autor Updated Successfully')
        conn.commit()
        return redirect(url_for('Index_autor'))
 
@app.route('/autor/delete/<int:id>', methods = ['POST','GET'])
def delete_autor(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('DELETE FROM biblioteca.autor WHERE id_autor = {0}'.format(id))
    conn.commit()
    flash('Autor Removed Successfully')
    return redirect(url_for('Index_autor'))


#CRUD LIVRO
@app.route('/livro')
def Index_livro():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT * FROM biblioteca.livro"
    cur.execute(query) # Execute the SQL
    list_livros = cur.fetchall()
    return render_template('index-livro.html', list_livros = list_livros)
 
@app.route('/livro/add_livro', methods=['POST'])
def add_livro():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        titulo = request.form['titulo']
        ano_lancamento = request.form['ano_lancamento']
        num_paginas = request.form['num_paginas']
        idioma = request.form['idioma']
        edicao = request.form['edicao']
        publicacao = request.form['publicacao']

        cur.execute("INSERT INTO biblioteca.livro (titulo, ano_lancamento, num_paginas, idioma, edicao, publicacao) VALUES (%s,%s,%s,%s,%s,%s)", (titulo, ano_lancamento, num_paginas, idioma, edicao, publicacao))
        conn.commit()
        flash('Autor Added successfully')
        return redirect(url_for('Index_livro'))

@app.route('/livro/edit/<int:id>', methods = ['POST', 'GET'])
def get_employee_livro(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('SELECT * FROM biblioteca.livro WHERE idLivro_ISBN = {0}'.format(id))
    data = cur.fetchall()
    cur.close()
    
    return render_template('edit-livro.html', livro = data[0])
 
@app.route('/livro/update/<id>', methods=['POST'])
def update_livro(id):
    if request.method == 'POST':
        titulo = request.form['titulo']
        ano_lancamento = request.form['ano_lancamento']
        num_paginas = request.form['num_paginas']
        idioma = request.form['idioma']
        edicao = request.form['edicao']
        publicacao = request.form['publicacao']
         
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute("""UPDATE biblioteca.livro 
        SET titulo = %s,
        ano_lancamento = %s,
        num_paginas = %s,
        idioma = %s,
        edicao = %s,
        publicacao = %s
        WHERE idLivro_ISBN = %s""", (titulo, ano_lancamento, num_paginas, idioma, edicao, publicacao, id))
    
        flash('Autor Updated Successfully')
        conn.commit()
        return redirect(url_for('Index_livro'))
 
@app.route('/livro/delete/<int:id>', methods = ['POST','GET'])
def delete_livro(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('DELETE FROM biblioteca.livro WHERE idLivro_ISBN = {0}'.format(id))
    conn.commit()
    flash('Autor Removed Successfully')
    return redirect(url_for('Index_livro'))
 
if __name__ == "__main__":
    app.run(debug=True)
