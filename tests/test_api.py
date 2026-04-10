"""Quick smoke test for the Phase 5 recommendation API."""
import requests

resp = requests.post('http://127.0.0.1:8080/phase5/recommend', json={
    'city': 'Bengaluru',
    'locality': 'BTM',
    'budget': 1000,
    'preferred_cuisines': [],
    'min_rating': 3.0,
    'top_k': 5,
})

print(f'Status: {resp.status_code}')
data = resp.json()
print(f'Valid: {data["preference_valid"]}')
print(f'Recommendations: {len(data["recommendations"])} found')
if data['recommendations']:
    print(f'First recommendation: {data["recommendations"][0]["name"]}')
