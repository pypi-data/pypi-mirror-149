import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { IDocumentManager } from '@jupyterlab/docmanager';

import { MainAreaWidget } from '@jupyterlab/apputils';

import { ILauncher } from '@jupyterlab/launcher';

import { labsLogoIcon } from './asset';

import { Launcher } from './widget';

const PLUGIN_ID = '@epi2melabs/epi2melabs-wfpage:plugin';

const COMMAND = 'create-epi2me-labs-launcher';

const CATEGORY = 'EPI2ME Labs';

/**
 * Initialization data for the epi2melabs-wfpage extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  autoStart: true,
  requires: [ILauncher, ISettingRegistry, IDocumentManager],
  activate: (
    app: JupyterFrontEnd,
    launcher: ILauncher,
    settings: ISettingRegistry,
    docTrack: IDocumentManager
  ) => {
    const { commands, shell } = app;

    const createLauncherWidget = (
      shell: JupyterFrontEnd.IShell,
      docTrack: IDocumentManager,
      plugin_settings: ISettingRegistry.ISettings
    ) => {
      const content = new Launcher(app, docTrack, plugin_settings);
      const widget = new MainAreaWidget<Launcher>({ content });
      widget.title.label = 'EPI2ME Labs';
      shell.add(widget, 'main');
    };

    Promise.all([app.restored, settings.load(PLUGIN_ID)]).then(
      ([, _settings]) => {
        commands.addCommand(COMMAND, {
          caption: 'Create an EPI2ME Labs launcher',
          label: 'EPI2ME Labs',
          icon: labsLogoIcon,
          execute: () => createLauncherWidget(shell, docTrack, _settings)
        });

        createLauncherWidget(shell, docTrack, _settings);

        if (launcher) {
          launcher.add({
            command: COMMAND,
            category: CATEGORY
          });
        }

        app.commands.execute('filebrowser:hide-main');
      }
    );
  }
};

export default plugin;
