import React from 'react';
import { ServerDetailProps } from './types';

export class ServerDetailForm extends React.Component<ServerDetailProps> {
  constructor(props: ServerDetailProps) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
  }

  handleSubmit(event: React.SyntheticEvent): void {
    event.preventDefault();
    const target = event.target as typeof event.target & {
      serverName: { value: string };
      serverAddress: { value: string };
      hostOS: { value: string };
      restPort: { value: string };
      gsqlPort: { value: string };
      gdpsPort: { value: string };
    };
    this.props.submitServerDetail({
      serverName: target.serverName.value,
      serverAddress: target.serverAddress.value.replace(/\/+$/g, ''),
      hostOS: target.hostOS.value,
      restPort: target.restPort.value,
      gsqlPort: target.gsqlPort.value,
      gdpsPort: target.gdpsPort.value
    });
    this.props.setEditingState(false);
  }

  handleCancel(): void {
    this.props.setEditingState(false);
  }

  render(): JSX.Element {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Server Name <br />
          <input
            className="bottom-margin"
            type="text"
            name="serverName"
            placeholder="My First Server"
            defaultValue={this.props.serverName}
          />
        </label>
        <br />
        <label>
          Server Address <br />
          <input
            className="bottom-margin"
            type="text"
            name="serverAddress"
            placeholder="http://127.0.0.1"
            defaultValue={this.props.serverAddress}
          />
        </label>
        <br />
        <label>
          Host OS <br />
          <select
            name="hostOS"
            defaultValue={this.props.hostOS}
            className="bottom-margin"
          >
            <option value="linux">linux</option>
            <option value="mac">mac</option>
          </select>
        </label>
        <br />
        <label>
          REST Port <br />
          <input
            className="bottom-margin"
            type="text"
            name="restPort"
            placeholder="9000"
            defaultValue={this.props.restPort}
          />
        </label>
        <br />
        <label>
          GSQL Port <br />
          <input
            className="bottom-margin"
            type="text"
            name="gsqlPort"
            placeholder="14240"
            defaultValue={this.props.gsqlPort}
          />
        </label>
        <br />
        <label>
          GDPS Port <br />
          <input
            className="bottom-margin"
            type="text"
            name="gdpsPort"
            placeholder="8000"
            defaultValue={this.props.gdpsPort}
          />
        </label>
        <br />
        <button type="submit">Submit</button>
        <button type="button" onClick={this.handleCancel}>
          Cancel
        </button>
      </form>
    );
  }
}
