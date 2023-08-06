# EDOS - Endevel Digital Ocean Setup
python 3.10

to execute docker commands you need to have swarm 1, swarm 2 and swarm3 in your ssh/config
## Installation:


### With active virtual environment
`pip install git+ssh://git@gitlab.endevel.cz/endevel/internal/edos.git`

### Install it under user
`python3 -m pip install --user git+ssh://git@gitlab.endevel.cz/endevel/internal/edos.git`

# What you will need to setup EDOS
1. Digital Ocean personal token. You can generate it in DO admin.
2. Digital Ocean Spaces AWS tokens. There are in all secrets in projects. Just look at it or send DM to @bstepa.
3. Swarmpit API Token. **Paste it without *Bearer* keyword**. You can get your token from your account settings in swarmpit.doc.endevel.cz. If you don't have account, send DM to @bstepa


# Configuration
First of all run `edos-configure` to configure your tokens

# How to use it
then you can run `edos` or `edos --help` to see which commands are available

# WIP:

- `edos database recreate <cluster_id> <database_name>` -- currently not working (DO API 500)
- `edos spaces <bucket_name> setCors` ? is needed


### Autocomplete
Sourcing the completion script in your shell enables edos autocompletion.

`Zsh`
1. Generate the autocomplete script
    ```sh
    _EDOS_COMPLETE=zsh_source edos > ~/.edos-completion.sh
    ```

2. Source the completion script in `~/.zshrc`
    ```sh
    echo 'autoload -U compinit && compinit' >> ~/.zshrc
    echo '. ~/.edos-completion.sh' >> ~/.zshrc
    source ~/.zshrc
    ```
`bash`
1. Generate the autocomplete script
    ```sh
    _EDOS_COMPLETE=bash_source edos > ~/.edos-completion.sh
    ```

2. Source the completion script in `~/.bashrc`
    ```sh
    echo '. ~/.edos-completion.sh' >> ~/.bashrc
    source ~/.bashrc
   ```
