from core.permissions import (
    Permission,
    get_role_permissions,
    ROLE_PERMISSIONS,
)


def main():

    print("=" * 60)
    print("GlavRyba AI")
    print("PERMISSIONS")
    print("=" * 60)

    for role in ROLE_PERMISSIONS:

        print()
        print(f"ROLE: {role}")
        print("-" * 40)

        permissions = get_role_permissions(
            role
        )

        if not permissions:
            print("Нет разрешений")
            continue

        for permission in sorted(
            permissions
        ):
            print(f"✅ {permission}")

    print()
    print("=" * 60)
    print("PERMISSIONS CHECK COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()