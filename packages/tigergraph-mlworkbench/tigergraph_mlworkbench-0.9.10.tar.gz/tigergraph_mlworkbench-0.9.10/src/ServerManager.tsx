import { ReactWidget } from '@jupyterlab/apputils';

import { JupyterFrontEnd } from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import React from 'react';

import '../style/index.css';

import { ServerIndex } from './ServerIndex';

export class ServerManager extends ReactWidget {
  private _jupyterApp: JupyterFrontEnd;
  private _jupyterSettings: ISettingRegistry.ISettings;
  constructor(
    jupyterApp: JupyterFrontEnd,
    settings: ISettingRegistry.ISettings
  ) {
    super();
    this.addClass('jp-ReactWidget');
    this._jupyterApp = jupyterApp;
    this._jupyterSettings = settings;
  }

  render(): JSX.Element {
    return (
      <div>
        <h4>TigerGraph Database Server</h4>
        <p>
          <a
            href="https://docs.tigergraph.com/ml-workbench/current/overview/"
            target="_blank"
          >
            Help
          </a>
        </p>
        <ServerIndex
          jupyterApp={this._jupyterApp}
          settings={this._jupyterSettings}
        />
      </div>
    );
  }
}
