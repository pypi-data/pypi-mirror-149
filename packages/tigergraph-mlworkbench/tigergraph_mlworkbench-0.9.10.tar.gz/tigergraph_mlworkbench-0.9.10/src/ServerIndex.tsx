import React from 'react';
import { ServerType, ServerIndexProps, ServerIndexState } from './types';
import { ServerController } from './ServerController';
import { ServerDetailForm } from './ServerDetailForm';

export class ServerIndex extends React.Component<
  ServerIndexProps,
  ServerIndexState
> {
  constructor(props: ServerIndexProps) {
    super(props);

    const servers = props.settings.get('servers')
      .composite as Array<ServerType>;
    this.state = {
      isAdding: false,
      serverList: servers ? servers : []
    };

    this.handleAddServer = this.handleAddServer.bind(this);
    this.setEditingState = this.setEditingState.bind(this);
    this.pushServer = this.pushServer.bind(this);
    this.updateServer = this.updateServer.bind(this);
  }

  handleAddServer(): void {
    this.setState({ isAdding: true });
  }

  setEditingState(state: boolean): void {
    this.setState({ isAdding: state });
  }

  pushServer(newServer: ServerType): void {
    const servers = [...this.state.serverList, newServer];
    this.props.settings
      .set('servers', servers)
      .then(() => {
        this.setState({ serverList: servers });
      })
      .catch(reason => {
        console.error(`Failed to update server list.\n${reason}`);
      });
  }

  updateServer(index: number, newServer: ServerType): void {
    const servers = [...this.state.serverList];
    servers[index] = newServer;
    this.props.settings
      .set('servers', servers)
      .then(() => {
        this.setState({ serverList: servers });
      })
      .catch(reason => {
        console.error(`Failed to update server list.\n${reason}`);
      });
  }

  render(): JSX.Element {
    if (this.state.isAdding) {
      return (
        <ServerDetailForm
          serverName="My Server"
          serverAddress="http://127.0.0.1"
          hostOS="linux"
          restPort="9000"
          gsqlPort="14240"
          gdpsPort="8000"
          setEditingState={this.setEditingState}
          submitServerDetail={this.pushServer}
        />
      );
    }
    return (
      <div>
        {this.state.serverList.map((server, index) => {
          return (
            <ServerController
              key={index}
              id={index}
              serverName={server.serverName}
              serverAddress={server.serverAddress}
              hostOS={server.hostOS}
              restPort={server.restPort}
              gsqlPort={server.gsqlPort}
              gdpsPort={server.gdpsPort}
              jupyterApp={this.props.jupyterApp}
              updateServer={this.updateServer}
            />
          );
        })}
        <button onClick={this.handleAddServer}>Add Server</button>
      </div>
    );
  }
}
