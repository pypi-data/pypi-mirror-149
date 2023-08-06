import logging

from django.db import migrations

logger = logging.getLogger(__name__)


MIGRATION_SQL = """
    /* Contribution plan and bundle*/
    DECLARE @SystemRole INT
    SELECT @SystemRole = role.RoleID from tblRole role where IsSystem=64;
    /* Contribution plan bundle*/
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 151101)
    BEGIN
        INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
        VALUES (@SystemRole, 151101, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 151102)
    BEGIN
        INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
        VALUES (@SystemRole, 151102, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 151103)
    BEGIN
        INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
        VALUES (@SystemRole, 151103, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 151104)
    BEGIN
        INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
        VALUES (@SystemRole, 151104, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 151106)
    BEGIN
        INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
        VALUES (@SystemRole, 151106, CURRENT_TIMESTAMP)
    END 
    /* Contribution plan */
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 151201)
    BEGIN
        INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
        VALUES (@SystemRole, 151201, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 151202)
    BEGIN
        INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
        VALUES (@SystemRole, 151202, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 151203)
    BEGIN
        INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
        VALUES (@SystemRole, 151203, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 151204)
    BEGIN
        INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
        VALUES (@SystemRole, 151204, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 151206)
    BEGIN
        INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
        VALUES (@SystemRole, 151206, CURRENT_TIMESTAMP)
    END 
"""


class Migration(migrations.Migration):
    dependencies = [
        ('contribution_plan', '0008_historicalpaymentplan_paymentplan')
    ]

    operations = [
        migrations.RunSQL(sql=MIGRATION_SQL),
    ]
