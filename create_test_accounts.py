"""
Script to create test accounts for all user roles
"""
from app import app, db, User, Applicant, Employer
from werkzeug.security import generate_password_hash

def create_test_accounts():
    with app.app_context():
        # Test accounts data
        accounts = [
            {
                'username': 'admin',
                'password': 'admin123',
                'role': 'admin'
            },
            {
                'username': 'applicant1',
                'password': 'applicant123',
                'role': 'applicant',
                'fullname': 'John Doe',
                'email': 'john.doe@email.com',
                'contact': '123-456-7890'
            },
            {
                'username': 'applicant2',
                'password': 'applicant123',
                'role': 'applicant',
                'fullname': 'Jane Smith',
                'email': 'jane.smith@email.com',
                'contact': '987-654-3210'
            },
            {
                'username': 'employer1',
                'password': 'employer123',
                'role': 'employer',
                'fullname': 'Bob Johnson',
                'email': 'bob.johnson@company.com',
                'company': 'Tech Corp',
                'contact': '555-1234'
            },
            {
                'username': 'employer2',
                'password': 'employer123',
                'role': 'employer',
                'fullname': 'Alice Williams',
                'email': 'alice.williams@business.com',
                'company': 'Business Solutions',
                'contact': '555-5678'
            }
        ]
        
        print("Creating test accounts...\n")
        
        for account in accounts:
            username = account['username']
            
            # Check if user already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                print(f"  [SKIP] {username} already exists, skipping...")
                continue
            
            # Create User account
            new_user = User(
                username=username,
                password=generate_password_hash(account['password']),
                role=account['role']
            )
            db.session.add(new_user)
            db.session.flush()  # Get the user ID
            
            # Create profile based on role
            if account['role'] == 'applicant':
                new_profile = Applicant(
                    user_id=new_user.id,
                    fullname=account.get('fullname', username),
                    email=account.get('email', ''),
                    contact_number=account.get('contact', ''),
                    skills='N/A',
                    experience=0
                )
                db.session.add(new_profile)
                print(f"  [OK] Created applicant: {username} ({account.get('fullname', username)})")
                
            elif account['role'] == 'employer':
                new_profile = Employer(
                    user_id=new_user.id,
                    fullname=account.get('fullname', username),
                    email=account.get('email', ''),
                    company=account.get('company', 'N/A'),
                    phone=account.get('contact', '')
                )
                db.session.add(new_profile)
                print(f"  [OK] Created employer: {username} ({account.get('fullname', username)} - {account.get('company', 'N/A')})")
            else:
                print(f"  [OK] Created admin: {username}")
        
        # Commit all changes
        db.session.commit()
        print("\n[SUCCESS] All accounts created successfully!")
        
        # Display summary
        print("\n=== ACCOUNT SUMMARY ===")
        users = User.query.all()
        print(f"\nTotal Users: {len(users)}")
        print("\nLogin Credentials:")
        print("-" * 50)
        for account in accounts:
            print(f"Username: {account['username']:<15} Password: {account['password']:<15} Role: {account['role']}")
        print("-" * 50)

if __name__ == '__main__':
    create_test_accounts()

