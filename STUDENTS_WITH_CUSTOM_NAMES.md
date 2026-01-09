# Create Students with Custom Names & Passwords on Render

## 🎯 What You Need

You can now create students with:
- ✅ **Full names** (e.g., "John Oladele Doe")
- ✅ **Matric numbers** (e.g., "STU001")
- ✅ **Passwords = Surname** (automatically generated from last name)

---

## 🚀 Three Ways to Do It

### Way 1️⃣: Single Student Command

**In Render Shell:**
```bash
python manage.py create_students_custom --name "John Doe" --matric STU001 --gender M --level 100
```

**Result:**
```
Username: stu001 (from matric number)
Full Name: John Doe
Password: Doe (surname capitalized)
Gender: Male
Level: 100
```

---

### Way 2️⃣: CSV File (BEST FOR BULK)

**Step 1: Create CSV file**
```bash
cat > students.csv << 'EOF'
full_name,matric_no,gender,level
John Oladele Doe,STU001,M,100
Alice Oluwatoyin Johnson,STU002,F,100
Michael Chukwuma Smith,STU003,M,200
Sarah Akinyi Williams,STU004,F,200
EOF
```

**Step 2: Run command**
```bash
python manage.py create_students_custom --csv students.csv
```

**Result:**
```
✅ John Oladele Doe (STU001) - Username: stu001, Password: Doe
✅ Alice Oluwatoyin Johnson (STU002) - Username: stu002, Password: Johnson
✅ Michael Chukwuma Smith (STU003) - Username: stu003, Password: Smith
✅ Sarah Akinyi Williams (STU004) - Username: stu004, Password: Williams
```

---

### Way 3️⃣: Generate CSV Locally

**Run this locally:**
```bash
python generate_students_csv.py
```

This creates `students.csv` with 8 sample students. Then upload and use:
```bash
python manage.py create_students_custom --csv students.csv
```

---

## 📝 CSV File Format

**Exactly this format (header row required):**
```csv
full_name,matric_no,gender,level
```

**Example:**
```csv
full_name,matric_no,gender,level
John Doe,STU001,M,100
Alice Smith,STU002,F,100
Michael Brown,STU003,M,200
Sarah Jones,STU004,F,200
```

---

## 🔐 Password Generation

**Automatic Formula:**
- Full Name: `John Oladele Doe`
- Last Word: `Doe`
- Password: `Doe` (capital first letter)

| Full Name | Password |
|-----------|----------|
| John Doe | Doe |
| Alice Johnson | Johnson |
| Michael O'Brien | O'brien |
| Sarah Williams | Williams |
| David da Silva | Silva |

---

## 👤 Login Information

**Login URL:** `https://your-app.onrender.com/accounts/login/`

**Option A: Use Matric Number**
- Username: `STU001`
- Password: `Doe`

**Option B: Use Lowercase Matric**
- Username: `stu001`
- Password: `Doe`

Both work! ✅

---

## 📋 Step-by-Step in Render

### Step 1: Open Shell
```
Dashboard → Your Service → Shell tab
```

### Step 2: Choose Your Method

**Method A (Single Student):**
```bash
python manage.py create_students_custom --name "John Doe" --matric STU001
```

**Method B (CSV - Recommended):**
```bash
cat > students.csv << 'EOF'
full_name,matric_no,gender,level
John Doe,STU001,M,100
Alice Johnson,STU002,F,100
Michael Smith,STU003,M,200
EOF
python manage.py create_students_custom --csv students.csv
```

### Step 3: Done! ✅

---

## 🎓 Example Flow

### Create 4 Students
```bash
cat > students.csv << 'EOF'
full_name,matric_no,gender,level
Chukwu Okafor,STU101,M,100
Zainab Hassan,STU102,F,100
Tunde Adeyemi,STU103,M,200
Amina Bello,STU104,F,200
EOF

python manage.py create_students_custom --csv students.csv
```

### Output
```
✅ Chukwu Okafor (STU101) - Username: stu101, Password: Okafor
✅ Zainab Hassan (STU102) - Username: stu102, Password: Hassan
✅ Tunde Adeyemi (STU103) - Username: stu103, Password: Adeyemi
✅ Amina Bello (STU104) - Username: stu104, Password: Bello
```

### Test Login
- Go to: `https://your-app.onrender.com/accounts/login/`
- Use: `STU101` / `Okafor`
- ✅ Success!

---

## 🛠️ All Commands Reference

| Task | Command |
|------|---------|
| Single student | `create_students_custom --name "John Doe" --matric STU001` |
| With gender/level | `create_students_custom --name "John Doe" --matric STU001 --gender M --level 200` |
| From CSV | `create_students_custom --csv students.csv` |
| With admin | `create_students_custom --admin --csv students.csv` |
| List students | `shell` → `from hostels.models import StudentProfile; StudentProfile.objects.all()` |

---

## ✨ Features

✅ Full name support (e.g., "John Oladele Doe")  
✅ Automatic password from surname  
✅ Matric number as username  
✅ Gender & level selection  
✅ Bulk CSV import  
✅ Admin account creation  
✅ Error handling & validation  
✅ Clear success messages  

---

## 📁 Files Provided

| File | Purpose |
|------|---------|
| `create_students_custom.py` | Django management command |
| `generate_students_csv.py` | Local CSV generator script |
| `students_sample.csv` | Sample CSV with 10 students |
| `CREATE_STUDENTS_CUSTOM.md` | Full detailed guide |
| `STUDENTS_COMMANDS.md` | Quick command reference |
| This file | Complete guide |

---

## 🐛 Common Issues

| Problem | Solution |
|---------|----------|
| "Command not found" | Make sure you're in Django shell (`python manage.py shell` first) |
| CSV file not found | Check file is in project root |
| "User already exists" | Different matric_no already used |
| Password wrong | Password = last word of full name, capitalized |
| Special characters | Use quotes around name: `"John O'Brien"` |

---

## 💡 Pro Tips

1. **Use CSV for bulk**: Much faster than one by one
2. **Test first**: Create 1-2 students, verify login works
3. **Backup CSV**: Keep your student list safe
4. **Password easy**: Students can remember surname easily
5. **Admin first**: Create admin with `--admin` flag before students

---

## 🎯 Next Steps

1. ✅ Create students using command above
2. ✅ Test login with one student
3. ✅ Submit hostel request as student
4. ✅ Approve request as admin
5. ✅ Check allocation

---

**Ready to create students? Pick a method and get started! 🚀**

For quick commands, see: `STUDENTS_COMMANDS.md`
