import logging

from django.db import migrations

logger = logging.getLogger(__name__)


MIGRATION_SQL = """
    DECLARE @SystemRole INT
    SELECT @SystemRole = role.RoleID from tblRole role where IsSystem=64;
    /* Payment plan */
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 157101)
    BEGIN
        INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
        VALUES (@SystemRole, 157101, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 157102)
    BEGIN
        INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
        VALUES (@SystemRole, 157102, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 157103)
    BEGIN
        INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
        VALUES (@SystemRole, 157103, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 157104)
    BEGIN
        INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
        VALUES (@SystemRole, 157104, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 157106)
    BEGIN
        INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
        VALUES (@SystemRole, 157106, CURRENT_TIMESTAMP)
    END 
"""


class Migration(migrations.Migration):
    dependencies = [
        ('contribution_plan', '0009_contributionplan_roles_for_admin')
    ]

    operations = [
        migrations.RunSQL(MIGRATION_SQL)
    ]
