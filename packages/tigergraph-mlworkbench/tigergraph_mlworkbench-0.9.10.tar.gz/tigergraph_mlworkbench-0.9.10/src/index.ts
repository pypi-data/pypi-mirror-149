import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { ILauncher } from '@jupyterlab/launcher';

import { IFileBrowserFactory } from '@jupyterlab/filebrowser';

import { Dialog, showDialog } from '@jupyterlab/apputils';

import { LabIcon } from '@jupyterlab/ui-components';

import { ServerManager } from './ServerManager';

import { MLTutorials } from './tutorial';

import tigerSvg from '../style/tigerIcon.svg';

export const tigerIcon = new LabIcon({
  name: '@tigergraph/mlworkbench',
  svgstr: tigerSvg
});

const PLUGIN_ID = '@tigergraph/mlworkbench:extension';

/**
 * Initialization data for the mlworkbench extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  autoStart: true,
  requires: [ISettingRegistry, ILauncher, IFileBrowserFactory],
  activate: (
    app: JupyterFrontEnd,
    settings: ISettingRegistry,
    launcher: ILauncher,
    browser: IFileBrowserFactory
  ) => {
    const { shell } = app;
    // Wait for the application to be restored and
    // for the settings for this plugin to be loaded
    Promise.all([app.restored, settings.load(PLUGIN_ID)])
      .then(([, setting]) => {
        // Add TG server manager
        const serverManager = new ServerManager(app, setting);
        serverManager.id = 'tigergraph-ml-workbench';
        serverManager.title.caption = 'ML Workbench';
        serverManager.title.icon = tigerIcon;
        shell.add(serverManager, 'left');

        // Add ML Workbench tutorials
        const commandID = 'mlworkbench:tutorial';
        app.commands.addCommand(commandID, {
          caption: 'TigerGraph ML Tutorial',
          label: 'TigerGraph ML Tutorial',
          iconClass: 'jp-TemplateIcon',
          isEnabled: () => true,
          execute: args => {
            showDialog({
              body: new MLTutorials(),
              buttons: [
                Dialog.cancelButton(),
                Dialog.okButton({ label: 'Open' })
              ],
              focusNodeSelector: 'input',
              title: 'TigerGraph ML Tutorials'
            }).then((event: Dialog.IResult<string>) => {
              if (event.button.label === 'Cancel') {
                return;
              }
              if (event.value) {
                fetch(event.value)
                  .then(resp => resp.json())
                  .then(content => {
                    const path = browser.defaultBrowser.model.path;

                    return new Promise(resolve => {
                      app.commands
                        .execute('docmanager:new-untitled', {
                          path,
                          type: 'notebook'
                        })
                        .then(model => {
                          app.commands
                            .execute('docmanager:open', {
                              factory: 'Notebook',
                              path: model.path
                            })
                            .then(widget => {
                              widget.context.ready.then(() => {
                                widget.model.fromJSON(content);
                                resolve(widget);
                              });
                            });
                        });
                    });
                  });
              }
            });
          }
        });
        launcher.add({
          category: 'Notebook',
          command: commandID,
          // eslint-disable-next-line max-len
          kernelIconUrl:
            'data:image/png;base64,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',
          rank: 1
        });
      })
      .catch(reason => {
        console.error(
          `Something went wrong when starting ml workbench.\n${reason}`
        );
      });
  }
};

export default plugin;
