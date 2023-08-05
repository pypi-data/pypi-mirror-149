"""Install a Reahl Linux Server

Use the InstallIt framework to install a Linux Server for a Reahl Application
"""

import argparse
import logging
from pathlib import Path
import shutil
import sys

from beetools import beearchiver, beeutils, beescript
import configparserext
import installit
from termcolor import colored

_PROJ_DESC = __doc__.split("\n")[0]
_PROJ_PATH = Path(__file__)
_PROJ_NAME = _PROJ_PATH.stem


class InstallReahlServer:
    """

    Parameters
    ----------

    Returns
    -------

    Examples
    --------
    # No proper doctest (<<<) because it is os dependent

    """

    def __init__(self, p_ini_pth, p_logger=None):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        self.success = True
        if p_logger:
            pass
        self.ini_path = p_ini_pth
        self.ini = configparserext.ConfigParserExt(inline_comment_prefixes="#")
        self.ini.read([self.ini_path])

        self.batch_name_prefix = self.ini.get("General", "BatchNamePrefix")
        self.command_name_prefix = self.ini.get("General", "CommandNamePrefix")
        self.curr_os = beeutils.get_os()
        self.data_dir = Path(self.ini.get("DEFAULT", "DataFolder"))
        self.domain_name_prefix = self.ini.get("General", "DomainNamePrefix")
        self.etc_dir = Path(self.ini.get("DEFAULT", "etcFolder"))
        self.install_userid = Path(self.ini.get("DEFAULT", "InstallUserId"))
        self.mysql_rights_prefix = self.ini.get("General", "MySQLRightsPrefix")
        self.nginx_root_dir = Path(self.ini.get("DEFAULT", "NginXRootFolder"))
        self.nginx_sites_available_dir = self.nginx_root_dir / "sites-available"
        self.nginx_sites_enabled_dir = self.nginx_root_dir / "sites-enabled"
        self.package_prefix = self.ini.get("General", "PackagePrefix")
        self.reahl_config_dir = Path(self.ini.get("DEFAULT", "ReahlConfigFolder"))
        self.reahl_db_dir = Path(self.ini.get("DEFAULT", "ReahlDbFolder"))
        self.reahl_distribution_dir = Path(
            self.ini.get("DEFAULT", "ReahlDistributionFolder")
        )
        self.reahl_dir = Path(self.ini.get("DEFAULT", "ReahlFolder"))
        self.target_os = self.ini.get("General", "TargetOS")
        self.test_mode = self.ini.getboolean("Test", "TestMode")
        self.user_prefix = self.ini.get("General", "UserPrefix")
        self.uwsgi_root_dir = Path(self.ini.get("DEFAULT", "UwsgiRootFolder"))
        self.uwsgi_apps_available_dir = self.uwsgi_root_dir / "apps-available"
        self.uwsgi_apps_enabled_dir = self.uwsgi_root_dir / "apps-enabled"
        self.venv_base_dir = Path(self.ini.get("DEFAULT", "VenvBaseFolder"))
        self.venv_suffix = Path(self.ini.get("General", "VenvSuffix"))
        self.www_dir = Path(self.ini.get("DEFAULT", "wwwFolder"))

        self.inst_tls = installit.InstallIt()
        pass

    # end __init__

    def create_db(self, p_reahl_app_name):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        if self.ini.getboolean(p_reahl_app_name, "CreateDb"):
            script_name = "create_db"
            db_system = self.ini.get(p_reahl_app_name, "DataBase")
            script_cmds, switches = self._get_create_db_script(db_system)
            script_cmds.append("{}\n".format(self.reahl_activate_env(p_reahl_app_name)))
            if self.ini.get(p_reahl_app_name, "CreateDbUser"):
                script_cmds.append(
                    "reahl createdbuser {}".format(
                        self.reahl_config_dir / p_reahl_app_name
                    )
                )
            if self.ini.get(p_reahl_app_name, "CreateDb"):
                script_cmds.append(
                    "reahl createdb {}".format(self.reahl_config_dir / p_reahl_app_name)
                )
            if self.ini.get(p_reahl_app_name, "CreateDbTables"):
                script_cmds.append(
                    "reahl createdbtables {}".format(
                        self.reahl_config_dir / p_reahl_app_name
                    )
                )
            if self.curr_os == beeutils.LINUX:
                script_cmds.append("exit")
                script_cmds.append("_EOF_")
            beescript.exec_batch_in_session(
                script_cmds,
                p_switches=switches,
                p_script_name=script_name,
                p_verbose=True,
            )
        pass

    def create_linux_users(self):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        success = True
        if self.curr_os == beeutils.LINUX:
            users = [
                x[1]
                for x in self.ini.get(
                    "LinuxUsers", self.user_prefix, p_prefix=True, p_split=True
                )
            ]
            success = self.inst_tls.create_linux_users(users, p_verbose=True)
        return success

    def create_mysql_users(self):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        success = True
        admin = self.ini.get("MySQLUsers", "Admin", p_split=True)
        users = [
            x[1]
            for x in self.ini.get(
                "MySQLUsers", self.user_prefix, p_prefix=True, p_split=True
            )
        ]
        success = (
            self.inst_tls.create_mysql_users(admin, users, p_verbose=True) and success
        )
        rights = [
            x[1]
            for x in self.ini.get(
                "MySQLUsers", self.mysql_rights_prefix, p_prefix=True, p_split=True
            )
        ]
        success = (
            self.inst_tls.grant_mysql_user_rights(admin, rights, p_verbose=True)
            and success
        )
        return success

    def create_nginx_config(self, p_domain_name):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        self.inst_tls.create_nginx_config(
            p_domain_name,
            self.nginx_root_dir,
            self.ini.get(p_domain_name, "ReahlApp"),
            self.ini.getboolean(p_domain_name, "SiteActive"),
            p_verbose=True,
        )
        pass

    def config_reahl_domain(self, p_reahl_app_name):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        settings = [self.ini.get(p_reahl_app_name, "SMTP", p_split=False)]
        self.inst_tls.create_reahl_mailutil_config(
            p_reahl_app_name, self.reahl_config_dir, settings, p_verbose=True
        )
        pass

    def create_reahl_config(self, p_reahl_app_name):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        self.inst_tls.create_reahl_config(
            p_reahl_app_name,
            self.reahl_config_dir,
            self.reahl_db_dir,
            self.ini.get(p_reahl_app_name, "DataBase"),
            self.inst_tls.make_userid(p_reahl_app_name),
            self.inst_tls.make_user_passwd(p_reahl_app_name),
            p_verbose=True,
        )
        pass

    def create_reahl_system_account_model_config(self, p_reahl_app_name):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        self.inst_tls.create_reahl_systemaccountmodel_config(
            p_reahl_app_name,
            self.reahl_config_dir,
            self.ini.get(p_reahl_app_name, "eMail"),
            p_verbose=True,
        )
        pass

    def create_reahl_web_config(self, p_reahl_app_name):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        web_site_root = self.ini.get(p_reahl_app_name, "WebSiteRoot")
        self.inst_tls.create_reahl_web_config(
            p_reahl_app_name,
            self.reahl_config_dir,
            self.www_dir,
            web_site_root,
            p_verbose=True,
        )
        pass

    def create_uwsgi_ini(self, p_reahl_app_name):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        parms = {
            "uwsgiProcesses": self.ini.get(p_reahl_app_name, "uwsgiProcesses"),
            "uwsgiThreats": self.ini.get(p_reahl_app_name, "uwsgiThreats"),
            "AppActive": self.ini.getboolean(p_reahl_app_name, "AppActive"),
        }
        self.inst_tls.create_uwsgi_ini(
            p_reahl_app_name,
            self.uwsgi_root_dir,
            parms,
            self.venv_base_dir,
            p_reahl_app_name,
            p_verbose=True,
        )
        pass

    def _get_create_db_script(self, p_db_system):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        switches = []
        if self.curr_os == beeutils.LINUX:
            switches = ["-x"]
        if p_db_system == "sqlite":
            script_cmds = []
            if self.curr_os == beeutils.LINUX:
                script_cmds = ["sudo -u www-data bash -l << _EOF_"]
        elif p_db_system == "mysql":
            admin = self.ini.get("MySQLUsers", "Admin", p_split=True)
            script_cmds = []
            if self.curr_os == beeutils.LINUX:
                script_cmds = ["sudo -i << _EOF_", f"export MYSQL_PWD={admin[1]}\n"]
            else:
                script_cmds.append("SET MYSQL_PWD={}\n".format(admin[1]))
        elif p_db_system == "postgresql":
            script_cmds = []
            if self.curr_os == beeutils.LINUX:
                script_cmds = ["sudo -i << _EOF_"]
            pass
        else:
            print(colored("System terminated!", "red"))
            print(
                beearchiver.msg_error(
                    "Unknown database system: {}\nSystem terminated...".format(
                        p_db_system
                    )
                )
            )
            sys.exit()
        return script_cmds, switches

    def install(self):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        batch = [
            x[1]
            for x in self.ini.get(
                "{}01".format(self.batch_name_prefix),
                self.command_name_prefix,
                p_prefix=True,
                p_split=True,
            )
        ]
        beescript.exec_batch(batch, p_verbose=True)
        self.secure_mysql()
        self.start_firewall()
        batch = [
            x[1]
            for x in self.ini.get(
                "{}02".format(self.batch_name_prefix),
                self.command_name_prefix,
                p_prefix=True,
                p_split=True,
            )
        ]
        beescript.exec_batch(batch, p_verbose=True)
        self.create_linux_users()
        self.create_mysql_users()
        self.install_system_prereq_packages()
        for reahl_wheel in self.ini.get(
            "ReahlWheels", self.package_prefix, p_prefix=True, p_split=False
        ):
            reahl_app_name = self.inst_tls.get_reahl_app_name(reahl_wheel[1])
            beescript.exec_cmd(
                ["python3", "-m", "venv", self.make_reahl_env_dir(reahl_app_name)]
            )
            self.install_reahl_prereq_packages(reahl_app_name)
            self.install_reahl_apps(reahl_app_name, reahl_wheel[1])
            reahl_app_www_pth = self.www_dir / reahl_app_name
            reahl_app_www_pth.mkdir(parents=True, exist_ok=True)
            if self.curr_os == beeutils.LINUX:
                beescript.exec_cmd(["sudo", "chmod", "777", reahl_app_www_pth])
                beescript.exec_cmd(
                    ["sudo", "chown", "www-data.www-data", reahl_app_www_pth]
                )
            self.config_reahl_domain(reahl_app_name)
            self.create_reahl_config(reahl_app_name)
            self.create_reahl_system_account_model_config(reahl_app_name)
            self.create_reahl_web_config(reahl_app_name)
            self.create_uwsgi_ini(reahl_app_name)
            self.create_db(reahl_app_name)
        for domain_name in self.ini.get(
            "Domains", self.domain_name_prefix, p_prefix=True, p_split=False
        ):
            self.create_nginx_config(domain_name[1])
        batch = [
            x[1]
            for x in self.ini.get(
                "{}03".format(self.batch_name_prefix),
                self.command_name_prefix,
                p_prefix=True,
                p_split=True,
            )
        ]
        beescript.exec_batch(batch, p_verbose=True)
        pass

    def install_reahl_prereq_packages(self, p_app_name):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        switches = []
        script_name = "install_reahl_prereq_packages"
        script_cmds = []
        if self.curr_os == beeutils.LINUX:
            switches = ["-x"]
            script_cmds = ["sudo -i << _EOF_"]
        script_cmds.append("{}\n".format(self.reahl_activate_env(p_app_name)))
        for package in self.ini.get(
            "ReahlPreReqPackages", self.package_prefix, p_prefix=True, p_split=True
        ):
            script_cmds.append("pip3 install {}".format(package[1][0]))
        if self.curr_os == beeutils.LINUX:
            script_cmds.append("exit")
            script_cmds.append("_EOF_")
        beescript.exec_batch_in_session(
            script_cmds, p_script_name=script_name, p_verbose=True, p_switches=switches
        )
        pass

    def install_reahl_apps(self, p_reahl_app_name, p_reahl_wheel):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        switches = []
        script_cmds = []
        script_name = "installReahlWheels"
        if self.curr_os == beeutils.LINUX:
            switches = ["-x"]
            script_cmds = ["sudo -i << _EOF_"]
        script_cmds.append("{}\n".format(self.reahl_activate_env(p_reahl_app_name)))
        script_cmds.append(
            "pip3 install --find-links {} {}".format(
                self.reahl_distribution_dir,
                self.reahl_distribution_dir / p_reahl_wheel,
            )
        )
        if self.curr_os == beeutils.LINUX:
            script_cmds.append("exit")
            script_cmds.append("_EOF_")
        beescript.exec_batch_in_session(
            script_cmds, p_script_name=script_name, p_verbose=True, p_switches=switches
        )
        pass

    def install_system_prereq_packages(self):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        script_cmds = []
        for package in self.ini.get(
            "SystemPreReqPackages", self.package_prefix, p_prefix=True, p_split=True
        ):
            if self.curr_os == beeutils.LINUX:
                script_cmds.append("sudo pip3 install {}".format(package[1][0]))
            else:
                script_cmds.append("pip3 install {}".format(package[1][0]))
        switches = []
        if self.curr_os == beeutils.LINUX:
            switches = ["-x"]
        beescript.exec_batch_in_session(
            script_cmds,
            p_script_name="InstallSystemPreReqPackages",
            p_switches=switches,
            p_verbose=True,
        )
        pass

    def make_reahl_env_dir(self, p_app_name):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        return self.venv_base_dir / Path("{}{}".format(p_app_name, self.venv_suffix))

    def _prepare_test(self):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """

        def remove_dirs(p_dirs_to_delete):
            for folder in p_dirs_to_delete:
                if folder.is_dir():
                    # contents = folder.glob( '**' )
                    for item in folder.iterdir():
                        # path = os.path.join( folder, item )
                        if item.is_dir():
                            shutil.rmtree(item, ignore_errors=True)
                        elif item.is_file():
                            item.unlink()
                    shutil.rmtree(folder, ignore_errors=True)

        success = True
        if self.curr_os == beeutils.WINDOWS:
            if self.data_dir.is_dir():
                folders_to_delete = [
                    self.etc_dir,
                    self.nginx_root_dir,
                    self.reahl_dir,
                    self.reahl_config_dir,
                    # self.usrLocal_dir,
                    self.uwsgi_root_dir,
                    self.www_dir,
                    self.www_dir,
                ]
                remove_dirs(folders_to_delete)
            else:
                self.data_dir.mkdir()
            self.etc_dir.mkdir()
            for reahl_wheel in self.ini.get(
                "ReahlWheels", self.package_prefix, p_prefix=True, p_split=False
            ):
                reahl_app_name = self.inst_tls.get_reahl_app_name(reahl_wheel[1])
                beeutils.rm_tree(self.make_reahl_env_dir(reahl_app_name))
            # for wheel in self.ini.get( 'ReahlWheels', self.package_prefix, p_prefix = True, p_split = False ):
            #     wheel_pth = Path( 'D:\\', 'Dropbox', 'Lib', 'Wheels', wheel[ 1 ])
            #     shutil.copy( wheel_pth, self.etc_dir )
        elif self.curr_os == beeutils.LINUX:
            users = [
                x[1]
                for x in self.ini.get(
                    "LinuxUsers", self.user_prefix, p_prefix=True, p_split=True
                )
            ]
            success = self.inst_tls.delete_linux_users(users)

            list_to_del = [
                Path("/etc", "uwsgi", "apps-enabled", "RealtimeeventsCo.ini"),
                Path("/etc", "uwsgi", "apps-available", "RealtimeeventsCo.ini"),
                Path("/etc", "nginx", "sites-enabled", "RealtimeeventsCo.conf"),
                Path("/etc", "nginx", "sites-available", "RealtimeeventsCo.conf"),
            ]
            for pth in list_to_del:
                beeutils.rm_tree(pth)
                print(beearchiver.msg_info("del {}".format(pth)))

        admin = self.ini.get("MySQLUsers", "Admin", p_split=True)
        users = [
            [x[1][0], x[1][2]]
            for x in self.ini.get(
                "MySQLUsers", self.user_prefix, p_prefix=True, p_split=True
            )
        ]
        success = self.inst_tls.delete_mysql_users(admin, users) and success
        return success

    def run(self):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        if beeutils.get_os() == self.target_os:
            self.install()
        else:
            print(
                beearchiver.msg_error(
                    "Configuration not for this operating system\nTarget OS:\t{}\nCurrent OS:\t{}".format(
                        self.target_os, self.curr_os
                    )
                )
            )
        pass

    def reahl_activate_env(self, p_app_name):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        # reahl_activate = self.make_reahl_env_dir( p_app_name ) / 'bin' / 'activate'
        if self.curr_os == beeutils.LINUX:
            script_cmd = "source {}".format(
                self.make_reahl_env_dir(p_app_name) / "bin" / "activate"
            )
        else:
            script_cmd = "{}".format(
                self.make_reahl_env_dir(p_app_name) / "Scripts" / "activate"
            )
        return script_cmd

    def secure_mysql(self):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        switches = []
        if self.curr_os == beeutils.LINUX:
            switches.append(["-x"])
        # script_name = 'secure_mysql'
        admin = self.ini.get("MySQLUsers", "Admin", p_split=True)
        # script_cmds = [ 'sudo mysql --user=root --password={} <<_EOF_'.format( admin[ 1 ])]
        script_cmds = self.inst_tls.make_sql_base_cmd(admin) + [
            "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '{}';".format(
                admin[1]
            )
        ]
        beescript.exec_cmd(script_cmds, p_verbose=True)
        script_cmds = self.inst_tls.make_sql_base_cmd(admin) + [
            "DELETE FROM mysql.user WHERE User='';"
        ]
        beescript.exec_cmd(script_cmds, p_verbose=True)
        script_cmds = self.inst_tls.make_sql_base_cmd(admin) + [
            "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"
        ]
        beescript.exec_cmd(script_cmds, p_verbose=True)
        script_cmds = self.inst_tls.make_sql_base_cmd(admin) + [
            "DROP DATABASE IF EXISTS test;"
        ]
        beescript.exec_cmd(script_cmds, p_verbose=True)
        script_cmds = self.inst_tls.make_sql_base_cmd(admin) + [
            "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"
        ]
        beescript.exec_cmd(script_cmds, p_verbose=True)
        script_cmds = self.inst_tls.make_sql_base_cmd(admin) + ["FLUSH PRIVILEGES;"]
        beescript.exec_cmd(script_cmds, p_verbose=True)
        pass

    def start_firewall(self):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        if self.curr_os == beeutils.LINUX:
            switches = ["-x"]
            script_name = "start_firewall"
            script_cmds = [
                "sudo ufw allow OpenSSH",
                "sudo ufw allow 'Nginx HTTP'",
                "yes | sudo ufw enable",
                "sudo ufw status",
            ]
            beescript.exec_batch_in_session(
                script_cmds,
                p_script_name=script_name,
                p_verbose=True,
                p_switches=switches,
            )
        pass

    def _validate_test(self):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        pass


def init_logger():
    logger = logging.getLogger(_PROJ_NAME)
    logger.setLevel(beeutils.DEF_LOG_LEV)
    file_handle = logging.FileHandler(beeutils.LOG_FILE_NAME, mode="w")
    file_handle.setLevel(beeutils.DEF_LOG_LEV_FILE)
    console_handle = logging.StreamHandler()
    console_handle.setLevel(beeutils.DEF_LOG_LEV_CON)
    file_format = logging.Formatter(
        beeutils.LOG_FILE_FORMAT, datefmt=beeutils.LOG_DATE_FORMAT
    )
    console_format = logging.Formatter(beeutils.LOG_CONSOLE_FORMAT)
    file_handle.setFormatter(file_format)
    console_handle.setFormatter(console_format)
    logger.addHandler(file_handle)
    logger.addHandler(console_handle)
    return logger


def project_desc():
    return _PROJ_DESC


def read_args():
    arg_parser = argparse.ArgumentParser(description="Get configuration parameters")
    arg_parser.add_argument(
        "-c",
        "--config-path",
        help="Config file name",
        default=arg_parser.prog[: arg_parser.prog.find(".") + 1] + "ini",
    )
    arg_parser.add_argument(
        "--log", required=False, help="Activate logging", default=False
    )
    args = arg_parser.parse_args()
    ini_path = args.config_path
    log = args.log
    return ini_path, log


if __name__ == "__main__":
    ini_pth, init_log = read_args()
    if init_log:
        logger = init_logger()
    b_tls = beearchiver.Archiver(
        _PROJ_DESC,
        _PROJ_PATH,
        p_app_ini_file_name=ini_pth,
    )
    b_tls.print_header(p_cls=False)
    rhl_server = InstallReahlServer(ini_pth)
    if rhl_server.success:
        rhl_server.run()
    b_tls.print_footer()
