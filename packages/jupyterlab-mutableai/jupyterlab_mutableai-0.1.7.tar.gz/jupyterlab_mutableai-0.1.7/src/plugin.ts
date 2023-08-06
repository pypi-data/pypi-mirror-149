import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  ContextConnector,
  ICompletionManager,
  KernelConnector
} from '@jupyterlab/completer';

import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';

import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { MainAreaWidget } from '@jupyterlab/apputils';
import { settingsIcon } from '@jupyterlab/ui-components';
import { SettingsWidget } from './widgets/Settings';
import { IMainMenu } from '@jupyterlab/mainmenu';

import { ITranslator } from '@jupyterlab/translation';
import { CompletionConnector } from './connectors/connector';
import { CustomConnector } from './connectors/customConnector';
import { PLUGIN_ID, IMutableAI } from './tokens';
import {
  invoke,
  invokeNotebook,
  select,
  selectNotebook,
  toggleFlag,
  updateSettings
} from './commands';
import { MutableAIManager } from './manager';

const plugin: JupyterFrontEndPlugin<IMutableAI> = {
  id: PLUGIN_ID,
  autoStart: true,
  provides: IMutableAI,
  requires: [
    IFileBrowserFactory,
    ISettingRegistry,
    IMainMenu,
    ITranslator,
    INotebookTracker,
    ICompletionManager
  ],
  activate: (
    app: JupyterFrontEnd,
    factory: IFileBrowserFactory,
    settings: ISettingRegistry,
    mainMenu: IMainMenu,
    translator: ITranslator,
    notebooks: INotebookTracker,
    completionManager: ICompletionManager
  ): IMutableAI => {
    const { commands, contextMenu, docRegistry } = app;
    /* 
      Initialized main mutableAI manager object.
    */

    const manager = new MutableAIManager({
      translator,
      mainMenu,
      commands,
      contextMenu,
      factory,
      getSettings: (): Promise<ISettingRegistry.ISettings> =>
        settings.load(PLUGIN_ID),
      docRegistry
    });

    console.log('Mutable AI context menu is activated!');
    let flag = true;

    /**
     * Load the settings for this extension
     *
     * @param setting Extension settings
     */

    function loadSetting(setting: ISettingRegistry.ISettings): void {
      // Read the settings and convert to the correct type
      flag = setting.get('flag').composite as boolean;
    }

    // Wait for the application to be restored and
    // for the settings for this plugin to be loaded
    Promise.all([app.restored, settings.load(PLUGIN_ID)]).then(
      ([, setting]) => {
        // Read the settings
        loadSetting(setting);

        // Listen for your plugin setting changes using Signal
        setting.changed.connect(loadSetting);

        /*
          Mutable AI toggle AutoComplete flag in main menu command.
        */
        commands.addCommand(toggleFlag, {
          label: 'AutoComplete',
          isToggled: () => flag,
          execute: () => {
            // Programmatically change a setting
            Promise.all([setting.set('flag', !flag)])
              .then(() => {
                const newFlag = setting.get('flag').composite as boolean;
                console.log(
                  `Mutable AI updated flag to '${
                    newFlag ? 'enabled' : 'disabled'
                  }'.`
                );
              })
              .catch(reason => {
                console.error(
                  `Something went wrong when changing the settings.\n${reason}`
                );
              });
          }
        });

        /*
          Mutable AI update settings in main menu command.
        */
        commands.addCommand(updateSettings, {
          label: 'Update Mutable AI Settings',
          execute: () => {
            const close = () => app.shell.currentWidget?.close();
            const content = new SettingsWidget(setting, close);
            const widget = new MainAreaWidget<SettingsWidget>({ content });
            widget.title.label = 'MutableAI Settings';
            widget.title.icon = settingsIcon;
            app.shell.add(widget, 'main');
          }
        });

        // /*
        //   Mutable AI transform file in context menu command.
        // */
        // commands.addCommand(processFile, {
        //   label: 'Fast Forward to Production with MutableAI',
        //   caption: 'Mutable AI context menu.',
        //   icon: fastForwardIcon,
        //   execute: () => {
        //     const file = factory.tracker.currentWidget?.selectedItems().next();
        //     const apiKey = setting.get('apiKey').composite as string;
        //     const transformDomain = setting.get('transformDomain')
        //       .composite as string;

        //     const dataToSend = { name: file?.path, apiKey, transformDomain };

        //     // POST request
        //     const reply = requestAPI<any>('TRANSFORM_NB', {
        //       body: JSON.stringify(dataToSend),
        //       method: 'POST'
        //     });

        //     // Log to console
        //     reply
        //       .then(response => console.log('Transformed Successfully!'))
        //       .catch(e => console.log('Transformation failed!', e));
        //   }
        // });

        notebooks.widgetAdded.connect(
          (sender: INotebookTracker, panel: NotebookPanel) => {
            let editor = panel.content.activeCell?.editor ?? null;
            const session = panel.sessionContext.session;
            const options = { session, editor };
            const connector = new CompletionConnector([]);
            const handler = completionManager.register({
              connector,
              editor,
              parent: panel
            });

            const updateConnector = () => {
              editor = panel.content.activeCell?.editor ?? null;
              options.session = panel.sessionContext.session;
              options.editor = editor;
              handler.editor = editor;

              const kernel = new KernelConnector(options);
              const context = new ContextConnector(options);

              /*
               * The custom connector is getting initialized with settings.
               * This is used to get the updated settings while making the
               * completer api call.
               */
              const custom = new CustomConnector(options, panel, setting);

              handler.connector = new CompletionConnector([
                custom,
                kernel,
                context
              ]);
            };

            // Update the handler whenever the prompt or session changes
            panel.content.activeCellChanged.connect(updateConnector);
            panel.sessionContext.sessionChanged.connect(updateConnector);
          }
        );

        // Add notebook completer command.
        app.commands.addCommand(invokeNotebook, {
          execute: () => {
            const panel = notebooks.currentWidget;
            if (panel && panel.content.activeCell?.model.type === 'code') {
              return app.commands.execute(invoke, {
                id: panel.id
              });
            }
          }
        });
        // Add notebook completer select command.
        app.commands.addCommand(selectNotebook, {
          execute: () => {
            const id = notebooks.currentWidget && notebooks.currentWidget.id;

            if (id) {
              return app.commands.execute(select, { id });
            }
          }
        });

        // Set enter key for notebook completer select command.
        app.commands.addKeyBinding({
          command: selectNotebook,
          keys: ['Enter'],
          selector: '.jp-Notebook .jp-mod-completer-active'
        });
      }
    );
    return manager;
  }
};

export default plugin;
