import json
from django.shortcuts import render
from django.conf import settings
import openai
from Employee.models import *
from datetime import date

def ClientHomePage(request):
    return render(request,'client_main_page.html')


SYSTEM_PROMPT = """
You are an assistant that extracts structured caregiver matching requirements from phone conversation transcripts.

Respond in valid JSON format only, with all fields always present, in the following order and exact keys:

- client_name: string or "Any"
- Client_age: integer or "Any"
- Preferred_caregiver_gender: "F", "M", or "Any"
- Preferred_caregiver_age_min: integer or "Any"
- Preferred_caregiver_age_max: integer or "Any"
- Care_location: string or "Any"
- Language_preference: string, list of strings, or "Any"
- Required_certifications: list of keys from:
  [
    "student_nurse_id", "nmbi_cert", "fetac_level_5", "social_care_cert",
    "cpr_cert", "patient_moving", "elder_abuse", "ppe_training", "infection_control",
    "safeguarding_adults", "hand_hygiene", "fire_safety", "children_first", "gdpr"
  ]
  or an empty list if none
- Required_occupational_health: list of keys from:
  ["hep_b", "mmr_immunity", "varicella_immunity"]
  or an empty list if none
- Notes: list of keywords only, representing specific client requirements or care needs (e.g., "dementia care", "meal_preparation", "night_shift", "mobility_assistance"). Do not include full sentences.

If any information is not mentioned in the transcript, fill that field with "Any" for strings or integers, or an empty list for lists.

Only respond with the JSON object. Do not include any extra text.
"""

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def Summarizer(request):
    extracted_data = {
        "client_name": "Any",
        "Client_age": "Any",
        "Preferred_caregiver_gender": "Any",
        "Preferred_caregiver_age_min": "Any",
        "Preferred_caregiver_age_max": "Any",
        "Care_location": "Any",
        "Language_preference": "Any",
        "Required_certifications": [],
        "Required_occupational_health": [],
        "Notes": [],
    }
    transcript = ""

    if request.method == "POST":
        transcript = request.POST.get("prompt", "").strip()
        if transcript:
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"Transcript:\n{transcript}"}
                    ],
                    max_tokens=700,
                    temperature=0.3,
                )
                json_text = response.choices[0].message.content.strip()
                data = json.loads(json_text)

                for key in extracted_data:
                    if key in data and data[key] not in [None, "", {}, []]:
                        extracted_data[key] = data[key]

            except Exception as e:
                extracted_data = {"error": f"Error parsing GPT response: {str(e)}"}

    return render(request, 'summary.html', {
        'summary': extracted_data,
        'transcript': transcript,
    })


def calculate_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def employee_summary(request):
    field_groups = {
        "Personal Information": [
            'title', 'forenames', 'surname', 'age', 'gender', 'email', 'phone_mobile', 'pps_number', 'language'
        ],
        "Professional Qualifications / Certifications": [
            'student_nurse_id', 'nmbi_cert', 'fetac_level_5', 'social_care_cert'
        ],
        "General Training Certifications": [
            'cpr_cert', 'patient_moving', 'elder_abuse', 'ppe_training', 'infection_control', 
            'safeguarding_adults', 'hand_hygiene', 'fire_safety', 'children_first', 'gdpr'
        ],
        "Occupational Health": [
            'hep_b', 'mmr_immunity', 'varicella_immunity'
        ]
    }

    field_groups_display = {}
    for group, fields in field_groups.items():
        field_groups_display[group] = [
            "Age" if field == "age" else field.replace("_", " ").title()
            for field in fields
        ]

    
    employees = []
    for emp in EmployeeApplication.objects.all():
        row = []
        for group_fields in field_groups.values():
            for field in group_fields:
                if field == 'age':
                    row.append(calculate_age(emp.date_of_birth))
                else:
                    row.append(getattr(emp, field))
        employees.append(row)

    return render(request, 'employee_suggestion.html', {
        'field_groups': field_groups,
        'field_groups_display': field_groups_display,
        'employees': employees,
    })

'''

def match_employees(request):
    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        client_age = request.POST.get('Client_age')
        preferred_gender = request.POST.get('Preferred_caregiver_gender')
        preferred_age_min = request.POST.get('Preferred_caregiver_age_min')
        preferred_age_max = request.POST.get('Preferred_caregiver_age_max')
        care_location = request.POST.get('Care_location')
        language_preference = request.POST.get('Language_preference')

        
        certifications_raw = request.POST.get('Required_certifications', '')
        required_certifications = [c.strip() for c in certifications_raw.split(',') if c.strip()]

        health_raw = request.POST.get('Required_occupational_health', '')
        required_occupational_health = [h.strip() for h in health_raw.split(',') if h.strip()]

        
        notes = request.POST.getlist('Notes')

       
        context = {
            'client_name': client_name,
            'client_age': client_age,
            'preferred_gender': preferred_gender,
            'preferred_age_min': preferred_age_min,
            'preferred_age_max': preferred_age_max,
            'care_location': care_location,
            'language_preference': language_preference,
            'required_certifications': required_certifications,
            'required_occupational_health': required_occupational_health,
            'notes': notes,
        }

        # You will later match employees here, for now just show data:
        return render(request, 'match_results.html', context)

    return render(request, 'match_results.html', {'error': 'Invalid request method'})

'''
from datetime import date
from django.shortcuts import render
from Employee.models import EmployeeApplication
import openai

client = openai.OpenAI(api_key="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")


def calculate_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def match_employees(request):
    if request.method != 'POST':
        return render(request, 'match_results.html', {'error': 'Invalid request method'})

    # Extract client preferences from form
    client_data = {
        'name': request.POST.get('client_name'),
        'age': request.POST.get('Client_age'),
        'preferred_gender': request.POST.get('Preferred_caregiver_gender'),
        'preferred_age_min': request.POST.get('Preferred_caregiver_age_min'),
        'preferred_age_max': request.POST.get('Preferred_caregiver_age_max'),
        'care_location': request.POST.get('Care_location'),
        'language_preference': request.POST.get('Language_preference'),
        'required_certifications': [
            c.strip() for c in request.POST.get('Required_certifications', '').split(',') if c.strip()
        ],
        'required_occupational_health': [
            h.strip() for h in request.POST.get('Required_occupational_health', '').split(',') if h.strip()
        ],
        'notes': request.POST.getlist('Notes'),
    }

    # Build structured employee data
    employee_list = []
    for emp in EmployeeApplication.objects.all():
        emp_dict = {
            'name': f"{emp.forenames} {emp.surname}",
            'age': calculate_age(emp.date_of_birth),
            'gender': emp.gender,
            'language': emp.language,
            'certifications': {
                'student_nurse_id': emp.student_nurse_id,
                'nmbi_cert': emp.nmbi_cert,
                'fetac_level_5': emp.fetac_level_5,
                'social_care_cert': emp.social_care_cert,
                'cpr_cert': emp.cpr_cert,
                'patient_moving': emp.patient_moving,
                'elder_abuse': emp.elder_abuse,
                'ppe_training': emp.ppe_training,
                'infection_control': emp.infection_control,
                'safeguarding_adults': emp.safeguarding_adults,
                'hand_hygiene': emp.hand_hygiene,
                'fire_safety': emp.fire_safety,
                'children_first': emp.children_first,
                'gdpr': emp.gdpr,
            },
            'occupational_health': {
                'hep_b': emp.hep_b,
                'mmr_immunity': emp.mmr_immunity,
                'varicella_immunity': emp.varicella_immunity,
            }
        }
        employee_list.append(emp_dict)

    # GPT prompt
    messages = [
        {
            "role": "system",
            "content": "You are an expert caregiver recruiter. Match suitable employees based on client's care preferences. Choose the top 1–3 most suitable employees. Justify each selection briefly."
        },
        {
            "role": "user",
            "content": f"""
Client Requirements:
{client_data}

Employee Candidates:
{employee_list}

Return a list of up to 3 best-matching employees with reasons.
"""
        }
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.4
        )
        gpt_response = response.choices[0].message.content
    except Exception as e:
        gpt_response = f"Error getting response from GPT: {str(e)}"

    return render(request, 'match_results.html', {
        'client_name': client_data['name'],
        'client_age': client_data['age'],
        'preferred_gender': client_data['preferred_gender'],
        'preferred_age_min': client_data['preferred_age_min'],
        'preferred_age_max': client_data['preferred_age_max'],
        'care_location': client_data['care_location'],
        'language_preference': client_data['language_preference'],
        'required_certifications': client_data['required_certifications'],
        'required_occupational_health': client_data['required_occupational_health'],
        'notes': client_data['notes'],
        'gpt_matches': gpt_response,
    })

