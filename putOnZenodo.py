import requests

ACCESS_TOKEN = 'YOUR_TOKEN_HERE'
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# STEP 1 — Create deposition
metadata = {
    'metadata': {
        'title': 'Beyond Spacetime: A Fluid-Dynamic Theory of Gravity and Time from Vorticity',
        'upload_type': 'publication',
        'publication_type': 'article',
        'description': 'This research presents a novel theoretical framework in which gravity and time emerge from vorticity structure in an incompressible æther...',
        'creators': [{'name': 'Iskandarani, Omar', 'affiliation': 'Independent Researcher, Groningen, The Netherlands'}],
        'keywords': [
            'entropic gravity', 'vorticity', 'æther theory', 'time dilation', 'topological bifurcation',
            'swirl clock', 'Schwarzian action', 'emergent spacetime', 'fluid gravity', 'Kairos event'
        ],
        'license': 'cc-by-4.0'
    }
}

r = requests.post('https://zenodo.org/api/deposit/depositions',
                  params={'access_token': ACCESS_TOKEN},
                  json=metadata, headers=headers)

deposition = r.json()
deposition_id = deposition['id']
print(f"Created deposition: {deposition_id}")

# STEP 2 — Upload your PDF or ZIP
files = {'file': open("vam_paper.pdf", 'rb')}
r = requests.post(f'https://zenodo.org/api/deposit/depositions/{deposition_id}/files',
                  params={'access_token': ACCESS_TOKEN},
                  files=files)

print("Upload complete:", r.status_code)

# STEP 3 — Optional: Publish
r = requests.post(f'https://zenodo.org/api/deposit/depositions/{deposition_id}/actions/publish',
                  params={'access_token': ACCESS_TOKEN})
print("Published:", r.status_code)
