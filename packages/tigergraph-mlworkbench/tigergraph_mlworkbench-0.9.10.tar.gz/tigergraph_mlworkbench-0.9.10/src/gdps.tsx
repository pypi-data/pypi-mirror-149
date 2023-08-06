import React from 'react';

import {
  GDPSControllerState,
  GDPSControllerProps,
  GDPSInstallerState,
  GDPSInstallerProps,
  TmpOutputFormProps,
  SSHFormProps,
  VolumeMountFormProps
} from './types';

export class GDPSController extends React.Component<
  GDPSControllerProps,
  GDPSControllerState
> {
  constructor(props: GDPSControllerProps) {
    super(props);

    this.state = {
      renderView: 'testConnection'
    };
  }

  async fetchWithTimeout(resource: string, timeout = 3000): Promise<Response> {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);
    const response = await fetch(resource, {
      signal: controller.signal
    });
    clearTimeout(id);
    return response;
  }

  componentDidMount(): void {
    this.fetchWithTimeout(
      this.props.serverAddress.replace('https', 'http') +
        ':' +
        this.props.gdpsPort +
        '/ping',
      1000
    ).then(
      resp => {
        if (resp.ok) {
          this.setState({ renderView: 'successConnection' });
        } else {
          this.setState({ renderView: 'failedConnection' });
        }
      },
      error => {
        this.setState({ renderView: 'failedConnection' });
      }
    );
  }

  render(): JSX.Element {
    if (this.state.renderView === 'testConnection') {
      return <div>Pinging GDPS...</div>;
    } else if (this.state.renderView === 'successConnection') {
      return (
        <div>
          <p>GDPS is running happily on server {this.props.serverAddress}</p>
          <button onClick={this.props.handleExit}>Ok</button>
        </div>
      );
    } else if (this.state.renderView === 'failedConnection') {
      return (
        <div>
          <p>
            Failed to reach GDPS. Would you like to (re)install it to the
            server?
          </p>
          <button
            onClick={() => this.setState({ renderView: 'gdpsInstaller' })}
          >
            Yes
          </button>
          <button onClick={this.props.handleExit}>No</button>
        </div>
      );
    } else if (this.state.renderView === 'gdpsInstaller') {
      return (
        <GDPSInstaller
          handleExit={this.props.handleExit}
          serverAddress={this.props.serverAddress}
          jupyterApp={this.props.jupyterApp}
          hostOS={this.props.hostOS}
          restPort={this.props.restPort}
          gsqlPort={this.props.gsqlPort}
        />
      );
    } else {
      return <div>Something went wrong. Please reload.</div>;
    }
  }
}

class GDPSInstaller extends React.Component<
  GDPSInstallerProps,
  GDPSInstallerState
> {
  constructor(props: GDPSInstallerProps) {
    super(props);

    this.state = {
      renderView: 'intro',
      tg_output_path: '',
      local_output_path: '',
      isLocalInstall:
        props.serverAddress.includes('127.0.0.1') ||
        props.serverAddress.includes('localhost')
          ? true
          : false,
      sshUsername: '',
      sshKeyfile: '',
      dbuser: '',
      tg_cluster_mode: false
    };

    this.handleVolumeMount = this.handleVolumeMount.bind(this);
    this.handleTmpOutput = this.handleTmpOutput.bind(this);
    this.handleInstall = this.handleInstall.bind(this);
    this.handleSSH = this.handleSSH.bind(this);
  }

  handleVolumeMount(state: {
    local_output_path: string;
    tg_output_path: string;
  }): void {
    this.setState(state);
    this.setState({
      renderView: this.state.isLocalInstall ? 'toInstall' : 'ssh'
    });
  }

  handleTmpOutput(state: {
    local_output_path: string;
    tg_output_path: string;
  }): void {
    this.setState(state);
    this.setState({
      renderView: this.state.isLocalInstall ? 'toInstall' : 'ssh'
    });
  }

  handleSSH(state: {
    sshUsername: string;
    sshKeyfile: string;
    dbuser: string;
  }): void {
    this.setState(state);
    this.setState({ renderView: 'toInstall' });
  }

  handleInstall(): void {
    const ssh = ['ssh', '-o StrictHostKeyChecking=no'];
    if (this.state.sshKeyfile) {
      ssh.push('-i', '"' + this.state.sshKeyfile + '"');
    }
    ssh.push(
      this.state.sshUsername +
        '@' +
        this.props.serverAddress.replace('https://', '').replace('http://', '')
    );
    const appName = 'start_gdps_' + this.props.hostOS;
    const timestamp = new Date(Date.now());
    const cmds = [
      'mkdir -p ~/tg_gdps/logs;',
      'cd ~/tg_gdps;',
      'curl -O https://tg-mlworkbench.s3.us-west-1.amazonaws.com/gdps/' +
        appName +
        ' && ',
      'chmod +x ' + appName + ';',
      '{ tg_output_path=' + this.state.tg_output_path.trim(),
      'local_output_path=' + this.state.local_output_path.trim(),
      'tg_cluster_mode=' + this.state.tg_cluster_mode.toString(),
      'tg_host=' +
        (this.props.serverAddress.includes('https')
          ? this.props.serverAddress
          : 'http://localhost'),
      'tg_rest_port=' + this.props.restPort,
      'tg_gs_port=' + this.props.gsqlPort,
      'nohup ./' +
        appName +
        ' >> logs/' +
        timestamp.toISOString() +
        '.log 2>&1 & };',
      'echo; echo; echo; echo Installation finished.'
    ];
    this.setState({ renderView: 'installing' });

    const sshPrefix =
      ssh.join(' ') +
      (this.state.dbuser && this.state.dbuser !== this.state.sshUsername
        ? ' -t "su - ' + this.state.dbuser + ' -c '
        : ' "bash -i -c ');
    const exec = this.state.isLocalInstall
      ? cmds.join(' ') + '\n'
      : sshPrefix + "'" + cmds.join(' ') + "'" + '"' + '\n';
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
    if (this.state.renderView === 'intro') {
      return (
        <div>
          <p>
            To install GDPS onto this server, we first need to know how the
            TigerGraph database is set up there.
          </p>
          <button
            type="button"
            onClick={() => this.setState({ renderView: 'container' })}
          >
            Ok
          </button>
        </div>
      );
    } else if (this.state.renderView === 'container') {
      return (
        <div>
          <p>Is TigerGraph database running in a container?</p>
          <button
            type="button"
            onClick={() => this.setState({ renderView: 'volumeMount' })}
          >
            Yes
          </button>
          <button
            type="button"
            onClick={() => this.setState({ renderView: 'cluster' })}
          >
            No
          </button>
        </div>
      );
    } else if (this.state.renderView === 'cluster') {
      return (
        <div>
          <p>
            Is TigerGraph database running on a single machine or a cluster?
          </p>
          <button
            type="button"
            onClick={() =>
              this.setState({ tg_cluster_mode: false, renderView: 'tmpOutput' })
            }
          >
            Single
          </button>
          <button
            type="button"
            onClick={() =>
              this.setState({ tg_cluster_mode: true, renderView: 'tmpOutput' })
            }
          >
            Cluster
          </button>
        </div>
      );
    } else if (this.state.renderView === 'volumeMount') {
      return <VolumeMountForm update={this.handleVolumeMount} />;
    } else if (this.state.renderView === 'tmpOutput') {
      return <TmpOutputForm update={this.handleTmpOutput} />;
    } else if (this.state.renderView === 'ssh') {
      return <SSHForm update={this.handleSSH} />;
    } else if (this.state.renderView === 'toInstall') {
      return (
        <div>
          <p>
            Thanks for providing all the information. A terminal will open on
            the right and install GDPS to the server. Continue?
          </p>
          <button onClick={this.handleInstall}>Yes!</button>
          <button onClick={this.props.handleExit}>Hmm, maybe later</button>
        </div>
      );
    } else if (this.state.renderView === 'installing') {
      return (
        <div>
          <p>Installing GDPS. See the terminal on the right for progress.</p>
          <button onClick={this.props.handleExit}>Close</button>
        </div>
      );
    } else {
      return <div>Something went wrong. Please reload.</div>;
    }
  }
}

class VolumeMountForm extends React.Component<VolumeMountFormProps> {
  constructor(props: VolumeMountFormProps) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event: React.SyntheticEvent): void {
    event.preventDefault();
    const target = event.target as typeof event.target & {
      volumeMount: { value: string };
    };
    const volumeMount = target.volumeMount.value;
    const [host_dir, container_dir] = volumeMount.split(':');
    this.props.update({
      local_output_path: host_dir.trim() + '/gdpstmp',
      tg_output_path: container_dir.trim() + '/gdpstmp'
    });
  }

  render(): JSX.Element {
    return (
      <form onSubmit={this.handleSubmit}>
        <p>
          What is the argument after the -v flag (volume mount) when you started
          the container? (This info will be used by GDPS to read output from
          database)
        </p>
        <input
          type="text"
          name="volumeMount"
          placeholder="/folder/on/host:/folder/in/container"
          defaultValue=""
          required
        />
        <button type="submit">Next</button>
      </form>
    );
  }
}

class TmpOutputForm extends React.Component<TmpOutputFormProps> {
  constructor(props: TmpOutputFormProps) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event: React.SyntheticEvent): void {
    event.preventDefault();
    const target = event.target as typeof event.target & {
      tmpOutput: { value: string };
    };
    this.props.update({
      local_output_path: target.tmpOutput.value.trim(),
      tg_output_path: target.tmpOutput.value.trim()
    });
  }

  render(): JSX.Element {
    return (
      <form onSubmit={this.handleSubmit}>
        <p>
          Where would you like the database to write temporary outputs? (Please
          make sure that both the database and your account have access to the
          folder.) If it doesn't exist, the folder will be created.
        </p>
        <input
          type="text"
          name="tmpOutput"
          placeholder="/home/tigergraph/gdpstmp"
          defaultValue="/home/tigergraph/gdpstmp"
          required
        />
        <button type="submit">Next</button>
      </form>
    );
  }
}

class SSHForm extends React.Component<SSHFormProps> {
  constructor(props: SSHFormProps) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event: React.SyntheticEvent): void {
    event.preventDefault();
    const target = event.target as typeof event.target & {
      username: { value: string };
      keyfile: { value: string };
      dbuser: { value: string };
    };
    this.props.update({
      sshUsername: target.username.value.trim(),
      sshKeyfile: target.keyfile.value.trim(),
      dbuser: target.dbuser.value.trim()
    });
  }

  render(): JSX.Element {
    return (
      <form onSubmit={this.handleSubmit}>
        <p>
          Finally, we will SSH into the server and install GDPS. Please provide
          your SSH credentials (no sudo needed) and the database username. If
          the database and SSH usernames are the same, leave the database
          username blank. A termial will open on the right showing the progress
          and asking for password if needed.
        </p>
        <input
          type="text"
          name="username"
          placeholder="ssh username"
          defaultValue=""
          required
        />
        <input
          type="text"
          name="keyfile"
          placeholder="path to ssh key file"
          defaultValue=""
        />
        <input
          type="text"
          name="dbuser"
          placeholder="database username"
          defaultValue=""
        />
        <br />
        <button type="submit">Next</button>
      </form>
    );
  }
}
