# Django Group and Permission Management Guide

This guide explains how to create and manage the 'Editors', 'Viewers', and 'Admins' groups in the Django admin site and assign custom permissions to them.

## 1. Access the Django Admin Site
- Start your Django development server: `python manage.py runserver`
- Go to `http://127.0.0.1:8000/admin/` in your browser and log in with a superuser account.

## 2. Create Groups
1. In the admin sidebar, click on **Groups**.
2. Click **Add Group**.
3. Enter the group name (e.g., `Editors`, `Viewers`, or `Admins`).
4. Click **Save and continue editing**.

## 3. Assign Permissions to Groups
1. On the group edit page, find the **Permissions** section.
2. Use the filter/search to find your custom permissions:
   - Can view book (`can_view`)
   - Can create book (`can_create`)
   - Can edit book (`can_edit`)
   - Can delete book (`can_delete`)
3. Select the relevant permissions for each group:
   - **Viewers**: Only `can_view`
   - **Editors**: `can_view`, `can_create`, `can_edit`
   - **Admins**: All four permissions
4. Click **Save**.

## 4. Add Users to Groups
1. In the admin sidebar, click on **Users**.
2. Select a user to edit.
3. In the **Groups** section, add the user to the desired group(s).
4. Click **Save**.

## 5. Managing Permissions
- Users inherit permissions from their groups.
- You can also assign permissions directly to individual users if needed.

---

For more details, see the [Django documentation on groups and permissions](https://docs.djangoproject.com/en/stable/topics/auth/default/#groups).
