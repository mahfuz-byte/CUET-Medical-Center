import os

file_path = r'd:\IP2\frontend\assets\js\app.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()


old_roster_logic = """    fetch('assets/data/roster.json')
      .then(function(r){ if (!r.ok) throw new Error('HTTP '+r.status); return r.json(); })
      .then(function(data){
        if (docList) {
          var docs = (data && data.doctors) || [];
          docList.innerHTML = docs.length ? docs.map(function(d){
            return '<div class="item">\\n'
              + '  <div class="item-title">'+(d.name||'Unknown')+' — '+(d.dept||'')+'</div>\\n'
              + '  <div class="item-meta">'+(d.title||'')+' | '+(d.hours||'')+'</div>\\n'
              + '  <div>'+(d.bio||'')+'</div>\\n'
              + '</div>';
          }).join('') : '<div class="item">No doctors listed.</div>';
          docList.removeAttribute('aria-busy');
        }
        if (ambList) {
          var ambs = (data && data.ambulances) || [];
          ambList.innerHTML = ambs.length ? ambs.map(function(a){
            return '<div class="item">\\n'
              + '  <div class="item-title">'+(a.id||'Ambulance')+'</div>\\n'
              + '  <div class="item-meta">Status: '+(a.status||'Unknown')+' | '+(a.contact||'')+'</div>\\n'
              + '</div>';
          }).join('') : '<div class="item">No ambulances listed.</div>';
          ambList.removeAttribute('aria-busy');
        }
      })
      .catch(function(){
        if (docList) { docList.innerHTML = '<div class="item">Failed to load roster.</div>'; docList.removeAttribute('aria-busy'); }
        if (ambList) { ambList.innerHTML = '<div class="item">Failed to load roster.</div>'; ambList.removeAttribute('aria-busy'); }
      });"""

new_roster_logic = """    Promise.all([
      fetch(API_BASE_URL + '/roster/doctors/').then(r => r.json()).catch(e => []),
      fetch(API_BASE_URL + '/roster/ambulances/').then(r => r.json()).catch(e => [])
    ]).then(function([doctors, ambulances]){
        if (docList) {
          docList.innerHTML = doctors.length ? doctors.map(function(d){
            return '<div class="item">\\n'
              + '  <div class="item-title">'+(d.name||'Unknown')+' — '+(d.dept||'')+'</div>\\n'
              + '  <div class="item-meta">'+(d.title||'')+' | '+(d.hours||'')+'</div>\\n'
              + '</div>';
          }).join('') : '<div class="item">No doctors listed.</div>';
          docList.removeAttribute('aria-busy');
        }
        if (ambList) {
          ambList.innerHTML = ambulances.length ? ambulances.map(function(a){
            return '<div class="item">\\n'
              + '  <div class="item-title">'+(a.ambulance_id||'Ambulance')+'</div>\\n'
              + '  <div class="item-meta">Status: '+(a.status||'Unknown')+' | '+(a.contact||'')+'</div>\\n'
              + '</div>';
          }).join('') : '<div class="item">No ambulances listed.</div>';
          ambList.removeAttribute('aria-busy');
        }
    });"""

content = content.replace(old_roster_logic, new_roster_logic)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.js")
