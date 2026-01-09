# Create Students with Custom Names & Passwords

## 🎯 Quick Start

### Method 1: Single Student (Easiest)

**In Render Shell:**
```bash
python manage.py create_students_custom --name "John Doe" --matric STU001 --gender M --level 100
```

**Result:**
- ✅ Username: `stu001` (from matric number)
- ✅ Full Name: `John Doe`
- ✅ Password: `Doe` (surname capitalized)
- ✅ Gender: Male
- ✅ Level: 100

---

### Method 2: Multiple Students from CSV File (Best)

#### Step 1: Create CSV File
Create a file named `students.csv` with this format:

```csv
full_name,matric_no,gender,level
John Doe,STU001,M,100
Alice Johnson,STU002,F,100
Michael Smith,STU003,M,200
Sarah Williams,STU004,F,200
David Brown,STU005,M,300
```

#### Step 2: Upload CSV to Render
1. In Render Shell, create the file:
   ```bash
   cat > students.csv << 'EOF'
   full_name,matric_no,gender,level
   John Doe,STU001,M,100
   Alice Johnson,STU002,F,100
   Michael Smith,STU003,M,200
   EOF
   ```

#### Step 3: Run Command
```bash
python manage.py create_students_custom --csv students.csv
```

**Result:** All students created with passwords = surname

---

## 📝 Password Rules

| Full Name | Username | Password | Matric |
|-----------|----------|----------|--------|
| John Doe | stu001 | Doe | STU001 |
| Alice Johnson | stu002 | Johnson | STU002 |
| Michael Smith | stu003 | Smith | STU003 |
| Sarah Williams | stu004 | Williams | STU004 |

**Pattern:** Password = Last word of full name + Capitalize first letter

---

## 🛠️ Command Examples

### Create Single Student
```bash
python manage.py create_students_custom \
  --name "John Doe" \
  --matric STU001 \
  --gender M \
  --level 100
```

### Create Multiple from CSV
```bash
python manage.py create_students_custom --csv students.csv
```

### Create with Admin
```bash
python manage.py create_students_custom --admin --csv students.csv
```

### Different Gender/Level
```bash
python manage.py create_students_custom \
  --name "Sarah Williams" \
  --matric STU004 \
  --gender F \
  --level 200
```

---

## 📋 CSV File Format

### Required Columns
```
full_name,matric_no,gender,level
```

### Example (Copy-Paste Ready)
```csv
full_name,matric_no,gender,level
John Doe,STU001,M,100
Alice Johnson,STU002,F,100
Michael Smith,STU003,M,200
Sarah Williams,STU004,F,200
David Brown,STU005,M,300
Emily Davis,STU006,F,300
James Wilson,STU007,M,400
Jessica Martinez,STU008,F,400
```

### Valid Values
- **gender**: M or F
- **level**: 100, 200, 300, or 400

---

## 🧑‍💻 How to Use in Render

### Step 1: Open Render Shell
```
Render Dashboard → Your Service → Shell tab
```

### Step 2: Create CSV Data
```bash
cat > students.csv << 'EOF'
full_name,matric_no,gender,level
John Doe,STU001,M,100
Alice Johnson,STU002,F,100
Michael Smith,STU003,M,200
EOF
```

### Step 3: Run Command
```bash
python manage.py create_students_custom --csv students.csv
```

### Step 4: See Results
```
✅ John Doe (STU001) - Username: stu001, Password: Doe
✅ Alice Johnson (STU002) - Username: stu002, Password: Johnson
✅ Michael Smith (STU003) - Username: stu003, Password: Smith
```

---

## 🔐 Login Information

After creating, students can login with:

**Using Matric Number:**
- URL: `https://your-app.onrender.com/accounts/login/`
- Username: `STU001`
- Password: `Doe`

**Using Username:**
- URL: `https://your-app.onrender.com/accounts/login/`
- Username: `stu001`
- Password: `Doe`

Both work! ✅

---

## 📊 Examples

### Example 1: Create John Doe
```bash
python manage.py create_students_custom \
  --name "John Doe" \
  --matric STU001
```
- Username: `stu001`
- Password: `Doe`
- Gender: M (default)
- Level: 100 (default)

### Example 2: Create with All Details
```bash
python manage.py create_students_custom \
  --name "Sarah O'Brien" \
  --matric STU002 \
  --gender F \
  --level 200
```
- Username: `stu002`
- Password: `O'brien`
- Gender: F
- Level: 200

### Example 3: Bulk from CSV
```bash
python manage.py create_students_custom --admin --csv students.csv
```
- Creates admin account
- Creates all students from CSV
- Shows all passwords

---

## ✅ Verification

### Check Created Students
```bash
python manage.py shell
```

Then:
```python
from hostels.models import StudentProfile
for s in StudentProfile.objects.all():
    print(f"{s.matric_no}: {s.user.get_full_name()}")
exit()
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No input provided" | Use `--name` & `--matric` or `--csv` |
| User already exists | That username already created, use different matric_no |
| CSV file not found | Make sure CSV is in project root |
| Password wrong | Password = surname capitalized (last word of full name) |

---

## 💡 Tips

1. **Use CSV for bulk**: Much faster than creating one by one
2. **Password = Surname**: Makes it easy to remember
3. **Sample file**: We provided `students_sample.csv` with 10 students
4. **Test login**: Always verify at least one student can login
5. **Admin first**: Use `--admin` flag first time to create admin account

---

## Files Provided

- **`create_students_custom.py`** - The Django command
- **`students_sample.csv`** - Sample student data
- This file - **Complete guide**

---

**Ready to create students? Start with the examples above! 🚀**
