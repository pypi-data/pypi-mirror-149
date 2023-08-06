from globus_cli import utils


class MissingLoginError(ValueError):
    def __init__(self, missing_servers, *, assume_gcs=False):
        self.missing_servers = missing_servers
        self.assume_gcs = assume_gcs

        server_string = utils.format_list_of_words(*missing_servers)
        message_prefix = utils.format_plural_str(
            "Missing {login}",
            {"login": "logins"},
            len(missing_servers) != 1,
        )

        login_cmd = "globus login"
        if assume_gcs:
            login_cmd = "globus login " + " ".join(
                [f"--gcs {s}" for s in missing_servers]
            )

        self.message = (
            message_prefix + f" for {server_string}, please run\n\n  {login_cmd}\n"
        )
        super().__init__(self.message)

    def __str__(self):
        return self.message
