import os

file_path = r'd:\IP2\frontend-temp\admin.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add getHeaders helper
headers_script = """        function getHeaders() {
            return {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
            };
        }
        
        const API_URL = 'http://127.0.0.1:8000/api';
"""
if "function getHeaders()" not in content:
    content = content.replace('// Load all admin data from localStorage', headers_script + '\n        // Load all admin data from backend')


content = content.replace('''
        function loadDoctors() {
            const doctors = JSON.parse(localStorage.getItem('doctors') || '[]');
            const list = document.getElementById('doctorList');
            
            if (doctors.length === 0) {
                list.innerHTML = '<div class="item-list-empty">No doctors added yet</div>';
                return;
            }

            list.innerHTML = doctors.map((doc, idx) => `
                <div class="item-row">
                    <div class="item-info">
                        <div class="item-info-text">
                            <strong>${doc.name}</strong>
                            <span>${doc.dept} - ${doc.title}</span>
                            <span style="color: #9ca3af; font-size: 0.85rem;">${doc.hours}</span>
                        </div>
                    </div>
                    <button class="btn-danger" onclick="removeDoctor(${idx})">Delete</button>
                </div>
            `).join('');
        }
''', '''
        async function loadDoctors() {
            const list = document.getElementById('doctorList');
            try {
                const res = await fetch(`${API_URL}/roster/doctors/`, { headers: getHeaders() });
                const doctors = await res.json();
                if (doctors.length === 0) {
                    list.innerHTML = '<div class="item-list-empty">No doctors added yet</div>';
                    return;
                }
                list.innerHTML = doctors.map(doc => `
                    <div class="item-row">
                        <div class="item-info">
                            <div class="item-info-text">
                                <strong>${doc.name}</strong>
                                <span>${doc.dept} - ${doc.title}</span>
                                <span style="color: #9ca3af; font-size: 0.85rem;">${doc.hours}</span>
                            </div>
                        </div>
                        <button class="btn-danger" onclick="removeDoctor(${doc.id})">Delete</button>
                    </div>
                `).join('');
            } catch (err) {
                console.error(err);
            }
        }
''')

content = content.replace('''
        document.getElementById('addDoctorBtn').addEventListener('click', () => {
            const name = document.getElementById('doctorName').value.trim();
            const dept = document.getElementById('doctorDept').value.trim();
            const title = document.getElementById('doctorTitle').value.trim();
            const hours = document.getElementById('doctorHours').value.trim();

            if (!name || !dept || !title || !hours) {
                showToast('Please fill all fields', 'error');
                return;
            }

            const doctors = JSON.parse(localStorage.getItem('doctors') || '[]');
            doctors.push({ name, dept, title, hours });
            localStorage.setItem('doctors', JSON.stringify(doctors));

            // Clear inputs
            document.getElementById('doctorName').value = '';
            document.getElementById('doctorDept').value = '';
            document.getElementById('doctorTitle').value = '';
            document.getElementById('doctorHours').value = '';

            loadDoctors();
            showToast('Doctor added successfully');
        });
''', '''
        document.getElementById('addDoctorBtn').addEventListener('click', async () => {
            const name = document.getElementById('doctorName').value.trim();
            const dept = document.getElementById('doctorDept').value.trim();
            const title = document.getElementById('doctorTitle').value.trim();
            const hours = document.getElementById('doctorHours').value.trim();

            if (!name || !dept || !title || !hours) {
                showToast('Please fill all fields', 'error');
                return;
            }

            try {
                await fetch(`${API_URL}/roster/doctors/`, {
                    method: 'POST',
                    headers: getHeaders(),
                    body: JSON.stringify({ name, dept, title, hours })
                });

                document.getElementById('doctorName').value = '';
                document.getElementById('doctorDept').value = '';
                document.getElementById('doctorTitle').value = '';
                document.getElementById('doctorHours').value = '';

                loadDoctors();
                showToast('Doctor added successfully');
            } catch (err) {
                showToast('Failed to add doctor', 'error');
            }
        });
''')

content = content.replace('''
        function removeDoctor(idx) {
            const doctors = JSON.parse(localStorage.getItem('doctors') || '[]');
            doctors.splice(idx, 1);
            localStorage.setItem('doctors', JSON.stringify(doctors));
            loadDoctors();
            showToast('Doctor removed');
        }
''', '''
        async function removeDoctor(id) {
            try {
                await fetch(`${API_URL}/roster/doctors/${id}/`, {
                    method: 'DELETE',
                    headers: getHeaders()
                });
                loadDoctors();
                showToast('Doctor removed');
            } catch(e) {}
        }
''')

content = content.replace('''
        function loadAmbulances() {
            const ambulances = JSON.parse(localStorage.getItem('ambulances') || '[]');
            const list = document.getElementById('ambulanceList');
            
            if (ambulances.length === 0) {
                list.innerHTML = '<div class="item-list-empty">No ambulances added yet</div>';
                return;
            }

            list.innerHTML = ambulances.map((amb, idx) => `
                <div class="item-row">
                    <div class="item-info">
                        <div class="item-info-text">
                            <strong>${amb.id}</strong>
                            <span style="color: ${amb.status === 'Available' ? '#10b981' : amb.status === 'On Duty' ? '#3b82f6' : '#ef4444'}; font-weight: 600;">${amb.status}</span>
                            <span style="color: #9ca3af; font-size: 0.85rem;">${amb.contact}</span>
                        </div>
                    </div>
                    <button class="btn-danger" onclick="removeAmbulance(${idx})">Delete</button>
                </div>
            `).join('');
        }
''', '''
        async function loadAmbulances() {
            const list = document.getElementById('ambulanceList');
            try {
                const res = await fetch(`${API_URL}/roster/ambulances/`, { headers: getHeaders() });
                const ambulances = await res.json();
                if (ambulances.length === 0) {
                    list.innerHTML = '<div class="item-list-empty">No ambulances added yet</div>';
                    return;
                }
                list.innerHTML = ambulances.map(amb => `
                    <div class="item-row">
                        <div class="item-info">
                            <div class="item-info-text">
                                <strong>${amb.ambulance_id}</strong>
                                <span style="font-weight: 600;">${amb.status}</span>
                                <span style="color: #9ca3af; font-size: 0.85rem;">${amb.contact}</span>
                            </div>
                        </div>
                        <button class="btn-danger" onclick="removeAmbulance(${amb.id})">Delete</button>
                    </div>
                `).join('');
            } catch(e) {}
        }
''')


content = content.replace('''
        document.getElementById('addAmbulanceBtn').addEventListener('click', () => {
            const id = document.getElementById('ambulanceId').value.trim();
            const status = document.getElementById('ambulanceStatus').value.trim();
            const contact = document.getElementById('ambulanceContact').value.trim();

            if (!id || !status || !contact) {
                showToast('Please fill all fields', 'error');
                return;
            }

            const ambulances = JSON.parse(localStorage.getItem('ambulances') || '[]');
            ambulances.push({ id, status, contact });
            localStorage.setItem('ambulances', JSON.stringify(ambulances));

            document.getElementById('ambulanceId').value = '';
            document.getElementById('ambulanceStatus').value = '';
            document.getElementById('ambulanceContact').value = '';

            loadAmbulances();
            showToast('Ambulance added successfully');
        });

        function removeAmbulance(idx) {
            const ambulances = JSON.parse(localStorage.getItem('ambulances') || '[]');
            ambulances.splice(idx, 1);
            localStorage.setItem('ambulances', JSON.stringify(ambulances));
            loadAmbulances();
            showToast('Ambulance removed');
        }
''', '''
        document.getElementById('addAmbulanceBtn').addEventListener('click', async () => {
            const ambulance_id = document.getElementById('ambulanceId').value.trim();
            const status = document.getElementById('ambulanceStatus').value.trim();
            const contact = document.getElementById('ambulanceContact').value.trim();

            if (!ambulance_id || !status || !contact) {
                showToast('Please fill all fields', 'error');
                return;
            }

            try {
                await fetch(`${API_URL}/roster/ambulances/`, {
                    method: 'POST',
                    headers: getHeaders(),
                    body: JSON.stringify({ ambulance_id, status, contact })
                });

                document.getElementById('ambulanceId').value = '';
                document.getElementById('ambulanceStatus').value = '';
                document.getElementById('ambulanceContact').value = '';

                loadAmbulances();
                showToast('Ambulance added successfully');
            } catch(e) { showToast('Error', 'error'); }
        });

        async function removeAmbulance(id) {
            try {
                await fetch(`${API_URL}/roster/ambulances/${id}/`, {
                    method: 'DELETE',
                    headers: getHeaders()
                });
                loadAmbulances();
                showToast('Ambulance removed');
            } catch(e) {}
        }
''')

# For Pharmacy
content = content.replace('''
        function loadPharmacy() {
            const medicines = JSON.parse(localStorage.getItem('medicines') || '[]');
            const list = document.getElementById('pharmacyList');

            if (medicines.length === 0) {
                list.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: #9ca3af; padding: 20px;">No medicines added yet</div>';
                return;
            }

            list.innerHTML = medicines.map((med, idx) => `
                <div class="medicine-card">
                    <div>
                        <div class="medicine-name">${med.name}</div>
                        <div class="medicine-dosage">${med.dosage}</div>
                    </div>
                    <button class="btn-danger" style="width: 100%;" onclick="removeMedicine(${idx})">Remove</button>
                </div>
            `).join('');
        }

        document.getElementById('addMedicineBtn').addEventListener('click', () => {
            const name = document.getElementById('medicineName').value.trim();
            const dosage = document.getElementById('medicineDosage').value.trim();

            if (!name || !dosage) {
                showToast('Please fill all fields', 'error');
                return;
            }

            const medicines = JSON.parse(localStorage.getItem('medicines') || '[]');
            medicines.push({ name, dosage });
            localStorage.setItem('medicines', JSON.stringify(medicines));

            document.getElementById('medicineName').value = '';
            document.getElementById('medicineDosage').value = '';

            loadPharmacy();
            showToast('Medicine added successfully');
        });

        function removeMedicine(idx) {
            const medicines = JSON.parse(localStorage.getItem('medicines') || '[]');
            medicines.splice(idx, 1);
            localStorage.setItem('medicines', JSON.stringify(medicines));
            loadPharmacy();
            showToast('Medicine removed');
        }
''', '''
        async function loadPharmacy() {
            const list = document.getElementById('pharmacyList');
            try {
                const res = await fetch(`${API_URL}/records/medicines/`, { headers: getHeaders() });
                const medicines = await res.json();
                if (medicines.length === 0) {
                    list.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: #9ca3af; padding: 20px;">No medicines added yet</div>';
                    return;
                }
                list.innerHTML = medicines.map(med => `
                    <div class="medicine-card">
                        <div>
                            <div class="medicine-name">${med.name}</div>
                            <div class="medicine-dosage">${med.dosage}</div>
                        </div>
                        <button class="btn-danger" style="width: 100%;" onclick="removeMedicine(${med.id})">Remove</button>
                    </div>
                `).join('');
            } catch(e) {}
        }

        document.getElementById('addMedicineBtn').addEventListener('click', async () => {
            const name = document.getElementById('medicineName').value.trim();
            const dosage = document.getElementById('medicineDosage').value.trim();

            if (!name || !dosage) {
                showToast('Please fill all fields', 'error');
                return;
            }

            try {
                await fetch(`${API_URL}/records/medicines/`, {
                    method: 'POST',
                    headers: getHeaders(),
                    body: JSON.stringify({ name, dosage })
                });

                document.getElementById('medicineName').value = '';
                document.getElementById('medicineDosage').value = '';
                loadPharmacy();
                showToast('Medicine added successfully');
            } catch(e) { showToast('Error', 'error'); }
        });

        async function removeMedicine(id) {
            try {
                await fetch(`${API_URL}/records/medicines/${id}/`, {
                    method: 'DELETE',
                    headers: getHeaders()
                });
                loadPharmacy();
                showToast('Medicine removed');
            } catch(e) {}
        }
''')


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated admin.html")
