from flask import Blueprint, render_template, request, redirect, url_for, current_app, send_from_directory, abort, Response
from werkzeug.utils import secure_filename, safe_join
from models import fetch_all_pets, fetch_all_policies, fetch_pet_policies, add_pet_policy, get_db_connection, fetch_pet_insurance, fetch_report, fetch_appointments

import sqlite3
import os
import logging
from datetime import datetime

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    pets = fetch_all_pets()
    appointments= fetch_appointments()
    pet_ins = fetch_pet_insurance()
    policies = fetch_all_policies()
    report = fetch_report()
    return render_template('index.html', pets=pets, pet_ins=pet_ins, policies=policies, report=report, appointments=appointments)

@main_blueprint.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        name = request.form['name']
        animal = request.form['animal']
        age=request.form['age']
        allergies=request.form['allergies']
        conn = get_db_connection()
        conn.execute('INSERT INTO pets (name, animal,age,allergies) VALUES (?, ?,?,?)', (name,animal,age,allergies))
        conn.commit()
        conn.close()
        return redirect(url_for('main.index'))
    return render_template('add_pet.html')

# new additon
@main_blueprint.route('/update_pet/<int:pet_id>', methods=['GET', 'POST'])
def update_pet(pet_id):
    conn = get_db_connection()
    pet = conn.execute('SELECT * FROM pets WHERE id = ?', (pet_id,)).fetchone()
    
    if request.method == 'POST':
        name = request.form['name']
        animal = request.form['animal']
        age=request.form['age']
        allergies=request.form['allergies']
        
        conn.execute('UPDATE pets SET name = ?, animal = ?,age=?,allergies= ? WHERE id = ?', (name,animal,age,allergies,pet_id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('main.index'))
    
    conn.close()
    return render_template('update_pet.html', pet=pet)

@main_blueprint.route('/delete_pet/<int:pet_id>', methods=['POST'])
def delete_pet(pet_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM pets WHERE id = ?', (pet_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('main.index'))

# end of new additon


@main_blueprint.route('/upload_report', methods=['GET', 'POST'])
def upload_report():
    if request.method == 'POST':
        pet_id = request.form['pet_id']
        report_name = request.form['report_name']
        file = request.files['file']
        filename = secure_filename(file.filename)
        
        # Ensure the upload directory exists
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Save the file
        file.save(os.path.join(upload_folder, filename))
        
        # Save report details to the database
        conn = get_db_connection()
        conn.execute('INSERT INTO reports (report_name, report_file, pet_id) VALUES (?, ?, ?)',
                     (report_name, filename, pet_id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('main.index'))
    
    pets = fetch_all_pets()
    return render_template('upload_report.html', pets=pets)

@main_blueprint.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'POST':
        pet_id = request.form['pet_id']
        date = request.form['date']
        description = request.form['description']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO appointments (pet_id, date, description) VALUES (?, ?, ?)',
                     (pet_id, datetime.strptime(date, '%Y-%m-%dT%H:%M'), description))
        conn.commit()
        conn.close()
        
        return redirect(url_for('main.index'))
    
    pets = fetch_all_pets()
    return render_template('appointments.html', pets=pets)

@main_blueprint.route('/emergency_contacts')
def emergency_contacts():
    conn = get_db_connection()
    contacts = conn.execute('SELECT * FROM emergency_contacts').fetchall()
    conn.close()
    return render_template('emergency_contacts.html', contacts=contacts)

@main_blueprint.route('/insurance', methods=['GET', 'POST'])
def insurance():
    pets = fetch_all_pets()
    policies = fetch_all_policies()
    
    selected_policy = None
    selected_pet_policies = []

    if request.method == 'POST':
        pet_id = request.form.get('pet_id')
        policy_id = request.form.get('policy_id')

        if pet_id and policy_id:  # Link pet with insurance policy
            add_pet_policy(pet_id, policy_id)

        if pet_id:  # Fetch policies for selected pet
            selected_pet_policies = fetch_pet_policies(pet_id)

    return render_template('insurance.html', pets=pets, policies=policies, selected_pet_policies=selected_pet_policies)

@main_blueprint.route('/display_report/<filename>')
def display_report(filename):
    directory = os.path.join(current_app.root_path, 'uploads')
    try:
        # Ensure the filename is safe to use
        safe_filename = secure_filename(filename)
        file_path = os.path.join(directory, safe_filename)
        
        # Read the file
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # Set the response headers to display the content in the browser
        response = Response(file_content, mimetype='application/pdf')
        response.headers['Content-Disposition'] = 'inline; filename=' + safe_filename
        
        return response
    except FileNotFoundError:
        abort(404)  # File not found
    except Exception as e:
        logging.error(f"Error displaying file: {str(e)}")
        abort(500)  # Internal server error

