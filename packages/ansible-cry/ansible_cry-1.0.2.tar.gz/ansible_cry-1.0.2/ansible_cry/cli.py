#!/usr/bin/env python3
import re
import sys

from plumbum import cli
from ansible.parsing.vault import VaultLib, VaultSecret
from pathlib import Path


class CRY(cli.Application):
    DESCRIPTION = "CRY me a river of encrypted data. Cry cry Cry."

    show_params = cli.Flag(["--show-params"], default=False,
                           help="Show parameters given to cry and exit.")
    decrypt = cli.Flag(["-d", "--decrypt"], default=False,
                       help="Encrypt by default, add -d to decrypt")

    config_file = cli.SwitchAttr("--config", cli.ExistingFile,
                                 help="Filename with the vault password.",
                                 default=f"{Path.home()}/.vault.pass")

    def main(self):
        if self.show_params:
            print(sys.argv)

        if not self.nested_command:
            print("No command given")
            return 1  # error exit code
        with open(self.config_file, 'r') as pass_file:
            self.vault_lib = VaultLib([(None, VaultSecret(pass_file.read().encode()))])


@CRY.subcommand("file")
class CRYFile(cli.Application):
    show_context = cli.Flag(["-c", "--show-context"], default=False,
                            help="Show the context around the string to decode")

    def main(self, *files):
        for file in files:
            with open(file, 'r') as f:
                file_in_str = f.read()
            if self.parent.decrypt:
                values = decrypt(file_in_str, self.parent.vault_lib)
                for val in values:
                    if self.show_context:
                        print(f"{val[0]}\n{val[1]}\n")
                    else:
                        print(val[1])
            else:
                value = encrypt(file_in_str, self.parent.vault_lib)
                print(value)


@CRY.subcommand("string")
class CRYString(cli.Application):
    stdin = cli.Flag(["-s", "--stdin"], default=False,
                     help="Use stdin as source")

    def main(self, *strings):

        if self.stdin:
            strings = [sys.stdin.read()]

        if self.parent.decrypt:
            for s in strings:
                values = decrypt(s, self.parent.vault_lib)
                for val in values:
                    print(val[1])
        else:
            for s in strings:
                print(encrypt(s.strip(), self.parent.vault_lib))


def decrypt(s: str, v: VaultLib) -> str:
    decrypted_strings = []
    s += '\n\n'
    regex = r"\$ANSIBLE_VAULT;[0-9.]+;[A-Z0-9]+\n([0-9\sa-z])+^"
    matches = re.finditer(regex, s, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        m = match.group()
        if m:
            m = m.strip().replace(' ', '').replace('\t', '')
            start = match.start()
            context = s[:start + 10].split('\n')[-2:][0].strip()
            decrypted_strings += [(context, f"{v.decrypt(m).decode()}")]
    return decrypted_strings


def encrypt(s: str, v: VaultLib) -> str:
    return v.encrypt(s).decode()


if __name__ == "__main__":
    try:
        CRY.run()
    except (Exception, RuntimeError) as e:
        raise Exception(f"There is an error in your command parameters. Please verify them: '{sys.argv}'. "
                        f"Upper exception:{e}")
