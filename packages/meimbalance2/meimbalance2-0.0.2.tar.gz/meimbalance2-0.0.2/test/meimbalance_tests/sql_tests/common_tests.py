from typing import Type
from unittest import TestCase

from meimbalance2.sql.common import build_connection_string
from meimbalance2.common import mienums


class TestConnectionStringBuilder(TestCase):

    def test_missing_password_raises(self):
        # Verify that providing no parameter raises an error
        with self.assertRaises(ValueError):
            cs = build_connection_string(
                server="",
                database="",
                username="",
                driver=None,
                use_platform=mienums.OsPlatform.linux
            )

    def test_missing_password_raises(self):
        # Verify that providing no parameter raises an error
        with self.assertRaises(ValueError):
            cs = build_connection_string(
                server="",
                database="",
                password="",
                driver=None,
                use_platform=mienums.OsPlatform.linux
            )

    def test_default_username_and_password(self):
        # Tests that passing username and password into the connection string works for default behavior
        cs = build_connection_string(
            server="",
            database="",
            username="abc",
            password="123",
            driver=None,
            use_platform=mienums.OsPlatform.linux
        )

    def test_default_username_and_password_no_protocol(self):
        # Tests that passing username and password into the connection string works for default behavior
        cs = build_connection_string(
            server="",
            database="",
            username="abc",
            password="123",
            protocol=mienums.SqlProtocol.password,
            driver=None,
            use_platform=mienums.OsPlatform.linux
        )

        self.assertNotIn(";Authentication", cs)

    def test_msi_protocol_added_enum(self):
        # Tests that the protocol is added for msi
        cs = build_connection_string(
            server="",
            database="",
            protocol=mienums.SqlProtocol.msi,
            driver=None,
            use_platform=mienums.OsPlatform.linux
        )

        self.assertIn(";Authentication=" + str(mienums.SqlProtocol.msi), cs)

    def test_msi_default_no_uid(self):
        # Tests that the protocol is added for msi
        cs = build_connection_string(
            server="",
            database="",
            protocol=mienums.SqlProtocol.msi,
            driver=None,
            use_platform=mienums.OsPlatform.linux
        )

        self.assertNotIn(";UID=", cs)

    def test_msi_uid(self):
        # Tests that the protocol is added for msi
        cs = build_connection_string(
            server="",
            database="",
            protocol=mienums.SqlProtocol.msi,
            msi_uid='123456r414',
            driver=None,
            use_platform=mienums.OsPlatform.linux
        )

        self.assertIn(";UID=123456r414", cs)

    def test_interactive_protocol_added_enum(self):
        # Tests that the protocol is added for interactive
        cs = build_connection_string(
            server="",
            database="",
            protocol=mienums.SqlProtocol.interactive,
            driver=None,
            use_platform=mienums.OsPlatform.linux
        )

        self.assertIn(";Authentication=" + str(mienums.SqlProtocol.interactive), cs)

    def test_integrated_protocol_added_enum(self):
        # Tests that the protocol is added for integrated
        cs = build_connection_string(
            server="",
            database="",
            protocol=mienums.SqlProtocol.integrated,
            driver=None,
            use_platform=mienums.OsPlatform.linux
        )

        self.assertIn(";Authentication=" + str(mienums.SqlProtocol.integrated), cs)

    def test_msi_protocol_added_string(self):
        # Tests that the protocol is added for msi
        cs = build_connection_string(
            server="",
            database="",
            protocol=str(mienums.SqlProtocol.msi),
            driver=None,
            use_platform=mienums.OsPlatform.linux
        )

        self.assertIn(";Authentication=" + str(mienums.SqlProtocol.msi), cs)

    def test_driver_none_returns_odbc_linux(self):
        # Tests that the default handling returns odbc for linux
        cs = build_connection_string(
            server="",
            database="",
            protocol=mienums.SqlProtocol.msi,
            driver=None,
            use_platform=mienums.OsPlatform.linux
        )

        self.assertIn("DRIVER={ODBC Driver 17 for SQL Server}", cs)

    def test_driver_not_given_returns_odbc_linux(self):
        # Tests that the default handling returns odbc for linux
        cs = build_connection_string(
            server="",
            database="",
            protocol=mienums.SqlProtocol.msi,
            use_platform=mienums.OsPlatform.linux
        )

        self.assertIn("DRIVER={ODBC Driver 17 for SQL Server}", cs)

    def test_driver_none_returns_sql_windows(self):
        # Tests that the default handling returns sql for linux
        cs = build_connection_string(
            server="",
            database="",
            protocol=mienums.SqlProtocol.msi,
            driver=None,
            use_platform=mienums.OsPlatform.windows
        )

        self.assertIn("DRIVER={SQL Server}", cs)

    def test_driver_not_given_returns_sql_windows(self):
        # Tests that the default handling returns sql for linux
        cs = build_connection_string(
            server="",
            database="",
            protocol=mienums.SqlProtocol.msi,
            use_platform=mienums.OsPlatform.windows
        )

        self.assertIn("DRIVER={SQL Server}", cs)

    def test_missing_server_raises(self):
        # Tests that missing parameters raise errors
        with self.assertRaises(TypeError):
            cs = build_connection_string(
                database="",
                protocol=mienums.SqlProtocol.msi,
            )

    def test_missing_database_raises(self):
        # Tests that missing parameters raise errors
        with self.assertRaises(TypeError):
            cs = build_connection_string(
                server="",
                protocol=mienums.SqlProtocol.msi,
            )
