import logging

from django.db import migrations

logger = logging.getLogger(__name__)


MIGRATION_SQL = """
    DECLARE @SystemRole INT
    SELECT @SystemRole = role.RoleID from tblRole role where IsSystem=64;
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 150101)
    BEGIN
	    INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
	    VALUES (@SystemRole, 150101, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 150102)
    BEGIN
	    INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
	    VALUES (@SystemRole, 150102, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 150103)
    BEGIN
	     INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
	     VALUES (@SystemRole, 150103, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 150104)
    BEGIN
	    INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
	    VALUES (@SystemRole, 150104, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 150201)
    BEGIN
	    INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
	    VALUES (@SystemRole, 150201, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 150202)
    BEGIN
	    INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
	    VALUES (@SystemRole, 150202, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 150203)
    BEGIN
	    INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
	    VALUES (@SystemRole, 150203, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 150204)
    BEGIN
	    INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
	    VALUES (@SystemRole, 150204, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 150206)
    BEGIN
	    INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
	    VALUES (@SystemRole, 150206, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 150301)
    BEGIN
	    INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
	    VALUES (@SystemRole, 150301, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 150302)
    BEGIN
	    INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
	    VALUES (@SystemRole, 150302, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 150303)
    BEGIN
	    INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
	    VALUES (@SystemRole, 150303, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 150304)
    BEGIN
	    INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
	    VALUES (@SystemRole, 150304, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 150306)
    BEGIN
	    INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
	    VALUES (@SystemRole, 150306, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 150401)
    BEGIN
	    INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
	    VALUES (@SystemRole, 150401, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 150402)
    BEGIN
	    INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
	    VALUES (@SystemRole, 150402, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 150403)
    BEGIN
	    INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
	    VALUES (@SystemRole, 150403, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 150404)
    BEGIN
	    INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
	    VALUES (@SystemRole, 150404, CURRENT_TIMESTAMP)
    END 
    IF NOT EXISTS (SELECT * FROM [tblRoleRight] WHERE [RoleID] = @SystemRole AND [RightID] = 150406)
    BEGIN
	    INSERT [dbo].[tblRoleRight] ([RoleID], [RightID], [ValidityFrom]) 
	    VALUES (@SystemRole, 150406, CURRENT_TIMESTAMP)
    END 
"""


class Migration(migrations.Migration):
    dependencies = [
        ('policyholder', '0015_auto_20210624_1243')
    ]

    operations = [
        migrations.RunSQL(sql=MIGRATION_SQL),
    ]
