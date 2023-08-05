# CRY
Encrypt and decrypt ansible-vault string/file perfect external tools

```
CRY me a river of encrypted data. Cry cry Cry.

Utilisation:
    cry [OPTIONS] [SUB_COMMAND [OPTIONS]] 

Meta-options:
    -h, --help                        Print this message
    --help-all                        Prints help messages of all sub-commands and quits
    -v, --version                     Show version

Options:
    --config VALEUR:ExistingFile      Filename with the vault password.; default: $HOME/.vault.pass
    -d, --decrypt                     Encrypt by default, add -d to decrypt
    --show-params                     Show parameters given to cry and exit.

Sub-commands:
    file                              see 'cry file --help' for infos
    string                            see 'cry string --help' for infos
```

```
Utilisation:
    cry file [OPTIONS] files...

Hidden-switches:
    -h, --help              Print this message
    --help-all              Prints help messages of all sub-commands and quits
    -v, --version           Show version

Options:
    -c, --show-context      Show the context around the string to decode
```

```
Utilisation:
    cry string [OPTIONS] strings...

Hidden-switches:
    -h, --help         Print this message
    --help-all         Prints help messages of all sub-commands and quits
    -v, --version      Show version

Options:
    -s, --stdin        Use stdin as source
```