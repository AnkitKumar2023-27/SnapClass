from src.components.database.config import supabase
import bcrypt


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()


def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def check_teacher_exists(username):
    username = username.strip()
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0


def create_teacher(username, password, name):
    username = username.strip()
    data = {"username": username, "password": hash_pass(password), "name": name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username, password):
    username = username.strip()
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher["password"]):
            return teacher
    return None


def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data

def create_student(name, email=None, phone=None,
                   face_embedding=None, 
                   voice_embedding=None):
    data = {
        "name": name,
        "email": email,
        "phone": phone,
        "face_embedding": face_embedding,
        "voice_embedding": voice_embedding
    }
    response = supabase.table("students").insert(data).execute()
    return response.data[0]


def get_teacher_subjects(teacher_id):
    response = supabase.table("subjects").select(
        "*, subject_student(count), attendance_logs(*)"
    ).eq("teacher_id", teacher_id).execute()

    subjects = response.data

    for sub in subjects:
        sub['total_students'] = sub.get("subject_student", [{}])[0].get('count', 0)
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['timestamp'][:10] for log in attendance))
        sub['total_classes'] = unique_sessions
        sub.pop('subject_student', None)
        sub.pop('attendance_logs', None)

    return subjects


def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    response = supabase.table("subjects").insert(data).execute()
    return response.data


def get_subjects_by_teacher(teacher_id):
    response = supabase.table("subjects").select("*").eq("teacher_id", teacher_id).execute()
    return response.data


def delete_subject(subject_id):
    response = supabase.table("subjects").delete().eq("subject_id", subject_id).execute()
    return response.data


def enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, 'subject_id': subject_id}
    response = supabase.table('subject_student').insert(data).execute()
    return response.data


def unenroll_student_from_subject(student_id, subject_id):
    response = supabase.table('subject_student').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
    return response.data


def check_student_enrolled(student_id, subject_id):
    response = supabase.table('subject_student').select('*').eq('subject_id', subject_id).eq('student_id', student_id).execute()
    return len(response.data) > 0


def get_student_subjects(student_id):
    response = supabase.table('subject_student').select(
        '*, subjects(*, attendance_logs(*))'
    ).eq('student_id', student_id).execute()
    return response.data


def get_student_attendance(student_id):
    response = supabase.table('attendance_logs').select('*').eq('student_id', student_id).execute()
    return response.data


def get_enrolled_students(subject_id):
    response = supabase.table('subject_student').select(
        "*, students(*)"
    ).eq('subject_id', subject_id).execute()
    return response.data


def log_attendance(subject_id, student_id, is_present=True):
    data = {
        "subject_id": subject_id,
        "student_id": student_id,
        "is_present": is_present
    }
    response = supabase.table("attendance_logs").insert(data).execute()
    return response.data


def create_attendance(logs):
    response = supabase.table("attendance_logs").insert(logs).execute()
    return response.data

def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance_logs').select(
        "*, subjects!inner(*, teachers!inner(teacher_id))"
    ).eq('subjects.teacher_id', teacher_id).execute()
    return response.data



def get_student_attendance_percentage(student_id, subject_id):
    response = supabase.table('attendance_logs').select(
        '*'
    ).eq('student_id', student_id).eq(
        'subject_id', subject_id
    ).execute()
    
    logs = response.data
    
    if not logs:
        return None
    
    total = len(logs)
    present = sum(1 for log in logs if log['is_present'])
    percentage = (present / total) * 100
    
    return {
        'total': total,
        'present': present,
        'absent': total - present,
        'percentage': round(percentage, 1)
    }


def get_all_students_attendance_for_subject(subject_id):
    enrolled = get_enrolled_students(subject_id)
    results = []
    
    for node in enrolled:
        student = node['students']
        stats = get_student_attendance_percentage(
            student['student_id'], subject_id
        )
        if stats:
            results.append({
                'student_id': student['student_id'],
                'name': student['name'],
                'email': student.get('email', ''),
                'phone': student.get('phone', ''),
                **stats
            })
    
    return results


def get_attendance_analytics(teacher_id):
    """
    Teacher ke saare subjects ki attendance data lo
    Join: attendance_logs → subjects → students
    """
    response = supabase.table('attendance_logs').select(
        """
        *,
        subjects!inner(
            subject_id,
            name,
            subject_code,
            teacher_id
        ),
        students(
            student_id,
            name
        )
        """
    ).eq('subjects.teacher_id', teacher_id).execute()

    return response.data


def get_student_full_data(student_id):
    response = supabase.table('subject_student').select(
        "*, subjects(subject_id, name, subject_code, section)"
    ).eq('student_id', student_id).execute()
    return response.data


def get_student_attendance_by_subject(student_id):
    response = supabase.table('attendance_logs').select(
        "*, subjects(name, subject_code)"
    ).eq('student_id', student_id).execute()
    return response.data


def get_student_stats_for_ai(student_id):
    enrolled_data   = get_student_full_data(student_id)
    attendance_data = get_student_attendance_by_subject(student_id)

    stats = {}

    for node in enrolled_data:
        sub    = node.get('subjects', {})
        sub_id = sub.get('subject_id')
        if sub_id:
            stats[sub_id] = {
                'name':                    sub.get('name', 'Unknown'),
                'code':                    sub.get('subject_code', ''),
                'section':                 sub.get('section', ''),
                'total':                   0,
                'present':                 0,
                'absent':                  0,
                'percentage':              0.0,
                'status':                  'No data',
                'dates':                   [],
                'classes_needed_for_75':   0,
            }

    for log in attendance_data:
        sub_id = log.get('subject_id')
        if sub_id and sub_id in stats:
            stats[sub_id]['total'] += 1
            if log.get('is_present'):
                stats[sub_id]['present'] += 1
            else:
                stats[sub_id]['absent'] += 1
            ts = log.get('timestamp')
            if ts:
                stats[sub_id]['dates'].append(ts[:10])

    for sub_id in stats:
        total   = stats[sub_id]['total']
        present = stats[sub_id]['present']
        if total > 0:
            pct = round((present / total) * 100, 1)
            stats[sub_id]['percentage'] = pct
            stats[sub_id]['status']     = (
                '✅ Safe'    if pct >= 75 else
                '⚠️ Low'    if pct >= 60 else
                '❌ Danger'
            )
            stats[sub_id]['classes_needed_for_75'] = max(
                0, int(0.75 * total) - present + 1
            )
        else:
            stats[sub_id]['percentage']            = 0.0
            stats[sub_id]['status']                = 'No attendance yet'
            stats[sub_id]['classes_needed_for_75'] = 0

    return list(stats.values())