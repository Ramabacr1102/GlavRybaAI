from pathlib import Path

ROOT = Path(__file__).parent.parent

required = [
    "main.py",
    "requirements.txt",
    "bot",
    "config",
    "core",
    "database"
]

print("=" * 50)
print("GlavRyba AI Project Check")
print("=" * 50)

errors = 0

for item in required:

    path = ROOT / item

    if path.exists():
        print(f"✅ {item}")
    else:
        print(f"❌ {item}")
        errors += 1

print("=" * 50)

if errors == 0:
    print("PROJECT STRUCTURE OK")
else:
    print(f"FOUND {errors} ERRORS")

print("=" * 50)