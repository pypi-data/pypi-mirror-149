import React from 'react';

import {
  DBControllerState,
  DBControllerProps,
  DBInstallerProps,
  DBInstallerState
} from './types';

export class DBController extends React.Component<
  DBControllerProps,
  DBControllerState
> {
  constructor(props: DBControllerProps) {
    super(props);

    this.state = {
      renderComponent: 'testConnection'
    };
  }

  async fetchWithTimeout(resource: string, timeout = 3000): Promise<Response> {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);
    const response = await fetch(resource, {
      mode: 'no-cors',
      signal: controller.signal
    });
    clearTimeout(id);
    return response;
  }

  componentDidMount(): void {
    this.fetchWithTimeout(
      this.props.serverAddress + ':' + this.props.restPort + '/echo',
      1000
    ).then(
      resp => {
        window.open(this.props.serverAddress + ':' + this.props.gsqlPort);
        this.props.handleExit();
      },
      error => {
        this.setState({ renderComponent: 'failedConnection' });
      }
    );
  }

  render(): JSX.Element {
    if (this.state.renderComponent === 'testConnection') {
      return <div>Pinging the database...</div>;
    } else if (this.state.renderComponent === 'failedConnection') {
      if (this.props.hostOS === 'linux') {
        return (
          <div>
            <p>
              Failed to reach database. Would you like to (re)install it to the
              server?
            </p>
            <button
              onClick={() => this.setState({ renderComponent: 'dbInstaller' })}
            >
              Yes
            </button>
            <button onClick={this.props.handleExit}>No</button>
          </div>
        );
      } else {
        return (
          <div>
            <p>
              Failed to reach database. Please check its status manually. If you
              haven't installed the database, try deploying a docker container
              to the server following the{' '}
              <a
                href="https://docs.tigergraph.com/tigergraph-server/current/getting-started/docker"
                target="_blank"
              >
                official guide
              </a>
              .
            </p>
            <button onClick={this.props.handleExit}>Back</button>
          </div>
        );
      }
    } else if (this.state.renderComponent === 'dbInstaller') {
      return (
        <DBInstaller
          handleExit={this.props.handleExit}
          hostOS={this.props.hostOS}
          serverAddress={this.props.serverAddress}
          jupyterApp={this.props.jupyterApp}
        />
      );
    } else {
      return <div>Something went wrong. Please reload.</div>;
    }
  }
}

class DBInstaller extends React.Component<DBInstallerProps, DBInstallerState> {
  constructor(props: DBInstallerProps) {
    super(props);

    const isLocal =
      props.serverAddress.includes('127.0.0.1') ||
      props.serverAddress.includes('localhost')
        ? true
        : false;
    this.state = {
      renderView: isLocal ? 'toInstall' : 'ssh',
      isLocalInstall: isLocal,
      sshUsername: '',
      sshKeyfile: ''
    };

    this.handleInstall = this.handleInstall.bind(this);
    this.handleSSH = this.handleSSH.bind(this);
  }

  handleSSH(event: React.SyntheticEvent): void {
    const target = event.target as typeof event.target & {
      username: { value: string };
      keyfile: { value: string };
    };
    this.setState({
      sshUsername: target.username.value,
      sshKeyfile: target.keyfile.value,
      renderView: 'toInstall'
    });
  }

  handleInstall(): void {
    const host =
      this.state.sshUsername +
      '@' +
      this.props.serverAddress.replace('https://', '').replace('http://', '');
    const ssh = ['ssh', '-o StrictHostKeyChecking=no'];
    if (this.state.sshKeyfile) {
      ssh.push('-i', '"' + this.state.sshKeyfile + '"');
    }
    ssh.push(host);
    const cmds = [
      'mkdir -p ~/tg_tmp;',
      'cd ~/tg_tmp;',
      'curl -O https://dl.tigergraph.com/enterprise-edition/tigergraph-3.4.0-offline.tar.gz;',
      'tar xzf tigergraph-3.4.0-offline.tar.gz;',
      'cd tigergraph-3.4.0-offline;',
      'sudo ./install.sh -n ;',
      'cd;',
      'rm -rf tg_tmp;',
      'echo; echo; echo; echo Installation finished.'
    ];
    this.setState({ renderView: 'installing' });

    const exec = this.state.isLocalInstall
      ? cmds.join(' ') + '\n'
      : ssh.join(' ') + ' "' + cmds.join(' ') + '"' + '\n';

    const commands = this.props.jupyterApp.commands;
    commands.execute('terminal:create-new').then(model => {
      const terminal = model.content;
      try {
        terminal.session.send({
          type: 'stdin',
          content: [exec]
        });
      } catch (e) {
        console.error(e);
        model.dispose();
      }
    });
  }

  render(): JSX.Element {
    if (this.state.renderView === 'ssh') {
      return (
        <form onSubmit={this.handleSSH}>
          <p>
            We will use SSH to install the database onto the server. Please
            provide your SSH credentials. `sudo` access is required. If using
            password for SSH, leave the private key blank and you will be
            prompted to enter password next on the terminal.
          </p>
          <input type="text" name="username" placeholder="username" />
          <input type="text" name="keyfile" placeholder="path to key file" />
          <br />
          <button type="submit">Next</button>
        </form>
      );
    } else if (this.state.renderView === 'toInstall') {
      return (
        <div>
          <p>
            A terminal will open on the right and install the database to the
            server. Continue?
          </p>
          <button onClick={this.handleInstall}>Yes!</button>
          <button onClick={this.props.handleExit}>hmm, maybe later</button>
        </div>
      );
    } else if (this.state.renderView === 'installing') {
      return (
        <div>
          <p>
            Installing Tigergraph database. See the terminal on the right for
            progress.
          </p>
          <button onClick={this.props.handleExit}>Close</button>
        </div>
      );
    } else {
      return <div>Something went wrong. Please reload.</div>;
    }
  }
}
